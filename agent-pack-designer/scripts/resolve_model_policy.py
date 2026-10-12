#!/usr/bin/env python3
"""Propose a model from supplied account-scoped evidence; never call a provider."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PolicyError(ValueError):
    """The policy or evidence cannot be interpreted safely."""


def strings(value: Any, name: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise PolicyError(f"{name} must be a list of nonempty strings")
    if len(value) != len(set(value)):
        raise PolicyError(f"{name} must not contain duplicates")
    return value


def text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PolicyError(f"{name} must be a nonempty string")
    return value


def context(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        raise PolicyError("context must be an object")
    return {key: text(value.get(key), f"context.{key}") for key in ("surface", "auth_method", "identity")}


def resolve(request: dict[str, Any], now: datetime | None = None) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise PolicyError("request must be an object")
    target = context(request.get("context"))
    parent = text(request.get("parent_model"), "parent_model")
    profile = text(request.get("profile"), "profile")
    profiles = request.get("profiles", {})
    if not isinstance(profiles, dict):
        raise PolicyError("profiles must be an object")
    for key, values in profiles.items():
        text(key, "profile name")
        strings(values, f"profiles.{key}")
    candidates = profiles.get(profile, [])
    allowed = None if "allowed_models" not in request else strings(request["allowed_models"], "allowed_models")
    unavailable = strings(request.get("unavailable_models", []), "unavailable_models")
    explicit = None if "model" not in request else text(request["model"], "model")
    effort = None if "reasoning_effort" not in request else text(request["reasoning_effort"], "reasoning_effort")

    def result(action: str, model: str | None, reason: str) -> dict[str, Any]:
        return {"verdict": "HOLD" if action == "hold" else "PASS_WITH_RISKS",
                "action": action, "model": model, "reasoning_effort": effort,
                "reason": reason, "context": target, "runtime_verification": "not_run"}

    def permitted(model: str) -> bool:
        return (allowed is None or model in allowed) and model not in unavailable

    def fallback(reason: str) -> dict[str, Any]:
        if explicit is not None or effort is not None:
            return result("hold", None, reason + "; explicit model/effort needs current evidence")
        if not permitted(parent):
            return result("hold", None, reason + "; parent is excluded or reported unavailable")
        return result("inherit", parent, reason + "; keep parent model and reasoning settings")

    catalog = request.get("catalog")
    if catalog is None:
        return fallback("account-scoped catalog is unavailable")
    if not isinstance(catalog, dict):
        raise PolicyError("catalog must be an object")
    catalog_context = context(catalog.get("context"))
    source = text(catalog.get("source"), "catalog.source")
    status = catalog.get("status")
    if not isinstance(status, str) or status not in {"current", "cached", "unknown"}:
        raise PolicyError("catalog.status must be current, cached, or unknown")
    observed = text(catalog.get("observed_at"), "catalog.observed_at")
    try:
        observed_at = datetime.fromisoformat(observed.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PolicyError("catalog.observed_at must be an ISO timestamp") from exc
    if observed_at.tzinfo is None:
        raise PolicyError("catalog.observed_at must include a timezone")
    maximum_age = request.get("max_catalog_age_seconds")
    if type(maximum_age) is not int or maximum_age <= 0:
        raise PolicyError("max_catalog_age_seconds must be a positive integer")
    models = catalog.get("models")
    if not isinstance(models, list):
        raise PolicyError("catalog.models must be a list")
    indexed: dict[str, dict[str, Any]] = {}
    for model in models:
        if not isinstance(model, dict):
            raise PolicyError("each catalog model must be an object")
        model_id = text(model.get("id"), "catalog model id")
        if model_id in indexed:
            raise PolicyError("catalog model ids must be unique")
        if "reasoning_efforts" in model:
            strings(model["reasoning_efforts"], "reasoning_efforts")
        indexed[model_id] = model
    age = ((now or datetime.now(timezone.utc)) - observed_at).total_seconds()
    if catalog_context != target:
        return fallback("catalog belongs to another surface, sign-in method, or identity")
    if status != "current" or age < 0 or age > maximum_age:
        return fallback("catalog is cached, unknown, stale, or future-dated")
    # Ordered profile mappings are approved candidates, not inferred model rankings.
    for candidate in ([explicit] if explicit is not None else candidates):
        if not permitted(candidate) or candidate not in indexed:
            continue
        supported_efforts = indexed[candidate].get("reasoning_efforts", [])
        if effort is not None and effort not in supported_efforts:
            continue
        decision = result("select", candidate, "approved candidate appears in supplied current catalog")
        decision["catalog_evidence"] = {"source": source, "observed_at": observed}
        return decision
    if explicit is not None or effort is not None:
        return result("hold", None, "explicit model/effort is excluded, unavailable, or unsupported")
    if parent not in indexed:
        return result("hold", None, "no eligible candidate; current catalog does not include parent")
    return fallback("no eligible candidate for requested profile")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path, help="JSON policy and optional normalized runtime catalog")
    args = parser.parse_args()
    try:
        decision = resolve(json.loads(args.request.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"verdict": "BLOCK", "reason": str(exc)}, indent=2))
        return 1
    print(json.dumps(decision, indent=2))
    return 2 if decision["verdict"] == "HOLD" else 0


if __name__ == "__main__":
    sys.exit(main())
