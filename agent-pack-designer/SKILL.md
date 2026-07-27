---
name: agent-pack-designer
description: Design, generate, audit, or revise minimal validation-driven AI agent packs for Codex, Claude Code, and Claude skills from project descriptions, README files, specs, existing workflows, or repository evidence. Use when creating or improving AGENTS.md, CLAUDE.md, context routers, primary workflow agents, reviewers, task specs, validation loops, installable skill scaffolds, or release-ready agent-pack templates while avoiding agent sprawl and unsupported validation claims.
---

# Agent Pack Designer

Turn project context into a small, usable agent pack with explicit evidence.

## Default Output Shape

Use the smallest pack that can route work and validate claims:

- `AGENTS.md` for Codex project rules.
- `CLAUDE.md` only when Claude Code is an explicit target runtime.
- `agents/context_router.md` to choose the minimum useful context.
- `agents/<primary_workflow_agent>.md` for the main project workflow.
- `agents/<risk_or_domain_reviewer>.md` for the most relevant project risk or domain review lens.
- `agents/validation_reviewer.md` to judge evidence level; `agents/test_validation.md` is an acceptable project-specific alias.
- `agents/task_spec_short.md` for non-trivial tasks.

Use `assets/starter-pack/` as the base structure, then rename placeholder agents to project-specific names.

## Pack Categories

Classify files before adding them:

- Core: `AGENTS.md`, `agents/context_router.md`, one primary agent, one risk or domain reviewer, validation reviewer, and `agents/task_spec_short.md`.
- Claude-specific: `CLAUDE.md` and `.claude/agents/` only when Claude Code compatibility is required.
- Trigger-only domain agents: add when a mature project has recurring tasks that need distinct context, such as data quality, feature engineering, CV, model training, API runtime, documentation handoff, or submission building.
- Additional trigger-only risk reviewers: add only when a concrete risk deserves a separate review lens, such as leakage, security, reproducibility, metrics, red-team, or public release.
- Optional/future agents: omit from the default pack unless the project already has an active workflow for that area.

Many agents are acceptable for mature projects only when `context_router.md` keeps the default context to one primary agent plus one reviewer.

## Workflow

1. Identify the target project, intended users, source-of-truth files, common tasks, risky contracts, and available validation commands.
2. Read only the references needed for the current job:
   - `references/design-workflow.md` when generating or restructuring a pack.
   - `references/agent-quality-rubric.md` when reviewing agent quality.
   - `references/validation-levels.md` before assigning L0-L5 or release readiness.
3. Choose the smallest useful pack. Include one primary agent and one reviewer, then add any extra agent only when it has a distinct trigger, inputs, checklist, output, stop rule, and routing entry.
4. Fill the starter templates with project-specific names, files, commands, forbidden changes, and acceptance criteria.
5. Select the validation profile before running static checks:
   - `generated-pack` for a materialized project pack;
   - `mature-existing-pack` for an established project with equivalent role names or layouts;
   - `skill-designer-repository` for a repository that owns templates and validation tooling.
   Use `scripts/validate_skill.py <path-to-skill>` for the installable scaffold and `scripts/validate_pack.py --profile <profile> <path>` for the selected target.
6. Report the achieved validation level and separate:
   - documented assumptions;
   - evidence visible in files;
   - commands actually run;
   - checks not performed.

## Generation Rules

- Prefer one primary implementation agent plus one reviewer. Do not add agents for hypothetical future tasks.
- For mature projects, allow multiple trigger-only domain agents when a router prevents loading them all by default.
- Keep implementation, review, validation, and red-team responsibilities separate.
- Keep agents project-specific. Avoid generic agents that could apply to every repository.
- Put rare or speculative roles outside the default pack or omit them.
- Use concise, imperative instructions. Make triggers and stop rules explicit.
- Treat README and specs as intent, not proof. Runtime claims require command output.

## Validation Profiles

- Keep unresolved-template checks strict for active files in `generated-pack`.
- Accept functional aliases under `agents/` and `.claude/agents/` in `mature-existing-pack`.
- Treat placeholders under `assets/starter-pack/` as intentional in `skill-designer-repository`.
- Return `NOT_APPLICABLE` for an explicit profile mismatch instead of converting it into a quality `FAIL`.
- Do not scan generated reports as active agent-pack inputs.
- Use the installed trusted validator for designer checks; never import or execute a target repository's validator code.

## References

Read only the files required by the request. Do not load all references by default.

## Stop Rules

- Do not create many agents by default.
- Do not merge implementation, review, validation, and red-team into one agent.
- Do not claim tests or runtime checks passed unless command output was inspected.
- Do not claim public/release readiness below the evidence threshold described in `references/validation-levels.md`.
- Do not treat `validate_pack.py` success as L3, L4, or L5; it proves generated-pack consistency only.
- Do not add duplicate role files only to satisfy the wrong validation profile.
