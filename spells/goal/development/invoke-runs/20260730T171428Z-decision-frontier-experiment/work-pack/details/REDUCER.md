# Implementation Detail: Frontier Reducer

## Purpose And Decision

Own the pure eligibility decision for every validated node. It returns the
complete projection and reasons; it does not claim, resolve, reconcile, or
write the input map.

## Inputs And Outputs

Inputs:

- validated decision map plus its SHA-256;
- zero or more active claim fixtures bound to that same digest.

Output:

```text
frontier_snapshot {
  source_digest
  nodes[id, eligible, exclusion_reasons[]]
  frontier_ids[]
}
```

## Data And State

The reducer builds read-only indexes for nodes, incoming blockers, and active
claims. Claims with a different source digest are invalid inputs, not active
claims. No store is touched.

## Algorithm

```text
verify validator receipt and exact map digest
index blocker edges by blocked_id
index current active claims by decision_id

for each node in lexical ID order:
  reasons = []
  if state != open: add "state:<state>"
  if state == fog: add "imprecise"
  if scope != in_scope: add "out_of_scope"
  if current active claim exists: add "active_claim"
  for each blocker in lexical ID order:
    if blocker.state not in {resolved, invalidated}:
      add "unresolved_blocker:<blocker_id>"
  sort and deduplicate reasons
  eligible = reasons is empty

frontier_ids = eligible node IDs in lexical order
emit canonical snapshot
```

State exclusion is evaluated before blockers, but output reasons are sorted so
iteration order cannot change bytes.

## Edge Cases And Failure Modes

- A claimed node remains `open` but is excluded with `active_claim`.
- Fog and out-of-scope nodes remain in the projection.
- An invalidated blocker no longer blocks; a superseded blocker still blocks
  unless the map explicitly resolves or invalidates it.
- A stale claim digest blocks the run instead of silently ignoring the claim.
- A graph without eligible nodes produces an empty frontier, not Way Clear.
- Any cycle receipt or source-digest mismatch blocks before projection.

## Acceptance

DFE-FIX-001 proves diamond membership and order. DFE-FIX-006 proves scope
retention. DFE-FIX-009 proves byte-identical replay. Fog and invalidated-state
fixtures are internal assertions supporting the later lifecycle witness.

