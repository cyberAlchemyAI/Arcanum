# SWU-IFR-001: Canonical Receipt Kernel

## Behavior

Produce one schema-valid, byte-reproducible operation receipt from canonical
inputs without reading or writing Inventory state.

## Inputs And Outputs

- Input: structured receipt body without `receipt_sha256`, explicit timestamp,
  and exact input/helper digests.
- Output: canonical UTF-8 JSON plus newline, operation fingerprint, receipt
  SHA-256, and schema validation result.

## Algorithm

1. Reject unknown or missing required fields.
2. Normalize objects and contract-ordered arrays deterministically.
3. Serialize without implicit wall-clock values.
4. Compute the operation fingerprint from canonical operation inputs.
5. Compute the receipt digest without self-inclusion, insert it, and serialize.
6. Repeat identical inputs and require byte identity.

## Exact Write Scope

```text
arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json
arcana/inventory/lib/operation-receipt.cjs
arcana/inventory/test/operation-receipt.test.cjs
```

No existing source, CLI, generated runtime, or consumer Inventory file is in
scope.

## Done

- normative receipt validates;
- missing/unknown fields and invalid digests fail;
- identical inputs produce byte-identical output;
- `operation_fingerprint` and `receipt_sha256` reproduce;
- implementation has no wall-clock or filesystem dependency.

## Validation

```sh
node --test arcana/inventory/test/operation-receipt.test.cjs
```

Expected receipt: `inventory.operation-receipt-kernel-result.v1`.

Passing successor: `SWU-IFR-002`.
