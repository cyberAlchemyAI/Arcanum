# Shared Execution Control

## Common Task Session contract

Applies to `SWU-TSGR-001` through `SWU-TSGR-010`.

### Canonical receipt digest

For all planning receipt schemas in this package, calculate `receipt_digest` as
lowercase SHA-256 over this exact preimage:

1. remove the top-level `receipt_digest` member;
2. serialize the remaining JSON as UTF-8;
3. sort every object key lexicographically;
4. preserve array order;
5. emit no insignificant whitespace;
6. escape only characters required by JSON;
7. emit no trailing newline.

Receipts in these schemas contain no non-integer JSON numbers, so numeric
cross-runtime normalization is not an open input. A validator must recompute this
preimage and reject mismatch.

- Execution limit: one selected SWU.
- Terminal source receipt:
  `work-pack/results/<SWU-ID>-RESULT.json`.
- Terminal source receipt schema:
  `schemas/task-session-swu-result.schema.json`,
  SHA-256 `c865ecf1ab020c7763f39a24b8b450e6947d78b91be126ca2bf29d38e53bf3c6`.
- The receipt must include SWU ID, result, files touched, validation command/results,
  acceptance evidence, blockers, residue, and handoff note.
- Planning synchronization route:
  `invoke:refresh:apply-approved`.
- Allowed planning delta classes:
  `evidence_added`, `blocker_opened`, `blocker_resolved`, `status_changed`,
  `route_changed`.
- Forbidden closeout scopes: implementation, next-task execution, authority,
  promotion, publication, deployment, destructive cleanup, policy acceptance,
  risk acceptance, and unrelated target.
- Expected Continuation Router join receipt:
  `work-pack/closeout/<SWU-ID>-CONTINUATION-OWNER-RECEIPT.json`.
- Continuation join receipt schema:
  `schemas/continuation-closeout-receipt.schema.json`,
  SHA-256 `7069cc3e17763c4993c0e0856f545cdbe106ba85dd0eb8380f05f9198a17e770`.
- Nested Invoke owner receipt schema:
  `schemas/invoke-refresh-owner-receipt.schema.json`,
  SHA-256 `13c232d477067477417544b9e4a4bf841c4887b10d852f49ee3dfecf7347fa1a`.
- The nested material package evidence must also validate against
  `spells/invoke/schemas/material-package-receipt.schema.json`,
  SHA-256 `2c4ef7c0529f419278a3af530783383d05ccf8e144a40e895f26c2c2d6b77b6b`.
- Owner results admitted: `pass` or `no-op`.
- Successor: at most the unique next dependency-satisfied SWU; never execute it.

## Declared planning target inventory

For every SWU closeout:

1. `WORK-PACK.md`;
2. the parent `work-pack/tasks/TASK-*.md`;
3. the current `work-pack/waves/W*.md`;
4. `CONTINUATION.json`.

The terminal source receipt is an immutable input, not an Invoke mutation target.
These planning-owned schemas exist before TSGR-001, so its closeout preflight does
not depend on the runner envelope schemas created by TSGR-002.

## Baseline rule

Immediately before mutation admission, capture SHA-256 for every implementation
write target and every planning closeout target. For a new path, bind an explicit
`absent` identity. If any target changes between capture and use:

- exact staged output already present may be classified
  `already-present-exact-output`;
- every other delta is `conflict` and blocks.

This dynamic preflight rule is necessary because earlier sequential SWUs legitimately
change shared runner and work-pack files. A digest copied from Invoke authoring time
would be stale by design.

## Current dirty-state rule

The live Task Session package contains pre-existing edits. A later SWU may touch an
already-dirty file only when its context pack:

1. records the current digest and diff selector;
2. proves the SWU's intended hunk does not discard the pending contract;
3. declares the merged postimage digest;
4. blocks if the live file changes again before application.

No SWU may normalize unrelated dirty files.

## Closeout validation

Run from this Invoke run directory:

```text
python3 validate-plan-package.py .
python3 -m json.tool CONTINUATION.json
```

Then run the SWU's product validation. Closeout blocks if the work-pack, task, wave,
or cursor disagrees.

## Execution-owner handoff shape

```yaml
swu_id: <exact SWU>
parent_task: <task>
objective: <one behavior>
write_scope: <exact paths>
dependencies: <accepted receipts>
done_criteria: <verifiable outcomes>
validation: <exact commands>
source_contracts: <paths and selectors>
known_blockers: <ids or none>
expected_return:
  result: pass | flag | block | interrupted
  files_touched: []
  validation: []
  blockers: []
  handoff_note: ""
```
