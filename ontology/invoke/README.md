# Invoke Ontology Package

This candidate is the durable, reusable ontology for the public Invoke capability. It replaces no canonical Invoke contract and does not turn validation evidence into authority.

The package keeps business and system definitions branch-local, expresses their alignment only in the bridge view, preserves the stable IDs and operation composition from the three legacy validation receipts, and retains unresolved residue instead of silently filling it.

## Public/private boundary

Public CAV2-derived content is limited to the definition and model contracts allowed by the Ontology Vault export policy. The package contains no private source paths or digests, proof material, source scripts, or evidence from other systems. Exact private provenance remains outside this public candidate.

Ontology records describe and validate structure. They do not decide authority, promotion, publication, runtime conformance, release admission, or canonical definition ownership.

## Validate

From the Arcanum repository root:

```bash
python3 ontology/invoke/scripts/validate.py
```

Receipt creation is explicit and append-only:

```bash
python3 ontology/invoke/scripts/validate.py --write-receipt
```
