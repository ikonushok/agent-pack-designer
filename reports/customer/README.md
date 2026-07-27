# Customer Audit Examples

This folder contains selected customer-facing agent-pack audit reports produced by:

```bash
python3 agent-pack-designer/scripts/validate_pack.py --profile mature-existing-pack --report-md reports/customer/report.md /path/to/project
```

Most generated customer reports stay gitignored because they can name private repositories, internal paths, and project-specific risks. The reports committed here are examples only because these target projects are already named in this repository's README, changelog, or validation evidence.

## Included Examples

| Report | Profile | Result | Why it is useful |
|---|---|---|---|
| [`customer-agent-pack-designer-agent-pack-audit-2026-07-27.md`](customer-agent-pack-designer-agent-pack-audit-2026-07-27.md) | `skill-designer-repository` | `PASS` | Shows how the validator audits this repository as a skill-designer project instead of treating it as a generated customer pack. |
| [`customer-credit-default-prediction-agent-pack-audit-2026-07-27.md`](customer-credit-default-prediction-agent-pack-audit-2026-07-27.md) | `mature-existing-pack` | `PASS_WITH_RISKS` | Shows a mature tabular ML project with many role agents, explicit routing, a validation alias, and missing Claude context. |
| [`customer-loan-offer-acceptance-prediction-agent-pack-audit-2026-07-27.md`](customer-loan-offer-acceptance-prediction-agent-pack-audit-2026-07-27.md) | `mature-existing-pack` | `PASS_WITH_RISKS` | Shows a second mature ML project with a similar agent layout, useful for checking repeatability across related but distinct projects. |
| [`customer-hiking-route-recommender-demo-agent-pack-audit-2026-07-27.md`](customer-hiking-route-recommender-demo-agent-pack-audit-2026-07-27.md) | `mature-existing-pack` | `FAIL` | Shows a negative audit where a known project is blocked by missing separate validation-review ownership and weak default-context routing. |
| [`customer-mt5-research-agent-pack-audit-2026-07-27.md`](customer-mt5-research-agent-pack-audit-2026-07-27.md) | `mature-existing-pack` | `PASS_WITH_RISKS` | Shows a mature high-risk trading/research project where many trigger-only agents can be acceptable when routing keeps default context small. |

## What These Audits Check

The mature-existing-pack report is intentionally not a generated-pack schema check. It reviews whether an existing project agent pack has:

- a root project contract such as [`AGENTS.md`](../../AGENTS.md);
- routing that prevents loading every role file by default;
- separate implementation, review, and validation ownership;
- a validation reviewer or accepted validation alias;
- clear protected contracts, forbidden changes, or project risk boundaries;
- enough decision vocabulary to distinguish pass, retest, hold, block, and pass-with-risks states;
- reasonable token economy for role files.

The reports do not prove the target project's runtime quality, model quality, financial safety, production readiness, or business correctness. They only audit the structure and evidence discipline of the target agent pack.

## When To Commit A Customer Report

Commit a report here only when all of the following are true:

- the target project is already named in public repository documentation or validation evidence;
- the report is useful as a distinct example, not just another copy of the same pattern;
- the report result and limitations are explicit;
- the report does not introduce new private project names that are not already documented;
- the report is regenerated with the current validator before staging.

Leave all other generated customer reports untracked under this gitignored folder.
