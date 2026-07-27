# Context Router

Goal: choose the smallest useful context, task mode, primary agent, reviewer, and validation path.

## Inputs

Inspect only what is needed:

- user request;
- `AGENTS.md`;
- `CLAUDE.md` when Claude Code is in scope;
- {{SOURCE_OF_TRUTH_FILES}};
- relevant tests, scripts, or CI config.

## Task Modes

- inspect: understand current behavior or files;
- plan: propose a scoped approach;
- patch: edit project files;
- docs-sync: align instructions with implementation;
- validation: prove a claim;
- release: check readiness and residual risk.

## Routing

| Trigger | Primary context | Agent | Reviewer | Validation |
|---|---|---|---|---|
| Main project workflow | {{PRIMARY_FILES}} | `agents/primary_agent.md` | none by default | {{DEFAULT_VALIDATION}} |
| Risk-sensitive change | {{RISK_FILES}} | `agents/primary_agent.md` | `agents/risk_reviewer.md` | {{RISK_VALIDATION}} |
| Validation or release claim | Evidence files and command output | `agents/validation_reviewer.md` | none | L0-L5 check |
| Multi-step task | User request and allowed files | `agents/task_spec_short.md` | as triggered | task-specific |

## Output

Return:

- task mode;
- files to inspect;
- files to avoid;
- primary agent;
- optional reviewer;
- forbidden changes;
- target validation level.
