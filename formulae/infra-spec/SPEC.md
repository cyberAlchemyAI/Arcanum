# Infra-Spec — Capability Spec (CANDIDATE)

Authored by: `invoke define` · Date: 2026-06-10 · Status: candidate (iterate-from-here)
Lifecycle owner (next): `sigil-development` (this is invoke-authored handoff context, not a completed lifecycle).

## 1. Definition

> **infra-spec** is a YAML-first, validator-backed **evidence substrate** that binds a project's operational contract (services, environments, boundaries, secrets, gates) to its runtime evidence (receipts, signals, drift), governing promotion through typed status (`specified → implemented → deployed → observed → validated → reflected → promoted`) and typed residue, where runtime evidence never self-promotes.

## 2. Non-negotiables (inherited from research)

- Research/instance claims need concrete path evidence.
- Canonical machine-readable schemas are YAML-first and validator-backed.
- Runtime evidence cannot become promotion authority by itself.
- Analogies (Lean reflection-tower, categorical, thermodynamic) must be labelled `analogy`, never load-bearing obligations.
- `schema ≠ instance`: enums/types only in the schema; concrete values live in instances.
- `block ≠ failure`: tooling errors are `blocked`, governance violations are `block`.

## 3. Record shape (the operational-contract spine)

Required floor: `infra_spec_id, schema_version, project, status_class(=candidate), runtime_profile, environments[≥1], services[≥1], gates[≥1], residue[≥1], promotion_status`.

| Field | Meaning | Notes |
| --- | --- | --- |
| `runtime_profile.name` | `dev / single-vps / split-vps / ha` | candidate portability ladder |
| `environments[]` | named envs + deploy_trigger | — |
| `services[]` | `name, owner, deployment, dependencies, reversal` | `owner` = governance authority, NOT runtime actor |
| `boundaries[]` | `kind ∈ {network, secret, data_store, tenant, policy, environment}` + `on_violation` | reuses dispatch `boundary` shape; kind enum redefined for infra |
| `state_namespaces[]` | `source/runtime/generated/local/private/evidence` + owner + write_policy | reuses dispatch `state_namespace` as-is |
| `gates[]` | fail-closed promotion/validation gates | adopt live pipeline gate ids where possible |
| `promotion_status.stage` | 7-state ladder | enum ships; transition rules remain candidate |
| `residue[]` | typed failure/unowned/drift/missing-receipt | counterexample discipline (≥1) |
| `reversal` | rollback/migration/backup/retention | **net-new** (absent across the whole infra surface today) |
| `receipts[] / observability` | evidence hooks (R3 recomposition) | optional-but-typed; justify, never grant |
| `analogy_labels[]` | borrowed-register claims labelled `analogy` | discipline made structural |

## 4. Dispatch-spec `$def` reuse map

| dispatch `$def` | infra-spec disposition |
| --- | --- |
| `boundary` | reuse shape, **redefine `kind` enum** |
| `state_namespace` | reuse as-is |
| `promotion_split` | reuse as-is (the evidence≠authority enforcer) |
| `receipt_expectation` | reuse with infra receipt ids |
| `authority_map` | reuse with infra slots (deploy/secrets/state) |
| `gate` / `gate_action` | reuse; `gate_action` inlined for self-containment |
| `technique_ref` | n/a |

## 5. Validation surface

Two layers, `scripts/validate-infra-spec.py`:
- **shape** — JSON Schema (`infra-spec.schema.json`).
- **governance** — 5 rules (fail-closed, status-floor, reversal, unowned-state, analogy-labelling).
- Proof: `fixtures/` — `spine-pass` → exit 0; all 9 `v-*` → exit 1. Verified at authoring time.

## 6. Known residue / iteration backlog

- 7-stage ladder transition semantics: unproven for infra (enum ships, rules candidate).
- `boundary.kind` enum: candidate; each value still wants a dedicated violation fixture.
- event/queue/backpressure, runtime `actor`, populated drift: deferred out of MVP.
- minimal-twin fixtures: `v-no-rollback-on-promoted` currently also trips the status-floor; sharpen to isolate the reversal rule.
- No real instance authored yet — pilot against a representative public example.

## 7. Next route

`invoke define` (this) → `sigil-development --new` (own the infra-spec lifecycle: validate, observe, reflect, promotion-readiness) → pilot `task-session` against a representative public example → explicit Arcanum owner gate for any status promotion.
