# Definition Card: Confusion And Diffusion

Status: local-research-only

## Source Meaning

Diffusion spreads source statistical structure across longer-range cryptogram
statistics. Confusion makes the relation between observed statistics and key
description difficult to exploit.

Source kind: primary-source

Evidence: `tracks/paper-claim-ledger.md` C10.

## Formal Or Structural Shape

```text
diffusion: local source statistics -> longer-range cryptogram statistics
confusion: observed statistics -> complex relation to key coordinates
```

## Notation

| Symbol | Meaning | Shared notation link |
| --- | --- | --- |
| `M` | message | n/a |
| `E` | cryptogram | n/a |
| `K` | key | n/a |

## Operator Reading

Diffusion reduces direct leverage from local observations. Confusion makes the
hidden coordinate system hard to recover even when statistics are visible.

## Use Carefully

- Keep both terms tied to an observer and a statistical attack.
- Do not treat either as a general virtue of complexity.

## Misuse Warning

- Confusing people is not Shannon confusion.
- Spreading work across files is not Shannon diffusion.

## Promotion Boundary

analogy-only

