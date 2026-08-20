# Ontology Vault Package Materialization Regression

Status: acceptance-critical reusable behavior evidence

This harness proves that Ontology Vault keeps a genuinely small one-off map as
one run artifact while requiring a governed package for durable, reusable,
multi-view, bridged, or evolving ontology state.

Run from the consuming repository root:

```bash
python3 arcanum/arcana/ontology-vault/development/package-materialization/test_materialization.py
```

The regression also proves that classification is non-mutating and that an
unresolved durable-package owner, root, or public/private classification blocks
before existing run artifacts can be used as a product-state store.

The bounded public-export regression is separate:

```bash
python3 arcanum/arcana/ontology-vault/development/package-materialization/test_public_export.py
python3 arcanum/arcana/ontology-vault/scripts/ontology_package.py validate-export \
  --policy arcanum/arcana/ontology-vault/contracts/cav2-public-export-policy.json \
  --contracts arcanum/arcana/ontology-vault/contracts/cav2-ontology-contracts.json
```

It proves an exact definition/model-contract allowlist and rejects private
paths, private digests, non-allowlisted IDs, executable carriers, and any claim
that ontology decides authority.
