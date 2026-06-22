---
artifact_id: GOAL-CONTRACTS-001
artifact_type: invoke-design-contracts
target: arcanum/spells/goal
status: draft
created_at: 2026-06-20
---

# Goal Spell Contracts

## Contract Authority

The source spell contract remains `arcanum/spells/goal/README.md`. This file
breaks that source contract into implementation-facing design contracts for
later Spellcraft, Task Session, and Experiment Harness work.

## Contract Matrix

| Contract | Owner | Inputs | Outputs | Pass | Block |
| --- | --- | --- | --- | --- | --- |
| Source authority contract | `goal` | Goal intent, candidate scope. | Bound source authority. | One source authority is selected. | Scope ambiguous or source unreadable. |
| Frontier contract | `goal` + `craft` | Bound source authority. | Frontier snapshot. | Snapshot contains nodes, blockers, gaps, and source ref. | Snapshot cannot be read safely. |
| Risk contract | `goal` | Frontier node, decision policy. | Risk tier. | Every node has tier. | Tier missing or protected operation lacks approval. |
| Route contract | `goal` + `dispatch-spec` | Node, risk tier, owner map. | Dispatch route. | Owner, technique, receipt, and fallback validate. | Route invalid or owner boundary unclear. |
| Execution contract | Delegated owner | Dispatch route. | Execution receipt. | Receipt is terminal and evidence-backed. | Lane remains open, hidden, or unjoined. |
| Audit contract | `goal` + reviewer | Receipt and done criteria. | Audit verdict. | Evidence satisfies done criteria and no veto. | Veto, missing evidence, or contradiction. |
| Staging contract | `goal` | Accepted source-changing progress. | Staged delta. | Delta has framed diff and validation expectation. | Direct active mutation or malformed delta. |
| Approval contract | `decision-gate` + user | Staged batch. | Approval token or deferral. | Batch-specific approval token and durable record exist. | Missing, ambient, or mismatched approval. |
| Promotion contract | `craft` | Approved batch. | Applied source update or validation block. | Apply validates through source owner. | Apply fails validation or partial apply risk exists. |
| Telemetry contract | Observability capabilities | Round and final result state. | Spell signal. | Signal recorded or skipped reason reported. | Missing telemetry silently hidden. |
| Promotion-readiness contract | `experiment-harness` + `spellcraft` | Reusable validation scenarios. | Promotion evidence. | Fail-closed behavior is proven. | Runtime success used as promotion evidence. |

## Output Contracts

### Goal Loop Result

The final result must report:

- spell id,
- goal intent,
- result status,
- rounds,
- decision profile reference or neutral default,
- frontier start/end,
- risk tier counts,
- dispatch count,
- audit verdict counts,
- staged deltas,
- promoted batches,
- stop reason,
- budget use,
- gap discovery summary,
- subagent closeout summary,
- telemetry state,
- extra sources,
- next route.

### Execution Receipt

A delegated owner receipt must report:

- owner id,
- route id,
- node id,
- status,
- evidence,
- files touched when applicable,
- validation,
- residue,
- reroute,
- terminal closeout state.

### Staged Delta

A staged delta must report:

- delta id,
- source authority,
- target,
- operation,
- proposed change,
- framed diff,
- validation expectation,
- promotion state,
- created by receipt id.

### Approval Token

An approval token must report:

- token id,
- batch id,
- approver or approval source,
- decision record reference,
- approval state,
- scope,
- expiration or reuse policy.

## Boundary Contracts

| Boundary | Contract |
| --- | --- |
| Public/private | Public files may include schema and neutral defaults only. Filled profile data stays outside the public package. |
| Generated surfaces | Generated host runtime files are produced by the runtime installer, not hand-authored. |
| Parent repo | Parent gitlinks move only after submodule commit/push and explicit publication request. |
| Delegated owners | `goal` composes owner capabilities but does not redefine their internal contracts. |
| Promotion | Experiment Harness evidence is required before draft status can promote. |

## Contract Drift Checks

| Check | Evidence |
| --- | --- |
| README and this contract file agree on source authority. | `README.md` Local Customization and Contract Authority above. |
| Rule IDs align with contract matrix. | `RULES.md` and Contract Matrix. |
| Schema files cover handoff artifacts. | `SCHEMAS.md` and `schemas/*.schema.json`. |
| Public boundary remains intact. | Public-boundary scan in `INVOKE-RESULT.md`. |

## Next Route

`spellcraft validate` should accept, reject, or refine this contract bundle
before any runtime SWU implements it.
