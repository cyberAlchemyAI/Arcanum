## Diagnose The First Real Failure

| Failure | Repair owner |
| --- | --- |
| source schema invalid | repair the authored shape, fixed constant, missing nullable field, or enum |
| exact ref is stale | recompute SHA-256 and byte size from the intended current file |
| selector does not resolve | choose a selector type and value that resolves in the referenced bytes |
| public source is outside public root | use public evidence inside Arcanum or make the registry private when the contract permits it |
| term or alias collision | choose non-colliding semantic identities after normalization |
| unresolved or self relation | point only to another definition id in the same source |
| layering output mismatch | pair `seed` with `IMPLEMENTATION-LAYERING.md` and `gap` with `LAYERING-GAP.md` |
| identity result is not pass | stop; the required identity denominator is not satisfied |
| structural schema invalid | repair the referenced Draft 2020-12 schema or classify the structural schema honestly |
| generated view drift | discard the output directory and rerun the compiler from the source; never hand-edit a generated view |

The compiler publishes atomically: schema, evidence, selector, semantic graph,
identity, or late view failures leave the requested output directory absent.
Do not reinterpret an absent bundle or a `BLOCK` message as a partial pass.
