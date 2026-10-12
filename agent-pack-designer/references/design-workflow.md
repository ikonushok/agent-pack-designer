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

Use [Specification Discovery](spec-discovery.md) to find task-relevant requirements in Spec Kit files, ordinary specification directories, documentation, or README sections. Extract deliverables, acceptance criteria, non-goals, constraints, and validation expectations with source references. Supplement missing or partial structured specs with ordinary docs; scaffold placeholders are not requirements.

Prefer source files over summaries:

- project purpose: README, product brief, package metadata, docs;
- architecture boundaries: source tree, module docs, ADRs, API specs;
- commands: package scripts, Makefile, CI config, test docs;
- existing agent rules: AGENTS.md, CLAUDE.md, .claude/agents;
- release gates: CI, lint, tests, smoke checks, deployment docs.

Treat README/spec claims as intent. Before assigning L3-L5, cross-check requirements against relevant implementation and tests, report conflicts, and collect the evidence required by [Validation Levels](validation-levels.md). Do not treat source or test files as proof that commands passed.

## 3. Inventory Deliverables

Before choosing agents, list the project deliverables from source-of-truth files:

- required tasks and acceptance criteria;
- submission artifacts and generated outputs;
- optional, bonus, extra-credit, stretch, or additional task sections;
- checklist tables, screenshots, etalon outputs, sample values, or expected review anchors;
- explicit non-goals or skipped sections.

Every deliverable must be handled in one of three ways:

- included in the primary workflow;
- included in a reviewer checklist or validation route;
- recorded as an explicit non-goal or status such as `implemented`, `not implemented`, `not claimed`, or `blocked`.

Do not convert optional deliverables into optional agents. Optional/future agent roles may be omitted, but optional project deliverables still need visible status so reviewers do not miss silent scope loss.

## 4. Route Minimal Context

Define what each future agent should inspect first. A useful router names:

- task triggers;
- files or glob patterns to inspect;
- files to avoid unless needed;
- default primary agent;
- reviewer trigger;
- validation command or manual check.

## 5. Select Agents

Add an agent only when all are true:

- it has a distinct recurring task;
- it needs different context than the main agent;
- it has a concrete checklist or output format;
- it reduces risk or repeated context loading.

Default to one primary workflow agent, `validation_reviewer.md`, and `task_spec_short.md`. Add one concrete risk or domain reviewer only when project evidence shows a recurring review need.

Classify every selected file:

| Category | Include when | Examples |
|---|---|---|
| Core | Needed for routing, primary work, task scoping, or evidence review | `AGENTS.md`, `context_router.md`, primary agent, `validation_reviewer.md`, `task_spec_short.md` |
| Claude-specific | Claude Code is an explicit target runtime | `CLAUDE.md`, `.claude/agents/` |
| Trigger-only domain | A mature project has a recurring workflow with distinct context | data quality, feature engineering, CV, model training, API/runtime, submission builder |
| Trigger-only risk/review | A concrete recurring risk needs the required review lens or an additional separate review lens | leakage, metrics, reproducibility, red-team, docs/release |
| Optional/future | The role is useful only for planned or rare work | observability, LTR/ranking, migration, future platform adapters |

Many trigger-only agents are acceptable in a mature project if `context_router.md` explicitly prevents loading all agents by default and routes to one primary agent plus zero or one triggered reviewer.

## 6. Define Contracts

Every generated pack should state:

- allowed files and non-goals;
- forbidden changes;
- acceptance criteria;
- validation level target;
- what counts as sufficient evidence.
- deliverable coverage status for required, submission, optional, bonus, and checklist artifacts.

### Code, knowledge and artifact lifecycle

Put the shared policy in generated `AGENTS.md`, with actual project paths and conventions. Extend the task spec and role checklists to apply it; do not create a new role for each item or ask permission merely because a file is new.

- Before adding code, locate the existing implementation, callers and entrypoint. Record the purpose of each new file and why reuse would not meet the request. A file outside the product-block inventory may be infrastructure, a test or a required snapshot; absence from a table and age alone do not prove it is redundant.
- Choose one canonical destination for each durable decision: requirements, data/API contracts, commands, architecture rationale or evaluation limits. Update the existing section and link from other documents. Transient status may stay in chat; decisions needed by another session must remain discoverable on disk.
- Separate maintained instructions from dated experiment/task history. Preserve versions, origin and applicability of historical evidence; do not accumulate contradictory "current" appendices. Create a standalone report only for a requested deliverable or reproducibility/comparison. Required preflight evidence belongs to the experiment's existing evidence set, with references from review passes instead of duplicate reports.
- Separate live source and permanent inputs from generated results using the project's layout. Source snapshots in an evidence set are valid reproducibility artifacts. Review imports, input paths and commands to ensure new permanent dependencies do not silently rely on disposable reports. Parameterize another frozen input version through the project's CLI/config when needed.
- Before completion, check integration through callers/imports, entrypoints, CLI, configs and docs; resolve task-local duplication and temporary workarounds. Retained compatibility paths need a concrete consumer, reason and condition for migration. Stay within the authorized scope.
- Before authorized archival, inspect reverse references, frozen provenance/hash contracts and active consumers/processes. Preserve needed inputs and human evidence, record old/new paths, verify preservation and update active links. Preserve historical hashes; version a changed producer/plan instead of relabeling its frozen history. If a consumer is active, leave its files in place and record the condition for later migration; do not stop it merely to tidy a directory.
- Start the final response with the result, immediately followed by a concrete next step and why it helps. Identify whether that step is already authorized work or a recommendation; if complete with no useful continuation, say so. At a blocker, name the missing input and how to obtain it. Do not invent follow-up work or substitute "I can continue" for an actionable step.

## 7. Validate and Report

Finish with:

- achieved validation level L0-L5;
- evidence inspected;
- commands run and results;
- missing evidence;
- residual risk;
- next smallest validation step.
- canonical location of new knowledge and disposition of temporary/transition artifacts.

Keep this evidence in the response and update existing knowledge sources when needed. A separate audit/completion file is not the default. Run [completion scenarios](agent-quality-rubric.md#completion-scenarios) when realistic application can add evidence; state unperformed behavioral checks rather than raising the level from template or keyword checks.
