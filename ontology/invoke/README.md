# Invoke Ontology Package

This candidate is the durable, reusable ontology for the public Invoke capability. It replaces no canonical Invoke contract and does not turn validation evidence into authority.

The package keeps business and system definitions branch-local, expresses their alignment only in the bridge view, preserves the stable IDs and operation composition from the three legacy validation receipts, and retains unresolved residue instead of silently filling it.

## Public/private boundary

Public CAV2-derived content is limited to the definition and model contracts allowed by the Ontology Vault export policy. The package contains no private source paths or digests, proof material, source scripts, or evidence from other systems. Exact private provenance remains outside this public candidate.

Ontology records describe and validate structure. They do not decide authority, promotion, publication, runtime conformance, release admission, or canonical definition ownership.

## Business concept contract

Business nodes bind `invoke-business-node/public-contract-v2` and expose one required `concept` object:

- `name` gives the concept's reader-facing identity.
- `role` classifies it with the business-role vocabulary.
- `meaning` states the precise candidate-scoped meaning supported by the node's claim, scope, evidence, and obligations.
- `plain_language` provides a short non-normative explanation for direct reading.

The shared public node contract still requires top-level `label` and `role`, so v2 retains them as compatibility projections. Validation requires `concept.name == label` and `concept.role == role`; neither copy may drift independently. The concept object does not replace canonical definitions, broaden the cited evidence, or change the node's candidate and non-authoritative posture.

The v1-to-v2 change and frozen v1 projections are recorded in `migration/preserved-identities.json#schema_amendments`.

## Validate

From the Arcanum repository root:

```bash
python3 ontology/invoke/scripts/validate.py
```

Receipt creation is explicit and append-only:

```bash
python3 ontology/invoke/scripts/validate.py --write-receipt
```
