# Agent Pack Audit Report: loan-offer-acceptance-prediction

## Executive Summary

- Target project: [loan-offer-acceptance-prediction](https://github.com/ikonushok/loan-offer-acceptance-prediction)
- Profile: `mature-existing-pack`
- Audit result: `PASS_WITH_RISKS EXISTING_PACK_AUDIT`
- Role agents found: 18
- Routing sources: [`agents/context_router.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/context_router.md), [`AGENTS.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/AGENTS.md), [`agents/README.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/README.md)
- Validation reviewer: [`agents/test_validation.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/test_validation.md)
- Claude context: absent

## What Works Well

- Root [`AGENTS.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/AGENTS.md) exists and centralizes project-level guidance.
- Routing source exists: [`agents/context_router.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/context_router.md), [`AGENTS.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/AGENTS.md), [`agents/README.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/README.md).
- Routing tells future agents not to load every role file at once, which protects context budget.
- Project-level forbidden changes or protected contracts are documented.
- Task spec agent exists, supporting scoped work before edits.
- 18 role-scoped agent files were found and can be routed by task.

## Problems And Risks

- [`CLAUDE.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/CLAUDE.md) is absent; Claude Code compatibility was not audited
- [`agents/baseline_builder.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/baseline_builder.md) lacks audit section signals: when to use
- [`agents/cv_validator.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/cv_validator.md) lacks audit section signals: when to use
- [`agents/data_quality.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/data_quality.md) lacks audit section signals: when to use
- [`agents/decision_log_handoff.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/decision_log_handoff.md) lacks audit section signals: when to use, output
- [`agents/eda_analyst.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/eda_analyst.md) lacks audit section signals: when to use
- [`agents/experiment_manager.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/experiment_manager.md) lacks audit section signals: when to use, checklist
- [`agents/feature_engineer.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/feature_engineer.md) lacks audit section signals: when to use, checklist
- [`agents/interpretability_reviewer.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/interpretability_reviewer.md) lacks audit section signals: when to use
- [`agents/leakage_guard.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/leakage_guard.md) lacks audit section signals: when to use
- [`agents/metric_validator.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/metric_validator.md) lacks audit section signals: when to use
- [`agents/model_ensembler.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/model_ensembler.md) lacks audit section signals: when to use
- [`agents/model_trainer.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/model_trainer.md) lacks audit section signals: when to use
- [`agents/red_team.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/red_team.md) lacks audit section signals: when to use
- [`agents/reproducibility_reviewer.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/reproducibility_reviewer.md) lacks audit section signals: when to use
- [`agents/submission_builder.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/submission_builder.md) lacks audit section signals: when to use
- [`agents/test_validation.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/test_validation.md) lacks audit section signals: when to use, inspect first

## Recommended Changes

- Add short Inspect First sections to role files that currently imply context but do not name initial files or artifacts.
- Add explicit When to Use triggers to role files that rely only on external routing.

## Token Economy

- The pack has a positive token-economy pattern: routing discourages loading all agents.
- Approximate total role-agent text: 10491 tokens across 18 files.
- Approximate minimal routed context: 4938 tokens before task-specific source files.
- No role file is estimated above the heavy threshold.

## Agent-By-Agent Review

| Agent | Kind | Est. tokens | Token economy | Missing audit signals |
|---|---|---:|---|---|
| [`agents/architect.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/architect.md) | primary | 608 | lean | none |
| [`agents/baseline_builder.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/baseline_builder.md) | reviewer | 503 | lean | when to use |
| [`agents/cv_validator.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/cv_validator.md) | reviewer | 605 | lean | when to use |
| [`agents/data_quality.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/data_quality.md) | reviewer | 739 | moderate | when to use |
| [`agents/decision_log_handoff.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/decision_log_handoff.md) | reviewer | 335 | lean | when to use, output |
| [`agents/drift_adaptation.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/drift_adaptation.md) | reviewer | 938 | moderate | none |
| [`agents/eda_analyst.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/eda_analyst.md) | reviewer | 558 | lean | when to use |
| [`agents/experiment_manager.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/experiment_manager.md) | reviewer | 421 | lean | when to use, checklist |
| [`agents/feature_engineer.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/feature_engineer.md) | primary | 847 | moderate | when to use, checklist |
| [`agents/interpretability_reviewer.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/interpretability_reviewer.md) | reviewer | 418 | lean | when to use |
| [`agents/leakage_guard.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/leakage_guard.md) | reviewer | 689 | lean | when to use |
| [`agents/metric_validator.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/metric_validator.md) | reviewer | 485 | lean | when to use |
| [`agents/model_ensembler.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/model_ensembler.md) | reviewer | 495 | lean | when to use |
| [`agents/model_trainer.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/model_trainer.md) | reviewer | 601 | lean | when to use |
| [`agents/red_team.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/red_team.md) | reviewer | 855 | moderate | when to use |
| [`agents/reproducibility_reviewer.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/reproducibility_reviewer.md) | reviewer | 407 | lean | when to use |
| [`agents/submission_builder.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/submission_builder.md) | reviewer | 527 | lean | when to use |
| [`agents/test_validation.md`](https://github.com/ikonushok/loan-offer-acceptance-prediction/blob/main/agents/test_validation.md) | reviewer | 460 | lean | when to use, inspect first |

## Validation Evidence

- Command: `python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack /path/to/project`
- Result: `PASS_WITH_RISKS EXISTING_PACK_AUDIT`
- This report audits existing-pack quality and routing. It does not claim generated-pack L2 consistency.
