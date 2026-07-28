#!/usr/bin/env python3
"""Validate generated packs, mature packs, and skill designer repositories."""

from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


VALIDATION_ALIASES = [
    "agents/validation_reviewer.md",
    "agents/test_validation.md",
    ".claude/agents/validation-reviewer.md",
    ".claude/agents/validation_reviewer.md",
    ".claude/agents/test-validation.md",
    ".claude/agents/test_validation.md",
]

TASK_SPEC_ALIASES = [
    "agents/task_spec_short.md",
    ".claude/agents/task-spec-short.md",
    ".claude/agents/task_spec_short.md",
]

PROFILE_GENERATED = "generated-pack"
PROFILE_MATURE = "mature-existing-pack"
PROFILE_DESIGNER = "skill-designer-repository"
PROFILES = [PROFILE_GENERATED, PROFILE_MATURE, PROFILE_DESIGNER]

VERDICT_PASS = "PASS"
VERDICT_PASS_WITH_RISKS = "PASS_WITH_RISKS"
VERDICT_FAIL = "FAIL"
VERDICT_NOT_APPLICABLE = "NOT_APPLICABLE"
VERDICT_INCONCLUSIVE = "INCONCLUSIVE"
VERDICT_TOOL_ERROR = "TOOL_ERROR"

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

ROUTING_SOURCES = [
    "agents/context_router.md",
    "AGENTS.md",
    "agents/README.md",
    "agents/README_agents_index.md",
    "CLAUDE.md",
]

AUDIT_AGENT_ALIASES = {
    "goal": ["Goal:", "Mission", "Primary objective", "# "],
    "when to use": ["When to Use", "Use for", "Use when", "Use before", "Use after"],
    "inspect first": ["Inspect First", "Source identity", "File identity", "Inputs"],
    "checklist": ["Checklist", "Check", "Choose validation", "Attack surfaces"],
    "stop rules": ["Stop Rules", "Critical", "Critical red flags", "Decision rules", "Reject fake validation", "Failure criteria", "Do not"],
    "output": ["Output", "Output additions"],
}

AUDIT_ROUTING_TERMS = [
    "load only",
    "routing",
    "context router",
    "one primary",
    "one main agent",
]

AUDIT_DECISION_TERMS = [
    "PASS_WITH_RISKS",
    "RETEST",
    "HOLD",
    "BLOCK",
]

TOKEN_LIGHT = 700
TOKEN_MODERATE = 1200

DESIGNER_REQUIRED_SKILL_FILES = [
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

MATERIALIZED_TEMPLATE_VALUES = {
    "{{PROJECT_NAME}}": "designer-profile-smoke-project",
    "{{SOURCE_OF_TRUTH_FILES}}": "README.md and tests/",
    "{{PRIMARY_FILES}}": "src/ and tests/",
    "{{PRIMARY_WORKFLOW_TRIGGER}}": "the main project workflow",
    "{{RISK_AREA}}": "public contracts",
    "{{RISK_TRIGGER}}": "public API or validation changes",
    "{{RISK_FILES}}": "src/, tests/, and README.md",
    "{{DEFAULT_VALIDATION}}": "L1",
    "{{RISK_VALIDATION}}": "L2",
}


@dataclass(frozen=True)
class AgentAuditRow:
    """One existing role file row for a customer-facing audit report."""

    relative: str
    kind: str
    estimated_tokens: int
    token_economy: str
    missing_signals: list[str]


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


def unique_paths(paths: list[Path]) -> list[Path]:
    return sorted(set(paths))


def generated_candidate_paths(root: Path) -> list[Path]:
    paths = [root / "AGENTS.md", root / "CLAUDE.md"]
    for agents_dir in role_directories(root):
        paths.extend(agents_dir.glob("*.md"))
    return unique_paths(paths)


def active_generated_files(root: Path) -> list[Path]:
    return [path for path in generated_candidate_paths(root) if path.is_file() and not path.is_symlink()]


def role_directories(root: Path) -> list[Path]:
    return [path for path in [root / "agents", root / ".claude/agents"] if path.is_dir()]


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


def audit_agent_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    excluded_names = {"context_router.md", "task_spec_short.md", "task-spec-short.md"}
    for agents_dir in role_directories(root):
        paths.extend(
            path
            for path in agents_dir.glob("*.md")
            if path.is_file()
            and not path.is_symlink()
            and not path.name.lower().startswith("readme")
            and path.name.lower() not in excluded_names
        )
    return unique_paths(paths)


def audit_agent_candidate_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    excluded_names = {"context_router.md", "task_spec_short.md", "task-spec-short.md"}
    for agents_dir in role_directories(root):
        paths.extend(
            path
            for path in agents_dir.glob("*.md")
            if (path.is_file() or path.is_symlink())
            and not path.name.lower().startswith("readme")
            and path.name.lower() not in excluded_names
        )
    return unique_paths(paths)


def find_existing_validation_reviewer(root: Path) -> Path | None:
    exact = has_any_file(root, VALIDATION_ALIASES)
    if exact is not None:
        return exact
    for path in audit_agent_files(root):
        name = path.stem.lower().replace("-", "_")
        text = read_text(path).lower()
        name_signal = any(term in name for term in ["validation", "validator", "evidence", "test"])
        content_signal = "validation" in text and has_any_term(text, ["evidence", "checks", "verdict", "L0"])
        if name_signal and content_signal:
            return path
    return None


def has_any_term(text: str, terms: list[str]) -> bool:
    return any(contains(text, term) for term in terms)


def is_existing_primary_agent(path: Path) -> bool:
    name = path.name.lower()
    text = read_text(path).lower()
    if "reviewer" in name or "validator" in name or "validation" in name:
        return False
    return (
        any(term in name for term in ["architect", "engineer", "primary", "main_agent"])
        or "primary design" in text
        or "primary workflow" in text
        or "main implementation" in text
    )


def is_existing_reviewer_agent(path: Path) -> bool:
    if is_existing_primary_agent(path):
        return False
    name = path.name.lower()
    text = read_text(path).lower()
    review_terms = [
        "reviewer",
        "validator",
        "validation",
        "red_team",
        "red-team",
        "risk",
        "adversarial",
        "verdict",
        "critical red flags",
        "do not accept",
    ]
    return any(term in name or term in text for term in review_terms)


def existing_routing_sources(root: Path) -> list[Path]:
    return [
        root / relative
        for relative in ROUTING_SOURCES
        if (root / relative).is_file() and not (root / relative).is_symlink()
    ]


def active_existing_files(root: Path) -> list[Path]:
    paths = [root / "AGENTS.md", root / "CLAUDE.md"]
    paths.extend(existing_routing_sources(root))
    paths.extend(audit_agent_candidate_paths(root))
    for relative in VALIDATION_ALIASES + TASK_SPEC_ALIASES:
        paths.append(root / relative)
    return unique_paths([path for path in paths if path.is_file() or path.is_symlink()])


def designer_skill_roots(root: Path) -> list[Path]:
    candidates = [root]
    candidates.extend(path.parent for path in root.glob("*/SKILL.md"))
    return unique_paths(
        [
            path
            for path in candidates
            if (path / "SKILL.md").is_file() and (path / "assets/starter-pack").is_dir()
        ]
    )


def is_skill_designer_repository(root: Path) -> bool:
    return bool(designer_skill_roots(root))


def estimate_tokens(text: str) -> int:
    """Approximate token count for planning context cost; not a tokenizer."""
    return max(1, len(text) // 4)


def token_economy_label(token_count: int) -> str:
    if token_count <= TOKEN_LIGHT:
        return "lean"
    if token_count <= TOKEN_MODERATE:
        return "moderate"
    return "heavy"


def audit_section_gaps(text: str) -> list[str]:
    return [
        section
        for section, aliases in AUDIT_AGENT_ALIASES.items()
        if not has_any_term(text, aliases)
    ]


def collect_agent_audit_rows(root: Path) -> list[AgentAuditRow]:
    rows: list[AgentAuditRow] = []
    for path in audit_agent_files(root):
        text = read_text(path)
        token_count = estimate_tokens(text)
        kind = "primary" if is_existing_primary_agent(path) else "reviewer"
        rows.append(
            AgentAuditRow(
                relative=path.relative_to(root).as_posix(),
                kind=kind,
                estimated_tokens=token_count,
                token_economy=token_economy_label(token_count),
                missing_signals=audit_section_gaps(text),
            )
        )
    return rows


def markdown_list(items: list[str]) -> str:
    if not items:
        return "- None found."
    return "\n".join(f"- {item}" for item in items)


def profile_result_label(profile: str, errors: list[str], warnings: list[str]) -> str:
    if errors:
        return VERDICT_FAIL
    if warnings:
        if profile == PROFILE_MATURE:
            return f"{VERDICT_PASS_WITH_RISKS} EXISTING_PACK_AUDIT"
        return f"{VERDICT_PASS_WITH_RISKS} {profile}"
    if profile == PROFILE_GENERATED:
        return f"{VERDICT_PASS} L2"
    if profile == PROFILE_MATURE:
        return f"{VERDICT_PASS} EXISTING_PACK_AUDIT"
    return f"{VERDICT_PASS} {profile}"


def build_existing_pack_report(root: Path, errors: list[str], warnings: list[str], require_claude: bool) -> str:
    """Build a customer-facing Markdown report for an existing-pack audit."""
    routing_sources = existing_routing_sources(root)
    validation_path = find_existing_validation_reviewer(root)
    agent_rows = collect_agent_audit_rows(root)

    agents_md = root / "AGENTS.md"
    agents_text = read_text(agents_md) if agents_md.is_file() and not agents_md.is_symlink() else ""
    routing_text = "\n".join(read_text(path).lower() for path in routing_sources)
    has_load_only = any(term in routing_text for term in ["load only", "do not load all", "one primary", "one main agent"])
    has_task_spec = has_any_file(root, TASK_SPEC_ALIASES) is not None
    has_claude = (root / "CLAUDE.md").is_file()
    has_protected_contracts = has_any_term(agents_text, ["Protected contracts", "Forbidden Changes", "Do not"])
    decision_text = agents_text
    if validation_path:
        decision_text += "\n" + read_text(validation_path)
    has_decision_vocab = not [term for term in AUDIT_DECISION_TERMS if term not in decision_text]

    total_agent_tokens = sum(row.estimated_tokens for row in agent_rows)
    default_context_tokens = estimate_tokens(agents_text)
    default_context_tokens += sum(estimate_tokens(read_text(path)) for path in routing_sources if path.name.lower().startswith("readme"))
    primary_rows = [row for row in agent_rows if row.kind == "primary"]
    reviewer_rows = [row for row in agent_rows if row.kind != "primary"]
    if primary_rows:
        default_context_tokens += min(row.estimated_tokens for row in primary_rows)
    if reviewer_rows:
        default_context_tokens += min(row.estimated_tokens for row in reviewer_rows)

    good: list[str] = []
    if agents_md.is_file():
        good.append("Root AGENTS.md exists and centralizes project-level guidance.")
    if routing_sources:
        good.append("Routing source exists: " + ", ".join(path.relative_to(root).as_posix() for path in routing_sources) + ".")
    if has_load_only:
        good.append("Routing tells future agents not to load every role file at once, which protects context budget.")
    if has_protected_contracts:
        good.append("Project-level forbidden changes or protected contracts are documented.")
    if has_task_spec:
        good.append("Task spec agent exists, supporting scoped work before edits.")
    if agent_rows:
        good.append(f"{len(agent_rows)} role-scoped agent files were found and can be routed by task.")

    problems: list[str] = []
    if errors:
        problems.extend(errors)
    if not validation_path:
        problems.append("No separate validation reviewer was found, so evidence ownership is not explicit.")
    if warnings:
        problems.extend(warnings)
    if not has_decision_vocab:
        problems.append("Decision vocabulary is not fully standardized across AGENTS.md.")
    if require_claude and not has_claude:
        problems.append("Claude Code compatibility was required but CLAUDE.md was not found.")

    recommendations: list[str] = []
    if not validation_path:
        recommendations.append("Add a validation reviewer under agents/ or .claude/agents/ to own evidence, commands run, missing checks, and validation level.")
    if not has_decision_vocab:
        recommendations.append("Standardize review verdicts around PASS, PASS_WITH_RISKS, RETEST, HOLD, and BLOCK.")
    if any("inspect first" in row.missing_signals for row in agent_rows):
        recommendations.append("Add short Inspect First sections to role files that currently imply context but do not name initial files or artifacts.")
    if any("when to use" in row.missing_signals for row in agent_rows):
        recommendations.append("Add explicit When to Use triggers to role files that rely only on external routing.")
    heavy_rows = [row for row in agent_rows if row.token_economy == "heavy"]
    if heavy_rows:
        recommendations.append("Shorten heavy agent files or move rare details to references so default task routing stays cheap.")
    if not routing_sources or not has_load_only:
        recommendations.append("Add or strengthen a context router that selects one primary agent plus at most one reviewer by default.")

    token_findings: list[str] = []
    if has_load_only:
        token_findings.append("The pack has a positive token-economy pattern: routing discourages loading all agents.")
    else:
        token_findings.append("Token risk: routing does not clearly prevent loading the whole agents directory.")
    token_findings.append(f"Approximate total role-agent text: {total_agent_tokens} tokens across {len(agent_rows)} files.")
    token_findings.append(f"Approximate minimal routed context: {default_context_tokens} tokens before task-specific source files.")
    if heavy_rows:
        token_findings.append("Heavy role files: " + ", ".join(f"{row.relative} (~{row.estimated_tokens})" for row in heavy_rows) + ".")
    else:
        token_findings.append("No role file is estimated above the heavy threshold.")

    agent_table = [
        "| Agent | Kind | Est. tokens | Token economy | Missing audit signals |",
        "|---|---|---:|---|---|",
    ]
    for row in agent_rows:
        missing = ", ".join(row.missing_signals) if row.missing_signals else "none"
        agent_table.append(
            f"| `{row.relative}` | {row.kind} | {row.estimated_tokens} | {row.token_economy} | {missing} |"
        )
    if not agent_rows:
        agent_table.append("| none | - | 0 | - | no role agents found |")

    result_label = profile_result_label(PROFILE_MATURE, errors, warnings)
    command = f"python3 agent-pack-designer/scripts/validate_pack.py --profile {PROFILE_MATURE} {root}"
    lines = [
        f"# Agent Pack Audit Report: {root.name}",
        "",
        "## Executive Summary",
        "",
        f"- Target project: `{root}`",
        f"- Profile: `{PROFILE_MATURE}`",
        f"- Audit result: `{result_label}`",
        f"- Role agents found: {len(agent_rows)}",
        f"- Routing sources: {', '.join(f'`{path.relative_to(root).as_posix()}`' for path in routing_sources) if routing_sources else 'none'}",
        f"- Validation reviewer: `{validation_path.relative_to(root).as_posix()}`" if validation_path else "- Validation reviewer: missing",
        f"- Claude context: {'present' if has_claude else 'absent'}",
        "",
        "## What Works Well",
        "",
        markdown_list(good),
        "",
        "## Problems And Risks",
        "",
        markdown_list(problems),
        "",
        "## Recommended Changes",
        "",
        markdown_list(recommendations),
        "",
        "## Token Economy",
        "",
        markdown_list(token_findings),
        "",
        "## Agent-By-Agent Review",
        "",
        "\n".join(agent_table),
        "",
        "## Validation Evidence",
        "",
        f"- Command: `{command}`",
        f"- Result: `{result_label}`",
        "- This report audits existing-pack quality and routing. It does not claim generated-pack L2 consistency.",
        "",
    ]
    return "\n".join(lines)


def build_skill_designer_report(root: Path, errors: list[str], warnings: list[str], require_claude: bool) -> str:
    """Build a customer-facing Markdown report for an agent-pack designer repository."""
    skill_roots = designer_skill_roots(root)
    skill_root = skill_roots[0] if len(skill_roots) == 1 else None

    has_skill_scaffold = skill_root is not None and all((skill_root / relative).is_file() for relative in DESIGNER_REQUIRED_SKILL_FILES)
    materialized_errors: list[str] = []
    materialized_warnings: list[str] = []
    if skill_root is not None:
        materialized_errors, materialized_warnings = validate_materialized_starter_pack(skill_root)
    materialized_label = profile_result_label(PROFILE_GENERATED, materialized_errors, materialized_warnings)

    good: list[str] = []
    if has_skill_scaffold:
        good.append("The installable skill scaffold and starter-pack assets are present.")
    if materialized_label == f"{VERDICT_PASS} L2":
        good.append("Materialized starter-pack smoke validation passes L2.")
    good.append("Repository-local assistant workspace files are outside the package surface.")

    problems: list[str] = []
    if errors:
        problems.extend(errors)
    if warnings:
        problems.extend(warnings)

    recommendations: list[str] = []
    if not recommendations:
        recommendations.append("Keep the designer profile in CI so future template or agent changes are checked against the correct repository type.")

    result_label = profile_result_label(PROFILE_DESIGNER, errors, warnings)
    skill_package = skill_root.relative_to(root).as_posix() if skill_root is not None else "missing or ambiguous"
    command = f"python3 agent-pack-designer/scripts/validate_pack.py --profile {PROFILE_DESIGNER} {root}"
    lines = [
        f"# Skill Designer Repository Audit Report: {root.name}",
        "",
        "## Executive Summary",
        "",
        f"- Target project: `{root}`",
        f"- Profile: `{PROFILE_DESIGNER}`",
        f"- Audit result: `{result_label}`",
        f"- Skill package: `{skill_package}`",
        "- Repository-local assistant files: ignored",
        f"- Materialized starter-pack check: `{materialized_label}`",
        "",
        "## What Works Well",
        "",
        markdown_list(good),
        "",
        "## Problems And Risks",
        "",
        markdown_list(problems),
        "",
        "## Recommended Changes",
        "",
        markdown_list(recommendations),
        "",
        "## Package Surface",
        "",
        markdown_list(
            [
                "The public surface is the installable `agent-pack-designer/` package plus selected docs, tests, reports, and CI.",
                "Root `AGENTS.md`, root `CLAUDE.md`, `.claude/`, `.codex/`, `.agents/`, and root `agents/` are local workspace files when present.",
            ]
        ),
        "",
        "## Validation Evidence",
        "",
        f"- Command: `{command}`",
        f"- Result: `{result_label}`",
        "- This report audits the agent-pack designer repository itself. Starter-pack template placeholders are intentional and are checked only after materialization.",
        "",
    ]
    return "\n".join(lines)


def validate_existing_pack(root: Path, require_claude: bool) -> tuple[list[str], list[str]]:
    """Audit a mature existing pack without requiring generated starter-pack shape."""
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        return [f"pack path does not exist: {root}"], warnings
    if not root.is_dir():
        return [f"pack path is not a directory: {root}"], warnings

    for path in active_existing_files(root):
        if path.is_symlink():
            errors.append(f"{path.relative_to(root).as_posix()} must not be a symlink")

    agents_md = root / "AGENTS.md"
    if not agents_md.is_file() or agents_md.is_symlink():
        errors.append("missing required file: AGENTS.md")
    else:
        agents_text = read_text(agents_md)
        for term in ["Working Rules", "Validation"]:
            if not contains(agents_text, term):
                warnings.append(f"AGENTS.md does not name {term}")
        if not has_any_term(agents_text, ["Forbidden Changes", "Protected contracts", "Do not"]):
            warnings.append("AGENTS.md does not clearly state forbidden changes or protected contracts")

    claude = root / "CLAUDE.md"
    if require_claude and (not claude.is_file() or claude.is_symlink()):
        errors.append("missing required file for Claude target: CLAUDE.md")
    elif not claude.is_file():
        warnings.append("CLAUDE.md is absent; Claude Code compatibility was not audited")

    routing_sources = existing_routing_sources(root)
    if not routing_sources:
        errors.append("missing routing source; expected agents/context_router.md, AGENTS.md, agents/README.md, or agents/README_agents_index.md")
    else:
        routing_text = "\n".join(read_text(path) for path in routing_sources)
        if not has_any_term(routing_text, AUDIT_ROUTING_TERMS):
            warnings.append("routing sources do not clearly state routing or load-only guidance")

    validation_path = find_existing_validation_reviewer(root)
    if validation_path is None:
        errors.append("missing validation reviewer under agents/ or .claude/agents/")
    else:
        validation_text = read_text(validation_path)
        if not has_any_term(validation_text, ["validation", "evidence", "checks", "L0"]):
            warnings.append(f"{validation_path.relative_to(root)} does not clearly own validation evidence review")
        missing_levels = [term for term in REQUIRED_VALIDATION_TERMS if term not in validation_text]
        if missing_levels:
            warnings.append(
                f"{validation_path.relative_to(root)} is a validation alias but lacks level terms: {', '.join(missing_levels)}"
            )

    task_spec = has_any_file(root, TASK_SPEC_ALIASES)
    if task_spec is None:
        warnings.append("task_spec_short.md is absent; spec-first task scoping may be informal")

    agent_files = audit_agent_files(root)
    if not agent_files:
        errors.append("missing role-scoped agent files under agents/ or .claude/agents/")
    else:
        has_primary = any(is_existing_primary_agent(path) for path in agent_files)
        has_reviewer = any(is_existing_reviewer_agent(path) for path in agent_files)
        if not has_primary:
            errors.append("missing identifiable primary workflow agent under agents/ or .claude/agents/")
        if not has_reviewer:
            errors.append("missing identifiable reviewer/risk/validation agent under agents/ or .claude/agents/")

        if len(agent_files) > 6 and routing_sources:
            routing_text = "\n".join(read_text(path).lower() for path in routing_sources)
            if "load only" not in routing_text and "do not load all" not in routing_text and "one main agent" not in routing_text:
                warnings.append("many agents exist, but routing does not clearly keep default context small")

        for path in agent_files:
            text = read_text(path)
            relative = path.relative_to(root).as_posix()
            missing = [
                section
                for section, aliases in AUDIT_AGENT_ALIASES.items()
                if not has_any_term(text, aliases)
            ]
            if missing:
                warnings.append(f"{relative} lacks audit section signals: {', '.join(missing)}")

    decision_text = ""
    if agents_md.is_file() and not agents_md.is_symlink():
        decision_text += read_text(agents_md)
    if validation_path is not None:
        decision_text += "\n" + read_text(validation_path)
    missing_decisions = [term for term in AUDIT_DECISION_TERMS if term not in decision_text]
    if missing_decisions:
        warnings.append(f"decision vocabulary incomplete: {', '.join(missing_decisions)}")

    for path in active_existing_files(root):
        if path.is_symlink():
            continue
        text = read_text(path)
        for token in TEMPLATE_TOKENS:
            if token in text:
                errors.append(f"unresolved template token {token!r} in {path.relative_to(root)}")

    return errors, warnings


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

    for path in generated_candidate_paths(root):
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

    for path in active_generated_files(root):
        text = read_text(path)
        for token in TEMPLATE_TOKENS:
            if token in text:
                errors.append(f"unresolved template token {token!r} in {path.relative_to(root)}")

    return errors, warnings


def validate_installable_skill(skill_root: Path) -> tuple[list[str], list[str]]:
    validator_path = Path(__file__).resolve().with_name("validate_skill.py")
    spec = importlib.util.spec_from_file_location("_agent_pack_validate_skill", validator_path)
    if spec is None or spec.loader is None:
        raise ValidationFileError(f"could not load skill validator: {validator_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.validate_skill(skill_root)


def validate_materialized_starter_pack(skill_root: Path) -> tuple[list[str], list[str]]:
    with tempfile.TemporaryDirectory(prefix="agent-pack-designer-profile-") as temporary:
        materialized = Path(temporary) / "generated-pack"
        shutil.copytree(skill_root / "assets/starter-pack", materialized)
        for path in active_generated_files(materialized):
            content = read_text(path)
            for source, target in MATERIALIZED_TEMPLATE_VALUES.items():
                content = content.replace(source, target)
            path.write_text(content, encoding="utf-8")
        return validate_pack(materialized, require_claude=True)


def validate_skill_designer_repository(root: Path, require_claude: bool) -> tuple[list[str], list[str]]:
    """Validate a repository that owns a reusable agent-pack design skill."""
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        return [f"repository path does not exist: {root}"], warnings
    if not root.is_dir():
        return [f"repository path is not a directory: {root}"], warnings

    skill_roots = designer_skill_roots(root)
    if len(skill_roots) != 1:
        return [f"expected one skill package with SKILL.md and assets/starter-pack, found {len(skill_roots)}"], warnings
    skill_root = skill_roots[0]

    for relative in DESIGNER_REQUIRED_SKILL_FILES:
        path = skill_root / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"missing required skill file: {path.relative_to(root).as_posix()}")

    starter_agents = skill_root / "assets/starter-pack/AGENTS.md"
    if starter_agents.is_file() and "{{PROJECT_NAME}}" not in read_text(starter_agents):
        errors.append("starter-pack/AGENTS.md must retain the {{PROJECT_NAME}} template placeholder")

    skill_errors, skill_warnings = validate_installable_skill(skill_root)
    errors.extend(f"skill scaffold: {error}" for error in skill_errors)
    warnings.extend(f"skill scaffold: {warning}" for warning in skill_warnings)

    generated_errors, generated_warnings = validate_materialized_starter_pack(skill_root)
    errors.extend(f"materialized starter pack: {error}" for error in generated_errors)
    warnings.extend(f"materialized starter pack: {warning}" for warning in generated_warnings)

    return errors, warnings


def profile_applicability(root: Path, profile: str) -> tuple[str, str] | None:
    if not root.exists() or not root.is_dir():
        return None

    skill_roots = designer_skill_roots(root)
    if profile == PROFILE_DESIGNER:
        if not skill_roots:
            return VERDICT_NOT_APPLICABLE, "no skill package with SKILL.md and assets/starter-pack was found"
        if len(skill_roots) > 1:
            return VERDICT_INCONCLUSIVE, f"multiple skill packages match the designer profile: {len(skill_roots)}"
        return None

    if profile == PROFILE_GENERATED and skill_roots:
        return VERDICT_NOT_APPLICABLE, f"repository matches {PROFILE_DESIGNER}; select that profile explicitly"
    return None


def build_terminal_report(root: Path, profile: str, verdict: str, detail: str) -> str:
    return "\n".join(
        [
            f"# Agent Pack Audit Report: {root.name}",
            "",
            "## Executive Summary",
            "",
            f"- Target project: `{root}`",
            f"- Profile: `{profile}`",
            f"- Audit result: `{verdict}`",
            f"- Detail: {detail}",
            "",
            "## Validation Evidence",
            "",
            "- No quality verdict was produced because the selected profile was not applicable or validation could not complete.",
            "",
        ]
    )


def write_report(path: Path, content: str) -> str | None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        return str(exc)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an agent pack or skill designer repository.")
    parser.add_argument("pack_path", help="Path to the profile root")
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        help=f"Validation profile; defaults to {PROFILE_GENERATED}",
    )
    parser.add_argument("--require-claude", action="store_true", help="Require CLAUDE.md for Claude Code target")
    parser.add_argument(
        "--audit-existing",
        action="store_true",
        help=f"Compatibility alias for --profile {PROFILE_MATURE}",
    )
    parser.add_argument(
        "--report-md",
        help=f"Write a Markdown report for the {PROFILE_MATURE} or {PROFILE_DESIGNER} profile",
    )
    args = parser.parse_args()

    if args.audit_existing and args.profile and args.profile != PROFILE_MATURE:
        parser.error(f"--audit-existing conflicts with --profile {args.profile}")
    profile = PROFILE_MATURE if args.audit_existing else (args.profile or PROFILE_GENERATED)
    if args.report_md and profile not in {PROFILE_MATURE, PROFILE_DESIGNER}:
        parser.error(f"--report-md is only supported with --profile {PROFILE_MATURE} or {PROFILE_DESIGNER}")

    root = Path(args.pack_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        detail = f"profile root is not a readable directory: {root}"
        print(f"ERROR: {detail}")
        print(f"RESULT: {VERDICT_TOOL_ERROR} {profile}")
        return 2

    applicability = profile_applicability(root, profile)
    if applicability:
        verdict, detail = applicability
        print(f"INFO: {detail}")
        if args.report_md:
            report_path = Path(args.report_md).expanduser().resolve()
            report_error = write_report(report_path, build_terminal_report(root, profile, verdict, detail))
            if report_error:
                print(f"ERROR: could not write report: {report_error}")
                print(f"RESULT: {VERDICT_TOOL_ERROR} {profile}")
                return 2
            print(f"REPORT: {report_path}")
        print(f"RESULT: {verdict} {profile}")
        return 2

    try:
        if profile == PROFILE_MATURE:
            errors, warnings = validate_existing_pack(root, args.require_claude)
        elif profile == PROFILE_DESIGNER:
            errors, warnings = validate_skill_designer_repository(root, args.require_claude)
        else:
            errors, warnings = validate_pack(root, args.require_claude)
    except ValidationFileError as exc:
        print(f"ERROR: {exc}")
        print(f"RESULT: {VERDICT_TOOL_ERROR} {profile}")
        return 2
    except OSError as exc:
        print(f"ERROR: {exc}")
        print(f"RESULT: {VERDICT_TOOL_ERROR} {profile}")
        return 2

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if args.report_md:
        report_path = Path(args.report_md).expanduser().resolve()
        if profile == PROFILE_DESIGNER:
            report_content = build_skill_designer_report(root, errors, warnings, args.require_claude)
        else:
            report_content = build_existing_pack_report(root, errors, warnings, args.require_claude)
        report_error = write_report(report_path, report_content)
        if report_error:
            print(f"ERROR: could not write report: {report_error}")
            print(f"RESULT: {VERDICT_TOOL_ERROR} {profile}")
            return 2
        print(f"REPORT: {report_path}")

    result = profile_result_label(profile, errors, warnings)
    print(f"RESULT: {result}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
