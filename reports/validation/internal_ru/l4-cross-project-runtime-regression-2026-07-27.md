# L4 runtime regression protocol — 2026-07-27

## Сводка

| Поле | Значение |
|---|---|
| Проверяемый skill | `agent-pack-designer` |
| Цель проверки | Подтвердить L4 evidence через несколько generated-pack-guided real-project simulation tasks |
| Метод | Target repos скопированы в `/private/tmp`, старые agent-файлы исключены, generated packs наложены поверх temp-копий |
| Target repo mutation | Нет изменений, сделанных этим протоколом; все simulated edits выполнены только в `/private/tmp` |
| Итог | `PASS_WITH_RISKS` for L4 evidence |
| Ограничение | Это не L5: нет public release readiness pass, install verification, red-team audit и language/publication pass |

## Target repositories

| Project | Original target path | Simulation path | Generated pack path | Target status note |
|---|---|---|---|---|
| `go_through_the_forest` | `/Users/bobrsubr/PycharmProjects/_sakhalin/go_through_the_forest` | `/private/tmp/agent-pack-designer-l4-forest-sim-20260727` | `/private/tmp/agent-pack-designer-l4-forest-pack-20260727` | `git status --short` clean after protocol |
| `credit-default-prediction` | `/Users/bobrsubr/PycharmProjects/_researches/credit-default-prediction` | `/private/tmp/agent-pack-designer-l4-credit-sim-20260727` | `/private/tmp/agent-pack-designer-l2-credit-default-20260727` | `experiments/experiment_log.csv` was already modified in the target status check; this protocol did not write target files |
| `loan-offer-acceptance-prediction` | `/Users/bobrsubr/PycharmProjects/_researches/loan-offer-acceptance-prediction` | `/private/tmp/agent-pack-designer-l4-loan-sim-20260727` | `/private/tmp/agent-pack-designer-l2-loan-offer-20260727` | `git status --short` clean after protocol |

## Generated pack setup

| Project | Setup method | Pack validator result |
|---|---|---|
| `go_through_the_forest` | Created a new minimal generated pack in `/private/tmp` from `assets/starter-pack/`, filled project-specific source-of-truth files, workflow trigger, risk trigger, and validation commands | `RESULT: PASS L2` |
| `credit-default-prediction` | Reused existing materialized generated pack from the L2 protocol and overlaid it on a thin temp copy | `RESULT: PASS L2` |
| `loan-offer-acceptance-prediction` | Reused existing materialized generated pack from the L2 protocol and overlaid it on a temp copy with raw CSV fixtures and submissions | `RESULT: PASS L2` |

## Simulation tasks

| Project | Task mode selected through generated pack | Small real-project simulation task | Changed files in temp copy | Reviewer trigger |
|---|---|---|---|---|
| `go_through_the_forest` | `docs-sync` / risk-sensitive validation | Add an explicit validation-evidence boundary to offline evaluation docs | `docs/07_README_evaluation.md` | Recommendation metrics, runtime artifacts, API/runtime smoke claim boundary |
| `credit-default-prediction` | `docs-sync` / validation | Add a validation-evidence note for credit-default model-result reporting in a thin copy | `experiments/validation_evidence_l4_simulation.md` | ROC-AUC, leakage, id-level aggregation, submission-readiness claims |
| `loan-offer-acceptance-prediction` | risk-sensitive validation | Add a submission-contract simulation note after running staged-upload contract tests | `reports/validation/l4_submission_contract_simulation_2026-07-27.md` | Submission CSVs, card hashes, leaderboard/upload claims |

## Commands run

| Project | Command | Result |
|---|---|---|
| `go_through_the_forest` generated pack | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l4-forest-pack-20260727` | `RESULT: PASS L2` |
| `go_through_the_forest` simulation pack | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l4-forest-sim-20260727` | `RESULT: PASS L2` |
| `go_through_the_forest` fast suite baseline | `python3 -m src.tests.run_fast_suite` | Unit portion passed; API contract tests failed at import because `fastapi` was unavailable |
| `go_through_the_forest` targeted unit checks | `PYTHONPATH=/private/tmp/agent-pack-designer-l4-forest-sim-20260727 python3 -m unittest discover -s src/tests/unit -p 'test_*.py'` | `Ran 5 tests ... OK` before and after the temp docs change |
| `credit-default-prediction` simulation pack | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l4-credit-sim-20260727` | `RESULT: PASS L2` |
| `credit-default-prediction` syntax check | `python3 -m compileall -q src/credit_scoring scripts` | Passed |
| `loan-offer-acceptance-prediction` simulation pack | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l4-loan-sim-20260727` | `RESULT: PASS L2` |
| `loan-offer-acceptance-prediction` full available contract attempt | `python3 -m pytest tests/test_no_leakage.py tests/test_sample_weights.py tests/test_submission_contract.py` | Failed during collection because `catboost` was unavailable |
| `loan-offer-acceptance-prediction` submission contract | `python3 -m pytest tests/test_submission_contract.py` | `7 passed` before and after the temp report change |
| Target mutation check | `git status --short` in each target repo | Forest clean, loan clean, credit had pre-existing `M experiments/experiment_log.csv` |
| Skill scaffold validation | `python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer` | `RESULT: PASS L0` |

## Diff evidence in temp copies

| Project | Diff inspected | Result |
|---|---|---|
| `go_through_the_forest` | `diff -u <target>/docs/07_README_evaluation.md <simulation>/docs/07_README_evaluation.md` | Only `## Граница validation evidence` section was added |
| `credit-default-prediction` | `diff -u /dev/null <simulation>/experiments/validation_evidence_l4_simulation.md` | New validation-evidence note only |
| `loan-offer-acceptance-prediction` | `diff -u /dev/null <simulation>/reports/validation/l4_submission_contract_simulation_2026-07-27.md` | New submission-contract simulation note only |

## Reviewer verdict

| Reviewer | Verdict | Evidence |
|---|---|---|
| Risk reviewer | `PASS_WITH_RISKS` | Generated packs correctly routed risk-sensitive tasks to reviewer context; temp edits narrowed claim boundaries and did not require target repo mutation |
| Validation reviewer | `PASS_WITH_RISKS` at L4 | Three materially different projects completed generated-pack-guided simulations in `/private/tmp`; missing dependencies prevented the strongest runtime checks for forest API and loan leakage/sample-weight tests |

## Validation level

| Level | Статус | Доказательства |
|---|---|---|
| L0 | PASS | Skill scaffold validator passed |
| L1 | PASS | Existing sample/agent comparison report remains available |
| L2 | PASS | All generated packs used in simulations passed `validate_pack.py` |
| L3 | PASS | Existing hiking-route real-project simulation remains available |
| L4 | `PASS_WITH_RISKS` | Three cross-project generated-pack-guided real-project simulations completed in `/private/tmp` |
| L5 | NOT CLAIMED | No red-team release audit, install verification, public-language pass, or release readiness protocol |

## Вывод

| Вопрос | Ответ |
|---|---|
| Можно ли заявить L4? | Да, как L4 evidence с verdict `PASS_WITH_RISKS` для текущей ветки |
| Что именно доказано? | Generated packs можно использовать для нескольких разных real-project simulation tasks без изменения target repos; routing, reviewer triggers, task boundaries, validation evidence и residual risk reports остаются согласованными |
| Что не доказано? | Полная runtime готовность всех target projects, model-quality reproduction, API smoke для forest в текущем Python, leakage/sample-weight tests для loan без `catboost`, L5/public release readiness |
| Следующий минимальный шаг | L5 protocol: language/publication pass для public docs/reports, install path verification, red-team release audit, затем release notes |
