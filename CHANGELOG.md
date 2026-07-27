# Changelog

## Unreleased

- Added L1/partial-L2 validation evidence from comparing real project agent packs for hiking-route recommendation, loan-offer acceptance prediction, and credit-default prediction.
- Added real-project guidance for core, trigger-only, and optional/future agents, including `test_validation.md` as a validation reviewer alias and `CLAUDE.md` as optional unless Claude Code is targeted.
- Strengthened `scripts/validate_pack.py` for repeatable generated-pack L2 consistency validation across required sections, router references, agent roles, validation reviewer terms, unresolved template tokens, and validation-level claims.
- Added an L2 candidate report from a materialized generated pack for `credit-default-prediction`.
- Added cross-project generated-pack L2 validation evidence for `credit-default-prediction`, `loan-offer-acceptance-prediction`, and `hiking-route-recommender-demo`.
- Added L3 real-project simulation evidence for `hiking-route-recommender-demo` using a generated pack in `/private/tmp`.
- Added L4-with-risks runtime regression evidence across generated-pack-guided simulations for `go_through_the_forest`, `credit-default-prediction`, and `loan-offer-acceptance-prediction`, with target repositories left unchanged.
- Documented language policy: public/installable files stay English, while Russian working validation reports require a language/publication pass before international release.

## v0.1.0

Initial installable release candidate.

- Added Codex skill metadata in `agent-pack-designer/agents/openai.yaml`.
- Strengthened `SKILL.md` with minimal-pack workflow, stop rules, and validation evidence reporting.
- Expanded starter-pack templates for `AGENTS.md`, `CLAUDE.md`, routing, primary workflow, risk review, task specs, and validation review.
- Added reference guidance for design workflow, agent quality, and validation levels.
- Added `agent-pack-designer/scripts/validate_skill.py` for L0 static scaffold validation.

Validation: L0 via `python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer`.
