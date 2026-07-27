# L2 profile regression validation — 2026-07-27

## Сводка

| Поле | Значение |
|---|---|
| Проверяемая функция | Профили `generated-pack`, `mature-existing-pack`, `skill-designer-repository` |
| Причина | Self-audit ошибочно выдал `FAIL` для designer repository |
| Итог | `PASS L2` для profile contracts и regression suite |
| Независимый review | `PASS` после двух циклов блокирующих findings и исправлений |
| Release status | Изменения остаются `Unreleased`; новый публичный release этим отчётом не заявляется |

## Исходный дефект

Первоначальный `mature-existing-pack` аудит был применён к `agent-pack-designer` как к обычному generated или mature pack. Он:

- не видел роли под `.claude/agents/`;
- считал намеренные starter placeholders незаполненными;
- сканировал validation и customer reports как активные pack files;
- менял результат после создания собственного отчёта.

Отчёт `reports/customer/customer-agent-pack-designer-agent-pack-audit-2026-07-27.md` помечен `INVALIDATED` и сохраняется только как regression evidence. Его `FAIL` не является оценкой качества агентов.

## Реализованные пункты

| # | Изменение | Статус |
|---:|---|---|
| 1 | Не добавлять фиктивный `agents/` для получения зелёного результата | PASS — существующие `.claude/agents/` поддерживаются |
| 2 | Пометить исходный self-audit как недействительный | PASS |
| 3 | Не выпускать старую реализацию audit mode | PASS — изменения остаются в `Unreleased` |
| 4 | Разделить три validation profile | PASS |
| 5 | Поддержать `agents/`, `.claude/agents/` и функциональные validation aliases | PASS |
| 6 | Ограничить placeholder scan активными profile files | PASS |
| 7 | Добавить positive/negative regression matrix | PASS — 17 тестов |
| 8 | Добавить terminal verdicts | PASS — `NOT_APPLICABLE`, `INCONCLUSIVE`, `TOOL_ERROR` |
| 9 | Выполнить cross-project и независимый review до readiness verdict | PASS |

## Red-to-green evidence

Первый согласованный regression test достиг production path и воспроизвёл три ошибки:

```text
Ran 3 tests
FAILED (failures=3)
```

После исправления основной набор и дополнительные boundary checks прошли:

```text
Ran 17 tests
OK
```

Команда:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

## Cross-project commands

| Target | Profile | Результат |
|---|---|---|
| Текущий repository | `skill-designer-repository` | `PASS_WITH_RISKS` — честно сохранены gaps собственных `.claude` agents |
| Текущий repository | `mature-existing-pack` | `PASS_WITH_RISKS EXISTING_PACK_AUDIT` |
| Credit-default materialized pack | `generated-pack` | `PASS L2` |
| Loan-offer materialized pack | `generated-pack` | `PASS L2` |
| Hiking-route materialized pack | `generated-pack` | `PASS L2` |
| `mt5-research` | `mature-existing-pack` | `PASS_WITH_RISKS EXISTING_PACK_AUDIT` |
| `mt5-research` через `--audit-existing` | Compatibility alias | `PASS_WITH_RISKS EXISTING_PACK_AUDIT` |
| Installable skill scaffold | `validate_skill.py` | `PASS L0` |

## Independent review

Отдельный read-only reviewer не редактировал файлы и не принимал существующие reports как доказательство без повторных команд.

1. Первый verdict: `FAIL`. Найдены четыре P1: поверхностный designer profile, запрет own mature audit, неполный `.claude` scan, необработанная ошибка записи report.
2. Второй verdict: `FAIL`. Найдена trust-boundary ошибка: исполнение target-owned `validate_skill.py`.
3. Финальный verdict: `PASS`. Подтверждены trusted sibling validator, отсутствие исполнения target code, 17 passing tests, три `PASS L2` generated packs, совместимый MT5 verdict и чистый diff.

## Границы доказательства

- `PASS L2` относится к profile contracts, routing/alias discovery, placeholder scope, verdict behavior и materialized starter smoke.
- Designer profile сам возвращает `PASS_WITH_RISKS`, поскольку собственные `.claude` agents имеют документированные audit-section gaps.
- Этот отчёт не повышает общий project claim выше ранее заявленных уровней и не создаёт новый release.
- Runtime качество проектов, model quality и production readiness не проверялись этой задачей.
