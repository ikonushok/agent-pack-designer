from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "agent-pack-designer/scripts/resolve_model_policy.py"
spec = importlib.util.spec_from_file_location("model_policy", SCRIPT)
assert spec is not None and spec.loader is not None
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)
NOW = datetime(2026, 10, 12, 0, 30, tzinfo=timezone.utc)


def request():
    context = {"surface": "local-test", "auth_method": "subscription", "identity": "personal"}
    return {
        "context": context,
        "parent_model": "main-model",
        "profile": "fast",
        "profiles": {"fast": ["fast-model", "approved-alternative"], "deep": ["main-model"]},
        "allowed_models": ["fast-model", "approved-alternative", "main-model"],
        "max_catalog_age_seconds": 3600,
        "catalog": {
            "context": copy.deepcopy(context), "source": "isolated test fixture", "status": "current",
            "observed_at": "2026-10-12T00:00:00Z",
            "models": [{"id": "fast-model", "reasoning_efforts": ["low"]},
                       {"id": "approved-alternative", "reasoning_efforts": ["high"]},
                       {"id": "main-model", "reasoning_efforts": ["high"]}],
        },
    }


class ModelPolicyTests(unittest.TestCase):
    def test_current_catalog_selects_approved_candidate_without_runtime_claim(self):
        result = policy.resolve(request(), NOW)
        self.assertEqual(("select", "fast-model", "not_run"),
                         (result["action"], result["model"], result["runtime_verification"]))
        self.assertEqual("PASS_WITH_RISKS", result["verdict"])

    def test_missing_catalog_inherits_parent(self):
        value = request()
        del value["catalog"]
        self.assertEqual("main-model", policy.resolve(value, NOW)["model"])
        self.assertEqual("inherit", policy.resolve(value, NOW)["action"])

    def test_stale_cached_unknown_future_and_mismatched_evidence_never_select(self):
        cases = []
        for status in ["cached", "unknown"]:
            value = request()
            value["catalog"]["status"] = status
            cases.append(value)
        for observed in ["2026-10-11T00:00:00Z", "2026-10-12T01:00:00Z"]:
            value = request()
            value["catalog"]["observed_at"] = observed
            cases.append(value)
        for key in ["surface", "auth_method", "identity"]:
            value = request()
            value["catalog"]["context"][key] = "another"
            cases.append(value)
        for value in cases:
            with self.subTest(catalog=value["catalog"]):
                self.assertEqual("inherit", policy.resolve(value, NOW)["action"])

    def test_empty_allowlist_blocks_candidates_and_parent(self):
        value = request()
        value["allowed_models"] = []
        self.assertEqual("HOLD", policy.resolve(value, NOW)["verdict"])
        del value["catalog"]
        self.assertEqual("HOLD", policy.resolve(value, NOW)["verdict"])

    def test_global_allowlist_overrides_profile_order(self):
        value = request()
        value["allowed_models"] = ["approved-alternative", "main-model"]
        self.assertEqual("approved-alternative", policy.resolve(value, NOW)["model"])

    def test_explicit_choice_overrides_profile_but_not_allowlist(self):
        value = request()
        value["model"] = "main-model"
        self.assertEqual("main-model", policy.resolve(value, NOW)["model"])
        value["allowed_models"] = ["fast-model"]
        self.assertEqual("hold", policy.resolve(value, NOW)["action"])

    def test_explicit_missing_or_unknown_model_is_never_substituted(self):
        value = request()
        value["model"] = "not-in-catalog"
        self.assertEqual("hold", policy.resolve(value, NOW)["action"])
        value["model"] = "fast-model"
        del value["catalog"]
        self.assertEqual("hold", policy.resolve(value, NOW)["action"])

    def test_new_catalog_model_is_not_automatically_approved(self):
        value = request()
        value["catalog"]["models"].insert(0, {"id": "new-model"})
        self.assertEqual("fast-model", policy.resolve(value, NOW)["model"])

    def test_retired_or_rejected_candidate_uses_only_approved_alternative(self):
        value = request()
        value["unavailable_models"] = ["fast-model"]
        self.assertEqual("approved-alternative", policy.resolve(value, NOW)["model"])
        value["catalog"]["models"] = [{"id": "main-model"}]
        self.assertEqual("inherit", policy.resolve(value, NOW)["action"])

    def test_missing_or_rejected_parent_cannot_be_inherited(self):
        value = request()
        value["profiles"] = {}
        value["catalog"]["models"] = []
        self.assertEqual("hold", policy.resolve(value, NOW)["action"])
        del value["catalog"]
        value["unavailable_models"] = ["main-model"]
        self.assertEqual("hold", policy.resolve(value, NOW)["action"])

    def test_reasoning_requirement_selects_supported_candidate(self):
        value = request()
        value["reasoning_effort"] = "high"
        self.assertEqual("approved-alternative", policy.resolve(value, NOW)["model"])

    def test_unsupported_or_unknown_reasoning_is_not_silently_removed(self):
        value = request()
        value["model"] = "fast-model"
        value["reasoning_effort"] = "high"
        self.assertEqual("hold", policy.resolve(value, NOW)["action"])
        del value["model"]
        value["catalog"]["models"] = [{"id": "fast-model"}, {"id": "main-model"}]
        self.assertEqual("hold", policy.resolve(value, NOW)["action"])
        del value["catalog"]
        self.assertEqual("hold", policy.resolve(value, NOW)["action"])

    def test_complex_research_can_use_deep_profile(self):
        value = request()
        value["profile"] = "deep"
        self.assertEqual("main-model", policy.resolve(value, NOW)["model"])

    def test_resolution_does_not_mutate_evidence(self):
        value = request()
        original = copy.deepcopy(value)
        policy.resolve(value, NOW)
        self.assertEqual(original, value)

    def test_malformed_evidence_is_rejected(self):
        changes = [("status", []), ("observed_at", "2026-10-12T00:00:00"),
                   ("models", [{"id": "same"}, {"id": "same"}]), ("models", {}),
                   ("models", [{"id": "a", "reasoning_efforts": "high"}])]
        for key, bad in changes:
            value = request()
            value["catalog"][key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(policy.PolicyError):
                policy.resolve(value, NOW)
        for bad_age in [True, 0, -1, 1.5, None]:
            value = request()
            value["max_catalog_age_seconds"] = bad_age
            with self.subTest(age=bad_age), self.assertRaises(policy.PolicyError):
                policy.resolve(value, NOW)

    def test_cli_exit_codes_and_parse_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "request.json"
            value = request()
            del value["catalog"]
            for payload, code, verdict in [(json.dumps(value), 0, "PASS_WITH_RISKS"),
                                          (json.dumps({**value, "allowed_models": []}), 2, "HOLD"),
                                          ("{", 1, "BLOCK"), ("[]", 1, "BLOCK")]:
                path.write_text(payload, encoding="utf-8")
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(code, result.returncode, result.stderr)
                self.assertEqual(verdict, json.loads(result.stdout)["verdict"])


if __name__ == "__main__":
    unittest.main()
