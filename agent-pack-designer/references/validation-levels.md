# Validation Levels

- L0: static check of files, Markdown, YAML, obvious contradictions.
- L1: one sample task through one agent or prompt.
- L2: full agent-pack consistency: routing, names, roles, templates.
- L3: simulation on one real project case.
- L4: cross-project regression on several projects.
- L5: red-team and public/release readiness.

## Evidence Required

- L0 requires file existence, naming, Markdown/frontmatter checks, and no obvious contradictions.
- L1 requires one realistic prompt or task using the pack and a recorded outcome.
- L2 requires consistency across router, agent names, roles, stop rules, and templates.
- L3 requires applying the pack to one real project case and inspecting the generated output.
- L4 requires repeated checks across several materially different project types.
- L5 requires release checks, red-team review, install path verification, and documented residual risk.

## Claim Rules

- Never claim runtime validation unless commands were actually run and inspected.
- Never claim public/release readiness below L3.
- Use PASS_WITH_RISKS when evidence is incomplete but no blocker is known.
- Use RETEST when a fix was made but the relevant check was not rerun.
- Use HOLD or BLOCK when the pack can misroute work, inflate agent count, or misstate validation.

## Tool Verdicts

- `PASS`: the selected profile's required checks passed.
- `PASS_WITH_RISKS`: required checks passed, but warnings or missing evidence remain.
- `FAIL`: the selected profile applies and a required contract is violated.
- `NOT_APPLICABLE`: the target is a different artifact type; select another profile.
- `INCONCLUSIVE`: the target shape is ambiguous, so no quality verdict can be defended.
- `TOOL_ERROR`: validation could not complete because the tool could not read or process its inputs.

`NOT_APPLICABLE`, `INCONCLUSIVE`, and `TOOL_ERROR` are terminal states, not weaker forms of `FAIL`.

## Naming Notes

- `validation_reviewer.md` is the default starter-pack name.
- `test_validation.md` is an acceptable project-specific alias when the agent maps tasks to L0-L5 and checks evidence sufficiency.
- Claude Code projects may use equivalent validation reviewer names under `.claude/agents/`.
- Do not count README validation wording as a validation reviewer unless a separate agent or router entry owns evidence review.
