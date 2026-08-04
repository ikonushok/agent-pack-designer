# Changelog

## Unreleased

- Clarify that optional/future agents are different from optional, bonus, extra-credit, stretch, and checklist deliverables.
- Add deliverable coverage inventory guidance so generated packs keep bonus and optional sections visible through explicit status rather than silently dropping them.
- Update starter primary and reviewer templates to require explicit deliverable status.
- Clarify that L2 validation proves structural consistency, not semantic coverage of every README/spec/checklist deliverable.

## v0.3.0 - 2026-07-29

- Added explicit `generated-pack`, `mature-existing-pack`, and `skill-designer-repository` validation profiles.
- Kept `validate_pack.py --audit-existing` as a compatibility alias for the mature-existing profile.
- Added `--report-md` customer-facing Markdown report output for existing-pack audits, including what works, risks, recommended changes, and token-economy estimates.
- Added gitignored `reports/customer/` as the default location for generated customer-facing audit reports.
- Added internal MT5 research existing-pack audit evidence under `reports/validation/internal_ru/`.
- Added regression coverage for Claude agent discovery, intentional starter placeholders, report idempotence, profile mismatch, and verdict vocabulary.
- Added `NOT_APPLICABLE`, `INCONCLUSIVE`, and `TOOL_ERROR` terminal verdicts so target or tool failures are not reported as agent-quality failures.
- Made designer-profile validation use the installed trusted validator instead of executing target-owned Python.
- Recorded independent red-team review with blocking findings fixed before the final `PASS` verdict.
- Added a release metadata validation script and CI check for `VERSION`, README release wording, and tag consistency.
- Recorded v0.3.0 L5 release-readiness evidence for the current package surface.

Validation: L5 package release readiness via `reports/validation/l5-release-readiness-2026-07-29.md`.

## v0.2.0

- Added L1/partial-L2 validation evidence from comparing real project agent packs for hiking-route recommendation, loan-offer acceptance prediction, and credit-default prediction.
- Added real-project guidance for core, trigger-only, and optional/future agents, including `test_validation.md` as a validation reviewer alias and `CLAUDE.md` as optional unless Claude Code is targeted.
- Strengthened `scripts/validate_pack.py` for repeatable generated-pack L2 consistency validation across required sections, router references, agent roles, validation reviewer terms, unresolved template tokens, and validation-level claims.
- Added an L2 candidate report from a materialized generated pack for `credit-default-prediction`.
- Added cross-project generated-pack L2 validation evidence for `credit-default-prediction`, `loan-offer-acceptance-prediction`, and `hiking-route-recommender-demo`.
- Added L3 real-project simulation evidence for `hiking-route-recommender-demo` using a generated pack in `/private/tmp`.
- Added L4-with-risks runtime regression evidence across generated-pack-guided simulations for `go_through_the_forest`, `credit-default-prediction`, and `loan-offer-acceptance-prediction`, with target repositories left unchanged.
- Added L5 package release-readiness evidence, including language/publication pass, clean install verification, generated-pack smoke validation, and red-team claim audit.
- Relocated Russian working validation reports under `reports/validation/internal_ru/` for publication hygiene while keeping public docs and the L5 report in English.
- Documented language policy: public/installable files stay English, while Russian working validation reports require a language/publication pass before international release.

Validation: L5 package release readiness via `reports/validation/l5-release-readiness-2026-07-27.md`.

## v0.1.0

Initial installable release candidate.

- Added Codex skill metadata in `agent-pack-designer/agents/openai.yaml`.
- Strengthened `SKILL.md` with minimal-pack workflow, stop rules, and validation evidence reporting.
- Expanded starter-pack templates for `AGENTS.md`, `CLAUDE.md`, routing, primary workflow, risk review, task specs, and validation review.
- Added reference guidance for design workflow, agent quality, and validation levels.
- Added `agent-pack-designer/scripts/validate_skill.py` for L0 static scaffold validation.

Validation: L0 via `python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer`.
