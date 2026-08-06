# Dispatch Technique Trace

| Technique | Activation | Artifact/gate effect | Validation expectation |
| --- | --- | --- | --- |
| `sequence` | Contract, producer, router, executor, and proof depend on earlier receipts. | Orders S1–S5 and all SWUs. | Every non-first step consumes a prior receipt. |
| `scu_swu_reduction` | High-complexity cross-capability change. | Eight one-behavior SWUs. | Each has one primary behavior and independent acceptance. |
| `recomposition_proof` | Split owners could hide integration gaps. | Plan Distill and final integration gate. | SWU receipts recompose into one direct-intent loop. |
| `owner_boundary_check` | Invoke, readiness audit, Router, Task Session, and outer loop have distinct authority. | Capability handoff boundaries. | No owner performs another owner's semantic work. |
| `approval_semantics_map` | Existing route approval conflates tool use with consequential effects. | Work-Pack binding versus stop-class decision. | Bound internal routes need no per-hop authorization; protected effects stop. |
| `execution_receipt_handoff` | Every owner hop must be joined. | S1–S5 receipt gates. | Missing or non-pass receipts withhold dependents. |
| `validation_loop` | Safety depends on negative route/admission cases. | Per-layer and final gates. | Existing and new fixtures pass. |
| `concrete_path_evidence` | Dirty repository and generated packages require exact scope. | SWU write scopes and validation. | No glob-derived mutation or silent overlap. |
| `artifact_contract_bridge` | Plan fields must be executable by runtime consumers. | Execution-entry schema and cross-capability fixture. | Producer/consumer schema parity passes. |
| `residue_ledger` | Default adoption and unrelated dirty changes remain separate. | Work Pack blockers and closeout. | Residue stays named and cannot become completion. |
| `observability_grouping` | One outer run contains several owner/unit receipts. | Dispatch/run correlation fields. | Trace keeps dispatch, binding, owner hop, task, and SWU identities. |

## Skipped techniques

- `fanout`, `tournament`, and `dialectic`: implementation dependencies are
  serial; parallel lifecycle work would add joins without shortening the
  critical path.
- `route_menu`: tool/owner selection is mechanical inside the Work Pack; a menu
  would recreate the authorization ceremony being removed.
- `memory_loop`: current canonical sources and local implementation evidence are
  sufficient; no knowledge promotion is requested.
- `protected_action_mapping`: protected effects are stop classes, not actions
  this dispatch performs.

## Full dispatch

Required because implementation crosses Spellcraft, Sigil Development, Task
Session, and generated-package boundaries. See
`work-pack-execution-grant.dispatch.json`.

