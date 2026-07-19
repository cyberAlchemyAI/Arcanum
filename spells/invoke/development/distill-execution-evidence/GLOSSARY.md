# Glossary: Distill Execution Evidence

| Term | Definition | Status |
| --- | --- | --- |
| Distill execution evidence | Validator-checkable projection covering a Distill run's role, process, technique, result, and reviewed-input obligations | proposed contract |
| `DistillExecutionReceipt` | Recommended versioned projection assembled from runtime events and reviewed-input provenance | proposed architecture |
| Runtime event | Append-only record emitted by the execution boundary for a capability probe, role start/finish, reconciliation, or closeout | proposed architecture |
| True-subagent path | Proposer and Balancer execute as distinct runtime invocations when supported | existing Distill policy |
| Role-simulation path | One runtime performs explicit ordered Proposer and Balancer passes when subagents are unavailable | existing Distill fallback policy |
| Evidence validator | Deterministic component that resolves events and checks schema, semantics, provenance, and cross-artifact agreement | proposed component |
| Validation result | Validator-owned pass, flag, or block result consumed by Invoke's handoff gate | proposed component |
| Reviewed-input provenance | Evidence sufficient to identify the artifacts and content evaluated by Distill | required outcome; mechanism pending acceptance |
| Exact immutable-content identity | Digest or another reference that identifies reviewed content exactly and immutably | proposed architecture condition |
| Superseding record | New append-only result that references but does not rewrite historical evidence | proposed replay behavior |
| Mutation-capable route | Handoff to a capability that may change source, state, or governed artifacts | existing routing concept |

## Non-Collapse Rules

- A receipt is not execution proof unless the validator resolves its runtime evidence.
- A runtime event is not a verdict; the validator derives the accepted result.
- A Distill role pair is not automatically an anti-bias dispatch group.
- A superseding record does not erase or falsify the historical record.
