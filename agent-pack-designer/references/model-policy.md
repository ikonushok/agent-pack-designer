# Model and Permission Policy

Read when a project needs actual subagents, model assignment, or runtime permission configuration. A shared role Markdown file is context; it does not select a model or authorize delegation. Keep the policy in the project's existing maintained configuration or `AGENTS.md`. Add no role solely to select models.

## Role Contract

For each existing role, record a task profile (`fast`, `balanced`, or `deep`, or project-specific names), selection rationale, allowed candidates, explicit user choice if any, supported reasoning effort, permission intent, output/evidence format, and the condition for escalation. A difficult investigation can need the deep profile; a researcher is not automatically a lightweight task. Compare total task cost, latency, missed dependencies and parent rework before claiming savings.

Profiles express requirements, not a permanent ranking of provider models. Map them to concrete candidates using current official capability information, project observations and user preferences. An ordered candidate list authorizes those choices for that profile; it must respect the user's spending/quality constraints. Do not infer cost or quality from model names. New or newly listed models are not automatically approved candidates.

Default to the parent's model and reasoning settings when no reliable selection evidence is available and inheritance satisfies user constraints. An explicit unavailable model is a `HOLD`, not permission to silently substitute another. Escalation to a stronger model is a separate decision from increasing permissions.

## Discover Availability

1. Identify product surface, authentication method and account/workspace or API project. Use a non-secret identity label; do not save credentials, tokens or private account details in a pack.
2. Prefer the authenticated runtime's supported account-scoped catalog or model choices. Record source and timezone-aware observation time, and whether the result is current, cached or unknown. A configured model, public catalog, subscription name, cached CLI catalog, or price page does not establish account access. A user-provided list can be used as declared evidence, with its source and limits stated.
3. Match evidence to the same surface, sign-in method and identity used for delegation. ChatGPT, ChatGPT Work, local/cloud Codex, OpenAI API, Claude Code subscription, Anthropic API and cloud gateways are separate boundaries. If no supported discovery tool is exposed, inherit or request the missing choices only when needed; do not scrape authentication stores or invent an API.
4. Apply user allowlists, approved profile candidates and current reasoning support. Choose a refresh interval appropriate to the project; refresh at session setup, identity/surface changes, expiry, retirement or access failure. Never commit an account catalog as universal permanent truth.
5. After an authorized launch, inspect the actual resolved model and result if the runtime exposes them. Listing is evidence for a proposal, not proof of a successful launch, remaining quota, tool support or model quality.

At an access/quota failure, use only a previously approved fallback that still meets task requirements and budget, or return work to the parent when permitted. Do not infer that another model has quota or is cheaper. Do not retry the same rejected choice indefinitely; after one refresh/reselection attempt, report the blocker or continue on the approved parent path. Explicit user choices remain authoritative.

## Optional Deterministic Resolver

`scripts/resolve_model_policy.py` reads a supplied JSON policy and normalized catalog and prints a proposal. It does not discover accounts, call providers, launch agents, write configurations, install hooks, enforce permissions, or retry failures. A runtime adapter or the invoking agent supplies evidence through supported discovery tools. Without such an adapter, discovery remains an instruction-driven workflow. Output always says `runtime_verification: not_run`.

Request fields:

| Field | Meaning |
|---|---|
| `context` | Exact `surface`, `auth_method`, `identity` strings for this delegation boundary |
| `parent_model` | Model currently used by the parent |
| `profile`, `profiles` | Requested profile and ordered, user-approved candidate IDs for each profile |
| `allowed_models` | Optional global allowlist; omission adds no restriction, an empty list allows none, including inheritance |
| `model`, `reasoning_effort` | Optional explicit requirements; no silent replacement or effort removal |
| `unavailable_models` | Optional IDs rejected in this session; never select or inherit them |
| `catalog` | Optional evidence object with matching `context`, `source`, `status`, `observed_at`, and `models` |
| `max_catalog_age_seconds` | Positive project-selected freshness window; required when a catalog is supplied |

Each catalog model has an `id` and optionally a `reasoning_efforts` string list. Missing effort metadata means unsupported/unknown for an explicit effort. The catalog `status` is `current`, `cached`, or `unknown`; only current, matching, unexpired evidence can select a concrete candidate. The caller is responsible for the truth of normalized evidence. The resolver cannot authenticate its source. Syntactically invalid evidence returns `BLOCK` rather than guessing.

Example with synthetic IDs (replace with approved models and newly observed evidence; the timestamp is illustrative):

```json
{
  "context": {"surface": "codex-local", "auth_method": "subscription", "identity": "personal"},
  "parent_model": "main-model",
  "profile": "fast",
  "profiles": {"fast": ["research-model"], "deep": ["main-model"]},
  "allowed_models": ["research-model", "main-model"],
  "max_catalog_age_seconds": 3600,
  "catalog": {
    "context": {"surface": "codex-local", "auth_method": "subscription", "identity": "personal"},
    "source": "authenticated runtime discovery",
    "status": "current",
    "observed_at": "2026-10-12T00:00:00Z",
    "models": [{"id": "research-model"}, {"id": "main-model"}]
  }
}
```

Run `python3 scripts/resolve_model_policy.py /path/to/request.json` from the installed skill directory. Exit 0 is `PASS_WITH_RISKS` with `select` or `inherit`; exit 2 is `HOLD`; exit 1 is `BLOCK` for malformed policy/evidence. These are selection decisions, not L3-L5 runtime validation.

## Permission Modes and Runtime Mapping

Keep three separate intents: `read-only` for inspection, `scoped-write` for authorized implementation, and `validation-output` for checks that need caches or generated results. Prefer a single writer plus research/review subagents when useful, but allow isolated implementation workers when the real workflow requires them. Model changes never expand scope or rights.

Generate native files only for an explicitly targeted runtime, after checking its current supported schema and client capabilities. Keep one maintained role body and reference it where supported; avoid contradictory copies. Where a runtime requires embedded instructions, identify the shared source and synchronization owner.

- **Claude Code:** project subagents use `.claude/agents/*.md` frontmatter for `model`, `tools`, `disallowedTools` and supported permission options. `model: inherit` preserves model inheritance. `tools: Read, Grep, Glob` is a narrow exploration tool set. Allowing Bash or MCP adds potential mutation paths; denying Write/Edit alone does not close them. Hook-added instructions express intent; guards must cover the actual tool surface. Plugin subagents have different field support. Verify on the installed version.
- **Local Codex:** custom agents can set `model`, `model_reasoning_effort` and sandbox settings in `.codex/agents/*.toml` on supported clients. For inheritance omit explicit model/effort overrides. A documented `sandbox_mode = "read-only"` is a configuration request; parent session overrides and connector permissions still matter. Inspect effective settings before claiming enforcement.
- **ChatGPT Work / other hosted environments:** use exposed model and delegation controls. Local Codex TOML or Claude hooks are not evidence of equivalent hosted enforcement. If per-agent configuration is unavailable, retain portable policy, inherit available settings and state the limitation.

For claimed enforcement, exercise allowed reading and attempted writes through relevant file, shell, MCP and external-service paths in an isolated environment. Verify the primary agent's intended rights separately. If only local file protection was tested, name that boundary. No permission intent or static configuration check proves comprehensive read-only behavior.

## Behavioral Acceptance

| Scenario | Expected observation |
|---|---|
| No account catalog exposed | Parent inheritance or a scoped missing-input result; no guessed model |
| Stale/cached catalog or different account/surface/sign-in | Refresh or inheritance; no selection from mismatched evidence |
| Explicit unavailable model, unsupported effort, empty allowlist | `HOLD`; no silent substitution or constraint removal |
| Model added/retired, access failure or quota exhausted | Refresh, approved fallback or parent path; bounded attempts; no inferred quota/cost |
| Complex research | Profile follows reasoning requirements, not the role's researcher label |
| Researcher attempts write; validation writes cache | Effective runtime restrictions exercised separately from legitimate output needs |

## Official Sources

Checked 2026-10-12; recheck before producing native configuration. This is not a frozen model catalog.

- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents): model/tool configuration and runtime-specific restrictions.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks): context injection versus tool-call decisions.
- [OpenAI subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): model/reasoning configuration, inheritance, local/hosted boundaries and runtime overrides.
- [Workspace model availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability): surface and authentication boundaries.
- [Sign in with ChatGPT model discovery](https://developers.openai.com/siwc/token-sharing-open-source/models-and-inference): supported account-scoped discovery, cache caveat and quota failures; available only in integrations exposing this flow.
- [OpenAI API model list](https://developers.openai.com/api/reference/resources/models/methods/list): authenticated API catalog; not a subscription-entitlement check for another product.
