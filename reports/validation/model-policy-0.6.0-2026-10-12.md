# Model Policy 0.6.0 Validation

Date: 2026-10-12 (Asia/Sakhalin). Package: 0.6.0. Scope: evidence recorded during local preparation of the update from 0.5.0; publication is tracked by the v0.6.0 tag and GitHub release.

## Result and Scope

Verdict: PASS_WITH_RISKS. L0 skill validation, L1 independent sample generation and L2 structural consistency of materialized templates and the sample pack passed. The Python resolver was exercised with synthetic evidence. Provider model discovery, native agent launch, account access, remaining quota, cost savings, model quality and permission enforcement are not established by these checks. L3-L5 readiness is not claimed.

The change extends existing roles rather than adding a model-selection agent. The optional resolver consumes supplied normalized evidence and prints a proposal; supported runtime discovery remains a workflow for the invoking agent or a separately provided adapter. It reads no authentication stores and deploys nothing. Historical 0.5.0 code/knowledge/artifact contracts remain active.

## Commands Actually Run

Environment: macOS, Python 3.14.6 for repository checks.

| Command | Observed result |
|---|---|
| `python3 -m unittest discover -s tests` | PASS: 47 tests, no skips |
| `python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer` | PASS L0 |
| `python3 agent-pack-designer/scripts/validate_pack.py --profile skill-designer-repository .` | PASS; includes L2 structural checks on materialized starter templates |
| `python3 agent-pack-designer/scripts/validate_release_metadata.py .` | PASS for locally prepared, untagged metadata |
| `/Users/bobrsubr/venv/breakdowns_of_mining_trucks/bin/python /Users/bobrsubr/.codex/skills/.system/skill-creator/scripts/quick_validate.py agent-pack-designer` | PASS: Skill is valid |
| Clean temporary package copy, staged `validate_skill.py`, and staged resolver CLI with fresh synthetic catalog | PASS L0 and expected model-selection proposal, `runtime_verification: not_run` |
| `git diff --check` | PASS |

Skill Creator's validator initially could not import PyYAML using the default and bundled Python interpreters. It then passed with an existing local virtual environment containing PyYAML; no dependencies were installed. Linux CI and Windows checks were not run during local preparation; GitHub Actions records any subsequent CI run for the published commit.

## Regression Evidence

The 16 new resolver tests cover current and missing catalogs, cached/unknown/stale/future evidence, account/surface/sign-in mismatches, empty allowlists including parent inheritance, user-choice precedence, newly listed models, failed/retired candidates, unavailable parents, explicit supported/unsupported/unknown reasoning settings, deep investigation profiles, malformed evidence, CLI exit codes and input immutability.

Existing regression cases still cover mature-pack compatibility, materialized starter consistency, target-validator isolation and template/role contracts. The missing-contract cases now include the shared model/permission section and both task-spec policy/evidence fields. They prove structural presence, not effective enforcement or good model judgments.

## Independent Forward Test

An independent subagent applied the revised skill to a synthetic Python CSV daily-summary CLI in `/private/tmp/agent_pack_060_cli_7nxge6k_`. The request targeted local Codex with subscription sign-in, one read-only research/review subagent, primary ownership of code changes, fast/deep task preferences and no supplied account catalog. Provider calls and installation were prohibited.

Observed output: parent model/effort inheritance, no guessed model IDs or account labels, fast/deep profiles shared by the existing reviewer, one implementation owner, and native configuration/launch explicitly deferred because installed-client support was not established within the isolated test. The validation role remained a checklist rather than another launched agent. Inspecting the generated files and captured command evidence confirmed these decisions.

The skill scaffold passed L0, the generated pack passed L2, and three synthetic CLI tests passed. This is L1 sample-prompt evidence with L2 structural checks, not a real-project L3 simulation. It does not exercise provider discovery, actual subagents in the generated project or enforcement.

The existing current-level validator initially misread an explanatory L2 requirement on the same line as `Current validation level: L0` as a higher-level claim. Separating status and explanatory requirement yielded PASS on rerun. The validator heuristic was not changed in this release; use a standalone status line. No contradiction was found in the new model-policy guidance.

The [single evidence snapshot](fixtures/model-policy-0.6.0.json) preserves the request, generated project/pack sources and captured outcomes without caches or credentials. Original temporary artifacts remain available; no active consumer was moved or removed. Snapshot SHA-256: `8383642e119475781b224f1e71c75cf06d7af66a087c8145da8d730485d476da`.

## Publication and Integration

Both version files, README status/release notes and changelog identify 0.6.0. New reference and helper are discoverable from the skill and README; existing roles point to one shared policy. No model catalog, credential, runtime configuration or new role is embedded in the package. The pre-existing untracked `.specify/` directory is outside the change.

Publication-language scan passed across 28 public Markdown/Python/YAML/text files (including tests, excluding historical `internal_ru` reports); the JSON snapshot was checked separately. Final local-link existence passed for 59 links in changed documents, including the snapshot link; snapshot integrity was also verified. This language/publication pass does not establish international release readiness or L5.

The local installed skill was updated from 0.5.0 to 0.6.0. All 20 clean package files were compared byte-for-byte with the repository and installed copy; the installed validator passed L0. Backup: `/Users/bobrsubr/.codex/skill-backups/agent-pack-designer-0.5.0-2026-10-12-50d491d1ce`. At the end of local preparation, no GitHub tag, push or publication had been performed. Subsequent publication does not raise the validation level recorded here.

## Remaining Evidence

- Native configuration schema loading and actual resolved model on each supported installed client.
- Account-specific discovery and refresh against real supported runtime tools.
- Access/quota failure with a real approved fallback and bounded retry observations.
- Permission enforcement through local files, shell, MCP and external-service paths; primary-agent rights checked separately.
- Comparative quality, total task cost, latency and parent rework on realistic workloads.
- Linux/Windows regressions and any future L3-L5 release assessment.

The next recommended validation is a scoped native-runtime trial using a supported account catalog and isolated read/write checks. This report does not authorize provider calls, account changes, publication or new spending.
