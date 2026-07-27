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

REQUIRED_VALIDATION_TERMS = [
    "L0",
    "L1",
    "L2",
    "L3",
    "L4",
    "L5",
]

REQUIRED_SECTIONS = {
    "AGENTS.md": [
        "Project:",
        "Working Rules",
        "Forbidden Changes",
        "Validation",
        "Current validation level:",
    ],
    "CLAUDE.md": [
        "Context Order",
        "Validation",
        "L0-L5",
    ],
    "agents/context_router.md": [
        "Inputs",
        "Task Modes",
        "Routing",
        "Primary context",
        "Reviewer",
        "Validation",
        "Output",
        "target validation level",
    ],
    "agents/task_spec_short.md": [
        "Goal:",
        "Non-goals:",
        "Source of truth:",
        "Allowed files:",
        "Files to avoid:",
        "Validation target:",
        "Validation method:",
        "Acceptance criteria:",
        "Stop conditions:",
        "Validation level achieved:",
        "Commands run:",
        "Residual risk:",
    ],
    "agents/validation_reviewer.md": [
        "Evidence Levels",
        "Checklist",
        "Verdicts",
        "PASS_WITH_RISKS",
        "RETEST",
        "HOLD",
        "BLOCK",
        "Report",
        "achieved level",
        "commands run",
        "missing evidence",
        "residual risk",
    ],
}

REQUIRED_AGENT_SECTIONS = [
    "Goal:",
    "When to Use",
    "Inspect First",
    "Checklist",
    "Stop Rules",
    "Output",
]

REQUIRED_REVIEWER_SECTIONS = [
    "Goal:",
    "When to Use",
    "Inspect First",
    "Checklist",
    "Verdicts",
    "PASS_WITH_RISKS",
    "BLOCK",
    "Output",
]

TEMPLATE_TOKENS = [
    "{{",
    "}}",
    "PROJECT_NAME",
    "SOURCE_OF_TRUTH_FILES",
    "PRIMARY_FILES",
    "PRIMARY_WORKFLOW_TRIGGER",
    "RISK_AREA",
    "RISK_TRIGGER",
    "RISK_FILES",
    "DEFAULT_VALIDATION",
    "RISK_VALIDATION",
]

AGENT_CORE_NAMES = {
    "context_router.md",
    "task_spec_short.md",
    "validation_reviewer.md",
    "test_validation.md",
}


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


def contains(text: str, term: str) -> bool:
    return term.lower() in text.lower()


def require_terms(root: Path, relative: str, terms: list[str], errors: list[str]) -> None:
    path = root / relative
    if not path.is_file():
        return
    text = read_text(path)
    for term in terms:
        if not contains(text, term):
            errors.append(f"{relative} missing required term: {term}")


def agent_kind(path: Path) -> str:
    name = path.name.lower()
    text = read_text(path).lower()
    if "reviewer" in name or "guard" in name or "validator" in name or "verdicts" in text:
        return "reviewer"
    return "primary"


def validate_current_level(root: Path, errors: list[str]) -> None:
    agents = root / "AGENTS.md"
    if not agents.is_file():
        return
    for line in read_text(agents).splitlines():
        if line.lower().startswith("current validation level:"):
            if "L0" not in line:
                errors.append("AGENTS.md must not claim generated-pack validation above L0 before project checks run")
            return
    errors.append("AGENTS.md missing current validation level statement")


def validate_router_references(root: Path, agent_files: list[Path], errors: list[str]) -> None:
    router = root / "agents/context_router.md"
    if not router.is_file():
        return
    router_text = read_text(router)
    for agent_file in agent_files:
        relative = agent_file.relative_to(root).as_posix()
        if relative not in router_text:
            errors.append(f"agents/context_router.md does not route to agent file: {relative}")
    if validation_path := has_any_file(root, VALIDATION_ALIASES):
        relative = validation_path.relative_to(root).as_posix()
        if relative not in router_text:
            errors.append(f"agents/context_router.md does not route to validation reviewer: {relative}")


def validate_agents(root: Path, agent_files: list[Path], errors: list[str]) -> None:
    has_primary = False
    has_reviewer = False

    for path in agent_files:
        relative = path.relative_to(root).as_posix()
        kind = agent_kind(path)
        if kind == "reviewer":
            has_reviewer = True
            require_terms(root, relative, REQUIRED_REVIEWER_SECTIONS, errors)
        else:
            has_primary = True
            require_terms(root, relative, REQUIRED_AGENT_SECTIONS, errors)

    if not has_primary:
        errors.append("missing primary workflow agent under agents/")
    if not has_reviewer:
        errors.append("missing separate risk or domain reviewer under agents/")


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

    for relative, terms in REQUIRED_SECTIONS.items():
        if relative == "CLAUDE.md" and not (root / relative).is_file():
            continue
        require_terms(root, relative, terms, errors)

    validation_path = has_any_file(root, VALIDATION_ALIASES)
    if validation_path is None:
        aliases = ", ".join(VALIDATION_ALIASES)
        errors.append(f"missing validation reviewer; expected one of: {aliases}")

    agent_files = [
        path
        for path in (root / "agents").glob("*.md")
        if path.name not in AGENT_CORE_NAMES
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

    validate_router_references(root, agent_files, errors)
    validate_agents(root, agent_files, errors)
    validate_current_level(root, errors)

    if validation_path is not None:
        validation_text = read_text(validation_path)
        for term in REQUIRED_VALIDATION_TERMS:
            if term not in validation_text:
                errors.append(f"{validation_path.relative_to(root)} missing validation level: {term}")

    for path in markdown_files(root):
        text = read_text(path)
        for token in TEMPLATE_TOKENS:
            if token in text:
                errors.append(f"unresolved template token {token!r} in {path.relative_to(root)}")

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
    print("RESULT: PASS L2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
