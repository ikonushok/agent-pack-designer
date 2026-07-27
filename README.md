# agent-pack-designer

Design minimal AI agent packs for Codex and Claude from project descriptions.

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

Early scaffold.

Current validation level: L0 - static file structure only.

## Install for Codex

From the repository root:

    mkdir -p ~/.codex/skills
    cp -R agent-pack-designer ~/.codex/skills/agent-pack-designer

Restart Codex, then use:

    Use $agent-pack-designer to design a minimal agent pack for this project from README.md and AGENTS.md.

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
      <primary_domain_agent>.md
      validation_reviewer.md
      task_spec_short.md
    optional_agents/
      README.md
    templates/
      task_spec_short.md

## Design Principles

- Minimal context first.
- One main agent, one reviewer, one validation path.
- Project-specific agents stay inside the target project.
- README is a living specification, not proof of implementation.
- Tests, smoke checks, dry-runs, and command output are evidence.
- Do not add agents for hypothetical future tasks.

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
      references/
      assets/starter-pack/
    .claude/agents/
    AGENTS.md
    CLAUDE.md
    README.md
    LICENSE

## Roadmap

- Add stronger starter templates.
- Add sample generated packs from real project cases.
- Add validation script for required files and frontmatter.
- Add npm-based installer.
- Forward-test on several project types.
- Prepare first tagged release.

## License

MIT
