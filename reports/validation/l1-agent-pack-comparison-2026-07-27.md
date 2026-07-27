# L1/L2 сравнение agent-pack — 2026-07-27

## Сводка

| Поле | Значение |
|---|---|
| Проверяемый skill | `agent-pack-designer` |
| Цель проверки | Сравнить рекомендации минимального workflow с агентами, которые реально лежат в проектах |
| Проекты | `hiking-route-recommender-demo`, `loan-offer-acceptance-prediction`, `credit-default-prediction` |
| Итоговый уровень | L1 достигнут; есть частичные доказательства L2 |
| Ограничение | Материализованный новый pack не генерировался |
| Проверки runtime проектов | Не запускались |

## Текущее состояние проекта

| Область | Состояние | Вывод |
|---|---|---|
| Release tag | `v0.1.0` создан на commit `516924701f873f089710240d85f19ab2e71afcb9` | Первый installable release зафиксирован как L0 |
| Skill scaffold | Есть `SKILL.md`, `agents/openai.yaml`, `references/`, `assets/starter-pack/`, `scripts/validate_skill.py` | Структура соответствует installable Codex skill |
| Starter-pack | Есть шаблоны `AGENTS.md`, `CLAUDE.md`, `context_router.md`, `primary_agent.md`, `risk_reviewer.md`, `task_spec_short.md`, `validation_reviewer.md` | Базовая заготовка покрывает минимальный pack |
| Validation script | `agent-pack-designer/scripts/validate_skill.py` | Есть повторяемая L0-проверка scaffold |
| Release docs | `README.md`, `CHANGELOG.md`, `VERSION` | Документация релиза есть, текущая ветка уже содержит L1 evidence после тега |
| Validation reports | `reports/validation/l1-agent-pack-comparison-2026-07-27.md` | Добавлен первый real-project validation report |
| Git status на момент отчёта | Изменения отчёта, `README.md` и `CHANGELOG.md` подготовлены после тега | Эти изменения относятся к следующему commit после `v0.1.0` |
| P1 guidance после отчёта | `SKILL.md` и references обновлены по findings | Добавлены категории agents, alias `test_validation.md`, правило про опциональный `CLAUDE.md` |

## Результаты проверки

| Проверка | Команда / метод | Результат | Уровень |
|---|---|---|---|
| Статическая проверка scaffold | `python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer` | `RESULT: PASS L0` | L0 |
| Проверка формата Codex skill | `quick_validate.py agent-pack-designer` из `skill-creator` | `Skill is valid!` | L0 |
| Проверка diff на пробельные ошибки | `git diff --check` | Ошибок нет | L0 |
| Сравнение с hiking route demo | Ручная сверка `README.md`, `AGENTS.md`, `agents/*` | Найден полезный gap: нет отдельного router и validation reviewer | L1, частично L2 |
| Сравнение с loan-offer ML project | Ручная сверка `README.md`, `AGENTS.md`, `agents/context_router.md`, `agents/test_validation.md`, `agents/*` | Структура подтверждает core-модель skill; 21 agent оправдан при наличии router | L1, частично L2 |
| Сравнение с credit-default ML project | Ручная сверка `README.md`, `AGENTS.md`, `agents/context_router.md`, `agents/test_validation.md`, `agents/*` | Самый чистый пример router + validation reviewer; 20 agents оправданы mature workflow | L1, частично L2 |

## Итоговый вывод

| Вопрос | Ответ |
|---|---|
| Готов ли `agent-pack-designer` как installable skill? | Да, на уровне L0 release tag `v0.1.0` |
| Подтверждена ли полезность workflow на реальных проектах? | Да, достигнут L1: проверены три реальных agent-pack проекта |
| Можно ли честно заявить L2? | Пока нет полностью; есть частичные доказательства L2, но не было materialized generated-pack check |
| Главный подтверждённый design choice | `AGENTS.md + context_router.md + primary agent + validation reviewer + task_spec_short.md` работает как core |
| Главная поправка к skill | Для mature ML projects нужно разрешать много trigger-only agents, если router удерживает default context маленьким |
| Главный найденный gap в starter guidance | Нужно явно описать категории `ядро`, `по триггеру`, `optional/future`, а также alias `test_validation.md` для validation reviewer |
| Следующий engineering step | Сделать materialized pack check для L2 и добавить generated-pack consistency validator |

## Что делать дальше

| Приоритет | Действие | Зачем | Ожидаемый результат |
|---|---|---|---|
| P0 | Закоммитить текущий отчёт, `README.md` и `CHANGELOG.md` отдельным commit после `v0.1.0` | Сохранить L1 evidence отдельно от L0 release tag | Выполнено: commit `7284e14` |
| P1 | Обновить `SKILL.md`: добавить правило `core / trigger-only / optional-future agents` | Закрыть главный вывод из трёх реальных проектов | Выполнено в рабочей ветке |
| P1 | Обновить references: добавить `test_validation.md` как допустимый alias для `validation_reviewer.md` | Убрать расхождение с реальными ML-проектами | Выполнено в рабочей ветке |
| P1 | Уточнить в `SKILL.md`, что `CLAUDE.md` нужен только при явном target runtime Claude Code | Не заставлять каждый pack создавать лишний файл | Выполнено в рабочей ветке |
| P2 | Сгенерировать materialized pack в `/private/tmp` для одного из трёх проектов | Перейти от ручного сравнения к проверке результата генерации | Следующий шаг |
| P2 | Добавить generated-pack consistency validator | Сделать L2 повторяемым, а не ручным | Следующий шаг |
| P3 | Прогнать cross-project regression на всех трёх проектах после правок | Проверить, что новый guidance не ломает разные типы проектов | Подготовка к L4 |
| P3 | Подготовить `v0.2.0` после L2 validator | Выпустить версию не только со scaffold, но и с evidence-driven generation checks | Release с более сильным validation story |

| Рекомендуемый ближайший шаг | Почему именно он |
|---|---|
| Сначала commit текущего отчёта и README/CHANGELOG | Выполнено: commit `7284e14` |
| Затем правка `SKILL.md` и references по findings | Выполнено в рабочей ветке; нужно закоммитить |
| Затем materialized generated-pack check | Это следующий минимальный путь от L1/partial L2 к полноценному L2 |

## Проверенные источники

| Источник | Что проверялось |
|---|---|
| `agent-pack-designer/SKILL.md` | Правила минимального pack, маршрутизация, правила остановки, validation claims |
| `agent-pack-designer/references/design-workflow.md` | Процесс выбора агентов и доказательств |
| `agent-pack-designer/references/agent-quality-rubric.md` | Критерии качества и риска agent sprawl |
| `agent-pack-designer/references/validation-levels.md` | L0-L5 и правила validation claim |
| `hiking-route-recommender-demo/README.md` | Назначение проекта, pipeline, команды проверки |
| `hiking-route-recommender-demo/AGENTS.md` | Реальные правила и матрица маршрутизации |
| `hiking-route-recommender-demo/agents/*` | Фактические доменные agents и reviewers |
| `loan-offer-acceptance-prediction/README.md` | Назначение проекта, ML workflow, уровни проверки |
| `loan-offer-acceptance-prediction/AGENTS.md` | Основной контекст, protected contracts, active agents |
| `loan-offer-acceptance-prediction/agents/*` | Router, validation agent, доменные agents |
| `credit-default-prediction/README.md` | Назначение проекта, long-format ML workflow, уровни проверки |
| `credit-default-prediction/AGENTS.md` | Основной контекст, protected contracts, active agents |
| `credit-default-prediction/agents/*` | Router, validation agent, доменные agents |

## Сравнение проектов

| Проект | Фактический agent-pack | Совпадение с skill | Основной пробел | Вердикт |
|---|---:|---|---|---|
| `hiking-route-recommender-demo` | `AGENTS.md` + `agents/` без router/validation reviewer | Частичное | Маршрутизация и validation evidence встроены в `AGENTS.md`/`agents/README.md`, но не выделены в отдельные агенты | PASS_WITH_RISKS |
| `loan-offer-acceptance-prediction` | `AGENTS.md` + `context_router.md` + `task_spec_short.md` + `test_validation.md` + 21 agent | Сильное | Pack слишком большой для стартовой заготовки, но router удерживает default context маленьким | PASS |
| `credit-default-prediction` | `AGENTS.md` + `context_router.md` + `task_spec_short.md` + `test_validation.md` + 20 agents | Сильное | Нет `CLAUDE.md`, совместимость с Claude Code не оформлена отдельным файлом | PASS |

## Файлы ядра по проектам

| Файл / роль | Hiking | Loan offer | Credit default | Вывод для skill |
|---|---|---|---|---|
| `AGENTS.md` | Есть | Есть | Есть | Обязательное ядро |
| `CLAUDE.md` | Нет | Нет | Нет | Опционален, если Claude Code явно входит в scope |
| `agents/context_router.md` | Нет | Есть | Есть | Должен быть ядром starter-pack |
| Основной agent | `architect.md` | `architect.md` | `architect.md` | `architect.md` является хорошим project-specific именем primary agent |
| Validation reviewer | Нет | `test_validation.md` | `test_validation.md` | `test_validation.md` нужно признать допустимым alias для `validation_reviewer.md` |
| `agents/task_spec_short.md` | Есть | Есть | Есть | Должен быть ядром |
| Red-team agent | Есть | Есть | Есть | Использовать по триггеру, не включать в default context |

## Hiking Route Recommender Demo

| Проверка | Наблюдение | Оценка |
|---|---|---|
| Путь | `/Users/bobrsubr/PycharmProjects/_petprojects/hiking-route-recommender-demo` | Проверен локально |
| Основной контекст | `AGENTS.md` есть | PASS |
| Router | `agents/context_router.md` отсутствует | Пробел |
| Validation reviewer | `validation_reviewer.md` / `test_validation.md` отсутствует | Пробел |
| Task spec | `agents/task_spec_short.md` есть | PASS |
| Основной agent | `architect.md` хорошо покрывает проектирование изменений | PASS |
| Доменные reviewers | `recommender_reviewer.md`, `data_quality_reviewer.md`, `api_runtime_reviewer.md`, `candidate_merger_reviewer.md`, `docs_handoff.md` | Оправданы как агенты по триггеру |
| Опциональные/future agents | `observability_reviewer.md`, `ltr_dataset_reviewer.md` | Не должны входить в default context |
| Итог | Полезный mature demo pack, но router/validation лучше выделить отдельно | PASS_WITH_RISKS |

## Loan Offer Acceptance Prediction

| Проверка | Наблюдение | Оценка |
|---|---|---|
| Путь | `/Users/bobrsubr/PycharmProjects/_researches/loan-offer-acceptance-prediction` | Проверен локально |
| Основной контекст | `AGENTS.md + agents/context_router.md + one primary agent + zero or one reviewer` явно задан | PASS |
| Router | `agents/context_router.md` отделяет категорию, режим, primary agent, reviewer, validation level | PASS |
| Validation reviewer | `agents/test_validation.md` мапит работы на L0-L5 | PASS |
| Task spec | `agents/task_spec_short.md` есть | PASS |
| Количество agents | 21 специализированный agent file | Риск только без router; с router приемлемо |
| Дополнительный доменный агент | `drift_adaptation.md` | Оправдан train/test drift и data-ceiling задачами |
| Соответствие starter-pack | Ядро совпадает; доменные agents должны использоваться по триггеру | PASS |
| Итог | Хороший пример mature competition ML pack | PASS |

## Credit Default Prediction

| Проверка | Наблюдение | Оценка |
|---|---|---|
| Путь | `/Users/bobrsubr/PycharmProjects/_researches/credit-default-prediction` | Проверен локально |
| Основной контекст | `AGENTS.md + agents/context_router.md + one primary agent + zero or one reviewer` явно задан | PASS |
| Router | `agents/context_router.md` отделяет категорию задачи, режим, forbidden changes, validation level | PASS |
| Validation reviewer | `agents/test_validation.md` мапит работы на L0-L5 | PASS |
| Task spec | `agents/task_spec_short.md` есть | PASS |
| Количество agents | 20 специализированных agent files | Приемлемо для mature workflow |
| Доменная специфика | Long-format, агрегация на уровне `id`, leakage, sequence models, ensembling, submission readiness | Оправдывает специализированных reviewers |
| Отличие от loan-offer | Нет `drift_adaptation.md` | Оправдано: drift описан в rules/docs, но не выделен в отдельную recurring role |
| Итог | Самый чистый пример router + validation reviewer для starter-pack design | PASS |

## Классификация agents

| Категория | Agents | Где подтверждено | Рекомендация для `agent-pack-designer` |
|---|---|---|---|
| Ядро | `AGENTS.md`, `context_router.md`, `architect.md`, `task_spec_short.md`, `test_validation.md` / `validation_reviewer.md` | Loan offer, credit default | Держать в starter guidance |
| Доменные по триггеру | `data_quality.md`, `eda_analyst.md`, `feature_engineer.md`, `cv_validator.md`, `baseline_builder.md`, `model_trainer.md`, `model_ensembler.md`, `metric_validator.md`, `submission_builder.md` | Loan offer, credit default | Разрешать для mature workflows при наличии router |
| Риск/review по триггеру | `leakage_guard.md`, `red_team.md`, `readme_consistency_reviewer.md`, `reproducibility_reviewer.md`, `interpretability_reviewer.md`, `decision_log_handoff.md` | Loan offer, credit default, hiking частично | Не включать все в default context |
| Опциональные/future | `observability_reviewer.md`, `ltr_dataset_reviewer.md`, `drift_adaptation.md` при отсутствии явного drift workflow | Hiking, loan offer | Помечать как optional/future |

## Выводы для `agent-pack-designer`

| Тип | Наблюдение | Изменение для следующей версии |
|---|---|---|
| Подтверждено | Правило minimal pack корректно для новых проектов | Оставить |
| Подтверждено | `context_router.md` нужен как отдельный core-файл | Оставить в starter-pack |
| Подтверждено | Validation reviewer нужен отдельно от README/AGENTS | Оставить в starter-pack |
| Уточнение | Mature ML projects могут иметь 20+ agents без agent sprawl, если router держит default context маленьким | Добавить секцию про mature packs |
| Уточнение | `test_validation.md` используется как фактическое имя validation reviewer | Добавить alias в SKILL.md/references |
| Уточнение | `CLAUDE.md` отсутствует во всех трех проверенных проектах | Указать, что файл нужен только при явном Claude Code target |
| Риск | Starter-pack может выглядеть слишком маленьким для mature competition workflow | Добавить раздел core vs trigger-only vs optional/future |

## Уровень валидации

| Уровень | Статус | Доказательства | Ограничение |
|---|---|---|---|
| L0 | PASS | Skill scaffold прошел статическую проверку ранее | Не доказывает полезность workflow |
| L1 | PASS | Три реальных проекта сравнены с workflow skill | Не генерировался новый pack |
| L2 | PARTIAL | Два проекта подтвердили согласованность router/roles/validation; один проект выявил пробел | Нет materialized generated-pack check |
| L3 | NOT CLAIMED | Реальные проекты использованы как cases с доказательствами | Не было полноценной симуляции генерации pack и внедрения |
| L4 | NOT CLAIMED | Не выполнялось | Нет harness для cross-project regression |
| L5 | NOT CLAIMED | Не выполнялось | Нет release/red-team package audit выше L0 |

## Недостающие проверки

| Пробел | Почему важно | Минимальная следующая проверка |
|---|---|---|
| Нет materialized generated pack | Нельзя полностью заявить L2 | Сгенерировать pack в `/private/tmp` для одного проекта и сравнить с реальным |
| Нет generated-pack validator | L2 пока ручной | Добавить скрипт проверки router/agent names/roles/validation claims |
| Нет runtime tests target projects | Сравнение проверяло agent-pack, не ML/runtime | Не требуется для agent-pack L1, но нужно для project runtime claims |
| Нет CLAUDE.md compatibility pass | Claude Code support пока только из skill design | Проверить один generated pack с `CLAUDE.md` |

## Минимальный следующий шаг

| Приоритет | Действие | Ожидаемый уровень |
|---|---|---|
| P1 | Добавить в skill guidance раздел `core / trigger-only / optional-future agents` | Укрепляет L1 findings |
| P1 | Добавить alias `test_validation.md` для validation reviewer | Убирает расхождение с реальными ML packs |
| P2 | Сгенерировать materialized pack для одного проекта в `/private/tmp` | Закрывает L2 |
| P2 | Добавить generated-pack consistency validator | Делает L2 повторяемым |
