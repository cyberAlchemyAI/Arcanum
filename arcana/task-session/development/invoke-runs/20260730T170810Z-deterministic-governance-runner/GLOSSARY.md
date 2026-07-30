# Glossary: Deterministic Task Session Governance Runner

| Term | Definition |
| --- | --- |
| governance evaluator | pure production CLI that evaluates Task Session policy and emits a schema-valid decision receipt without mutating implementation or owner targets |
| governance runner | bounded controller that orders and checkpoints one Task Session governance run |
| phase receipt | immutable evidence for one monotonic runner phase, bound to its predecessor |
| execution ticket | immutable authorization envelope for one admitted SWU; it is not an implementation command |
| executor receipt | structured evidence returned by the separate implementation executor |
| target classifier | deterministic `apply`, `already-present-exact-output`, or `conflict` comparison |
| staged output | candidate bytes produced outside the live target and bound by digest |
| owner hook | registered side job whose semantics remain owned by another capability |
| joined receipt | owner receipt whose identity, schema, inputs, and result were validated by the runner |
| continuity cursor | terminal non-execution handle naming the unique next route or blocker |
| output-only re-admission | admission that allows declared governance evidence after implementation mutation closes, without reopening implementation scope |
| product-neutral fixture | synthetic public evidence that contains no consuming-project prose or identifiers |
| terminal write | final write by a role after which that role may not mutate the run |

