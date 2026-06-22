# Iteration And Stop Policy

## Iteration Policy

1. Start with `handoff-pack.md` and `handoff-index.json`.
2. Validate source/design/plan recomposition.
3. Record pass, flag, or block.
4. If blocked, stop and report blockers, residue, and reroute.
5. If flagged, name every gap, owner, and repair path.
6. If passed, state that the next selectable unit is a later runtime SWU, not an
   automatic continuation.

## Stop Conditions

Stop blocked when:

- lifecycle owner authority is unclear,
- public/private boundary is unclear or violated,
- generated-surface boundary is unclear or violated,
- schema home decision blocks validation,
- Craft source-state sync would require active mutation,
- validation evidence is insufficient,
- runtime implementation would be required to complete this SWU.

## Blocked Report Rule

The blocked report must include:

- `swu_id`,
- blocked reason,
- evidence inspected,
- blocker owner,
- exact unblock action,
- next route.
