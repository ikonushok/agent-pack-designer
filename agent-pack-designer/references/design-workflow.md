# Design Workflow

1. Classify the task: inspect, plan, patch, design, docs sync, validation, red-team.
2. Identify project source of truth: README, AGENTS.md, CLAUDE.md, specs, tests, CI, scripts.
3. Design minimal context routing.
4. Add only agents with distinct triggers and checklists.
5. Add reviewers for risky contracts: validation, README/spec drift, security, data leakage, release.
6. Define forbidden changes and acceptance criteria.
7. Report achieved validation level.
