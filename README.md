# agent-pack-designer

Design minimal, validation-driven AI agent packs for Codex and Claude Code from project descriptions, README files, technical specs, or existing repository evidence.

`agent-pack-designer` is a portable Codex skill for creating or auditing small project-specific agent packs. It focuses on routing, role separation, validation ownership, and evidence boundaries, while avoiding speculative agents that increase maintenance cost.

It helps produce:

- [`AGENTS.md`](AGENTS.md) for Codex project rules.
- [`CLAUDE.md`](CLAUDE.md) for Claude Code project memory.
- `agents/context_router.md` for choosing the minimum useful context.
- one primary project-specific workflow agent.
- one risk or domain reviewer.
- `agents/validation_reviewer.md` for evidence and validation claims.
- `agents/task_spec_short.md` for non-trivial tasks.
- optional extra agents only when current project evidence justifies them.

## Operating Workflow

Use `agent-pack-designer` in two main situations:

| Situation | Use this path | Expected result |
|---|---|---|
| You are starting from a project description, README, technical spec, or lightly documented repository | Create a new minimal pack | A small generated pack with one primary agent, one reviewer, validation ownership, and clear Codex/Claude support boundaries |
| Your project already has agents, reviewers, routing files, Claude files, or project memory | Audit the existing mature pack first | A read-only diagnosis of routing, role separation, validation claims, token economy, and the smallest justified update |

The safest first run for a new user is an audit or proposal before adding files:

    Use $agent-pack-designer to audit this project for a minimal Codex/Claude agent pack. Check current docs, routing needs, validation evidence, and agent count. Propose the smallest useful pack or update, but do not create files yet.

For a new minimal pack:

    Use $agent-pack-designer to design a minimal Codex/Claude agent pack for this project from README.md and the current repository. Keep it small, create only justified agents, and state validation level.

For an existing mature pack:

    Use $agent-pack-designer to audit the existing agent pack against the current repository. Check routing, role separation, validation claims, token economy, and Codex/Claude compatibility. If the pack is outdated, propose the smallest update: revise existing agents first, add new agents only when justified, and state validation level.

Run the audit again when the project materially changes, for example when:

- new subsystems or recurring workflows appear;
- validation commands, CI, deployment, or release gates change;
- documentation grows beyond the assumptions in the current agents;
- the project gains a new dominant risk, such as security, data quality, model leakage, reproducibility, API runtime, or release readiness;
- Codex or Claude Code support is added, removed, or made explicit.

The expected outcome is not always a new agent. Often the right update is a tighter `agents/context_router.md`, clearer validation ownership, renamed project-specific agents, or removal of speculative roles.

Use the default generated-pack shape for new packs. Use the `mature-existing-pack` profile when auditing a real project that already has its own agent layout:

    python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack /path/to/project

For a customer-facing audit report:

    python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack --report-md reports/customer/report.md /path/to/project

## Status

Version: 0.2.0

Current release `v0.2.0`: L5 package release readiness for the `agent-pack-designer` skill package.

Evidence currently recorded in [`reports/validation/`](reports/validation/):

- L1 sample prompt evidence.
- L2 generated-pack consistency evidence across three projects.
- L3 real-project simulation evidence for `hiking-route-recommender-demo`.
- L4-with-risks cross-project runtime regression evidence.
- L5 package release-readiness evidence.

Scope boundaries:

- L5 applies to this package's release surface, install path, public documentation, red-team review, and recorded residual risk.
- `validate_pack.py --profile generated-pack` proves L2 structural consistency for a generated pack. It does not prove target-project runtime behavior.
- Runtime, production, deployment, model-quality, or project-specific claims require separate command output or recorded evidence.

## Codex And Claude Code Support

| Surface | Support model | What this repository provides |
|---|---|---|
| Codex | Installable skill | [`agent-pack-designer/SKILL.md`](agent-pack-designer/SKILL.md), [`agents/openai.yaml`](agent-pack-designer/agents/openai.yaml), references, starter pack templates, and validation scripts |
| Claude Code | Project memory and reviewer agents | [`CLAUDE.md`](CLAUDE.md) plus `.claude/agents/` guidance for architecture, compatibility, and validation review |
| Generated project packs | Cross-tool project guidance | [`AGENTS.md`](AGENTS.md) for Codex, optional [`CLAUDE.md`](CLAUDE.md) for Claude Code, shared `agents/` routing and reviewer files when the target project needs both |

Codex has the direct install path. Claude Code support is file-based: use this repository's [`CLAUDE.md`](CLAUDE.md) and `.claude/agents/`, or generate equivalent project files for a target repository.

## Install For Codex

From the repository root:

    mkdir -p ~/.codex/skills
    cp -R agent-pack-designer ~/.codex/skills/agent-pack-designer

Restart Codex, then use:

    Use $agent-pack-designer to design a minimal agent pack for this project from README.md and AGENTS.md.

The installable skill folder contains:

    agent-pack-designer/
      SKILL.md
      agents/openai.yaml
      references/
      assets/starter-pack/
      scripts/validate_skill.py
      scripts/validate_pack.py

## Use With Claude Code

Claude Code can use:

1. `CLAUDE.md` for project memory and working rules.
2. `.claude/agents/` for reviewer agents that check architecture, compatibility, and validation.

Example prompt:

    Use this repository to design a minimal Codex/Claude agent pack for my project. Keep the pack small and state validation level.

## Expected Output

A generated project pack should normally contain:

    AGENTS.md
    CLAUDE.md
    agents/
      context_router.md
      primary_agent.md
      risk_reviewer.md
      validation_reviewer.md
      task_spec_short.md

Rename `primary_agent.md` and `risk_reviewer.md` to project-specific names when the target project has clear domain language. Keep one risk or domain reviewer in every generated pack. When no single specialized risk dominates, keep it as a lightweight general project risk reviewer rather than adding multiple speculative reviewers.

## Validation Levels

| Level | What it proves | What it does not prove |
|---|---|---|
| L0 | Files, Markdown, YAML, naming, and obvious contradictions were statically checked | The pack works for a real task |
| L1 | One realistic prompt or task was tried and recorded | The pack is consistent across all routes or project types |
| L2 | Generated-pack routing, names, roles, stop rules, and templates are structurally consistent | Runtime behavior, production readiness, or mature-pack quality |
| L3 | The pack was applied to one real project case and the output was inspected | Cross-project robustness |
| L4 | Several materially different project cases were checked | Public release readiness or absence of residual risk |
| L5 | Release checks, red-team review, install verification, public docs, and residual risk were recorded | Runtime readiness of every target project using the pack |

Claim rules:

- Never claim runtime validation unless commands were actually run and inspected.
- Treat README and specs as intent, not proof of implementation.
- Treat tests, smoke checks, dry-runs, and command output as evidence.
- Do not treat `validate_pack.py` success as L3, L4, or L5; the generated-pack profile proves L2 structural consistency only.

## Validate

Validate the skill scaffold:

    python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer

Expected result:

    RESULT: PASS L0

Validate a generated project pack. This remains the default profile for backward compatibility:

    python3 agent-pack-designer/scripts/validate_pack.py --profile generated-pack /path/to/generated-pack

Expected result for a structurally consistent generated pack:

    RESULT: PASS L2

Audit an existing mature project pack without requiring the generated starter-pack shape:

    python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack /path/to/project

Validate a repository that owns an agent-pack design skill and intentional starter templates:

    python3 agent-pack-designer/scripts/validate_pack.py --profile skill-designer-repository /path/to/repository

Write a customer-facing Markdown audit report:

    python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack --report-md reports/customer/report.md /path/to/project

`--audit-existing` remains a compatibility alias for `--profile mature-existing-pack`.
The mature profile checks routing, role separation, validation ownership, audit-section signals, and token economy; it does not claim generated-pack L2 consistency.
Profile mismatches return `NOT_APPLICABLE`; ambiguous targets return `INCONCLUSIVE`; read or processing failures return `TOOL_ERROR`.
The designer profile uses the installed validator implementation and does not execute validator code from the target repository.
Customer-facing audit reports are generated artifacts; keep them under the gitignored [`reports/customer/`](reports/customer/) folder unless a report must become formal validation evidence.

Higher validation levels require recorded trials:

- L1: one sample project prompt.
- L2: generated-pack consistency review.
- L3: one real project simulation.
- L4: cross-project regression.
- L5: public/release readiness review.

## Example Audit Reports

Example customer-facing audit reports live under [`reports/customer/`](reports/customer/).

They were generated with:

    python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack --report-md reports/customer/<report-name>.md /path/to/project

These reports show the expected audit-report format for mature existing packs: routing, role separation, validation ownership, token economy, Codex/Claude compatibility, verdicts, and residual risks.

Customer reports are generated artifacts. They are examples and handoff outputs, not active agent-pack inputs. Keep new customer reports under the gitignored [`reports/customer/`](reports/customer/) folder unless a report must become formal validation evidence.

## Design Principles

- Minimal context first.
- One main agent, one reviewer, one validation path.
- Project-specific agents stay inside the target project.
- Separate implementation, review, validation, and red-team responsibilities.
- Prefer revising existing agents before adding new ones.
- Do not add agents for hypothetical future tasks.

## Language Policy

Public/installable skill files are kept in English. Russian validation reports are acceptable during active development. For the current release-readiness pass, earlier Russian working reports were relocated under [`reports/validation/internal_ru/`](reports/validation/internal_ru/), while public docs and the current L5 report are English.

## Repository Layout

    agent-pack-designer/
      SKILL.md
      agents/openai.yaml
      references/
      assets/starter-pack/
      scripts/validate_skill.py
      scripts/validate_pack.py
    .claude/agents/
    AGENTS.md
    CLAUDE.md
    CHANGELOG.md
    reports/validation/
    README.md
    VERSION
    LICENSE

## Release Notes

0.2.0 is tagged as the L5 package release-readiness release.

The release includes L2 generated-pack consistency validation, one L3 real-project simulation, an L4-with-risks runtime regression protocol across three target projects, and an L5 package release-readiness protocol.

Remaining post-0.2 work:

- Consider an installer only if manual copy becomes a recurring problem.

## License

MIT
