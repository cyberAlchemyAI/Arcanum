# Implementation Detail: Control Boundaries

## Purpose And Decisions

Define three separately executable decisions:

1. whether a selected node requires a hard human stop;
2. whether the decision route is actually clear;
3. whether decision closure changed any execution state.

## Shared Inputs And Outputs

Inputs are validated frontier/map receipts, decision-resolution evidence, and a
synthetic execution-state snapshot. Outputs are separate HITL, Way Clear, or
non-collapse receipts. None is accepted as an execution receipt.

## SWU-DFE-005 Algorithm: HITL

```text
read selected frontier node and source digest
if route != HITL: emit NOT_HITL and no human-stop receipt
require human owner
emit route receipt {decision_id, source_digest, owner, status: awaiting_human}
assert no resolution or reconciliation output exists
stop
```

Failures: missing owner, stale digest, non-eligible node, synthesized answer,
or any downstream proposal. DFE-FIX-011 includes the auto-resolution mutant.

## SWU-DFE-006 Algorithm: Way Clear

```text
validate map and source digest
remaining = nodes where scope == in_scope and state in {open, fog}
if remaining is not empty:
  emit blocked receipt with lexical remaining IDs and stable reasons
else:
  emit Way Clear receipt bound to source digest
```

An actively claimed `open` node still prevents Way Clear. Out-of-scope,
resolved, invalidated, and superseded nodes remain in history but do not block.
An empty frontier is insufficient when fog remains. DFE-FIX-012 covers clear,
open-decision, and fog cases.

## SWU-DFE-007 Algorithm: Non-Collapse

```text
canonicalize execution-state fixture; record before bytes and SHA-256
load decision resolution, reconciliation, and optional Way Clear receipts
store those receipts only in decision-evidence namespace
re-read execution-state fixture
require byte-for-byte equality and identical SHA-256
reject any task, SWU, or Goal execution status delta
```

The harness has no function that maps a decision status to an execution status.
DFE-FIX-008 includes a mutant attempting to mark an SWU complete and requires
rejection.

## State And Ordering

HITL may run after reconciliation behavior exists but stops before a
resolution. Way Clear consumes a later map independently. Non-collapse runs
after both receipt forms exist and observes them without applying them. The
three SWUs are serial for evidence custody, not because their acceptance
boundaries are merged.

## Validation Evidence

Each SWU writes its own baseline, validation result, terminal receipt, and
Spellcraft owner receipt. A pass in one SWU cannot compensate for a failure in
another.

