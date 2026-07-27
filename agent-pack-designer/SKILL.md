---
name: agent-pack-designer
description: Design minimal, validation-driven AI agent packs for Codex, Claude, and ChatGPT from project descriptions, README files, specs, or existing workflows. Use when creating AGENTS.md, CLAUDE.md, context routers, specialized agents, reviewers, templates, validation loops, or when auditing agent-pack quality and avoiding agent sprawl.
---

# Agent Pack Designer

Turn project context into a small, usable agent pack.

## Workflow

1. Identify project type, goal, source-of-truth files, risks, and validation commands.
2. Choose the smallest useful pack:
   - `AGENTS.md`
   - `CLAUDE.md` when Claude Code is used
   - `agents/context_router.md`
   - one primary domain/workflow agent
   - one reviewer when risk exists
   - `agents/validation_reviewer.md`
   - `agents/task_spec_short.md`
3. Keep domain-specific agents inside the generated project pack.
4. Put rare roles in `optional_agents/`.
5. State validation level L0-L5.
6. Separate what is documented, visible in files, confirmed by commands, and not checked.

## References

Read only what is needed:

- `references/design-workflow.md` for pack design steps.
- `references/agent-quality-rubric.md` for agent review.
- `references/validation-levels.md` for evidence labels.

## Assets

Use `assets/starter-pack/` as the base structure for generated packs.

## Stop Rules

- Do not create many agents by default.
- Do not merge implementation, review, validation, and red-team into one agent.
- Do not claim tests or runtime checks passed unless command output was inspected.
