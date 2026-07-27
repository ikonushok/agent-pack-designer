# L2 проверка materialized generated pack — 2026-07-27

## Сводка

| Поле | Значение |
|---|---|
| Проверяемый skill | `agent-pack-designer` |
| Проверяемый target project | `credit-default-prediction` |
| Target path | `/Users/bobrsubr/PycharmProjects/_researches/credit-default-prediction` |
| Generated pack path | `/private/tmp/agent-pack-designer-l2-credit-default-20260727` |
| Метод | Starter-pack был материализован во временный каталог и заполнен project-specific значениями |
| Итог | `PASS L2_CANDIDATE` |
| Ограничение | Pack не внедрялся в target repository и не использовался для runtime-задачи |

## Сгенерированный pack

| Файл | Статус | Назначение |
|---|---|---|
| `AGENTS.md` | Есть | Project rules для Codex |
| `CLAUDE.md` | Есть | Опциональная Claude Code совместимость из starter-pack |
| `agents/context_router.md` | Есть | Маршрутизация task mode, primary agent, reviewer, validation |
| `agents/primary_agent.md` | Есть | Основной workflow agent |
| `agents/risk_reviewer.md` | Есть | Reviewer для leakage, id-level aggregation, validation, metrics, submission |
| `agents/task_spec_short.md` | Есть | Краткий task spec перед нетривиальной работой |
| `agents/validation_reviewer.md` | Есть | Проверка evidence level L0-L5 |

## Подставленные project-specific значения

| Placeholder | Значение |
|---|---|
| `PROJECT_NAME` | `credit-default-prediction` |
| `SOURCE_OF_TRUTH_FILES` | `README.md`, `AGENTS.md`, `SOLUTION.md`, `src/credit_scoring/`, `configs/`, `scripts/`, `tests/`, `experiments/cards/` |
| `PRIMARY_FILES` | `src/credit_scoring/`, `scripts/`, `configs/`, `tests/`, `reproduce.sh`, `README.md`, `SOLUTION.md` |
| `PRIMARY_WORKFLOW_TRIGGER` | Работа с tabular credit-default ML pipeline |
| `RISK_AREA` | Leakage, id-level aggregation, validation, metrics, reproducibility, submission contracts |
| `RISK_TRIGGER` | Изменения raw data, target join, aggregation, CV split, model selection, ROC-AUC, predictions, submission CSV, public claims |

## Проверки

| Проверка | Команда / метод | Результат |
|---|---|---|
| Файлы generated pack | `find /private/tmp/agent-pack-designer-l2-credit-default-20260727 -maxdepth 3 -type f` | Найдены 7 ожидаемых файлов |
| Unresolved placeholders | `rg -n "\\{\\{" /private/tmp/agent-pack-designer-l2-credit-default-20260727` | Совпадений нет |
| Generated-pack validator | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l2-credit-default-20260727` | `RESULT: PASS L2_CANDIDATE` |

## Что проверяет `validate_pack.py`

| Область | Проверка |
|---|---|
| Core files | `AGENTS.md`, `agents/context_router.md`, `agents/task_spec_short.md` |
| Validation reviewer | Наличие `agents/validation_reviewer.md` или alias `agents/test_validation.md` |
| Primary/domain agent | Наличие хотя бы одного дополнительного agent под `agents/` |
| Router consistency | Наличие терминов `primary`, `reviewer`, `validation` |
| Task spec consistency | Наличие `Goal` и `Validation` |
| Validation levels | Наличие L0-L5 в validation reviewer |
| Template completion | Отсутствие unresolved `{{...}}` placeholders |

## Вывод

| Вопрос | Ответ |
|---|---|
| Можно ли повысить статус после L1? | Да, появился повторяемый L2 candidate check |
| Можно ли заявить полноценный L2? | Осторожно: `PASS L2_CANDIDATE`, потому что pack материализован и проверен, но не внедрён в target repo |
| Главный результат | Starter-pack можно заполнить для реального mature ML project без unresolved placeholders и с согласованными core-файлами |
| Главный остаточный риск | Validator пока проверяет структуру и базовую согласованность, но не качество wording каждого agent |
| Следующий шаг | Расширить validator semantic checks и прогнать generated-pack check на `loan-offer-acceptance-prediction` и `hiking-route-recommender-demo` |

## Уровень валидации

| Level | Статус | Доказательства |
|---|---|---|
| L0 | PASS | Skill scaffold и diff checks проходят |
| L1 | PASS | Есть сравнение с тремя реальными agent-pack проектами |
| L2 | CANDIDATE PASS | Один generated pack материализован и прошёл `validate_pack.py` |
| L3 | NOT CLAIMED | Pack не использовался в полноценной real project simulation |
| L4 | NOT CLAIMED | Нет cross-project generated-pack regression |
| L5 | NOT CLAIMED | Нет release/red-team package audit для следующей версии |
