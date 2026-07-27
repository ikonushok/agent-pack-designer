#!/usr/bin/env python3
"""Static validation for the agent-pack-designer skill scaffold."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


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
    "scripts/validate_skill.py",
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


class ValidationFileError(Exception):
    """Raised when a validation input cannot be read as expected text."""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationFileError(f"{path} is not valid UTF-8: {exc}") from exc
    except OSError as exc:
        raise ValidationFileError(f"{path} could not be read: {exc}") from exc


def strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_limited_openai_yaml(text: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    data: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    current_section = ""

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith("\t"):
            errors.append(f"agents/openai.yaml line {line_no} uses tab indentation")
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0:
            key, separator, value = line.partition(":")
            if not separator or value.strip():
                errors.append(f"agents/openai.yaml line {line_no} must be a top-level mapping key")
                current_section = ""
                continue
            current_section = key.strip()
            data.setdefault(current_section, {})
            continue

        if indent != 2:
            errors.append(f"agents/openai.yaml line {line_no} must use two-space indentation")
            continue
        if not current_section:
            errors.append(f"agents/openai.yaml line {line_no} is nested before a section")
            continue

        key, separator, value = line.partition(":")
        if not separator:
            errors.append(f"agents/openai.yaml line {line_no} is not key: value")
            continue
        value = value.strip()
        if value in {"[", "{"}:
            errors.append(f"agents/openai.yaml line {line_no} has an unclosed flow value")
            continue
        if value.count("[") != value.count("]") or value.count("{") != value.count("}"):
            errors.append(f"agents/openai.yaml line {line_no} has unbalanced brackets")
            continue

        if value.lower() == "true":
            parsed_value: Any = True
        elif value.lower() == "false":
            parsed_value = False
        else:
            parsed_value = strip_yaml_scalar(value)
        data[current_section][key.strip()] = parsed_value

    return data, errors


def load_openai_yaml(path: Path) -> tuple[dict[str, Any], list[str]]:
    text = read_text(path)
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        return parse_limited_openai_yaml(text)

    try:
        loaded = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return {}, [f"agents/openai.yaml is not valid YAML: {exc}"]
    if not isinstance(loaded, dict):
        return {}, ["agents/openai.yaml must be a mapping"]
    return loaded, []


def nested_value(data: dict[str, Any], section: str, key: str) -> Any:
    section_data = data.get(section)
    if not isinstance(section_data, dict):
        return None
    return section_data.get(key)


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
    errors: list[str] = []
    data, yaml_errors = load_openai_yaml(path)
    errors.extend(yaml_errors)
    if errors:
        return errors

    display_name = nested_value(data, "interface", "display_name")
    short_description = nested_value(data, "interface", "short_description")
    default_prompt = nested_value(data, "interface", "default_prompt")
    allow_implicit_invocation = nested_value(data, "policy", "allow_implicit_invocation")

    if display_name != "Agent Pack Designer":
        errors.append('agents/openai.yaml missing interface.display_name: "Agent Pack Designer"')
    if not isinstance(short_description, str) or not short_description.strip():
        errors.append("agents/openai.yaml missing interface.short_description")
    if not isinstance(default_prompt, str) or not default_prompt.startswith("Use $agent-pack-designer"):
        errors.append('agents/openai.yaml missing interface.default_prompt starting with "Use $agent-pack-designer"')
    if allow_implicit_invocation is not True:
        errors.append("agents/openai.yaml missing policy.allow_implicit_invocation: true")
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
    try:
        errors, warnings = validate_skill(root)
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
    print("RESULT: PASS L0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
