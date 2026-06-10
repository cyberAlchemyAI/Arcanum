# Infra-Spec MVP Fixtures — Falsification Surface

Candidate schema: `../infra-spec.schema.json` (self-contained Draft 2020-12).
Two-layer discipline (from dispatch-spec): **shape** layer = JSON Schema; **governance** layer = `../scripts/validate-infra-spec.py` (now BUILT). Both layers are exercised.

Exit-code matrix (`validate-infra-spec.py` over each fixture): `spine-pass` → exit 0; every `v-*` → exit 1. Verified at package authoring (`invoke define`, 2026-06-10) — **ALL FIXTURES MATCH**. The 3 governance fixtures now block via governance rules, not just shape.

| Fixture | Layer | Falsifies | Expected shape verdict | Result |
| --- | --- | --- | --- | --- |
| `spine-pass.json` | baseline | — (valid spine) | PASS | ✅ pass |
| `v-bad-runtime-profile.json` | shape | runtime_profile enum | FAIL | ✅ fail |
| `v-boundary-enum-leak.json` | shape | dispatch capability enum leaked into infra boundary.kind | FAIL | ✅ fail |
| `v-collapsed-status.json` | shape | collapsed bare `status` (namespacing) | FAIL | ✅ fail |
| `v-empty-environments.json` | shape | environments ≥1 | FAIL | ✅ fail |
| `v-empty-residue.json` | shape | residue ≥1 (counterexample discipline) | FAIL | ✅ fail |
| `v-missing-owner.json` | shape | service.owner required | FAIL | ✅ fail |
| `v-no-rollback-on-promoted.json` | governance | promoted without `reversal.rollback` (N12, gap G5) | shape PASS → needs script | ✅ shape-pass |
| `v-self-promoting-gate.json` | governance | promotion_guardrail `on_fail: flag` (evidence self-promotes, N11) | shape PASS → needs script | ✅ shape-pass |
| `v-status-floor.json` | governance | stage `validated` with no receipt/observability evidence (N5) | shape PASS → needs script | ✅ shape-pass |

## Governance rules enforced by `validate-infra-spec.py`
1. fail-closed gate: any `promotion_guardrail` (and `secret`/`data_store` boundary) must have `on_fail`/`on_violation: block`.
2. status-floor: `stage ≥ deployed` requires a matching receipt; `≥ validated` requires observability/SLO evidence; evidence_refs justify, never grant.
3. reversal obligation: `stage: promoted` (or a production env) requires `reversal.rollback`; every `data_store` boundary requires `reversal.backup`; every `migration.forward` requires `migration.reverse`.
4. unowned-state: every declared state path / `data_store` must appear in `state_namespaces` with exactly one owner.
5. analogy-labeling: borrowed-register vocabulary in free-text obligations requires an `analogy_labels[]` entry.
Tooling errors surface as `VALIDATION=blocked`, distinct from governance `block`.
