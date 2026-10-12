# Agent Quality Rubric

Use this rubric when reviewing generated agents or deciding whether another agent is justified.

## Required Fields

A good agent has:

- clear goal;
- specific when-to-use trigger;
- inputs to inspect first;
- focused checklist;
- output format;
- stop rules;
- sufficiency criteria;
- validation expectations.

## Quality Checks

Score each item as pass, risk, or fail:

- Scope: the agent owns one workflow or risk, not the whole project.
- Context: the agent starts from named files or patterns, not the full repository.
- Actionability: checklist items can be followed without extra interpretation.
- Separation: implementation, review, validation, and red-team work are not merged.
- Evidence: claims distinguish docs, inspected files, and executed commands.
- Portability: Codex and Claude-specific instructions are separated where needed.
- Model policy, when used: choices cite fresh evidence for the actual account/surface, respect explicit user constraints and have bounded fallback; permissions are verified separately from model selection. A role file or public model catalog is not proof of runtime access.
- Minimality: removing the agent would create real duplication or risk.
- Routing: every trigger-only agent is reachable from `context_router.md` or an equivalent routing matrix.
- Completion: the primary checks integration, temporary/transition artifacts and active links before declaring completion.
- Knowledge: durable decisions have one canonical maintained destination; transient status does not force a report file, and required experiment evidence is preserved.
- Continuation: the result is followed by a concrete next step and its purpose; recommendations do not silently expand authorization.

## Bad Signs

- usable for every task;
- duplicates another agent;
- loads the whole project by default;
- has no stop condition;
- asks future agents to trust README claims as proof;
- creates extra reviewers without a concrete risk or distinct review lens;
- uses platform-specific tooling without naming a fallback.
- ships many agents without a router that keeps default context small.
- creates a new report for every review pass, treats historical documents as current instructions, or deletes a snapshot merely because it duplicates source bytes.
- archives by age or block membership without checking frozen inputs, callers and active consumers.

## Completion Scenarios

Use a relevant real or isolated case to assess decisions and resulting artifacts. These are behavioral acceptance cases, not a request to add test/report files to every target repository. Name the evidence actually inspected; checking wording alone does not prove these outcomes.

| Case | Required observation | Failure signal |
|---|---|---|
| Ordinary verification, no new durable finding | Existing checks run; concise result, next action/purpose or completion; no gratuitous report | A report file is created just to announce PASS |
| New decision needed by another session | Existing canonical section updated; references remain current; decision can be found without chat history | Decision exists only in chat or contradictory copies |
| Reproducible experiment or required preflight | Frozen versions/inputs/commands/results/limits retained in one evidence set; reviewers reference it | Evidence discarded to reduce files, overwritten, or duplicated for each review |
| Authorized cleanup with an active consumer | Dependencies/processes checked; required inputs kept available; map/integrity recorded for completed moves, deferred items have a condition | Live input/code moved, process stopped merely for tidiness, or archive declared proof of integration |

Use [model-policy behavioral acceptance](model-policy.md#behavioral-acceptance) when model selection or permission enforcement is claimed. Offline resolver tests do not prove provider access, model quality, quota or runtime restrictions.

## Mature Pack Exception

A mature project may justify many agents when:

- each agent has a distinct recurring task or risk;
- `context_router.md` selects one primary agent and one reviewer by default;
- optional/future agents are labeled and not loaded in normal work;
- validation review remains separate from implementation and model selection;
- project evidence shows the roles match real workflows.

## Verdicts

- PASS: usable as-is for its named workflow.
- PASS_WITH_RISKS: usable, but validation or scope is incomplete.
- RETEST: likely usable after small edits and another validation pass.
- HOLD: needs design revision before use.
- BLOCK: unsafe, misleading, or too broad to include.
