# Definition Card: Validated Compaction

Status: `local-research-only`

## Source Meaning

A context-reduction operation checked for recoverability of key information,
with an explicit score, compression ratio, and less-aggressive retry when a
threshold is missed.

Source kind: `primary-source`

Evidence: paper §3.2, §4, §5

## Structural Shape

```text
compact(source, budget, obligations) -> candidate
validate(source, candidate, obligations) -> pass | fail
fail -> retry_less_aggressively | refuse
pass -> candidate + validation receipt
```

## Operator Reading

The preservation obligations must precede compression. A score without declared
invariants cannot show that the important information survived.

## Use Carefully

- Separate size reduction from semantic preservation.
- Retain provenance to the uncompacted source.
- Test repeated compaction for accumulated drift.

## Misuse Warning

- The paper does not disclose its validation mechanism, threshold semantics, or
  per-run fidelity traces. “Validated” therefore must not be rewritten as
  universally “lossless.”

## Promotion Boundary

`local-only`
