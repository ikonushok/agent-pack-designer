# Specification Discovery

Use before building a deliverable inventory or auditing a pack against project requirements. Spec Kit is one supported layout; ordinary documentation is also a valid input.

## Discover Relevant Sources

Start with files the user names and the project's documented source-of-truth rules. Within that scope:

1. Look for `.specify/memory/constitution.md` and `specs/*/spec.md`. Read the constitution for project-wide principles and the task-relevant feature specs for requirements. Read adjacent `plan.md`, `tasks.md`, or checklists only when they clarify constraints, deliverables, or validation.
2. If these files are absent or contain only scaffold placeholders, look for ordinary specifications under `spec/`, `specs/`, `docs/spec*`, `docs/requirements*`, and `docs/design*`, plus relevant README sections and linked documents. These patterns are discovery hints, not an exhaustive list or a required layout.
3. If the structured sources cover only part of the task, supplement them with relevant ordinary documentation. A constitution without feature specs supplies constraints but does not replace missing deliverables or acceptance criteria.
4. If no usable specification exists, use the user request, project description, and available repository evidence. Record missing requirements and assumptions; do not invent acceptance criteria or require Spec Kit setup.

List candidate paths first, then inspect only sources relevant to the task. Avoid loading every feature spec or design document by default. Exclude generated reports, archived requirements, and example/template content from active requirements unless the user or project explicitly selects them.

An existing `.specify/` directory does not establish usable requirements. Treat unresolved placeholders such as `[PROJECT_NAME]` and `[PRINCIPLE_1_NAME]` as missing information. For partially completed documents, retain concrete requirements and record unresolved fields separately.

## Extract Requirements

Build a compact inventory with source paths and section anchors. Preserve distinctions between required, optional, proposed, and explicitly excluded scope.

| Field | Extract | Carry into the pack |
|---|---|---|
| Deliverables | Required outputs, artifacts, submission items, optional/bonus/stretch items, and checklist-only outputs | Primary workflow, reviewer checklist, or explicit coverage status |
| Acceptance criteria | Observable success conditions, examples, expected values, and completion gates | Task spec and validation checklist |
| Non-goals | Excluded behavior, deferred work, and boundaries | Task spec and agent stop rules |
| Constraints | Constitution principles, architectural limits, allowed files, compatibility, and data restrictions | Project rules and relevant agent contracts |
| Validation expectations | Required checks, commands, evidence artifacts, and requested validation level | Validation reviewer and routing entries |

Mark unspecified fields as missing rather than deriving them from folder names. A design proposal is not an accepted requirement, and a checked task box is not proof of implementation or a passing test.

Keep enough provenance to explain which source supplied each requirement. Use the project's stated precedence and the user's current scope when documents disagree. If neither resolves a material conflict, report it and seek clarification before making a dependent scope decision. Do not silently discard a requirement because the current implementation differs.

## Check Evidence Before Raising Claims

Documentation establishes intent. Record implementation evidence and executed checks separately:

- At L0-L2, report the static or pack-consistency checks actually performed. These levels do not establish runtime behavior or complete semantic coverage of the requirements.
- Before claiming L3 or above, trace relevant deliverables and acceptance criteria to code, tests, or artifacts, apply the pack to a real project case, and inspect the result. Run and inspect commands when claiming runtime or test success.
- At L4, repeat relevant checks across materially different projects. At L5, also collect the release, installation, publication, and red-team evidence required by `validation-levels.md`.
- Record mismatches as documented intent, observed behavior, and missing or failing evidence. Use `PASS_WITH_RISKS` for incomplete evidence without a known blocker; use `HOLD` or `BLOCK` when unresolved conflicts prevent a defensible claim.

Code and test files alone do not establish L3-L5. Consult [Validation Levels](validation-levels.md) for the evidence required at each level.
