# Task Spec Short

Goal: scope non-trivial repository work before editing.

When to Use:
- changing `SKILL.md`, references, starter-pack templates, validators, CI, or public documentation;
- preparing a release, validation report, or customer-facing audit;
- coordinating work that touches more than one repository surface.

Inspect First:
- `AGENTS.md`;
- `README.md`;
- `agent-pack-designer/SKILL.md`;
- relevant files under `agent-pack-designer/references/`, `agent-pack-designer/assets/starter-pack/`, `agent-pack-designer/scripts/`, or `.claude/agents/`.

Checklist:
- state the goal and non-goals;
- name allowed files and files to avoid;
- identify the validation target, normally L0 for scaffold edits or L2 for generated-pack checks;
- list commands that must be run before claiming success;
- record residual risk when checks are skipped or incomplete.

Stop Rules:
- do not broaden the task into unrelated refactors;
- do not modify generated customer reports unless the task is explicitly about reports;
- do not claim runtime validation from static checks.

Output:
- scoped task summary;
- allowed files;
- validation target;
- commands to run;
- verdict: PASS / PASS_WITH_RISKS / RETEST / HOLD / BLOCK.
