# Task Matrix

| ID | Complexity | Scenario | Expected Output | Status |
| --- | --- | --- | --- | --- |
| spell-low | low | Small focused request. | Contract-shaped result. | pending |
| spell-medium | medium | Multi-part realistic request. | Contract-shaped result with gates. | pending |
| spell-complex | complex | Cross-boundary or lifecycle request. | Contract-shaped result with risks and next steps. | pending |
| recall-positive | low | Current, complete, safe, within-budget evidence. | Allow with source-bound pack handle. | contract-frozen |
| recall-stale | low | Selected source digest is stale. | Deny with `stale-source`; no pack handle. | contract-frozen |
| recall-missing | low | Required source is missing. | Deny with `missing-source`; no pack handle. | contract-frozen |
| recall-contradictory | medium | Current sources conflict on one obligation. | Deny with `contradictory-source`; no ranking override. | contract-frozen |
| recall-unsafe | medium | Selected path or content is outside safe scope. | Deny with `unsafe-source`; no pack handle. | contract-frozen |
| recall-over-budget | low | Strict pack exceeds the declared budget. | Deny with `over-budget`; no pack handle. | contract-frozen |
| recall-blocked-index | medium | Inventory lookup readiness is blocked. | Deny with `blocked-index`; no source selection. | contract-frozen |
