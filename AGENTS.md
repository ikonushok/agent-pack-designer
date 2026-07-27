# AGENTS.md

This repository builds `agent-pack-designer`: a portable skill for designing minimal, validation-driven AI agent packs for Codex and Claude from project descriptions.

## Roles

- Codex: edit files, inspect diffs, run validation, prepare releases.
- Claude Code: use `CLAUDE.md` plus `.claude/agents/` for architecture and compatibility review.
- Generated packs: must stay project-specific and minimal.

## Working Rules

1. Prefer a small pack: `AGENTS.md` / `CLAUDE.md`, `context_router.md`, one main agent, `validation_reviewer.md`, `task_spec_short.md`, and a reviewer only when a concrete recurring risk or domain workflow justifies it.
2. Do not add agents for hypothetical future tasks.
3. Separate implementation agents from reviewers.
4. Keep `SKILL.md` concise; move details to `references/`.
5. Generated outputs must state validation level: L0-L5.
6. Do not claim runtime validation unless commands were actually run.
7. Use `PASS`, `PASS_WITH_RISKS`, `RETEST`, `HOLD`, and `BLOCK` as the repository review verdict vocabulary.

## Language Policy

- Public/installable skill files must be English: `SKILL.md`, `references/`, `assets/starter-pack/`, scripts, `README.md`, `CHANGELOG.md`.
- Russian working reports are allowed under `reports/validation/` before international release.
- Before a public international release, run a language/publication pass: translate or relocate Russian reports, keep public docs English, and record the pass in validation evidence.
- Do not claim international/public readiness until the language/publication pass is complete.

## Validation

- L0: file structure and Markdown/YAML checks.
- L1: one sample project prompt.
- L2: generated pack consistency.
- L3: real project simulation.
- L4: cross-project regression.
- L5: public/release readiness.

Decision vocabulary:

- PASS: checks passed with sufficient evidence.
- PASS_WITH_RISKS: checks passed, but residual risk or missing evidence remains.
- RETEST: a change was made and the relevant check must be rerun.
- HOLD: design or evidence needs revision before release.
- BLOCK: unsafe, misleading, or unsupported claims must be fixed before proceeding.
