# CLAUDE.md

@AGENTS.md

This repository contains a portable agent-pack design skill for Codex and Claude.

Use the smallest useful context. Do not load every reference unless needed.

## Context Order

1. Use the imported `AGENTS.md` content for repository-level rules and validation vocabulary.
2. Read only the relevant `.claude/agents/` file for architecture, compatibility, or validation review.
3. Read `agent-pack-designer/SKILL.md` and the specific referenced file under `agent-pack-designer/references/` only when the task requires skill design details.

## Claude Code Agents

Use these reviewers when relevant:

- `agent-pack-architect` — design or restructure the skill/starter pack.
- `skill-compatibility-reviewer` — check Codex and Claude portability.
- `validation-reviewer` — check evidence level and release readiness.

## Constraints

- Keep generated project packs minimal.
- Preserve Codex / Claude / ChatGPT role separation.
- Do not turn README claims into evidence.
- Prefer incremental edits over broad restructuring.
- Use PASS, PASS_WITH_RISKS, RETEST, HOLD, and BLOCK as review verdicts.
