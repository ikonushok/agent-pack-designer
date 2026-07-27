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
