# Dispatch Technique Trace

## Route

```text
Context Builder frame
  -> Invoke Define
  -> Invoke Design
  -> deterministic Design validation
  -> Invoke Plan
  -> Distill validation
  -> Sigil Development handoff
```

Canonical machine document:
[INVOKE-DISPATCH.json](INVOKE-DISPATCH.json).

## Three Dispatch Dispositions

| Disposition | Result | Evidence |
| --- | --- | --- |
| Proposal | sequence selected; no fan-out or reusable Spell proposed | one target, ordered lifecycle gates, no independent mutation lanes |
| Structural validation | pass with zero blocks and zero flags | Dispatch schema, technique catalog, capability refs, gates, and boundaries |
| Execution | not authorized | no subagent dispatch, no selected SWU, no canonical target mutation |

## Technique-to-Contract Mapping

| Technique | Concrete Use | Evidence Or Gate |
| --- | --- | --- |
| sequence | every stage consumes a prior artifact, frame, or receipt | step dependencies s1 through s7 |
| frame_handoff | bounded selector-level evidence enters Define | `CONTEXT-PACK.md` and `CONTEXT-INDEX.json` |
| handle_handoff | stages consume artifact refs rather than copied owner state | Define and Design transports |
| residue_ledger | rejected scope and unproven claims keep an owner | `DECISIONS-AND-GAPS.md`, shared gaps |
| scu_swu_reduction | eight task-shaped concerns reduced to bounded behaviors | atomicity table and task split analyses |
| recomposition_proof | SWUs cover the Define requirements and Design rules | shared traceability |
| validation_loop | Design fixed point, Plan Distill, fixtures, and closeout | gates g-design, g-distill, and task evidence |
| concrete_path_evidence | every mutation and receipt path is explicit | task-local exact write scopes |
| artifact_contract_bridge | architecture witnesses become task acceptance evidence | validation strategy and SWU mappings |
| execution_receipt_handoff | Task Session returns baseline-bound source receipt | shared and task-local closeout contracts |
| authority_split_gate | authoring, execution, evidence, and lifecycle owners differ | boundary authority map and gate g-lifecycle |
| state_namespace_boundary | public canonical, plan/evidence, and consumer cache are separate | boundary state namespaces |
| owner_boundary_check | Invoke stops at Sigil Development handoff | step s7 and Plan transport |
| observability_grouping | Invoke parent and Distill child share dispatch identity | observability contract |

## Delegation Disposition

- Subagent strategy: none
- Reason: the route is serial, repository policy requires user confirmation
  before subagent dispatch, and no independent implementation lane was
  authorized.
- Orchestrate execution: not needed; no capability-bound delegated worker was
  spawned.
- Subagent lifecycle receipt: none

## Validation Expectation

The deterministic Dispatch validator returned `pass` with zero blocks and zero
flags. A structurally passing dispatch remains non-executing until one SWU is
separately selected.
