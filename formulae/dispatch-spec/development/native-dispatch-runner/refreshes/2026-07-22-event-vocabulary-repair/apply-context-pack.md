# Apply Context Pack — Event Vocabulary Repair Refresh

Mutation mode: apply-approved

## Apply obligations

1. Apply only the nine targets named in `apply-authorization.json`.
2. Preserve the blocked canary result, validator receipt, and Task Session receipt byte-for-byte.
3. Preserve SWU-NDR-010 historical PASS and add a new repair SWU.
4. Record SWU-NDR-011 attempt 1 as BLOCK.
5. Make SWU-NDR-010R the only next executable unit.
6. Keep SWU-NDR-012 locked until the append-only failure retry passes.
7. Keep retry writes under `failure/retry-001/`.
8. Validate manifest dependencies, route dispatch, artifact consistency, and public boundary.

## Pre-apply gate

- Explicit approval: present.
- Proposal dispatch: PASS with zero blocks and flags.
- Target hashes: 9/9 match the reviewed proposal.
- Blocked evidence hashes: 3/3 match the proposal.
- Source obligation coverage: 12/12.
- Inventory: lookup-only `no_inventory_match`; no authority contribution.

Strict coverage: PASS.
