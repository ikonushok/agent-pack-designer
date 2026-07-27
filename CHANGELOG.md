# Changelog

## Unreleased

- Added L1/partial-L2 validation evidence from comparing real project agent packs for hiking-route recommendation, loan-offer acceptance prediction, and credit-default prediction.
- Added real-project guidance for core, trigger-only, and optional/future agents, including `test_validation.md` as a validation reviewer alias and `CLAUDE.md` as optional unless Claude Code is targeted.

## v0.1.0

Initial installable release candidate.

- Added Codex skill metadata in `agent-pack-designer/agents/openai.yaml`.
- Strengthened `SKILL.md` with minimal-pack workflow, stop rules, and validation evidence reporting.
- Expanded starter-pack templates for `AGENTS.md`, `CLAUDE.md`, routing, primary workflow, risk review, task specs, and validation review.
- Added reference guidance for design workflow, agent quality, and validation levels.
- Added `agent-pack-designer/scripts/validate_skill.py` for L0 static scaffold validation.

Validation: L0 via `python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer`.
