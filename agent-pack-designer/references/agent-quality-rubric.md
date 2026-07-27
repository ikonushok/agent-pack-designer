# Agent Quality Rubric

Use this rubric when reviewing generated agents or deciding whether another agent is justified.

## Required Fields

A good agent has:

- clear goal;
- specific when-to-use trigger;
- inputs to inspect first;
- focused checklist;
- output format;
- stop rules;
- sufficiency criteria;
- validation expectations.

## Quality Checks

Score each item as pass, risk, or fail:

- Scope: the agent owns one workflow or risk, not the whole project.
- Context: the agent starts from named files or patterns, not the full repository.
- Actionability: checklist items can be followed without extra interpretation.
- Separation: implementation, review, validation, and red-team work are not merged.
- Evidence: claims distinguish docs, inspected files, and executed commands.
- Portability: Codex and Claude-specific instructions are separated where needed.
- Minimality: removing the agent would create real duplication or risk.

## Bad Signs

- usable for every task;
- duplicates another agent;
- loads the whole project by default;
- has no stop condition;
- asks future agents to trust README claims as proof;
- creates reviewers without a concrete risk;
- uses platform-specific tooling without naming a fallback.

## Verdicts

- PASS: usable as-is for its named workflow.
- PASS_WITH_RISKS: usable, but validation or scope is incomplete.
- RETEST: likely usable after small edits and another validation pass.
- HOLD: needs design revision before use.
- BLOCK: unsafe, misleading, or too broad to include.
