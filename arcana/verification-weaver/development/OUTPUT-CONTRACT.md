# Output Contract

`verification-weaver` emits a parent receipt named `VERIFICATION-WEAVE`.

The parent receipt proves routing and recomposition only. It preserves owner
statuses and must not upgrade, rewrite, or promote owner lane outputs.

## Required Fields

```yaml
schema_version: "0.1.0"
receipt_type: VERIFICATION-WEAVE
fixture_id: synthetic-target-id
fixture_role: positive
target:
  id: synthetic-target-id
  target_kind: spec_derivation
  source_refs:
    - synthetic://source/ref
classification:
  oracle_type: deterministic_derivation
lanes:
  - owner_capability_ref: arcanum/arcana/test-derivation
    owner_status: draft
    owned_verb: derive
    status: pass
evidence:
  - id: synthetic-evidence
    owner: arcanum/arcana/test-derivation
    artifact: synthetic://evidence/ref
gaps: []
residue: []
public_safety:
  private_path_scan: pass
  generated_output_scan: pass
status: pass
promotion_action: none
next_route:
  recommended_owner: none
```

## Enumerations

Valid `target_kind` values:

- `spec_derivation`
- `frontend_ux`
- `execution_repeatability`
- `architecture_gap`
- `research_evidence`
- `mixed`
- `unsupported`

Valid `classification.oracle_type` values:

- `deterministic_derivation`
- `fixture_runner`
- `proof_checker`
- `browser_evidence`
- `human_review`
- `research_run_data`
- `explicit_gap`
- `null`

Valid top-level `status` values:

- `pass`
- `flag`
- `block`

Valid `promotion_action` values:

- `none`
- `candidate-request`

## Owner Status Preservation

Owner lane status is descriptive. A parent receipt can carry:

- draft owner evidence;
- seed owner evidence;
- blocked owner evidence;
- explicit owner gaps.

The parent receipt cannot turn any of those into a promoted capability state.

## Mixed Targets

A `mixed` target must include:

- `classification.decomposition.required: true`;
- child owner lanes or an explicit decomposition gap;
- `status: flag` or `status: block` unless all child receipts exist.

## Unsupported Targets

An `unsupported` target must include:

- `unsupported_reason`;
- `status: block`;
- `promotion_action: none`;
- a next route or explicit gap.
