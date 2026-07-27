# Agent Pack Audit Report: credit-default-prediction

## Executive Summary

- Target project: `/Users/bobrsubr/PycharmProjects/_researches/credit-default-prediction`
- Profile: `mature-existing-pack`
- Audit result: `PASS_WITH_RISKS EXISTING_PACK_AUDIT`
- Role agents found: 17
- Routing sources: `agents/context_router.md`, `AGENTS.md`, `agents/README.md`
- Validation reviewer: `agents/test_validation.md`
- Claude context: absent

## What Works Well

- Root AGENTS.md exists and centralizes project-level guidance.
- Routing source exists: agents/context_router.md, AGENTS.md, agents/README.md.
- Routing tells future agents not to load every role file at once, which protects context budget.
- Project-level forbidden changes or protected contracts are documented.
- Task spec agent exists, supporting scoped work before edits.
- 17 role-scoped agent files were found and can be routed by task.

## Problems And Risks

- CLAUDE.md is absent; Claude Code compatibility was not audited
- agents/baseline_builder.md lacks audit section signals: when to use
- agents/cv_validator.md lacks audit section signals: when to use
- agents/data_quality.md lacks audit section signals: when to use
- agents/decision_log_handoff.md lacks audit section signals: when to use, output
- agents/eda_analyst.md lacks audit section signals: when to use
- agents/experiment_manager.md lacks audit section signals: when to use, checklist
- agents/feature_engineer.md lacks audit section signals: when to use, checklist
- agents/interpretability_reviewer.md lacks audit section signals: when to use
- agents/leakage_guard.md lacks audit section signals: when to use
- agents/metric_validator.md lacks audit section signals: when to use
- agents/model_ensembler.md lacks audit section signals: when to use
- agents/model_trainer.md lacks audit section signals: when to use
- agents/red_team.md lacks audit section signals: when to use
- agents/reproducibility_reviewer.md lacks audit section signals: when to use
- agents/submission_builder.md lacks audit section signals: when to use
- agents/test_validation.md lacks audit section signals: when to use, inspect first

## Recommended Changes

- Add short Inspect First sections to role files that currently imply context but do not name initial files or artifacts.
- Add explicit When to Use triggers to role files that rely only on external routing.

## Token Economy

- The pack has a positive token-economy pattern: routing discourages loading all agents.
- Approximate total role-agent text: 10334 tokens across 17 files.
- Approximate minimal routed context: 5483 tokens before task-specific source files.
- No role file is estimated above the heavy threshold.

## Agent-By-Agent Review

| Agent | Kind | Est. tokens | Token economy | Missing audit signals |
|---|---|---:|---|---|
| `agents/architect.md` | primary | 620 | lean | none |
| `agents/baseline_builder.md` | reviewer | 533 | lean | when to use |
| `agents/cv_validator.md` | reviewer | 682 | lean | when to use |
| `agents/data_quality.md` | reviewer | 826 | moderate | when to use |
| `agents/decision_log_handoff.md` | reviewer | 340 | lean | when to use, output |
| `agents/eda_analyst.md` | reviewer | 600 | lean | when to use |
| `agents/experiment_manager.md` | reviewer | 421 | lean | when to use, checklist |
| `agents/feature_engineer.md` | primary | 896 | moderate | when to use, checklist |
| `agents/interpretability_reviewer.md` | reviewer | 415 | lean | when to use |
| `agents/leakage_guard.md` | reviewer | 801 | moderate | when to use |
| `agents/metric_validator.md` | reviewer | 614 | lean | when to use |
| `agents/model_ensembler.md` | reviewer | 639 | lean | when to use |
| `agents/model_trainer.md` | reviewer | 907 | moderate | when to use |
| `agents/red_team.md` | reviewer | 636 | lean | when to use |
| `agents/reproducibility_reviewer.md` | reviewer | 407 | lean | when to use |
| `agents/submission_builder.md` | reviewer | 524 | lean | when to use |
| `agents/test_validation.md` | reviewer | 473 | lean | when to use, inspect first |

## Validation Evidence

- Command: `python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack /Users/bobrsubr/PycharmProjects/_researches/credit-default-prediction`
- Result: `PASS_WITH_RISKS EXISTING_PACK_AUDIT`
- This report audits existing-pack quality and routing. It does not claim generated-pack L2 consistency.
