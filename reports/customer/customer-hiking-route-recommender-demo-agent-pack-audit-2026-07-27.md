# Agent Pack Audit Report: hiking-route-recommender-demo

## Executive Summary

- Target project: [hiking-route-recommender-demo](https://github.com/ikonushok/hiking-route-recommender-demo)
- Profile: `mature-existing-pack`
- Audit result: `FAIL`
- Role agents found: 10
- Routing sources: [`AGENTS.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/AGENTS.md), [`agents/README.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/README.md)
- Validation reviewer: missing
- Claude context: absent

## What Works Well

- Root [`AGENTS.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/AGENTS.md) exists and centralizes project-level guidance.
- Routing source exists: [`AGENTS.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/AGENTS.md), [`agents/README.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/README.md).
- Project-level forbidden changes or protected contracts are documented.
- Task spec agent exists, supporting scoped work before edits.
- 10 role-scoped agent files were found and can be routed by task.

## Problems And Risks

- missing validation reviewer under [`agents/`](https://github.com/ikonushok/hiking-route-recommender-demo/tree/main/agents) or [`.claude/agents/`](https://github.com/ikonushok/hiking-route-recommender-demo/tree/main/.claude/agents)
- No separate validation reviewer was found, so evidence ownership is not explicit.
- [`AGENTS.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/AGENTS.md) does not name Working Rules
- [`CLAUDE.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/CLAUDE.md) is absent; Claude Code compatibility was not audited
- many agents exist, but routing does not clearly keep default context small
- [`agents/DEMO_ADAPTATION_REPORT.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/DEMO_ADAPTATION_REPORT.md) lacks audit section signals: when to use, inspect first, stop rules, output
- [`agents/api_runtime_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/api_runtime_reviewer.md) lacks audit section signals: when to use, inspect first
- [`agents/architect.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/architect.md) lacks audit section signals: inspect first, stop rules
- [`agents/candidate_merger_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/candidate_merger_reviewer.md) lacks audit section signals: when to use, inspect first
- [`agents/data_quality_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/data_quality_reviewer.md) lacks audit section signals: when to use, inspect first
- [`agents/docs_handoff.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/docs_handoff.md) lacks audit section signals: when to use, inspect first
- [`agents/ltr_dataset_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/ltr_dataset_reviewer.md) lacks audit section signals: when to use, inspect first
- [`agents/observability_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/observability_reviewer.md) lacks audit section signals: when to use, inspect first
- [`agents/recommender_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/recommender_reviewer.md) lacks audit section signals: when to use, inspect first
- [`agents/red_team.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/red_team.md) lacks audit section signals: inspect first, checklist
- decision vocabulary incomplete: PASS_WITH_RISKS, RETEST, HOLD, BLOCK
- Decision vocabulary is not fully standardized across [`AGENTS.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/AGENTS.md).

## Recommended Changes

- Add a validation reviewer under [`agents/`](https://github.com/ikonushok/hiking-route-recommender-demo/tree/main/agents) or [`.claude/agents/`](https://github.com/ikonushok/hiking-route-recommender-demo/tree/main/.claude/agents) to own evidence, commands run, missing checks, and validation level.
- Standardize review verdicts around PASS, PASS_WITH_RISKS, RETEST, HOLD, and BLOCK.
- Add short Inspect First sections to role files that currently imply context but do not name initial files or artifacts.
- Add explicit When to Use triggers to role files that rely only on external routing.
- Add or strengthen a context router that selects one primary agent plus at most one reviewer by default.

## Token Economy

- Token risk: routing does not clearly prevent loading the whole agents directory.
- Approximate total role-agent text: 5841 tokens across 10 files.
- Approximate minimal routed context: 3035 tokens before task-specific source files.
- No role file is estimated above the heavy threshold.

## Agent-By-Agent Review

| Agent | Kind | Est. tokens | Token economy | Missing audit signals |
|---|---|---:|---|---|
| [`agents/DEMO_ADAPTATION_REPORT.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/DEMO_ADAPTATION_REPORT.md) | reviewer | 850 | moderate | when to use, inspect first, stop rules, output |
| [`agents/api_runtime_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/api_runtime_reviewer.md) | reviewer | 460 | lean | when to use, inspect first |
| [`agents/architect.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/architect.md) | primary | 666 | lean | inspect first, stop rules |
| [`agents/candidate_merger_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/candidate_merger_reviewer.md) | reviewer | 449 | lean | when to use, inspect first |
| [`agents/data_quality_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/data_quality_reviewer.md) | reviewer | 684 | lean | when to use, inspect first |
| [`agents/docs_handoff.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/docs_handoff.md) | reviewer | 506 | lean | when to use, inspect first |
| [`agents/ltr_dataset_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/ltr_dataset_reviewer.md) | reviewer | 510 | lean | when to use, inspect first |
| [`agents/observability_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/observability_reviewer.md) | reviewer | 366 | lean | when to use, inspect first |
| [`agents/recommender_reviewer.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/recommender_reviewer.md) | reviewer | 571 | lean | when to use, inspect first |
| [`agents/red_team.md`](https://github.com/ikonushok/hiking-route-recommender-demo/blob/main/agents/red_team.md) | reviewer | 779 | moderate | inspect first, checklist |

## Validation Evidence

- Command: `python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack /path/to/project`
- Result: `FAIL`
- This report audits existing-pack quality and routing. It does not claim generated-pack L2 consistency.
