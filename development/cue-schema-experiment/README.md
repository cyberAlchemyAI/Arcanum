# Arcanum CUE Schema Adoption Experiment

This development-only package measures whether CUE can safely serve as an
Arcanum schema source, a secondary verifier, or neither. It does not change
schema ownership, authorize migration, or modify any canonical schema.

The experiment evaluates five frozen strata: the active Invoke Define/Design
schema graph, Orchestrate runtime schemas, Work-Pack Readiness schemas,
InfraSpec JSON/YAML parity, and the existing Distill v2 grammar plus a
non-canonical W2 semantic stressor. A separate census covers the frozen set of
225 canonical Arcanum JSON Schemas.

R0 preserves two current baseline blockers rather than attributing them to CUE:
Invoke has one Define authoring-closure digest failure after concurrent schema
additions, and Orchestrate has four errors from an absent hidden strategy-ledger
fixture. Their exact test denominators, exits, and summary markers are pinned.

Only the following development interfaces are public:

```text
scripts/run-cue-schema-experiment.py \
  --root <repository-root> \
  --cue-bin <verified-cue-binary> \
  --config <experiment-config> \
  --output-dir <absent-directory> \
  --output-format json

scripts/verify-cue-schema-experiment.py \
  --root <repository-root> \
  --cue-bin <verified-cue-binary> \
  --report <report-json>
```

All CUE and consumer processes run in a network-isolated, read-only Bubblewrap
sandbox. Their only writable locations are run-local output and temporary
directories. Generated JSON Schema bytes are compared directly; canonical JSON
normalization is reported separately and cannot upgrade an unstable raw result.
R3 mechanically inlines the exact local JSON Schema reference closure before
non-strict import, producing one native CUE prototype per targeted schema. It
does not add defaults or repair unsupported constraints; mutation parity exposes
anything the import omits. Each run carries both a full physical integrity digest
and a normalized `report_digest` that must match the second isolated run.

The final classification is one of `reject_cue`, `verifier_only`,
`bounded_adoption_candidate`, `broad_adoption_candidate`, or
`retain_json_schema`. Every result has `authority_effect: none` and stops before
Distill W1R/W2 implementation.
