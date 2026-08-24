---
spell: inventory-recall-context
status: candidate-l0
updated_at: 2026-08-07
authority_effect: none
---

# Implementation Layering

## Objective

Establish the smallest explicit runtime boundary that can admit a current,
complete, safe, within-budget Inventory-derived context pack into one task—or
deny it with a source-bound receipt.

## Layers

| Layer | Question | Included build | Required exit evidence | Deferred |
| --- | --- | --- | --- | --- |
| L0 | Can one explicit turn safely return a pack handle or abstain? | pure typed gate, current-source verification, host-native coordination contract, seven fixtures, receipts | positive allows; all six negative/degraded cases deny; exact current-source bindings; no protected writes | all automation and durable behavior |
| L1 | Is repeated behavior deterministic and diagnosable? | replay identity, stable reason codes, observer receipts | repeated-run equality and useful failure signals | cache and ranking optimization |
| L2 | Do governance, privacy, and degraded modes hold across repositories? | source-scope policy fixtures, telemetry failure, boundary validation | lifecycle and privacy validation receipts | packaging/distribution |
| L3 | Is host packaging credible? | generated packages and installation validation through existing owners | separate generation, install, and promotion receipts | release/deployment |

Only L0 is prepared by this work. L1-L3 remain unselected.

## L0 decomposition

### SWU-IRC-001 — Pure fail-closed gate

Create the typed records and a standard-library Python evaluator that derives
`RecallReceipt.injectionAllowed` from already-collected child evidence. It must
not call Inventory, Context Builder, Git, the network, or any write path.

This is the narrowest trust-building unit because negative-control semantics
can be proven independently of native capability invocation.

### SWU-IRC-002 — Current-source verifier and native coordinator boundary

Extend the runtime with safe path/selector/digest checks and the explicit
coordination boundary that consumes Inventory and Context Builder result
packets. The host-native agent still invokes those skills; the deterministic
module validates their packets and decides whether the returned pack handle is
admissible.

This unit must not create a nested model-backed CLI, daemon, hook, cache, or
writeback channel.

### TASK-IRC-VERIFY — L0 closure

Replay all seven cases, compare current source and protected-path digests,
record native receipts, and reconcile the lifecycle and execution-entry state.
This is closure-only work, not a third implementation SWU.

## Recomposition proof

```text
SWU-IRC-001 gate
  + SWU-IRC-002 source verifier/native packet coordinator
  + TASK-IRC-VERIFY live replay and no-write proof
  = one bounded L0 VerifiedRecallTurn
```

The equality is a planning hypothesis until live Task Session receipts exist.

## Stop conditions

Stop and return to Spellcraft when a proposed change requires automatic
invocation, persistence, new authority resolution, external effects, private
data movement, a public/private boundary crossing, child-contract redefinition,
or a weakened negative gate.
