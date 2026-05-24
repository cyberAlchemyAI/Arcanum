# Generalization Interrogation Review

Status: blockers closed where evidence is sufficient; design gaps filled into a profile contract.

## Scope

This review interrogates:

- [GENERALIZATION-DESIGN.md](GENERALIZATION-DESIGN.md)
- [GENERALIZATION-IMPLEMENTATION-PLAN.md](GENERALIZATION-IMPLEMENTATION-PLAN.md)
- [SIGIL-DEVELOPMENT-TEST-CASE.md](SIGIL-DEVELOPMENT-TEST-CASE.md)
- [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md)
- current harness scripts under `arcana/experiment-harness/scripts/`

## Verdict

Verdict: pass for design readiness; flag for implementation readiness.

The plan is coherent enough to implement the next layer. It had three named blockers, but two are design decisions that can be closed now and one is a later execution budget gate. The original design gaps are now filled by [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md); implementation remains pending.

## Closed Blockers

| Blocker | Decision | Rationale |
| --- | --- | --- |
| EH-B-001 | resolved: infer `generic-spell` or `generic-sigil` from `--type`, allow explicit `--profile` override. | Keeps current ergonomics and preserves an escape hatch for lifecycle-specific profiles. |
| EH-B-002 | resolved: use `arcana/distill` as the first real sigil target after profile initializer support exists. | It has a fresh lifecycle pack, examples, validation docs, and meaningful complexity. |
| EH-B-003 | reclassified: live Codex budget is a promotion gate, not an implementation blocker. | Mock loop validation can prove mechanics before spending live runtime budget. |

## Original Gaps Found

| Gap | Severity | Evidence | Plan Change |
| --- | --- | --- | --- |
| Missing profile metadata artifact. | high | `init-harness.sh` currently creates regimes and prompts, but no durable profile record. | Add `development/EXPERIMENT-PROFILE.md` or equivalent generated metadata. |
| Profile validation is underspecified. | high | `validate-harness.sh` checks layout, fixture pairs, outputs, reports, and contract output, but not lifecycle owner/profile drift. | Add validation checks for profile id, lifecycle owner, contract path, and regime/prompt references. |
| Regime validation does not know profiles. | medium | `validate-regime.sh` validates sections and prompt path only. | Keep regime validation generic, but have profile validation inspect generated regime content. |
| Starter scenario matrix is not concrete enough for implementation. | medium | Current plan names scenarios but does not define generated file names or required modes per profile. | Add generated profile artifacts and scenario IDs to plan. |
| Test case risks modifying a dirty real target. | medium | Current repository already has active Distill changes. | Run first proof in a copied `/tmp` target or require a clean/approved write scope before touching the real sigil. |
| Spellcraft proof comes after Sigil Development but lacks a minimal target. | low | Plan says run Spellcraft test case, but no target is named. | Add a toy spell target before real Spellcraft lifecycle proof. |
| Observability closeout is named but not wired to profile metadata. | medium | Existing reports can emit telemetry, but profile id and lifecycle owner are not required fields. | Add profile id and lifecycle owner to generalized run reports. |

## Design Gap Fill

| Gap | Filled Contract |
| --- | --- |
| Missing profile metadata artifact. | `development/EXPERIMENT-PROFILE.md` shape is defined in [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md). |
| Profile validation is underspecified. | Pass/flag/block profile validation rules are defined. |
| Regime validation does not know profiles. | Regime validation remains generic; profile validation cross-checks prompt/regime ids. |
| Starter scenario matrix is not concrete enough. | Profile prompt and regime ids are defined for `generic-spell`, `spellcraft`, `generic-sigil`, and `sigil-development`. |
| Test case risks modifying a dirty real target. | First proof boundary requires a sandbox copy before touching the real target. |
| Spellcraft proof lacks minimal target. | Plan now routes to a toy spell target before real proof. |
| Observability closeout is not wired to profile metadata. | Report fields now include profile id, lifecycle owner, artifact type, contract path, prompt set, regime set, and profile validation. |

## Remaining Implementation Gaps

| Gap | Severity | Route |
| --- | --- | --- |
| Profile metadata is specified but not generated yet. | high | EH-GEN-003 |
| Profile drift validation is specified but not implemented yet. | high | EH-GEN-006 |
| Profile scenarios are specified but not generated yet. | medium | EH-GEN-004 and EH-GEN-005 |
| Live Codex validation is not approved yet. | medium | Promotion gate after mock proof |

## Non-Gaps

- The plan should not introduce a profile plugin system yet. Two profiles are not enough pressure for a new extension framework.
- Live Codex execution should not be required before profile generation and mock loop validation work.
- Experiment Harness should not own spell or sigil lifecycle meaning. The boundary is correct.

## Revised Readiness

| Layer | Readiness | Note |
| --- | --- | --- |
| L0 | pass | Design artifacts exist and the closed unit is clear. |
| L1 | ready | Profile metadata and backward-compatible CLI parsing are specified. |
| L2 | ready | Concrete generated scenario IDs and files are specified. |
| L3 | ready | Profile drift validation rules are specified. |
| L4 | pending | Should wait until L1-L3 behavior exists. |
| L5 | pending | Should use `/tmp` copy or approved target write scope first. |
| L6 | pending | Needs toy spell target. |

## Recommended Next Action

Implement EH-GEN-003 through EH-GEN-006 in one bounded pass using [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md):

1. Add profile-aware initializer parsing.
2. Generate `development/EXPERIMENT-PROFILE.md`.
3. Generate concrete spell and sigil profile scenario files.
4. Add profile validation checks.
5. Dry-run initialization in `/tmp`.
6. Run mock loop validation on the generated sigil profile.
