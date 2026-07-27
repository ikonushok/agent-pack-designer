# Agent Pack Audit Report: mt5-research

## Executive Summary

- Target project: `/Users/bobrsubr/PycharmProjects/_trading/mt5-research`
- Profile: `mature-existing-pack`
- Audit result: `PASS_WITH_RISKS EXISTING_PACK_AUDIT`
- Role agents found: 16
- Routing sources: `AGENTS.md`, `agents/README_agents_index.md`, `CLAUDE.md`
- Validation reviewer: `agents/test_validation.md`
- Claude context: present

## What Works Well

- Root AGENTS.md exists and centralizes project-level guidance.
- Routing source exists: AGENTS.md, agents/README_agents_index.md, CLAUDE.md.
- Routing tells future agents not to load every role file at once, which protects context budget.
- Project-level forbidden changes or protected contracts are documented.
- Task spec agent exists, supporting scoped work before edits.
- 16 role-scoped agent files were found and can be routed by task.

## Problems And Risks

- agents/test_validation.md is a validation alias but lacks level terms: L0, L1, L2, L3, L4
- agents/candidate_selector.md lacks audit section signals: when to use, inspect first
- agents/cascade_builder.md lacks audit section signals: inspect first
- agents/data_quality.md lacks audit section signals: when to use
- agents/decision_log_handoff.md lacks audit section signals: inspect first
- agents/execution_reviewer.md lacks audit section signals: when to use, inspect first
- agents/grid_pending_order_reviewer.md lacks audit section signals: when to use, inspect first
- agents/monthly_cashflow_reviewer.md lacks audit section signals: when to use, inspect first
- agents/mql5_engineer.md lacks audit section signals: when to use
- agents/production_monitor.md lacks audit section signals: when to use, inspect first
- agents/risk_manager.md lacks audit section signals: when to use, inspect first
- agents/state_recovery_reviewer.md lacks audit section signals: when to use, inspect first
- agents/strategy_research.md lacks audit section signals: inspect first

## Recommended Changes

- Add short Inspect First sections to role files that currently imply context but do not name initial files or artifacts.
- Add explicit When to Use triggers to role files that rely only on external routing.

## Token Economy

- The pack has a positive token-economy pattern: routing discourages loading all agents.
- Approximate total role-agent text: 5222 tokens across 16 files.
- Approximate minimal routed context: 2665 tokens before task-specific source files.
- No role file is estimated above the heavy threshold.

## Agent-By-Agent Review

| Agent | Kind | Est. tokens | Token economy | Missing audit signals |
|---|---|---:|---|---|
| `agents/architect.md` | primary | 404 | lean | none |
| `agents/backtest_validator.md` | reviewer | 313 | lean | none |
| `agents/candidate_selector.md` | reviewer | 287 | lean | when to use, inspect first |
| `agents/cascade_builder.md` | reviewer | 306 | lean | inspect first |
| `agents/data_quality.md` | reviewer | 320 | lean | when to use |
| `agents/decision_log_handoff.md` | reviewer | 233 | lean | inspect first |
| `agents/execution_reviewer.md` | reviewer | 255 | lean | when to use, inspect first |
| `agents/grid_pending_order_reviewer.md` | reviewer | 239 | lean | when to use, inspect first |
| `agents/monthly_cashflow_reviewer.md` | reviewer | 244 | lean | when to use, inspect first |
| `agents/mql5_engineer.md` | primary | 320 | lean | when to use |
| `agents/production_monitor.md` | reviewer | 252 | lean | when to use, inspect first |
| `agents/red_team.md` | reviewer | 782 | moderate | none |
| `agents/risk_manager.md` | reviewer | 301 | lean | when to use, inspect first |
| `agents/state_recovery_reviewer.md` | reviewer | 254 | lean | when to use, inspect first |
| `agents/strategy_research.md` | reviewer | 288 | lean | inspect first |
| `agents/test_validation.md` | reviewer | 424 | lean | none |

## Validation Evidence

- Command: `python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack /Users/bobrsubr/PycharmProjects/_trading/mt5-research`
- Result: `PASS_WITH_RISKS EXISTING_PACK_AUDIT`
- This report audits existing-pack quality and routing. It does not claim generated-pack L2 consistency.
