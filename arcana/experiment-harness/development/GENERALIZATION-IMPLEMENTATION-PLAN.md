# Experiment Harness Generalization Implementation Plan

Status: refreshed implementation plan.

## Goal

Generalize Experiment Harness so Spellcraft and Sigil Development can request lifecycle-specific experiment profiles without duplicating harness mechanics or smuggling spell/sigil meaning into the harness.

## Success Condition

A reusable spell and a reusable sigil can each initialize a loop-ready harness with lifecycle-appropriate prompts, fixtures, regimes, validation shape, and observability closeout. Sigil Development can then be used as the first real test case: create or update a sigil's experiment pack, run validation, and record whether the produced evidence is usable.

## Refresh Summary

This plan was refreshed after interrogation and design-gap fill. The controlling implementation contract is now [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md).

The next execution slice is no longer open-ended design. It is:

1. implement profile-aware initialization,
2. generate `development/EXPERIMENT-PROFILE.md`,
3. generate profile starter prompts and regimes,
4. validate profile drift,
5. prove the flow in a sandbox copy before touching a real sigil.

## Layer Plan

| Layer | Decision Question | Smallest Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Can the profile boundary be documented without changing runtime behavior? | Generalization design, implementation plan, and test-case plan. | Docs exist and name owners, inputs, outputs, and deferred complexity. |
| L1 | Can `init-harness.sh` generate a profile-aware layout without breaking current `spell|sigil` usage? | Add optional `--profile` while preserving existing command shape. | Existing init command still works; profile files appear only when requested or inferred. |
| L2 | Can starter profiles produce useful lifecycle scenarios? | Add `spellcraft` and `sigil-development` profile templates. | Generated prompts/regimes mention the correct lifecycle owner and contract checks. |
| L3 | Can validation detect profile drift from the target lifecycle contract? | Add profile checks against target `SKILL.md` Quality Bar, Anti-Patterns, and output contract. | `validate-harness.sh` reports missing profile evidence as flag/block. |
| L4 | Can runtime adapters expose the generalized path ergonomically? | Document/adjust `experiment-harness`, `spellcraft`, and `sigil-development` command guidance. | Users can discover how to initialize profile-aware harnesses from each lifecycle surface. |
| L5 | Can Sigil Development prove the generalized harness? | Use Sigil Development to create/update one sigil experiment pack and validate it. | Test report shows generated experiment pack, validation result, gaps, and next route. |
| L6 | Can Spellcraft prove the generalized harness? | Use Spellcraft to create/update one spell experiment pack and validate it. | Test report shows generated spell experiment pack, validation result, gaps, and next route. |

## Task Breakdown

| Task | Layer | Status | Description | Write Scope | Acceptance Evidence |
| --- | --- | --- | --- | --- | --- |
| EH-GEN-001 | L0 | complete | Capture generalization design and boundary. | `development/GENERALIZATION-DESIGN.md` | Design names closed unit, lifecycle owners, and deferred complexity. |
| EH-GEN-002 | L0 | complete | Capture implementation plan and test route. | `development/GENERALIZATION-IMPLEMENTATION-PLAN.md`, `development/SIGIL-DEVELOPMENT-TEST-CASE.md` | Plan has layers, SWUs, gates, and test-case path. |
| EH-GEN-003 | L1 | complete | Extend initializer interface with optional profile argument and default inference. | `scripts/init-harness.sh`, README/SKILL docs | Backward-compatible `--type spell|sigil` remains valid; invalid profile/type combinations block. |
| EH-GEN-004 | L2 | complete | Add spell profile starter files. | `scripts/init-harness.sh`, profile templates | Spell prompts cover design, install/adapt, validate, observe/reflect. |
| EH-GEN-005 | L2 | complete | Add sigil profile starter files. | `scripts/init-harness.sh`, profile templates | Sigil prompts cover new, update, observe, reflect, harness validation. |
| EH-GEN-006 | L3 | complete | Add profile validation checks. | `scripts/validate-harness.sh`, profile templates | Validation flags or blocks missing profile metadata, lifecycle owner evidence, prompt/regime drift, or unreadable contract path. |
| EH-GEN-007 | L4 | pending | Update lifecycle surface guidance. | `README.md`, `SKILL.md`, `arcana/spellcraft/SKILL.md`, `arcana/sigil-development/SKILL.md` | Spellcraft and Sigil Development describe profile-aware harness use after behavior exists. |
| EH-GEN-008 | L5 | pending | Run Sigil Development test case. | sandbox target under `/tmp`, generated report | Report records pass/flag/block, profile validation, ownership separation, and usable evidence. |
| EH-GEN-009 | L6 | pending | Run Spellcraft test case. | toy spell target, generated report | Report records pass/flag/block, profile validation, ownership separation, and usable evidence. |

## Refreshed Execution Slices

| Slice | Tasks | Goal | Exit Check |
| --- | --- | --- | --- |
| S1 Profile-Aware Init | EH-GEN-003 | Preserve current initializer while adding profile inference and blocking rules. | `init-harness.sh <tmp> --type sigil` and `--profile sigil-development` both create valid layouts. |
| S2 Profile Starter Generation | EH-GEN-004, EH-GEN-005 | Generate prompts, regimes, fixtures, and `EXPERIMENT-PROFILE.md` from the selected profile. | Prompt/regime ids match [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md). |
| S3 Profile Validation | EH-GEN-006 | Detect profile drift before output validation. | `validate-harness.sh` reports `PROFILE_VALIDATION=pass|flag|block`. |
| S4 Lifecycle Surface Sync | EH-GEN-007 | Document the now-implemented behavior in Experiment Harness, Spellcraft, and Sigil Development. | Docs explain profile ownership without duplicating lifecycle contracts. |
| S5 Sigil Proof | EH-GEN-008 | Prove Sigil Development profile on a sandbox copy. | Sandbox test report is reviewable and does not mutate the real target. |
| S6 Spell Proof | EH-GEN-009 | Prove Spellcraft profile on a toy spell. | Toy spell report is reviewable. |

## Profile Contract

Detailed design contract: [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md).

Minimum profile fields:

```text
profile_id
artifact_type
lifecycle_owner
contract_path
scenario_pack
required_modes
prompt_set
regime_set
validation_focus
observability_focus
promotion_gate
```

The durable generated profile artifact is:

```text
development/EXPERIMENT-PROFILE.md
```

It must be created by `init-harness.sh` and contain the minimum profile fields above. Validation should treat the file as the boundary record between Experiment Harness mechanics and the lifecycle owner.

The first implementation may encode profiles in shell-generated markdown. A separate profile template directory is only needed if the shell script becomes hard to read or a third artifact family appears.

## Profile Modes

| Profile | Artifact Type | Lifecycle Owner | Required Scenarios |
| --- | --- | --- | --- |
| `generic-spell` | spell | experiment-harness with Spellcraft contract checks | low spell design, medium composition, complex lifecycle validation. |
| `spellcraft` | spell | spellcraft | design, install/adapt, validate, observe/reflect. |
| `generic-sigil` | sigil | experiment-harness with Sigil Development contract checks | low sigil run, medium update, complex reflection/promotion. |
| `sigil-development` | sigil | sigil-development | new, update, observe, reflect, harness-validation. |

Default inference:

- `--type spell` with no `--profile` infers `generic-spell`.
- `--type sigil` with no `--profile` infers `generic-sigil`.
- `--profile spellcraft` requires `--type spell`.
- `--profile sigil-development` requires `--type sigil`.
- unknown profile ids block initialization.

## Generated Scenario Files

| Profile | Prompt IDs | Regime IDs |
| --- | --- | --- |
| `generic-spell` | `spell-low`, `spell-medium`, `spell-complex` | `LIVE-SPELL-LOW-001`, `LIVE-SPELL-MEDIUM-001`, `LIVE-SPELL-COMPLEX-001` |
| `spellcraft` | `spellcraft-design-low`, `spellcraft-install-medium`, `spellcraft-validate-complex`, `spellcraft-reflect-complex` | `LIVE-SPELLCRAFT-DESIGN-001`, `LIVE-SPELLCRAFT-INSTALL-001`, `LIVE-SPELLCRAFT-VALIDATE-001`, `LIVE-SPELLCRAFT-REFLECT-001` |
| `generic-sigil` | `sigil-low`, `sigil-medium`, `sigil-complex` | `LIVE-SIGIL-LOW-001`, `LIVE-SIGIL-MEDIUM-001`, `LIVE-SIGIL-COMPLEX-001` |
| `sigil-development` | `sigil-new-low`, `sigil-update-medium`, `sigil-observe-medium`, `sigil-reflect-complex`, `sigil-harness-validation-complex` | `LIVE-SIGIL-NEW-001`, `LIVE-SIGIL-UPDATE-001`, `LIVE-SIGIL-OBSERVE-001`, `LIVE-SIGIL-REFLECT-001`, `LIVE-SIGIL-HARNESS-VALIDATION-001` |

## Validation Strategy

Deterministic checks:

- shell syntax for modified scripts,
- initializer dry run in `/tmp`,
- required generated files exist,
- `development/EXPERIMENT-PROFILE.md` exists and contains profile id, artifact type, lifecycle owner, contract path, scenario pack, and promotion gate,
- generated `.gitignore` protects outputs, runs, and loop evidence,
- generated prompts and regimes mention lifecycle owner and target contract,
- generated regime ids match the profile's `regime_set`,
- generated prompt ids match the profile's `prompt_set`,
- `validate-harness.sh` still passes existing phase gates.
- generated reports expose `PROFILE_ID`, `LIFECYCLE_OWNER`, `ARTIFACT_TYPE`, `CONTRACT_PATH`, `PROMPT_SET`, `REGIME_SET`, and `PROFILE_VALIDATION`.

Review checks:

- no profile takes ownership of artifact meaning away from Spellcraft or Sigil Development,
- prompts ask for real output bodies and reject save summaries,
- regimes include Quality Bar and Anti-Pattern criteria,
- generated harness remains portable to external repositories.

Live checks:

- run one mock loop for the generated sigil profile,
- later run real Codex loops only after explicit budget approval,
- use the Sigil Development test case before promoting the generalized path.

## Blockers And Gates

| Gate | Status | Rule |
| --- | --- | --- |
| EH-B-001 | resolved | Infer `generic-spell` or `generic-sigil` from `--type`; allow explicit `--profile` override. |
| EH-B-002 | resolved | Use `arcana/concept-layer-optimizer` as the first real sigil target after profile initialization exists; use a `/tmp` copy first if the target has unrelated dirty changes. |
| EH-B-003 | promotion gate | Approve live Codex budget before real loop runs. Mock phase gates are enough for implementation validation. |

## Open Gaps

| Gap | Severity | Owner | Resolution Route |
| --- | --- | --- | --- |
| Profile metadata must be proven on real lifecycle targets. | medium | experiment-harness + lifecycle owner | EH-GEN-008 and EH-GEN-009 run sandbox sigil and toy spell proofs. |
| Profile drift validation must be exercised beyond generated `/tmp` fixtures. | medium | experiment-harness + lifecycle owner | Use Sigil Development and Spellcraft proofs to check meaningful lifecycle contracts. |
| Generated scenario files may need refinement after real proofs. | low | experiment-harness | Treat proof findings as prompt/regime tuning inputs, not baseline implementation blockers. |
| Sigil test target may be dirty. | medium | sigil-development + experiment-harness | First test uses `/tmp` copy or explicitly approved write scope. |
| Spellcraft proof needs a target. | low | spellcraft + experiment-harness | Use a toy spell target before running against a real reusable spell. |
| Live Codex budget is not approved. | medium | lifecycle owner | Keep live loops as promotion evidence, not implementation evidence, until approval. |

## Design Gaps Filled

| Former Gap | Filled By |
| --- | --- |
| Profile metadata artifact shape was implied but not specified. | `GENERALIZATION-PROFILE-CONTRACT.md` defines `development/EXPERIMENT-PROFILE.md`. |
| CLI compatibility and profile inference were underspecified. | Profile contract defines accepted command forms and blocking rules. |
| Profile validation had no concrete pass/flag/block criteria. | Profile contract defines validation rules. |
| Generated reports did not have required profile fields. | Profile contract defines report fields. |
| First proof target risked modifying active work. | Profile contract requires sandbox copy first. |

## Implementation Order

1. Implement S1 through S3 as one bounded code pass.
2. Validate with shell syntax checks and `/tmp` initializer dry runs for `generic-sigil`, `sigil-development`, `generic-spell`, and `spellcraft`.
3. Run `validate-harness.sh` against at least one generated sigil profile layout and one generated spell profile layout.
4. Update lifecycle surface docs after behavior is proven.
5. Run the Sigil Development test case against a `/tmp` copy first.
6. Run the Spellcraft test case against a toy spell target.
7. Promote the generalized path only after both test reports are reviewable.

## Immediate Next Work

Run `EH-GEN-008` and `EH-GEN-009` from [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md) after selecting the sandbox sigil copy and toy spell target.

Minimum verification:

```bash
arcana/experiment-harness/development/run-phase-gates.sh
arcana/experiment-harness/scripts/init-harness.sh /tmp/<sandbox-sigil> --type sigil --profile sigil-development
arcana/experiment-harness/scripts/validate-harness.sh /tmp/<sandbox-sigil>
arcana/experiment-harness/scripts/init-harness.sh /tmp/<toy-spell> --type spell --profile spellcraft
arcana/experiment-harness/scripts/validate-harness.sh /tmp/<toy-spell>
```

## Observability

Each generalized harness run should report:

- profile id,
- lifecycle owner,
- target artifact,
- generated prompt and regime count,
- validation result,
- profile drift findings,
- live loop budget used,
- reflection trigger recommendation,
- next lifecycle owner.
