#!/usr/bin/env python3
"""Validate a generated project agent pack for L2 consistency."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


VALIDATION_ALIASES = [
    "agents/validation_reviewer.md",
    "agents/test_validation.md",
]

CORE_FILES = [
    "AGENTS.md",
    "agents/context_router.md",
    "agents/task_spec_short.md",
]

REQUIRED_ROUTER_TERMS = [
    "primary",
    "reviewer",
    "validation",
]

REQUIRED_TASK_SPEC_TERMS = [
    "Goal",
    "Validation",
]

REQUIRED_VALIDATION_TERMS = [
    "L0",
    "L1",
    "L2",
    "L3",
    "L4",
    "L5",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_any_file(root: Path, relatives: list[str]) -> Path | None:
    for relative in relatives:
        path = root / relative
        if path.is_file():
            return path
    return None


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def validate_pack(root: Path, require_claude: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        return [f"pack path does not exist: {root}"], warnings
    if not root.is_dir():
        return [f"pack path is not a directory: {root}"], warnings

    for relative in CORE_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if require_claude and not (root / "CLAUDE.md").is_file():
        errors.append("missing required file for Claude target: CLAUDE.md")

    validation_path = has_any_file(root, VALIDATION_ALIASES)
    if validation_path is None:
        aliases = ", ".join(VALIDATION_ALIASES)
        errors.append(f"missing validation reviewer; expected one of: {aliases}")

    agent_files = [
        path
        for path in (root / "agents").glob("*.md")
        if path.name not in {"README.md", "context_router.md", "task_spec_short.md", "validation_reviewer.md", "test_validation.md"}
    ] if (root / "agents").is_dir() else []
    if not agent_files:
        errors.append("missing primary or domain agent under agents/")

    router = root / "agents/context_router.md"
    if router.exists():
        router_text = read_text(router).lower()
        for term in REQUIRED_ROUTER_TERMS:
            if term not in router_text:
                errors.append(f"agents/context_router.md missing routing term: {term}")
        if len(agent_files) > 3 and "do not load all" not in router_text and "one primary" not in router_text:
            warnings.append("many agents exist, but router does not clearly keep default context small")

    task_spec = root / "agents/task_spec_short.md"
    if task_spec.exists():
        task_text = read_text(task_spec)
        for term in REQUIRED_TASK_SPEC_TERMS:
            if term not in task_text:
                errors.append(f"agents/task_spec_short.md missing term: {term}")

    if validation_path is not None:
        validation_text = read_text(validation_path)
        for term in REQUIRED_VALIDATION_TERMS:
            if term not in validation_text:
                errors.append(f"{validation_path.relative_to(root)} missing validation level: {term}")

    for path in markdown_files(root):
        text = read_text(path)
        if "{{" in text or "}}" in text:
            errors.append(f"unresolved template placeholder in {path.relative_to(root)}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated project agent pack.")
    parser.add_argument("pack_path", help="Path to a generated pack root")
    parser.add_argument("--require-claude", action="store_true", help="Require CLAUDE.md for Claude Code target")
    args = parser.parse_args()

    root = Path(args.pack_path).expanduser().resolve()
    errors, warnings = validate_pack(root, args.require_claude)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS L2_CANDIDATE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
