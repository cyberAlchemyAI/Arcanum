# Distill v2 Machine Contract — Execution Pack

## Status

`blocked-before-execution-candidate`. This file describes future wave order; it
does not route work to Task Session.

## Waves

| Wave | Contract | SWUs | Gate |
| --- | --- | --- | --- |
| W0 | [work-pack/waves/W0.md](work-pack/waves/W0.md) | none | Amended owner decision selected, independently reviewed, and exact source/target baselines frozen. |
| W1 | [work-pack/waves/W1.md](work-pack/waves/W1.md) | 001–007 | W0 PASS. Builds and structurally validates the eight-schema grammar. |
| W2 | [work-pack/waves/W2.md](work-pack/waves/W2.md) | 008–023 | W1 PASS. Adds eleven techniques, five modes, exact profile/source composition. |
| W3 | [work-pack/waves/W3.md](work-pack/waves/W3.md) | 024–025 | W2 PASS. Adds semantic validation and deterministic atomic finalization. |
| W4 | [work-pack/waves/W4.md](work-pack/waves/W4.md) | 026–028 | W3 PASS; cross-owner projection needs separate acceptance. Proves consumers, package parity, and no-effect lab. |

## Parallelism

The ordered frontier is deliberately serial. Schema definitions, concrete
instances, semantic validation, and consumers share exact identities and must
not race. Within one admitted SWU, independent positive and negative fixture
execution may fan out after the staged bytes are frozen, then join before a
single receipt.

## Stop Conditions

Stop before the next write on: changed owner decision, stale baseline, new or
removed target, failed schema/semantic/consumer test, private/public boundary
risk, cross-owner scope without acceptance, generated parity drift, publication,
deployment, destructive action, or external effect.
