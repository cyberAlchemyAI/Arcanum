# Implementation Detail: Resolution Reconciliation

## Purpose And Decision

Own validation of one resolution receipt and construction of an immutable,
causal graph-change proposal. It never applies the proposal to Craft or the
input fixture.

## Inputs And Outputs

Inputs:

- validated decision map and digest;
- active claim record;
- resolution receipt with decision ID, owner, route, source digest, and typed
  ordered actions.

Output:

```text
reconciliation_proposal {
  authority: proposal
  source_digest
  claim_id
  resolution_id
  actions[sequence, action_id, kind, target, payload]
  proposed_map_digest
}
```

## Data And State

Actions are closed variants:

- `add`: introduce a unique precise node;
- `graduate_fog`: propose `fog -> open` with a precise question and owner;
- `invalidate`: propose a retained terminal disposition;
- `supersede`: retain the old node and name its replacement;
- `unblock`: remove one edge only after its blocker is resolved or invalidated.

The input map is immutable. A staged in-memory copy exists solely to validate
the whole proposal and calculate `proposed_map_digest`.

## Algorithm

```text
validate map, claim, and resolution schemas
require matching source_digest, decision_id, owner, route, and active claim
require unique action_id and contiguous sequence starting at 0
staged = deep copy of map

for action in sequence order:
  add:
    reject existing ID; require precise question, route, owner, in-scope state
    stage node
  graduate_fog:
    require target.state == fog and precise question plus owner
    stage target.state = open and supplied fields
  invalidate:
    require target exists and is not already terminal
    stage state = invalidated; retain node and reason
  supersede:
    require target exists; replacement exists or was added earlier
    stage state = superseded; retain replacement reference
  unblock:
    require exact edge exists
    require blocker staged state in {resolved, invalidated}
    stage removal of exact edge

revalidate staged graph and schema
emit canonical proposal and staged digest
assert original map digest still matches source_digest
```

No implicit downstream edits are inferred. Every change requires a typed
action and causal reference.

## Edge Cases And Failure Modes

- Action order may matter; sequence is explicit and part of the receipt.
- A supersede action cannot reference a replacement added later.
- Invalidating an already resolved or invalidated node blocks.
- Unblocking an unresolved blocker blocks.
- A staged action that creates a cycle blocks the entire proposal.
- Any owner/route/digest mismatch blocks before action evaluation.
- Partial proposals are never emitted.

## Acceptance

DFE-FIX-005 proves fog is initially excluded and graduates only with a precise
question and owner. DFE-FIX-007 proves add, invalidate, supersede, and unblock
variants, retained history, causal references, staged validity, and unchanged
input bytes.

