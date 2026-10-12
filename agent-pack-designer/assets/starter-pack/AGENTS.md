# AGENTS.md

Project: {{PROJECT_NAME}}

This file is the project-specific contract for Codex.

## Working Rules

1. Start with `agents/context_router.md` and load only the context needed for the task.
2. Use `agents/primary_agent.md` for the main implementation or workflow path.
3. Use `agents/risk_reviewer.md` only when the task touches the named risk area.
4. Use `agents/validation_reviewer.md` before claiming tests, release readiness, or production safety.
5. Use `agents/task_spec_short.md` before non-trivial edits or multi-step work.
6. Keep changes scoped to the user request and the files allowed by the task spec.
7. Name the immediate action and its purpose at the start. In the final response, give the result followed immediately by the next step and why it is useful; distinguish recommendations from authorized work, or say no further step is needed.

## Code, Knowledge and Artifacts

- Find existing code, callers and the canonical document before adding files; justify each new file instead of duplicating a workflow.
- Check integration through entrypoints, imports/callers, CLI, configs and docs before completion. Resolve task-local duplication/temporary workarounds; document retained transition paths with their consumer, reason and migration condition.
- Map durable decisions to the project's maintained requirements, contracts, commands, architecture or evaluation documents. Keep one canonical source per fact and links elsewhere. Update current instructions; keep dated history distinct. Chat is sufficient for transient status, not the only store of knowledge another session needs.
- A standalone report needs a requested deliverable or reproducibility purpose. Preserve required preflight and frozen experiment evidence in one evidence set; review passes reference it. A completion report is normally response content, not another file.
- Follow the existing project layout for live code, permanent inputs, results and archives. Preserve source snapshots used as evidence. Avoid new permanent imports/input dependencies on disposable report directories; expose another frozen input version explicitly when needed.
- Archive only in authorized scope after checking callers, configs, commands, links, frozen provenance and active consumers. Preserve needed inputs/human evidence, verify preservation, map old/new paths and update current references. Keep historical hashes intact. Preserve active consumers and record deferred migration conditions; age alone is not a removal criterion.

## Model and Permissions

- Default: inherit the primary agent's model and reasoning settings when compatible with user constraints; no extra subagent is required. Role files do not switch models or authorize delegation.
- When model assignment is useful, maintain approved task profiles/candidates, explicit user choices, budget limits, evidence source/time/freshness and fallback in this section or the existing runtime configuration. Discover choices through exposed account-scoped runtime tools; match surface, sign-in method and identity. A plan name, public catalog or saved model setting does not prove access.
- Treat unavailable/stale evidence as unknown; inherit a permitted parent or identify the missing input. Preserve explicit model/effort requirements. Refresh at session/identity changes, expiry or failure; use only approved fallback and stop repeated failures after one refresh/reselection attempt. Do not silently expand cost, lower required quality or adopt a newly listed model.
- Keep model selection separate from rights: research/review normally reads, authorized implementation writes within scope, and validation may need caches/output in an allowed location. More reasoning does not grant more permissions.
- Native model/tool/sandbox configuration applies only to the named supported runtime. Report requested versus resolved model and permission intent versus observed enforcement. Do not claim read-only protection from prompt wording or Write/Edit denial while shell/MCP mutation paths remain available.

## Forbidden Changes

- Do not broaden scope without user approval.
- Do not add new agents for hypothetical future tasks.
- Do not merge implementation and review responsibilities into one agent.
- Do not claim validation beyond the evidence actually inspected.

## Validation

Current validation level: L0 until project-specific checks are run.

Report:

- files inspected;
- commands run and outcomes;
- validation level achieved;
- missing evidence;
- residual risk.
