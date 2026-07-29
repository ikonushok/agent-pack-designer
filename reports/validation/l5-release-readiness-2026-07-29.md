# L5 release readiness protocol - 2026-07-29

## Summary

| Field | Value |
|---|---|
| Skill under review | `agent-pack-designer` |
| Version | `0.3.0` |
| Objective | Verify release-readiness evidence for the current package surface after validation profile, CI, report, and release metadata updates |
| Verdict | `PASS L5` for package release readiness |
| Scope | Installable skill package, public documentation, validation evidence, release metadata, generated-pack smoke flow |
| Not in scope | Publishing to a registry or proving runtime behavior of target projects beyond recorded L4 simulations |

## Language and Publication Pass

| Check | Evidence | Result |
|---|---|---|
| Public/installable skill files | `agent-pack-designer/SKILL.md`, `references/`, `assets/starter-pack/`, scripts | English public surface retained |
| Public repository docs | `README.md`, `CHANGELOG.md` | English public surface retained |
| Working validation reports | Russian working reports remain under `reports/validation/internal_ru/` or ignored customer-report paths | Russian reports are kept out of the public package surface |
| Public validation report | This L5 report is written in English at `reports/validation/l5-release-readiness-2026-07-29.md` | Pass |
| Publication scan | CI language/publication scan over README, changelog, workflow, package, and public validation reports | Pass |

## Install Verification

| Check | Command | Result |
|---|---|---|
| Clean skill install copy | `cp -R agent-pack-designer /private/tmp/agent-pack-designer-l5-install-20260729.JpKkmi/codex-skills/agent-pack-designer` | Installed copy created |
| Installed skill scaffold validation | `python3 /private/tmp/agent-pack-designer-l5-install-20260729.JpKkmi/codex-skills/agent-pack-designer/scripts/validate_skill.py /private/tmp/agent-pack-designer-l5-install-20260729.JpKkmi/codex-skills/agent-pack-designer` | `RESULT: PASS L0` |
| Generated-pack smoke materialization | Copied installed `assets/starter-pack/` to `/private/tmp/agent-pack-designer-l5-install-20260729.JpKkmi/generated-pack-smoke` and filled project placeholders | Smoke pack created |
| Installed generated-pack validation | `python3 /private/tmp/agent-pack-designer-l5-install-20260729.JpKkmi/codex-skills/agent-pack-designer/scripts/validate_pack.py /private/tmp/agent-pack-designer-l5-install-20260729.JpKkmi/generated-pack-smoke` | `RESULT: PASS L2` |
| Smoke placeholder scan | `rg -n '\\{\\{|\\}\\}' /private/tmp/agent-pack-designer-l5-install-20260729.JpKkmi/generated-pack-smoke` | No matches |

## Release Checks

| Check | Command | Result |
|---|---|---|
| Skill scaffold validation from repo | `python3 agent-pack-designer/scripts/validate_skill.py agent-pack-designer` | `RESULT: PASS L0` |
| Designer repository profile validation | `python3 agent-pack-designer/scripts/validate_pack.py --profile skill-designer-repository .` | `RESULT: PASS skill-designer-repository` |
| Release metadata validation | `python3 agent-pack-designer/scripts/validate_release_metadata.py .` | `RESULT: PASS release metadata` |
| Unit tests | `python3 -m unittest discover -s tests` | 22 tests passed |
| Whitespace check | `git diff --check` | Passed |
| Language/publication scan | Python scan from `.github/workflows/validate.yml` | Passed |

## Tag Verification

| Check | Command | Expected result |
|---|---|---|
| Release tag on current release commit | `python3 agent-pack-designer/scripts/validate_release_metadata.py --require-head-tag .` | `RESULT: PASS release metadata` after tag `v0.3.0` is created on the release commit |

## Red-Team Review

| Area | Finding | Verdict |
|---|---|---|
| Agent sprawl | Starter pack still uses the minimal core pack: `AGENTS.md`, optional `CLAUDE.md`, router, one primary agent, one risk reviewer, validation reviewer, task spec | Pass |
| Validation overclaim | `validate_pack.py` is still documented as L2-only for generated-pack consistency; L3-L5 require recorded higher-level trials | Pass |
| Public readiness wording | Release readiness applies to the `agent-pack-designer` package, not to target project runtime systems | Pass |
| Language policy | Public/installable files and public validation reports are English; Russian working reports remain internal or ignored | Pass |
| Release metadata | `VERSION`, README status, README release notes, and tag validation are covered by `validate_release_metadata.py` | Pass |

## Validation Level

| Level | Status | Evidence |
|---|---|---|
| L0 | PASS | Skill scaffold validator passed |
| L1 | PASS | Existing real-project comparison evidence is retained in `reports/validation/internal_ru/` |
| L2 | PASS | Generated-pack consistency, designer profile validation, and smoke validation passed |
| L3 | PASS | Existing real-project simulation evidence is retained in `reports/validation/internal_ru/` |
| L4 | PASS_WITH_RISKS | Existing cross-project runtime regression evidence is retained in `reports/validation/internal_ru/` |
| L5 | PASS | Language/publication pass, release metadata validation, release checks, red-team review, and residual risks are recorded |

## Residual Risk

| Risk | Impact | Handling |
|---|---|---|
| L4 target runtime dependencies were incomplete in local Python | Forest API tests required `fastapi`; loan leakage/sample-weight tests required `catboost` | Kept as L4 target-runtime residual risk, not a blocker for package L5 |
| Manual install remains the documented path | Users must copy the skill folder manually | Installer remains optional unless manual copy becomes a recurring issue |
| Tag verification must run after tag creation | The release metadata script can require `v0.3.0` only after the release commit exists and is tagged | Run `validate_release_metadata.py --require-head-tag .` after creating tag `v0.3.0` |

## Conclusion

The current package surface has sufficient evidence to claim L5 package release readiness for `agent-pack-designer` version `0.3.0`: public docs are in English, package and designer-profile validation pass, release metadata is checked, unit tests pass, release checks pass, and red-team findings have no blocker. This claim does not extend to production readiness of downstream target projects that use generated packs.
