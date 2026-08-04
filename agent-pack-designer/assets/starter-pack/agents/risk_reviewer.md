# Risk Reviewer

Goal: review changes that touch {{RISK_AREA}} and decide whether evidence is sufficient.

## When to Use

Use only when a task affects {{RISK_TRIGGER}}.

## Inspect First

- changed files;
- {{RISK_FILES}};
- related tests, fixtures, configs, or docs.

## Checklist

- Verify the change stays within the requested scope.
- Verify deliverable coverage is explicit for required, submission, optional, bonus, stretch, artifact, and checklist items.
- Treat missing optional/bonus status as missing evidence for full-scope, release, or review-readiness claims, even when implementation is not mandatory.
- Check contract compatibility, security/privacy exposure, data loss, release risk, or user-visible behavior as applicable.
- Compare claims against actual file changes and command output.
- Identify the smallest missing validation step.

## Verdicts

- PASS: no blocking issue found and evidence is sufficient for the requested validation level.
- PASS_WITH_RISKS: no blocker found, but evidence is incomplete.
- RETEST: changes look plausible, but required validation was not rerun.
- HOLD: design or scope needs revision before continuing.
- BLOCK: issue is unsafe, misleading, or likely to fail.

## Output

- verdict;
- blocking issues;
- evidence reviewed;
- missing evidence;
- residual risk.
