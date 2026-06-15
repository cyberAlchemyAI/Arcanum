# Glossary Consistency: Craft Projection Layer

| Term | Definition | Notes |
| --- | --- | --- |
| ledger | `.craft/ledger.yml`, the canonical Craft state. | Source of truth. |
| index | `.craft/index.json`, a generated lookup manifest. | Not authoritative. |
| projection | A derived CSV or JSON view generated from the ledger. | Preferred term over table. |
| stale projection | A generated artifact whose recorded ledger hash differs from the current ledger. | Must flag or block use. |
| reconcile | A dry-run import process that turns edited projections into a proposed YAML patch. | Required before writeback. |
| pending by node | A compact status summary for each Craft context. | All-status fast path. |
| compatibility index | Existing embedded `indexes` data inside YAML ledgers. | May remain until generator-owned policy is selected. |

## Consistency Rule

Use `projection` for generated CSV files, `index` for generated JSON lookup
data, and `ledger` only for authoritative YAML.
