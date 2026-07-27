#!/usr/bin/env python3
"""Static validation for the agent-pack-designer skill scaffold."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SKILL_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/design-workflow.md",
    "references/agent-quality-rubric.md",
    "references/validation-levels.md",
    "assets/starter-pack/AGENTS.md",
    "assets/starter-pack/CLAUDE.md",
    "assets/starter-pack/agents/context_router.md",
    "assets/starter-pack/agents/primary_agent.md",
    "assets/starter-pack/agents/risk_reviewer.md",
    "assets/starter-pack/agents/task_spec_short.md",
    "assets/starter-pack/agents/validation_reviewer.md",
    "scripts/validate_pack.py",
]

REQUIRED_STARTER_TERMS = {
    "assets/starter-pack/AGENTS.md": ["Validation", "Forbidden Changes", "L0"],
    "assets/starter-pack/CLAUDE.md": ["Context Order", "Validation", "L0-L5"],
    "assets/starter-pack/agents/context_router.md": ["Routing", "Primary context", "target validation level"],
    "assets/starter-pack/agents/primary_agent.md": ["When to Use", "Checklist", "Stop Rules"],
    "assets/starter-pack/agents/risk_reviewer.md": ["When to Use", "Verdicts", "PASS_WITH_RISKS"],
    "assets/starter-pack/agents/task_spec_short.md": ["Goal", "Validation target", "Acceptance criteria"],
    "assets/starter-pack/agents/validation_reviewer.md": ["Evidence Levels", "Verdicts", "achieved level"],
}

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, str], list[str]]:
    text = read_text(skill_md)
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]

    try:
        _, raw_yaml, body = text.split("---\n", 2)
    except ValueError:
        return {}, ["SKILL.md frontmatter must be closed with ---"]

    data: dict[str, str] = {}
    for line_no, line in enumerate(raw_yaml.splitlines(), start=2):
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"SKILL.md frontmatter line {line_no} is not key: value")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        data[key] = value

    allowed = {"name", "description"}
    extra = sorted(set(data) - allowed)
    if extra:
        errors.append(f"SKILL.md frontmatter has unsupported keys: {', '.join(extra)}")
    for key in sorted(allowed):
        if not data.get(key):
            errors.append(f"SKILL.md frontmatter missing {key}")
    if not body.strip():
        errors.append("SKILL.md body is empty")
    return data, errors


def validate_openai_yaml(path: Path) -> list[str]:
    text = read_text(path)
    errors: list[str] = []
    required_terms = [
        'display_name: "Agent Pack Designer"',
        "short_description:",
        'default_prompt: "Use $agent-pack-designer',
        "allow_implicit_invocation: true",
    ]
    for term in required_terms:
        if term not in text:
            errors.append(f"agents/openai.yaml missing {term}")
    return errors


def validate_skill(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        return [f"skill path does not exist: {root}"], warnings
    if not root.is_dir():
        return [f"skill path is not a directory: {root}"], warnings

    for relative in REQUIRED_SKILL_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if (root / "README.md").exists():
        errors.append("skill folder must not contain README.md")

    skill_md = root / "SKILL.md"
    if skill_md.exists():
        frontmatter, fm_errors = parse_frontmatter(skill_md)
        errors.extend(fm_errors)
        name = frontmatter.get("name", "")
        if name and not NAME_RE.match(name):
            errors.append(f"skill name is not lowercase hyphen-case: {name}")
        if name and root.name != name:
            errors.append(f"skill directory name {root.name!r} must match frontmatter name {name!r}")
        description = frontmatter.get("description", "")
        if description and len(description) < 80:
            warnings.append("SKILL.md description may be too short for reliable triggering")
        body = read_text(skill_md)
        for term in ["assets/starter-pack/", "references/design-workflow.md", "validation level"]:
            if term not in body:
                errors.append(f"SKILL.md missing required navigation term: {term}")

    openai_yaml = root / "agents/openai.yaml"
    if openai_yaml.exists():
        errors.extend(validate_openai_yaml(openai_yaml))

    for relative, terms in REQUIRED_STARTER_TERMS.items():
        path = root / relative
        if not path.exists():
            continue
        text = read_text(path)
        for term in terms:
            if term not in text:
                errors.append(f"{relative} missing expected term: {term}")
        if "{{" not in text and relative not in {
            "assets/starter-pack/agents/task_spec_short.md",
            "assets/starter-pack/agents/validation_reviewer.md",
        }:
            warnings.append(f"{relative} has no project placeholders")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the agent-pack-designer skill scaffold.")
    parser.add_argument("skill_path", nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    root = Path(args.skill_path).expanduser().resolve()
    errors, warnings = validate_skill(root)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS L0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
