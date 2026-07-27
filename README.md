# agent-pack-designer

Design minimal, validation-driven AI agent packs for Codex and Claude from project descriptions.

agent-pack-designer is a portable skill for turning a project description, README, technical spec, or existing workflow into a small, validation-driven agent pack.

It helps create:

- AGENTS.md for Codex
- CLAUDE.md for Claude Code
- agents/context_router.md
- project-specific domain agents
- validation and risk reviewers
- task_spec_short.md
- optional agents only when justified

## Status

Version: 0.1.0

Tagged release `v0.1.0`: L0 - static scaffold validation via `agent-pack-designer/scripts/validate_skill.py`.

Current branch evidence: L1, L2 generated-pack consistency evidence across three projects, and L3 real-project simulation evidence for `hiking-route-recommender-demo` in `reports/validation/`.

## Install for Codex

From the repository root:

    mkdir -p ~/.codex/skills
    cp -R agent-pack-designer ~/.codex/skills/agent-pack-designer

Restart Codex, then use:

    Use $agent-pack-designer to design a minimal agent pack for this project from README.md and AGENTS.md.

The installable skill folder contains:

    agent-pack-designer/
      SKILL.md
      agents/openai.yaml
      references/
      assets/starter-pack/
      scripts/validate_skill.py
      scripts/validate_pack.py

## Use with Claude Code

Claude Code can use:

1. CLAUDE.md - project memory and working rules.
2. .claude/agents/ - reviewer agents for architecture, compatibility, and validation.

Example prompt:

    Use this repository to design a minimal Codex/Claude agent pack for my project. Keep the pack small and state validation level.

## Expected Output

A generated project pack should normally contain:

    AGENTS.md
    CLAUDE.md
    agents/
      context_router.md
      primary_agent.md
      risk_reviewer.md
      validation_reviewer.md
      task_spec_short.md

Rename `primary_agent.md` and `risk_reviewer.md` to project-specific names when the target project has clear domain language. Delete or omit `risk_reviewer.md` when there is no concrete recurring risk to review.

## Design Principles

- Minimal context first.
- One main agent, one reviewer, one validation path.
- Project-specific agents stay inside the target project.
- README is a living specification, not proof of implementation.
- Tests, smoke checks, dry-runs, and command output are evidence.
- Do not add agents for hypothetical future tasks.

## Language Policy

Public/installable skill files are kept in English. Russian validation reports are acceptable during active development, but an international public release requires a language/publication pass: translate or relocate Russian reports, keep public docs English, and record the result as validation evidence.

## Validation Levels

| Level | Meaning |
|---|---|
| L0 | Static file and Markdown/YAML structure check |
| L1 | One sample task through one prompt or agent |
| L2 | Generated pack consistency: routing, names, roles, templates |
| L3 | Real project simulation |
| L4 | Cross-project regression across several projects |
| L5 | Red-team and public/release readiness |

## Repository Layout

    agent-pack-designer/
      SKILL.md
      agents/openai.yaml
      references/
      assets/starter-pack/
      scripts/validate_skill.py
    .claude/agents/
    AGENTS.md
    CLAUDE.md
    CHANGELOG.md
    reports/validation/
    README.md
    VERSION
    LICENSE

## Validate

Run:

    python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer

Expected result for the skill scaffold:

    RESULT: PASS L0

Validate a generated project pack:

    python3 agent-pack-designer/scripts/validate_pack.py /path/to/generated-pack

Expected result for a structurally consistent generated pack:

    RESULT: PASS L2

Higher validation levels require generated-pack trials:

- L1: one sample project prompt.
- L2: generated pack consistency review.
- L3: one real project simulation.
- L4: cross-project regression.
- L5: public/release readiness review.

## Release Notes

0.1.0 is tagged as the L0 installable release.

Current unreleased work adds L2 generated-pack consistency validation and one L3 real-project simulation. This does not claim L4 or L5 because there is no multi-project runtime regression protocol, language/publication pass, install verification, or red-team release audit for the next public release.

Remaining post-0.1 work:

- Add a multi-project runtime regression protocol before claiming L4.
- Consider an installer only if manual copy becomes a recurring problem.

## License

MIT
