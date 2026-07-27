# Design Workflow

Use this workflow when generating or restructuring a project agent pack.

## 1. Classify the Work

Choose one primary task mode:

- inspect: understand repository shape and current instructions;
- plan: design files and responsibilities without editing;
- patch: update an existing pack;
- design: create a new pack from project evidence;
- docs-sync: align README/specs with agent instructions;
- validation: prove the pack is coherent;
- red-team: find prompt, routing, privacy, or release risks.

## 2. Identify Evidence

Prefer source files over summaries:

- project purpose: README, product brief, package metadata, docs;
- architecture boundaries: source tree, module docs, ADRs, API specs;
- commands: package scripts, Makefile, CI config, test docs;
- existing agent rules: AGENTS.md, CLAUDE.md, .claude/agents;
- release gates: CI, lint, tests, smoke checks, deployment docs.

Do not treat README claims as runtime evidence.

## 3. Route Minimal Context

Define what each future agent should inspect first. A useful router names:

- task triggers;
- files or glob patterns to inspect;
- files to avoid unless needed;
- default primary agent;
- reviewer trigger;
- validation command or manual check.

## 4. Select Agents

Add an agent only when all are true:

- it has a distinct recurring task;
- it needs different context than the main agent;
- it has a concrete checklist or output format;
- it reduces risk or repeated context loading.

Default to one primary workflow agent, one concrete risk or domain reviewer, `validation_reviewer.md`, and `task_spec_short.md`.

Classify every selected file:

| Category | Include when | Examples |
|---|---|---|
| Core | Needed for routing, primary work, task scoping, or evidence review | `AGENTS.md`, `context_router.md`, primary agent, `validation_reviewer.md`, `task_spec_short.md` |
| Claude-specific | Claude Code is an explicit target runtime | `CLAUDE.md`, `.claude/agents/` |
| Trigger-only domain | A mature project has a recurring workflow with distinct context | data quality, feature engineering, CV, model training, API/runtime, submission builder |
| Trigger-only risk/review | A concrete recurring risk needs the required review lens or an additional separate review lens | leakage, metrics, reproducibility, red-team, docs/release |
| Optional/future | The role is useful only for planned or rare work | observability, LTR/ranking, migration, future platform adapters |

Many trigger-only agents are acceptable in a mature project if `context_router.md` explicitly prevents loading all agents by default and routes to one primary agent plus one reviewer.

## 5. Define Contracts

Every generated pack should state:

- allowed files and non-goals;
- forbidden changes;
- acceptance criteria;
- validation level target;
- what counts as sufficient evidence.

## 6. Validate and Report

Finish with:

- achieved validation level L0-L5;
- evidence inspected;
- commands run and results;
- missing evidence;
- residual risk;
- next smallest validation step.
