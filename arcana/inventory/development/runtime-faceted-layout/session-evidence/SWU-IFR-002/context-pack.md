# Context Pack: SWU-IFR-002

## Selection

- selected unit: `SWU-IFR-002`
- layer: L1
- behavior: complete no-write append transition
- dependency: passing `SWU-IFR-001` receipt
- execution owner: Task Session

## Bound Inputs

| Source | SHA-256 |
| --- | --- |
| `WORK-PACK.md` | `6a407763988be3ddece458c04aebcfe1206c74ea55432034b7032fb343dcb75e` |
| `tasks/SWU-IFR-002.md` | `c30c61795bd5db5a429dbdd542430d84438f986e6d3efe7479023e87c8813192` |
| `lib/operation-receipt.cjs` | `97800a5ae5d7c2e3aac0dadcbadb8e46e402aca9f3608b5a32d93d665aef70cf` |
| `schemas/inventory.operation-receipt.v1.schema.json` | `170397094542d9017223f4f539810f5ee4ec2dc692493eb29a1e1827aacdadfb` |
| `scripts/validate-index-json.sh` | `c62ff1ad3e40660f73aa6bfd25f6570763a2c6fc88b73e6c3582ea537b54849c` |
| `scripts/validate_projection_conformance.py` | `b4b98a422b895f512bc2b95b79ac4b3bc381ab70374489ba7b0bde40ac65a2da` |
| accepted updater baseline | `c76c3f9a9b884c3d5f9166889bd527cd565c5d453b63817dab130fe26a8eb629` |

## Exact Implementation Write Scope

```text
arcana/inventory/bin/inventory
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/test/append-dry-run.test.cjs
arcana/inventory/test/fixtures/append-dry-run/
```

No implementation file in this scope was mutated.

## Obligations

1. Emit one deterministic canonical receipt for every failure-precedence state.
2. Resolve helpers package-relatively from an unrelated caller working
   directory.
3. Prove consumer `index.json` and `index.md` bytes are unchanged.
4. Preserve exact causal evidence; never invent a digest for an unavailable
   artifact.
5. Keep all apply writes and generated runtime mutation excluded.

## Blocking Contract Contradiction

The required L1 state machine and the accepted L0 receipt schema cannot
recompose:

| Required terminal state | Fact that may not exist | L0 field that requires it |
| --- | --- | --- |
| `tooling-unavailable` | missing helper bytes and complete bundle | `runtime.helpers[].sha256`, `runtime.bundle_sha256` |
| `invalid-request` | readable record bytes or normalized record | `inputs.record_sha256`, `inputs.normalized_record_sha256` |
| `baseline-blocked` before request validation | normalized record and staged candidate | normalized digest plus every `candidate` field |
| pre-candidate block | candidate index, human index, and report | three mandatory candidate digests |

The schema admits only lowercase 64-byte SHA-256 values for those fields and
the kernel rejects missing fields. Sentinel hashes would be false evidence,
while omitting fields would fail the normative schema.

## Gate Result

- context readiness: blocked
- scope safety: blocked
- implementation mutation: forbidden
- blocker owner: Sigil Development / receipt-contract lifecycle
- required repair: make evidence availability explicit, then revalidate L0 and
  reselect L1
