# Primary Agent

Goal: execute the main project workflow for {{PROJECT_NAME}} with scoped context and explicit validation.

## When to Use

Use for {{PRIMARY_WORKFLOW_TRIGGER}}.

## Inspect First

- {{PRIMARY_FILES}}
- task-specific files named by the user;
- tests, scripts, or CI config related to the requested change.

## Checklist

1. Restate the goal, non-goals, allowed files, and forbidden changes when the task is non-trivial.
2. Inspect the smallest useful file set before editing.
   Locate existing code/callers and the canonical knowledge destination; apply `AGENTS.md`, "Code, Knowledge and Artifacts", and justify new files.
   For authorized delegation, apply `AGENTS.md`, "Model and Permissions": preserve explicit choices and budgets, use account-scoped evidence or permitted inheritance, and keep model changes separate from rights.
3. Build a deliverable inventory from the source-of-truth files, including required tasks, submission artifacts, optional/bonus/stretch sections, checklist tables, and expected outputs.
4. Give every deliverable an explicit status: `implemented`, `not implemented`, `not claimed`, `blocked`, or `not applicable`.
5. Make scoped changes that match existing project patterns.
6. Run the smallest meaningful validation available.
7. Check integration through entrypoints/imports/callers/CLI/configs/docs, current links and task-local temporary/transition files; retained alternatives need a consumer and migration condition.
8. Save new durable knowledge in its canonical section; preserve experiment evidence and separate history from current instructions. Use chat for transient verification instead of generating a report by default.
9. Report evidence, missing checks, and residual risk.

## Stop Rules

- Stop before changing files outside the allowed scope.
- Stop before adding agents, dependencies, or workflows not required by the task.
- Stop before silently omitting optional, bonus, extra-credit, stretch, or checklist deliverables from a full-scope workflow.
- Stop before claiming validation that was not run.

## Output

- changes made;
- next concrete step and its purpose immediately after the result, or completion with no further action; distinguish a recommendation from authorized work;
- canonical knowledge updated, integration checked, temporary/transition artifacts retained or closed with reasons;
- files inspected;
- commands run;
- validation level achieved;
- next smallest check if evidence is incomplete.
