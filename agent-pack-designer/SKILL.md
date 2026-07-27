---
name: agent-pack-designer
description: Design, generate, audit, or revise minimal validation-driven AI agent packs for Codex, Claude Code, and Claude skills from project descriptions, README files, specs, existing workflows, or repository evidence. Use when creating or improving AGENTS.md, CLAUDE.md, context routers, primary workflow agents, reviewers, task specs, validation loops, installable skill scaffolds, or release-ready agent-pack templates while avoiding agent sprawl and unsupported validation claims.
---

# Agent Pack Designer

Turn project context into a small, usable agent pack with explicit evidence.

## Default Output Shape

Use the smallest pack that can route work and validate claims:

- `AGENTS.md` for Codex project rules.
- `CLAUDE.md` when Claude Code will use the project.
- `agents/context_router.md` to choose the minimum useful context.
- `agents/<primary_workflow_agent>.md` for the main project workflow.
- `agents/<risk_or_domain_reviewer>.md` only when a concrete risk exists.
- `agents/validation_reviewer.md` to judge evidence level.
- `agents/task_spec_short.md` for non-trivial tasks.

Use `assets/starter-pack/` as the base structure, then rename placeholder agents to project-specific names.

## Workflow

1. Identify the target project, intended users, source-of-truth files, common tasks, risky contracts, and available validation commands.
2. Read only the references needed for the current job:
   - `references/design-workflow.md` when generating or restructuring a pack.
   - `references/agent-quality-rubric.md` when reviewing agent quality.
   - `references/validation-levels.md` before assigning L0-L5 or release readiness.
3. Choose the smallest useful pack. Add an agent only when it has a distinct trigger, inputs, checklist, output, and stop rule.
4. Fill the starter templates with project-specific names, files, commands, forbidden changes, and acceptance criteria.
5. Run static validation when possible. Use `scripts/validate_skill.py <path-to-skill>` for this skill scaffold, or adapt the same checks for generated packs.
6. Report the achieved validation level and separate:
   - documented assumptions;
   - evidence visible in files;
   - commands actually run;
   - checks not performed.

## Generation Rules

- Prefer one primary implementation agent plus one reviewer. Do not add agents for hypothetical future tasks.
- Keep implementation, review, validation, and red-team responsibilities separate.
- Keep agents project-specific. Avoid generic agents that could apply to every repository.
- Put rare or speculative roles outside the default pack or omit them.
- Use concise, imperative instructions. Make triggers and stop rules explicit.
- Treat README and specs as intent, not proof. Runtime claims require command output.

## References

Read only the files required by the request. Do not load all references by default.

## Stop Rules

- Do not create many agents by default.
- Do not merge implementation, review, validation, and red-team into one agent.
- Do not claim tests or runtime checks passed unless command output was inspected.
- Do not claim public/release readiness below the evidence threshold described in `references/validation-levels.md`.
