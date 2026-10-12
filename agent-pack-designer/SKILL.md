---
name: agent-pack-designer
description: Design, generate, audit, or revise minimal validation-driven AI agent packs for Codex, Claude Code, and Claude skills from project descriptions, README files, specs, existing workflows, or repository evidence. Use when creating or improving AGENTS.md, CLAUDE.md, context routers, primary workflow agents, reviewers, task specs, validation loops, installable skill scaffolds, or release-ready agent-pack templates while avoiding agent sprawl and unsupported validation claims.
---

# Agent Pack Designer

Turn project context into a small, usable agent pack with explicit evidence.

## Installed Version

At the start of a task, read `VERSION` in this skill directory to identify the installed package version. Include that version in validation reports, audits, release-readiness assessments, and compatibility diagnosis when it helps trace the result. Do not add it to ordinary user-facing replies unless it is relevant.

## Changes in 0.6.0

- Add optional role-level model profiles, account-scoped availability evidence, explicit user constraints and bounded fallback rules.
- Separate model selection from permission intent and effective runtime enforcement across Claude Code, local Codex and hosted environments.
- Add an offline resolver for supplied policy/catalog evidence; it proposes choices without discovering credentials, launching agents or changing settings.
- Extend existing routing/task/review templates without adding roles. See [model policy](references/model-policy.md) for the contract, examples and validation limits; repository release notes preserve earlier changes.

## Default Output Shape

Use the smallest pack that can route work and validate claims:

- `AGENTS.md` for Codex project rules.
- `CLAUDE.md` only when Claude Code is an explicit target runtime.
- `agents/context_router.md` to choose the minimum useful context.
- `agents/<primary_workflow_agent>.md` for the main project workflow.
- `agents/<risk_or_domain_reviewer>.md` only when a concrete recurring risk or domain review workflow justifies it.
- `agents/validation_reviewer.md` to judge evidence level; `agents/test_validation.md` is an acceptable project-specific alias.
- `agents/task_spec_short.md` for non-trivial tasks.

Use `assets/starter-pack/` as the base structure, then rename placeholder agents to project-specific names.

## Pack Categories

Classify files before adding them:

- Core: `AGENTS.md`, `agents/context_router.md`, one primary agent, validation reviewer, and `agents/task_spec_short.md`.
- Conditional reviewer: add one risk or domain reviewer only when current project evidence shows a recurring risk or review workflow.
- Claude-specific: `CLAUDE.md` and `.claude/agents/` only when Claude Code compatibility is required.
- Trigger-only domain agents: add when a mature project has recurring tasks that need distinct context, such as data quality, feature engineering, CV, model training, API runtime, documentation handoff, or submission building.
- Additional trigger-only risk reviewers: add only when a concrete risk deserves a separate review lens, such as leakage, security, reproducibility, metrics, red-team, or public release.
- Optional/future agents: omit from the default pack unless the project already has an active workflow for that area.

Many agents are acceptable for mature projects only when `context_router.md` keeps the default context to one primary agent plus zero or one triggered reviewer.

## Workflow

1. Identify the target project, intended users, source-of-truth files, common tasks, risky contracts, and available validation commands.
2. Read only the references needed for the current job:
   - `references/spec-discovery.md` to locate specifications and extract project requirements from Spec Kit, ordinary docs, or README sections.
   - `references/design-workflow.md` when generating or restructuring a pack.
   - `references/model-policy.md` when assigning models, subagent permissions or runtime configuration; leave inheritance in place when this is not needed.
   - `references/agent-quality-rubric.md` when reviewing agent quality.
   - `references/validation-levels.md` before assigning L0-L5 or release readiness.
3. Build a deliverable coverage inventory from discovered specifications and other source-of-truth files, with source references, acceptance criteria, non-goals, constraints, and validation expectations. Include required, submission, optional, bonus, extra-credit, stretch, artifact, table, and checklist sections. Every deliverable must be represented in the primary workflow, reviewer checklist, or explicit non-goal/status.
4. Choose the smallest useful pack. Include one primary agent and validation reviewer; add a risk or domain reviewer only when it has a distinct trigger, inputs, checklist, output, stop rule, and routing entry.
5. Fill the starter templates with project-specific names, files, commands, forbidden changes, and acceptance criteria. Add a completion contract: reuse existing code, justify new files, choose canonical knowledge destinations, check integration and artifact lifecycle, and name the next step with its purpose. Use the project's existing layout; [references/design-workflow.md](references/design-workflow.md#6-define-contracts) defines the decisions to encode. These criteria do not add approval gates or permission to clean up unrelated files. When actual subagents are in scope, define model profiles, evidence freshness, user constraints, permission intent and approved fallback in the existing policy destination. Discover availability through exposed account-scoped runtime tools; never infer it from a plan name or public catalog. Generate native configuration only for a named supported runtime. The optional `scripts/resolve_model_policy.py` evaluates supplied evidence; it does not perform discovery or deployment.
6. Select the validation profile before running static checks:
   - `generated-pack` for a materialized project pack;
   - `mature-existing-pack` for an established project with equivalent role names or layouts;
   - `skill-designer-repository` for a repository that owns templates and validation tooling.
   Use `scripts/validate_skill.py <path-to-skill>` for the installable scaffold and `scripts/validate_pack.py --profile <profile> <path>` for the selected target.
7. Start the completion response with the result, then the next concrete step and its purpose (or state that no further step is needed). Distinguish authorized remaining work from a recommendation. Report the achieved validation level and separate:
   - documented assumptions;
   - evidence visible in files;
   - commands actually run;
   - checks not performed.

Use chat for transient verification status. Save cross-session knowledge in its canonical existing document; create a standalone report only for a requested deliverable or experiment reproducibility. Preserve required preflight/evidence with the experiment. An output format named "Report" does not require a new file.

## Generation Rules

- Prefer one primary implementation agent plus a reviewer only when a concrete recurring risk or domain workflow justifies it. Do not add agents for hypothetical future tasks.
- Optional/future agents are not the same as optional, bonus, extra-credit, stretch, or additional project deliverables. Do not silently omit optional deliverables from the project workflow; include explicit status such as `implemented`, `not implemented`, `not claimed`, or `blocked`.
- For mature projects, allow multiple trigger-only domain agents when a router prevents loading them all by default.
- Keep implementation, review, validation, and red-team responsibilities separate.
- A role file does not select a model or authorize delegation. Preserve explicit user choices; inherit permitted parent settings when availability is unknown. Model changes do not expand permissions. Validate actual launch/enforcement separately from policy or static configuration; use [model policy](references/model-policy.md) only when this work is relevant.
- Keep agents project-specific. Avoid generic agents that could apply to every repository.
- Put rare or speculative roles outside the default pack or omit them.
- Use concise, imperative instructions. Make triggers and stop rules explicit.
- Centralize the generated project's code/knowledge/artifact policy in `AGENTS.md`; route the primary, task spec and reviewers to it instead of copying the full policy into every role. Map facts to actual maintained files, keep current instructions separate from history, and distinguish snapshots from live code/inputs.
- Evaluate completion behavior using the four scenarios in [references/agent-quality-rubric.md](references/agent-quality-rubric.md#completion-scenarios). Static validator success proves structure, not that an agent made these decisions correctly; record scenarios actually exercised and those still untested.
- Treat README and specs as intent, not proof. Runtime claims require command output.
- Before claiming L3-L5, cross-check discovered requirements against relevant code and tests and collect the evidence required for that level. Report documentation/implementation conflicts explicitly.

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
