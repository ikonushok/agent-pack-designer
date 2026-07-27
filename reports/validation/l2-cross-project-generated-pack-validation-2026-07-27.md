# Cross-project L2 validation generated packs — 2026-07-27

## Сводка

| Поле | Значение |
|---|---|
| Проверяемый skill | `agent-pack-designer` |
| Цель проверки | Поднять L2 evidence выше `L2_CANDIDATE` за счет повторяемой materialized generated-pack проверки |
| Метод | Starter-pack материализован в `/private/tmp`, заполнен project-specific значениями и проверен усиленным `validate_pack.py` |
| Target repositories | Только чтение; исходные проекты не менялись |
| Итог | `PASS L2` для 3 из 3 generated packs |
| Ограничение | Это не L3/L4/L5: pack'и не внедрялись в target repositories и не использовались в полноценной runtime/project simulation |

## Generated packs

| Project | Target path | Generated pack path | Project type | Result |
|---|---|---|---|---|
| `credit-default-prediction` | `/Users/bobrsubr/PycharmProjects/_researches/credit-default-prediction` | `/private/tmp/agent-pack-designer-l2-credit-default-20260727` | Tabular credit-default ML pipeline | `PASS L2` |
| `loan-offer-acceptance-prediction` | `/Users/bobrsubr/PycharmProjects/_researches/loan-offer-acceptance-prediction` | `/private/tmp/agent-pack-designer-l2-loan-offer-20260727` | Tabular credit-offer acceptance ML pipeline | `PASS L2` |
| `hiking-route-recommender-demo` | `/Users/bobrsubr/PycharmProjects/_petprojects/hiking-route-recommender-demo` | `/private/tmp/agent-pack-designer-l2-hiking-route-20260727` | Synthetic recommendation API/demo pipeline | `PASS L2` |

## Материализованные файлы

| Pack file | Credit default | Loan offer | Hiking route | Назначение |
|---|---:|---:|---:|---|
| `AGENTS.md` | Есть | Есть | Есть | Codex project rules |
| `CLAUDE.md` | Есть | Есть | Есть | Optional Claude Code compatibility |
| `agents/context_router.md` | Есть | Есть | Есть | Minimal-context routing |
| `agents/primary_agent.md` | Есть | Есть | Есть | Main workflow agent |
| `agents/risk_reviewer.md` | Есть | Есть | Есть | Separate risk reviewer |
| `agents/task_spec_short.md` | Есть | Есть | Есть | Task contract template |
| `agents/validation_reviewer.md` | Есть | Есть | Есть | L0-L5 evidence reviewer |

## Project-specific routing evidence

| Project | Source-of-truth files | Primary workflow trigger | Risk trigger |
|---|---|---|---|
| `credit-default-prediction` | `README.md`, `AGENTS.md`, `SOLUTION.md`, package source, configs, scripts, tests, experiment cards | Tabular credit-default ML pipeline work | Raw data, target join, id aggregation, CV split, model selection, ROC-AUC, predictions, submissions, public claims |
| `loan-offer-acceptance-prediction` | `README.md`, `AGENTS.md`, `SOLUTION.md`, task brief, `src/alfa_credit/`, configs, scripts, tests, validation reports, submission cards | Credit-offer acceptance ML pipeline work | Raw data, target joins, `decision_day` folds, context-offer features, class weights, ROC-AUC claims, predictions, submissions, leaderboard statements |
| `hiking-route-recommender-demo` | `README.md`, `pyproject.toml`, P0 docs, architecture docs, evaluation docs, package source, scripts, tests, synthetic outputs | Synthetic hiking-route recommendation demo workflow | Synthetic data schemas, train/test split, retrieval scoring, fallback fill, business rules, metrics, FastAPI endpoints, production/business impact claims |

## Validator improvements

| Область | До | После |
|---|---|---|
| Result label | `PASS L2_CANDIDATE` | `PASS L2` for generated-pack cross-file consistency |
| Required sections | Проверялись отдельные термины | Проверяются обязательные разделы в `AGENTS.md`, `CLAUDE.md`, router, task spec, validation reviewer, primary agent, risk reviewer |
| Router consistency | Проверялись слова `primary`, `reviewer`, `validation` | Дополнительно проверяется, что router ссылается на реальные agent files |
| Role separation | Проверялся любой дополнительный agent | Проверяется наличие primary agent и отдельного reviewer |
| Template completion | Проверялись `{{` и `}}` | Дополнительно проверяются starter placeholder tokens |
| Validation claims | Не проверялись отдельно | `AGENTS.md` не должен заявлять current validation level выше L0 до project checks |

## Commands run

| Проверка | Команда | Результат |
|---|---|---|
| Credit default generated pack | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l2-credit-default-20260727` | `RESULT: PASS L2` |
| Loan offer generated pack | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l2-loan-offer-20260727` | `RESULT: PASS L2` |
| Hiking route generated pack | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l2-hiking-route-20260727` | `RESULT: PASS L2` |
| Generated pack file inventory | `find /private/tmp/agent-pack-designer-l2-loan-offer-20260727 -maxdepth 3 -type f` and hiking equivalent | 7 expected files in each new pack |
| Placeholder scan | `rg -n "\\{\\{|PROJECT_NAME|SOURCE_OF_TRUTH_FILES|PRIMARY_FILES|RISK_AREA|DEFAULT_VALIDATION" /private/tmp/agent-pack-designer-l2-*` | No matches |

## Уровень валидации

| Level | Статус | Доказательства |
|---|---|---|
| L0 | PASS | Skill scaffold validator остается обязательной проверкой |
| L1 | PASS | Существующий отчет сравнения real-project agent packs сохранен |
| L2 | PASS | 3 materialized generated packs прошли усиленный generated-pack validator |
| L3 | NOT CLAIMED | Generated packs не внедрялись в target repositories и не использовались в рабочей симуляции |
| L4 | NOT CLAIMED | Есть cross-project L2 evidence, но нет отдельного L4 regression protocol с полноценными задачами |
| L5 | NOT CLAIMED | Нет language/publication pass, install verification и red-team release audit для следующего public release |

## Вывод

| Вопрос | Ответ |
|---|---|
| Можно ли снять `L2_CANDIDATE`? | Да, для generated-pack consistency теперь есть усиленный validator и 3 успешных materialized проверки |
| Что именно доказано? | Starter-pack можно project-specifically заполнить для нескольких разных проектов без unresolved placeholders, misrouting и смешения primary/reviewer/validation responsibilities |
| Что не доказано? | Runtime usefulness, install path behavior, Claude/Codex live execution, release readiness |
| Следующий минимальный шаг | L3 simulation: применить generated pack к одному target project task без изменения target repo или с отдельным approved worktree |
