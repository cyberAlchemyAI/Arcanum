# Context Pack: SWU-IFR-001

## Selection

- selected unit: `SWU-IFR-001`
- layer: L0
- behavior: canonical operation receipt kernel
- execution owner: Task Session
- lifecycle owner status: accepted
- baseline Arcanum revision: `0f7d268b5c2c8b54b53ffe7ff6eb592bf2ebc8c6`

## Obligations

| Obligation | Selected evidence | Required proof |
| --- | --- | --- |
| exact task scope | `tasks/SWU-IFR-001.md` | only schema, pure kernel, and focused test change |
| deterministic receipt | `IMPLEMENTATION-LAYERING.md` L0 | repeated inputs produce identical UTF-8 bytes |
| complete receipt shape | accepted operation-receipt contract | normative receipt validates and rejects drift |
| digest binding | `tasks/SWU-IFR-001.md` | fingerprint and receipt digest reproduce |
| authority boundary | `WORK-PACK.md` | no currentness, promotion, or semantic-authority claim |
| continuation | `WORK-PACK.md` | a passing closeout selects only `SWU-IFR-002` |

## Bound Inputs

| Source | SHA-256 |
| --- | --- |
| `WORK-PACK.md` | `66ec1f81bbac2b6c0adada6fa4b3be158ea2511b77f6d9eafb667cbb31d4791a` |
| `tasks/SWU-IFR-001.md` | `10115b8a0fa71e9efce352ff1f8b383164921e272b5577dd7e66921964945251` |
| `IMPLEMENTATION-LAYERING.md` | `e20592f2cfb49779a011d9d8d4692d142e3f5d9269a4783417028fdb61ce2961` |
| `TRACEABILITY.md` | `74f2717e468bfbb747a47aa301c6f737de5cedde12db32c9922ad4dce19ddf9f` |
| accepted receipt specification | `7315e5cb19d294478aeccbd3e2431926de7bed78620ea6fd8803a5c4c8ce5d7f` |
| accepted receipt architecture | `e103e75e5c153620e6bc5957670a25072b68c6e0f7a4d7180f06730ba31aab30` |
| accepted receipt research findings | `e37e15c05c05020d6a4383d6ce0290bed4382d8a7c0575fd2b57dec521a52eb3` |

## Exact Implementation Write Scope

```text
arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json
arcana/inventory/lib/operation-receipt.cjs
arcana/inventory/test/operation-receipt.test.cjs
```

Task Session evidence and work-pack synchronization are lifecycle closeout
surfaces, not implementation scope expansion.

## Exclusions

- Inventory state reads or writes
- CLI or append-transition implementation
- generated runtime mutation
- consumer Inventory mutation
- implicit timestamps
- currentness, atomicity, migration, promotion, release, commit, or push

## Implementation Decisions

1. The constructor accepts the complete non-derived receipt body and rejects
   caller-supplied derived fields.
2. The operation fingerprint binds canonical operation inputs only: operation,
   mode, timestamp, Inventory root, runtime bundle, and exact input digests.
3. The receipt digest binds the complete normalized receipt including the
   operation fingerprint and excluding only `receipt_sha256`.
4. Schema-defined object order and contract-set array order are emitted
   deterministically; one trailing newline is mandatory.
5. Validation is pure and returns structured errors. Construction fails closed
   when the final receipt is invalid.

## Readiness

- dependency gate: pass
- context freshness: pass
- scope ambiguity: none
- decision gate: not required
- mutation authorization: `SWU-IFR-001` only
