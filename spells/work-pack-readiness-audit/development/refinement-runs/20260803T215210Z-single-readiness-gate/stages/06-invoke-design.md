# Stage 06 — Invoke Redefine / Design

## Design decision

Extend the v2 objective-execution projection with an opt-in `plan-then-admit` profile. Reuse its semantic-component architecture, but replace whole-artifact identities inside semantic components with normalized selected-value digests and remove execution-epoch material artifacts from the plan semantic digest. Keep v1 and strict v2 behavior unchanged.

## 1. Component and authority view

| Component | Owns | Must not own |
| --- | --- | --- |
| Work Pack Readiness Audit | semantic plan projection, graph/contract/receipt proof, ready frontier, manifest | selection, material production, mutation |
| Decision/selection owner | explicit choice of one ready SWU | audit proof or mutation admission |
| Material producer | selected-unit material package, baselines, and producer receipt | plan readiness or execution |
| Task Session | current selected-unit semantic drift and material admission immediately before mutation | plan authoring or material production |
| Invoke Refresh | genuine semantic plan repair and post-execution status/closeout synchronization | expected material-pending transition |

## 2. Data-contract view

Additive v2 configuration:

```json
{"admission_timing": "full-frontier|selected-unit-at-task-session"}
```

`full-frontier` preserves current behavior. The selected-unit profile emits a versioned `PlanSemanticManifest` containing:

- audit, classifier, and manifest schema versions;
- normalized selector-value digests for objective, owner, graph, declared write partitions, validation, terminal receipt, closeout contract, runtime, and risk/budget components;
- whole-artifact hashes as provenance only, not semantic identity;
- status and lifecycle receipt references in an explicitly mutable namespace outside the canonical semantic digest;
- per-unit material producer owner and declared material/write contract, but no package, producer receipt, or byte baseline in the plan semantic component;
- `plan_contract_status=pass`, `receipt_semantics_status=pass`, and per-unit `runtime_admission=pending|pass`;
- finite ready frontier;
- `selected_unit=null`, `selection_required=true`;
- `authority_effect=none`, `mutation_ready=false`;
- semantic drift policy and `next_owner=decision-gate`.

Task Session mutation admission adds one exact manifest reference and its expected canonical semantic digest. The consumer resolves current selectors, recomputes the selected semantic components, proves that the selected SWU belongs to the ready frontier, and only then evaluates the existing live material tuple.

## 3. State and event view

```text
draft
  → semantic-plan-audited/runtime-pending
  → explicitly-selected
  → material-produced
  → live-admitted
  → bounded-task-running
  → terminal-receipt
  → status/closeout synchronization
  → next explicitly-selected unit under the same semantic epoch
```

Semantic component drift returns to `draft`. Status-only closeout changes update owner receipts without invalidating the epoch. Material absence remains at `explicitly-selected`; material mismatch returns to `material-produced`.

## 4. Failure and compensation view

| Failure | Result | Recovery owner |
| --- | --- | --- |
| Graph, command, write, receipt, closeout-contract, runtime, risk, or semantic selector defect | readiness block | Invoke Plan/Refresh |
| Selected semantic value changes after manifest | Task Session block before mutation | rerun readiness on current plan |
| Whole file changes only in status/lifecycle projection | semantic epoch remains valid; current status is evaluated separately | lifecycle owner |
| Selected unit absent or not ready in current lifecycle status | selection/admission block | decision/lifecycle owner |
| Material absent | Task Session block, semantic manifest remains valid | material producer |
| Material stale or mismatched | Task Session block | material producer |
| Live admission absent or non-admit | mutation forbidden | Task Session/material owner |
| Legacy consumer | unchanged strict behavior | none |

## 5. Quality and validation view

Required fixture classes:

1. plan semantics pass with null material packages and return pending rows;
2. no material still blocks Task Session mutation;
3. exact selected material admits without a second readiness audit;
4. wrong or lifecycle-ineligible selected unit blocks;
5. graph, command, write, dependency, schema, closeout-contract, runtime, or risk semantic change blocks;
6. status-only and closeout-bookkeeping changes preserve the canonical semantic digest;
7. stale or mismatched material blocks;
8. v1 and strict v2 still block missing required material;
9. actual plan defect routes to Invoke Refresh;
10. successful plan-first projection routes to explicit selection, never directly to mutation.

## 6. Integration and versioning view

- Add a new v2-compatible manifest/profile version rather than silently changing current schemas.
- Add a canonical selected-value normalization function shared by audit generation, manifest comparison, and Task Session verification; do not duplicate the algorithm.
- Treat artifact byte digests as provenance and selector-value digests as semantic epoch identity.
- Consumers that do not understand the new profile fail closed.
- Sync generated Codex and Claude packages only from validated canonical sources.

## 7. Migration and rollout view

1. Land selected-value normalization and schema fixtures.
2. Implement plan-then-admit manifest generation behind opt-in v2 configuration.
3. Add Task Session manifest consumption and selected-unit semantic-drift checks.
4. Run audit-only, status-only-equivalence, consumer-only, and cross-capability integration fixtures.
5. Migrate the Anime.js work pack by generating one semantic manifest; later status closeouts reuse that epoch while semantics remain equal.
6. Evaluate making plan-then-admit the recommended profile only after fixture and live-package evidence.

## Design evidence ceiling

This is an authored design with planned fixtures. No canonical implementation, semantic-normalizer proof, or Task Session integration result exists yet.

## Verdict

`flag` pending the independent reviewer: the boundary is coherent, but the exact canonical selector set and lifecycle-status eligibility rule must be closed before planning can pass.
