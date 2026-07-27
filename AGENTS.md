# AGENTS.md

This repository builds `agent-pack-designer`: a portable skill for designing minimal, validation-driven AI agent packs for Codex and Claude from project descriptions.

## Roles

- Codex: edit files, inspect diffs, run validation, prepare releases.
- Claude Code: use `CLAUDE.md` plus `.claude/agents/` for architecture and compatibility review.
- Generated packs: must stay project-specific and minimal.

## Working Rules

1. Prefer a small pack: `AGENTS.md` / `CLAUDE.md`, `context_router.md`, one main agent, one reviewer, `validation_reviewer.md`, `task_spec_short.md`.
2. Do not add agents for hypothetical future tasks.
3. Separate implementation agents from reviewers.
4. Keep `SKILL.md` concise; move details to `references/`.
5. Generated outputs must state validation level: L0-L5.
6. Do not claim runtime validation unless commands were actually run.

## Validation

- L0: file structure and Markdown/YAML checks.
- L1: one sample project prompt.
- L2: generated pack consistency.
- L3: real project simulation.
- L4: cross-project regression.
- L5: public/release readiness.
