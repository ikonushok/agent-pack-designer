#!/usr/bin/env python3
"""Validate a generated project agent pack for L2 consistency."""

from __future__ import annotations

import argparse
import re
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

VALIDATION_LEVEL_RE = re.compile(r"\bL[0-5]\b")


class ValidationFileError(Exception):
    """Raised when a validation input cannot be read as expected text."""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationFileError(f"{path} is not valid UTF-8: {exc}") from exc
    except OSError as exc:
        raise ValidationFileError(f"{path} could not be read: {exc}") from exc


def has_any_file(root: Path, relatives: list[str]) -> Path | None:
    for relative in relatives:
        path = root / relative
        if path.is_file() and not path.is_symlink():
            return path
    return None


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file() and not path.is_symlink())


def contains(text: str, term: str) -> bool:
    return term.lower() in text.lower()


def require_terms(root: Path, relative: str, terms: list[str], errors: list[str]) -> None:
    path = root / relative
    if path.is_symlink():
        errors.append(f"{relative} must not be a symlink")
        return
    if not path.is_file():
        return
    require_terms_in_file(path, relative, terms, errors)


def require_terms_in_file(path: Path, display_name: str, terms: list[str], errors: list[str]) -> None:
    text = read_text(path)
    for term in terms:
        if not contains(text, term):
            errors.append(f"{display_name} missing required term: {term}")


def agent_kind(path: Path) -> str:
    name = path.name.lower()
    text = read_text(path).lower()
    if "reviewer" in name or "guard" in name or "validator" in name or "verdicts" in text:
        return "reviewer"
    return "primary"


def validate_current_level(root: Path, errors: list[str]) -> None:
    agents = root / "AGENTS.md"
    if not agents.is_file() or agents.is_symlink():
        return
    for line in read_text(agents).splitlines():
        if line.lower().startswith("current validation level:"):
            claimed_levels = set(VALIDATION_LEVEL_RE.findall(line.upper()))
            if claimed_levels != {"L0"}:
                errors.append("AGENTS.md must not claim generated-pack validation above L0 before project checks run")
            return
    errors.append("AGENTS.md missing current validation level statement")


def validate_router_references(root: Path, agent_files: list[Path], errors: list[str]) -> None:
    router = root / "agents/context_router.md"
    if not router.is_file() or router.is_symlink():
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

    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            errors.append(f"{path.relative_to(root).as_posix()} must not be a symlink")

    for relative in CORE_FILES:
        path = root / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"missing required file: {relative}")

    claude = root / "CLAUDE.md"
    if require_claude and (not claude.is_file() or claude.is_symlink()):
        errors.append("missing required file for Claude target: CLAUDE.md")

    for relative, terms in REQUIRED_SECTIONS.items():
        if relative == "agents/validation_reviewer.md":
            continue
        if relative == "CLAUDE.md" and not (root / relative).is_file():
            continue
        require_terms(root, relative, terms, errors)

    validation_path = has_any_file(root, VALIDATION_ALIASES)
    if validation_path is None:
        aliases = ", ".join(VALIDATION_ALIASES)
        errors.append(f"missing validation reviewer; expected one of: {aliases}")
    else:
        relative = validation_path.relative_to(root).as_posix()
        require_terms_in_file(
            validation_path,
            relative,
            REQUIRED_SECTIONS["agents/validation_reviewer.md"],
            errors,
        )

    agent_files = [
        path
        for path in (root / "agents").glob("*.md")
        if path.name not in AGENT_CORE_NAMES and path.is_file() and not path.is_symlink()
    ] if (root / "agents").is_dir() else []
    if not agent_files:
        errors.append("missing primary or domain agent under agents/")

    router = root / "agents/context_router.md"
    if router.exists() and not router.is_symlink():
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
    try:
        errors, warnings = validate_pack(root, args.require_claude)
    except ValidationFileError as exc:
        errors = [str(exc)]
        warnings = []

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
