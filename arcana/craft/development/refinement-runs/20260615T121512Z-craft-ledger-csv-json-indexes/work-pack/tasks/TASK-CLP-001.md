# TASK-CLP-001: Projection Contract

Goal: document `.craft/index.json` and `.craft/projections/*.csv` as generated
surfaces while preserving `.craft/ledger.yml` authority.

Acceptance:

- YAML authority is explicit.
- Generated projection metadata includes ledger hash, schema version, generator
  version, and generated timestamp.
- Embedded ledger indexes are described as compatibility or generator-owned
  lookup data.
