# Implementation Detail: Digest-Bound Claim

## Purpose And Decision

Own the single-process compare-and-set decision for one frontier node. A claim
prevents duplicate resolution work but never changes the decision state.

## Inputs And Outputs

Inputs:

- validated frontier snapshot;
- `claim_request {decision_id, source_digest, owner, expected_store_digest}`;
- current claim-store bytes or an explicitly absent store.

Outputs:

- accepted canonical claim record plus claim receipt; or
- rejection receipt with one stable code and unchanged store hash.

## Data And State

Claim record:

```text
claim_id
decision_id
source_digest
owner
claimed_at
status = active
previous_store_digest
```

The fixture claim store is non-authoritative. `claimed_at` is supplied by the
harness so replay remains deterministic.

## Algorithm

```text
validate frontier and request schemas
canonicalize current store; compute actual_store_digest

if request.source_digest != frontier.source_digest:
  reject STALE_SOURCE
if request.expected_store_digest != actual_store_digest:
  reject CAS_MISMATCH
if decision_id absent from frontier:
  reject UNKNOWN_DECISION
if frontier node eligible != true:
  reject NOT_ELIGIBLE
if active claim exists for decision_id and source_digest:
  reject ACTIVE_CLAIM

construct claim record from supplied deterministic fields
write sibling temporary file
fsync and atomically replace fixture store
emit accepted receipt with before/after hashes
```

Rejection precedence is stale source, CAS mismatch, unknown decision,
eligibility, then competing claim. Every rejection records the unchanged store
hash.

## Edge Cases And Failure Modes

- Two requests with the same expected digest: only the first replacement can
  pass; the second observes `CAS_MISMATCH`.
- Same decision under an old map digest is stale, not reusable.
- Claims for fog, out-of-scope, invalidated, or blocked nodes reject.
- Claim expiry, abandonment recovery, and multi-process locking are explicitly
  unsupported and must not be simulated as passing behavior.
- Interrupted temporary writes never replace the current store.

## Acceptance

DFE-FIX-002 proves current active-claim exclusion and competing rejection.
DFE-FIX-004 proves stale source rejection. Fixtures must bind before/after
store hashes and show no decision-map delta.

