# Define: Distill Execution Evidence

## Intent

Prevent Invoke from routing mutation-capable work from an authored Distill verdict alone.
An applicable Distill run must instead produce validator-checkable evidence that covers the
current Distill output contract and binds the result to the reviewed inputs and downstream
Invoke result.

## Problem Statement

Invoke currently asks for Distill but can preserve only `pass`, `flag`, or `block` text.
Its fixture runner can accept that text without proving finite role execution, categorized
objections, reconciliation, technique traces, or agreement with the work-pack. This makes a
correctly named call observationally indistinguishable from a fabricated label.

## Delivery Boundary

Included:

- a proposed execution-evidence contract for true-subagent and role-simulation paths;
- runtime-owned append-only event references;
- semantic, provenance, and cross-artifact validation;
- Invoke mode capability and evidence projection rules;
- adversarial fixtures;
- generated mirror synchronization after canonical acceptance;
- Workbench replay and a superseding evidence record.

Excluded:

- implementing deferred Invoke `full` or `validate` modes;
- changing Distill's true-subagent/fallback role policy;
- blanket anti-bias composition for every Invoke or Distill use;
- rewriting historical observability records;
- claiming the eleven-SWU Workbench decomposition is invalid;
- placing private authority prose in public Arcanum artifacts.

## Actors And Owners

| Actor | Responsibility | Authority Limit |
| --- | --- | --- |
| Invoke | Request Distill, assemble evidence handles, consume validator result | Cannot self-assert execution proof |
| Distill runtime adapter | Execute or label role passes and emit runtime events | Cannot approve Invoke handoff |
| Evidence assembler | Build a receipt projection from events and reviewed inputs | Cannot decide semantic validity |
| Evidence validator | Resolve events and evaluate semantic/provenance consistency | Cannot mutate reviewed artifacts |
| Spellcraft | Accept and revise Invoke spell contracts | Does not execute Workbench tasks |
| Sigil Development | Own any Distill lifecycle revision | Does not own Invoke mode composition |
| Task Session | Execute one accepted SWU | Cannot waive lifecycle or validation gates |

## Functional Requirements

1. Every applicable Distill run records parent Invoke identity, mode, finite budget, rounds,
   termination, role execution path, role trace, techniques, objections, reconciliation,
   verdict, gaps, recomposition status, and next route.
2. True-subagent evidence resolves distinct Proposer and Balancer runtime invocations.
3. Role simulation records a capability probe and ordered labeled role-pass events without
   invented native-agent identities.
4. The validator resolves runtime events for both paths and rejects fields that merely claim
   execution.
5. The validator checks reviewed-input provenance, role separation, round accounting,
   objection/reconciliation completeness, technique activation/skips, and cross-artifact
   verdict/count agreement.
6. Only the validator result can unlock mutation-capable routing.
7. `flag` requires named owners and repair paths; `block` and invalid evidence cannot unlock
   mutation.
8. Active Invoke modes project common evidence fields; deferred modes return
   `unsupported/deferred` before lifecycle processing.
9. Workbench replay preserves historical evidence and appends a superseding record.

## Non-Functional Requirements

- Fail closed on missing, stale, unresolved, or inconsistent evidence.
- Preserve append-only historical evidence.
- Keep the evidence projection serialization-independent at the contract level.
- Make deterministic validation runnable without a model.
- Preserve public/private boundaries during canonical and generated synchronization.
- Keep anti-bias composition bounded to qualifying governed multi-agent subject groups.

## Acceptance-Critical Decision

`DEC-DEE-001`: Spellcraft must accept, narrow, or reject the proposed versioned
`DistillExecutionReceipt` plus runtime-event architecture. Exact immutable-content identity
is a requirement of that proposed architecture only after lifecycle acceptance; before
acceptance, current law requires reviewed-input provenance sufficient for the accepted
validator design.

## Define Gate

**PASS for design authoring.** The target, boundaries, owners, requirements, exclusions, and
acceptance-critical decision are explicit. This is not implementation readiness.
