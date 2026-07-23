# Editorial Admission Fixtures

This corpus defines expected Whisper editorial-admission decisions before an evaluator exists. It is intentionally product-neutral and contains no production artifact text.

## Reading a fixture

- `input` describes the state and evidence presented to future validators.
- `expected` separates evidence binding, generation admission, and final-status evaluation.
- `primary_expectation` names the single causal verdict each fixture is designed to prove.
- `baseline_observation` is `not-enforced` in every file because this unit creates no evaluator.

The digest values are synthetic controls. Equal strings mean the references should bind; different strings mean they should not. This corpus does not claim that digest recomputation is implemented.

## Inventory

| Fixture | Regime | Control | Primary expectation |
| --- | --- | --- | --- |
| `WEG-GREEN-001` | medium | proven transport with complete exact evidence | `pass / all-required-evidence-admissible` |
| `WEG-RED-001` | low | candidate transport requests pass | `flag / transport-proof-candidate` |
| `WEG-RED-002` | medium | comprehension absent while machine axes pass | `flag / comprehension-required` |
| `WEG-RED-003` | low | volatile intent requests full derivative | `block / volatile-or-unfrozen` |
| `WEG-RED-004` | medium | approval binds another surface | `block / approval-surface-mismatch` |
| `WEG-RED-005` | low | conversational approval has no approval kind | `block / approval-kind-missing` |
| `WEG-RED-006` | complex | rendered retell lacks ownership accounting | `block / unaccounted-surface` |
| `WEG-RED-007` | complex | post-apply review binds the pre-apply digest | `flag / post-apply-artifact-mismatch` |

The machine-readable inventory is [manifest.json](manifest.json).
