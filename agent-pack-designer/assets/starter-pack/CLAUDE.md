# CLAUDE.md

Project: {{PROJECT_NAME}}

This file is the Claude Code project memory. Keep it concise and load extra docs only when the task requires them.

## Context Order

1. Read this file for project rules.
2. Read `AGENTS.md` when Codex compatibility or shared agent-pack behavior matters.
3. Read `agents/context_router.md` before choosing a specialized agent.
4. Read one primary agent and, only when triggered, one reviewer.

## Project Rules

- Respect the project source of truth: {{SOURCE_OF_TRUTH_FILES}}.
- Keep generated instructions project-specific and minimal.
- Treat README/spec claims as intent, not proof.
- State the validation level L0-L5 in final reports.

## Validation

Use the project commands listed in `agents/context_router.md` when available. Do not claim a command passed unless it was actually run and the result was inspected.
