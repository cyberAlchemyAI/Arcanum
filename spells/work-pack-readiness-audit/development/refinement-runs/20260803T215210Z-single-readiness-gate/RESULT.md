# Refine Result — Single readiness gate

## Outcome

The repeated pre-execution cycle is not necessary. The refined architecture uses:

```text
semantic plan audit once
  → explicit selected-unit receipt
  → selected-unit material production
  → single-use live Task Session admission
  → bounded mutation
  → existing post-execution Invoke Refresh closeout
```

Readiness is repeated only when immutable plan semantics change—not because material was intentionally absent during planning, later became available, or a prior SWU updated status/closeout evidence.

## Critical correction from review

A whole-file readiness receipt was rejected. Work Pack and handoff bytes legitimately change during closeout, so whole-file hashing would recreate the rerun problem. The repaired design instead uses normalized selector-value semantic digests and keeps lifecycle/status receipts outside the immutable plan epoch.

The independent reviewer also required:

- a per-unit semantic contract digest;
- explicit selection bound to the audited frontier and current dependencies;
- task/SWU/epoch/unit/attempt identity through every material and admission artifact;
- live target baseline hashes immediately before mutation;
- the full normalized command, write, receipt, closeout, owner, authority, and publication contract;
- a single-use admission receipt required by every mutating adapter and repeated in the terminal receipt.

All requirements are incorporated into the repaired design and Plan. They are planned, not implemented.

## Status

- Context baseline: `pass`
- Invoke Define: `pass`
- Initial design review: `block`
- Distill Repair: `pass`
- Invoke Plan and Plan Distill: `pass`
- Final Refine verdict: `pass`
- Evidence ceiling: `authored-repaired-plan`
- Selected SWU: none
- Mutation ready: false
- Canonical source changes: none
- Generated mirror changes: none

## Primary artifacts

- Definition: `stages/02-invoke-define.md`
- Independent critic: `stages/07-admission-boundary-critic.json`
- Repaired contract: `stages/08-single-gate-contract.json`
- Repair proof: `stages/08-distill-repair.md`
- Implementation layering: `stages/09-implementation-layering.md`
- Work Pack: `stages/09-work-pack.md`
- Execution Pack: `stages/09-execution-pack.md`
- Plan validation: `stages/09-plan-distill-validation.md`

## Next route

Route the Work Pack through `spellcraft` and explicitly select `SWU-SRG-001`, the manifest schema, as the smallest reversible trust-building unit. After the audit producer is proven, route the Task Session consumer changes through `sigil-development`. Do not begin a project Task Session from this Refine receipt.
