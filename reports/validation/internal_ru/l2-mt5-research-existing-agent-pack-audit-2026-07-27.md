# MT5 Research existing agent-pack audit — 2026-07-27

## Сводка

| Поле | Значение |
|---|---|
| Проверяемый skill | `agent-pack-designer` |
| Target project | `/Users/bobrsubr/PycharmProjects/_trading/mt5-research` |
| Цель проверки | Понять, является ли зрелый agent-pack `mt5-research` хорошим эталоном для `agent-pack-designer`, и что именно из него стоит переносить в генератор/валидатор |
| Метод | Read-only аудит существующего `AGENTS.md`, `CLAUDE.md`, `agents/*`, сравнение с `agent-pack-designer` rubric и starter-pack |
| Target repository writes | Не выполнялись |
| Итог по `mt5-research` pack | `PASS_WITH_RISKS` как mature existing pack |
| Итог по `agent-pack-designer` | `PASS_WITH_RISKS` для минимального `--audit-existing`; generated-pack flow сохранен строгим |

## Что проверялось

| Артефакт | Наблюдение |
|---|---|
| `mt5-research/AGENTS.md` | Содержит objective, working rules, protected contracts, routing, decision states и default review output |
| `mt5-research/CLAUDE.md` | Подробно описывает project context, routing, protected contracts, repository layout, MT5/MQL5 architecture, validation tooling и token hygiene |
| `mt5-research/agents/README_agents_index.md` | Выполняет роль легкого router/index: "Load only the agent needed", группы ролей, main/research/cascade/MQL5/handoff |
| `mt5-research/agents/*.md` | 17 role-scoped agents, включая primary, red-team, validation, domain reviewers и production reviewers |
| `agent-pack-designer/SKILL.md` | Разрешает mature projects иметь много trigger-only agents при условии, что router удерживает default context маленьким |
| `agent-pack-designer/references/agent-quality-rubric.md` | Даёт критерии качества: trigger, inspect-first, checklist, output, stop rules, separation, minimality, routing |
| `agent-pack-designer/scripts/validate_pack.py` | Проверяет generated starter-pack shape; после аудита добавлен отдельный `--audit-existing` режим для legacy/mature existing packs |

## Фактическая структура `mt5-research`

| Роль | Файл | Оценка оправданности |
|---|---|---|
| Primary design/scope control | `agents/architect.md` | `PASS` — главный агент для non-trivial changes; хорошо отделяет spec/design от реализации |
| Adversarial review | `agents/red_team.md` | `PASS` — отдельный red-team нужен из-за high-risk trading, overfit, cashflow, execution и production risks |
| Validation planning | `agents/test_validation.md` | `PASS_WITH_RISKS` — функционально является validation reviewer alias, но не использует полный L0-L5 формат `agent-pack-designer` |
| Strategy hypothesis | `agents/strategy_research.md` | `PASS` — отдельная recurring role для market hypothesis и parameter-search design |
| Data/export quality | `agents/data_quality.md` | `PASS` — отдельный контекст для MT5/CSV/XLSX schema, периодов, reconciliation |
| Backtest credibility | `agents/backtest_validator.md` | `PASS` — обязательная роль для Strategy Tester reports и rent/monthly claims |
| Candidate selection | `agents/candidate_selector.md` | `PASS` — selection/filter/dedup отличается от raw backtest validation |
| Cascade construction | `agents/cascade_builder.md` | `PASS` — portfolio/cascade composition требует отдельного контекста |
| Monthly cashflow | `agents/monthly_cashflow_reviewer.md` | `PASS` — rent/top-up/bad-month sequence является core project risk |
| Capital/risk/margin | `agents/risk_manager.md` | `PASS` — lot sizing, margin, DD и survival не должны смешиваться с selection |
| MQL5 implementation | `agents/mql5_engineer.md` | `PASS` — implementation role отделена от reviewers и trading research |
| Live execution realism | `agents/execution_reviewer.md` | `PASS` — spread/slippage/broker constraints не покрываются backtest validator |
| Pending-order lifecycle | `agents/grid_pending_order_reviewer.md` | `PASS` — justified by pending/grid EA behavior and duplicate/stale order risks |
| Restart/state recovery | `agents/state_recovery_reviewer.md` | `PASS` — justified by MT5 terminal restart/orphan order risks |
| Production monitoring | `agents/production_monitor.md` | `PASS` — justified only for forward/live-like workflows; should remain trigger-only |
| Reproducibility handoff | `agents/decision_log_handoff.md` | `PASS` — needed because results are reused across long research decisions |
| Task specification | `agents/task_spec_short.md` | `PASS` — matches spec-first rule and prevents premature implementation |

## Соответствие rubric

| Критерий | Оценка | Основание |
|---|---|---|
| Scope | `PASS` | Большинство agents владеют одним workflow или risk lens, а не всем проектом |
| Context | `PASS_WITH_RISKS` | Есть правило не читать все agents, но не у всех файлов есть явный `Inspect First` section |
| Actionability | `PASS` | Checklists конкретны для MT5 trading, rent, risk, MQL5, execution, production |
| Separation | `PASS` | Implementation, review, validation, red-team и handoff разделены |
| Evidence discipline | `PASS` | `AGENTS.md` требует traceability, period labeling, no production claims from backtests |
| Portability | `PASS_WITH_RISKS` | Есть `CLAUDE.md`, но agent files не нормализованы под generated starter-pack section names |
| Minimality | `PASS_WITH_RISKS` | 17 agents оправданы mature workflow, но это не minimal starter pack и не должно быть default для новых проектов |
| Routing | `PASS_WITH_RISKS` | Routing есть в `AGENTS.md` + `agents/README_agents_index.md`, но нет отдельного `agents/context_router.md` |

## Что в `mt5-research` является полезным эталоном

| Паттерн | Стоит перенести в `agent-pack-designer`? | Причина |
|---|---|---|
| Mature project exception with many trigger-only agents | Да, уже частично сделано | `mt5-research` подтверждает, что high-risk mature workflow может оправдать 15+ agents при строгом routing |
| Separate red-team agent | Да | Для trading/risk/security/production-like проектов red-team должен быть отдельным triggered reviewer |
| Separate validation alias `test_validation.md` | Да, уже разрешено | Файл реально выполняет validation-planning роль, даже если имя отличается от starter-pack |
| Domain-specific reviewers вместо generic `risk_reviewer.md` | Да | `backtest_validator`, `risk_manager`, `execution_reviewer` несут разный контекст и не должны сливаться |
| Strong protected contracts in `AGENTS.md` | Да | Это центральное качество pack: агенты ограничены evidence/risk contracts |
| Token hygiene for heavy artifacts | Да | Для проектов с тяжелыми reports/files agent-pack должен явно указывать read strategy |
| Routing equivalent outside `context_router.md` | Возможно | Нужно осторожно: это полезно для audit-existing, но generated packs лучше продолжать создавать с отдельным router |

## Что не стоит копировать вслепую

| Паттерн | Риск |
|---|---|
| Отсутствие отдельного `agents/context_router.md` | Для новых generated packs хуже машинной проверки и L2 consistency |
| Нестандартизированные headings (`Mission`, `Check`, `Critical red flags`) | Хорошо читается человеком, но текущий validator воспринимает как missing required terms |
| `agents/README_agents_index.md` в той же папке, что и role agents | Existing-pack audit должен исключать index file из agent list; generated packs лучше иметь router |
| 17 agents как начальная рекомендация | Для новых проектов это agent sprawl; оправдано только при mature evidence |
| `test_validation.md` без L0-L5 полного словаря | Роль полезна, но слабее для formal validation-level claims |

## `validate_pack.py` результаты на `mt5-research`

Команда:

```text
python3 agent-pack-designer/scripts/validate_pack.py /Users/bobrsubr/PycharmProjects/_trading/mt5-research
```

Результат: `RESULT: FAIL`.

Интерпретация: это не доказывает, что `mt5-research` agents плохие. Это доказывает, что текущий `validate_pack.py` проверяет generated starter-pack schema, а не existing mature pack quality. Основные причины fail:

- нет `agents/context_router.md`;
- routing находится в `AGENTS.md` и `agents/README_agents_index.md`;
- headings отличаются от starter-pack обязательных terms;
- `agents/README_agents_index.md` ошибочно анализируется как обычный agent;
- `test_validation.md` является practical validation reviewer, но не содержит полный L0-L5 vocabulary.

После добавления отдельного режима:

```text
python3 agent-pack-designer/scripts/validate_pack.py --audit-existing /Users/bobrsubr/PycharmProjects/_trading/mt5-research
```

Результат: `RESULT: PASS_WITH_RISKS EXISTING_PACK_AUDIT`.

Это подтверждает ожидаемое разделение:

- default mode: строгая generated-pack L2 consistency, `mt5-research` не проходит;
- `--audit-existing`: quality/routing/separation audit, `mt5-research` проходит с предупреждениями.

## Decision: нужно ли менять `agent-pack-designer`

| Возможное изменение | Решение | Обоснование |
|---|---|---|
| Подогнать generated starter-pack под `mt5-research` | `BLOCK` | Один успешный project pack не должен становиться универсальным шаблоном |
| Ослабить `validate_pack.py` по умолчанию | `BLOCK` | Default validator должен оставаться строгим для newly generated packs |
| Добавить `--audit-existing` режим | `PASS_WITH_RISKS` | Минимальный режим реализован; выдает audit result отдельно от `PASS L2` |
| Добавить `mt5-research` как mature reference в validation evidence | `PASS_WITH_RISKS` | Полезный новый тип проекта: high-risk trading/research/MQL5 |
| Улучшить docs про router-equivalent | `RETEST` | Можно уточнить, что это приемлемо для audit-existing, но не для generated default pack |
| Добавить detection for index files | `PASS_WITH_RISKS` | В `--audit-existing` index/readme files исключаются из role-agent checks |

## Рекомендация

Следующий минимальный шаг для улучшения `agent-pack-designer`: усилить уже добавленный `--audit-existing` режим отдельными tests/fixtures и, при необходимости, более точной scoring таблицей.

Минимальные требования и текущий статус:

1. Проверять `AGENTS.md`, `CLAUDE.md`, `agents/README_agents_index.md`, `agents/context_router.md` как возможные routing sources.
2. Исключать index/readme files из списка role agents.
3. Принимать section aliases: `Mission`/`Goal`, `Use for`/`When to Use`, `Check`/`Checklist`, `Critical red flags`/`Stop Rules`.
4. Частично закрыто: агентские gaps выводятся как warnings; per-agent verdict table пока не реализована.
5. Не разрешать existing pack автоматически claim L2 generated-pack consistency.

Открыто: пункт 4 пока реализован как warnings + aggregate result, а не как per-agent verdict table.

## Commands run

| Проверка | Команда | Результат |
|---|---|---|
| Target agent inventory | `find /Users/bobrsubr/PycharmProjects/_trading/mt5-research/agents -maxdepth 2 -type f -print` | Найдены `README_agents_index.md` и 17 role files |
| Target contracts | `sed -n '1,260p' /Users/bobrsubr/PycharmProjects/_trading/mt5-research/AGENTS.md` | Routing, protected contracts, decision states inspected |
| Target Claude context | `sed -n '1,220p' /Users/bobrsubr/PycharmProjects/_trading/mt5-research/CLAUDE.md` | Agent-native workflow, MT5 architecture, validation tooling inspected |
| Target agent index | `sed -n '1,260p' /Users/bobrsubr/PycharmProjects/_trading/mt5-research/agents/README_agents_index.md` | Minimal-context index inspected |
| Target agent samples | `for f in .../agents/*.md; do sed -n '1,90p' "$f"; done` | Role goals/checklists/output patterns inspected |
| Target pack validator check | `python3 agent-pack-designer/scripts/validate_pack.py /Users/bobrsubr/PycharmProjects/_trading/mt5-research` | `RESULT: FAIL`, interpreted as schema mismatch not quality verdict |
| Target existing-pack audit | `python3 agent-pack-designer/scripts/validate_pack.py --audit-existing /Users/bobrsubr/PycharmProjects/_trading/mt5-research` | `RESULT: PASS_WITH_RISKS EXISTING_PACK_AUDIT` |
| Generated-pack default validation | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l2-credit-default-20260727` | `RESULT: PASS L2` |
| Generated-pack smoke validation | `python3 agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l5-install-20260727/generated-pack-smoke` | `RESULT: PASS L2` |
| Skill scaffold validation | `python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer` | `RESULT: PASS L0` before and after this report was added |

## Уровень валидации

| Level | Статус | Доказательства |
|---|---|---|
| L0 | PASS | Skill scaffold validator passed before and after this report |
| L1 | PASS | Existing cross-project reports remain available |
| L2 | PASS_WITH_RISKS | Mature existing-pack audit implemented and run; generated-pack L2 still passes on existing materialized packs |
| L3 | NOT CLAIMED | No generated pack was applied to `mt5-research` simulation task |
| L4 | NOT CLAIMED | This is one additional project case, not a rerun of full cross-project regression |
| L5 | NOT CLAIMED | No public/release pass performed for a new release after this report |

## Вывод

`mt5-research` is a useful mature reference, but not a template to copy blindly. It shows that `agent-pack-designer` should eventually distinguish two jobs:

- generated-pack validation: strict starter-pack consistency;
- existing-pack audit: quality/routing/separation assessment for mature packs with different structure.

With `--audit-existing`, `validate_pack.py` can now report `mt5-research` as `PASS_WITH_RISKS EXISTING_PACK_AUDIT` while keeping the default generated-pack result as `FAIL` for non-template shape.
