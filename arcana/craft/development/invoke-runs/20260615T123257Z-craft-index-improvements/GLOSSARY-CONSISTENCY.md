# Glossary Consistency: Craft Index Improvements

| Term | Canonical Meaning | Consistency Decision |
| --- | --- | --- |
| ledger | `.craft/ledger.yml`, canonical Craft state. | Source of truth. |
| generated index | `.craft/index.json`, rebuildable machine lookup. | Not authoritative. |
| embedded index | `indexes:` section inside YAML ledgers. | Compatibility lookup until generator-owned policy is selected. |
| projection | `.craft/projections/*.csv`, generated flat review/import staging files. | Preferred over "table". |
| readiness index | Optional lookup handles that expose executable artifact, SWU, approval, execution mode, and blocked scopes. | Records readiness, not execution proof. |
| pending by node | Compact status summary for every Craft context/node. | Fast path for `state all`. |
| reconcile | Dry-run import process from edited CSV to proposed YAML patch. | No writeback before fixture proof. |
| public-safe fixture | Synthetic or already-public data used to validate generated outputs. | Required before public submodule publication. |

## Conflicts Resolved

- "CSV tables" becomes "CSV projections".
- "Index" is limited to machine lookup surfaces; it does not redefine content.
- "Readiness" does not mean "execution complete".
