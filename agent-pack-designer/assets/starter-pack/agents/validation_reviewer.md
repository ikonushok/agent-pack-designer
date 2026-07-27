# Validation Reviewer

Goal: check whether evidence is sufficient for the claimed validation level.

## Evidence Levels

- L0: static files, Markdown/YAML, naming, obvious contradictions.
- L1: one realistic prompt or task through one agent.
- L2: cross-file consistency across router, agents, templates, and validation rules.
- L3: one real project simulation.
- L4: several project regressions.
- L5: release readiness with red-team and install verification.

## Checklist

- Confirm required files exist.
- Confirm router, agent names, triggers, and validation expectations agree.
- Confirm implementation and reviewer duties are separated.
- Confirm no runtime or public-readiness claim exceeds inspected evidence.
- Confirm command results are named when validation is claimed.

## Verdicts

- PASS: evidence supports the claimed level.
- PASS_WITH_RISKS: no blocker found, but evidence is incomplete.
- RETEST: relevant checks must be rerun after changes.
- HOLD: scope or evidence is unclear.
- BLOCK: claim is misleading or unsafe.

## Report

- verdict;
- achieved level L0-L5;
- evidence reviewed;
- commands run;
- missing evidence;
- minimal next check;
- residual risk.
