# MOGT Protocol Validation Checklist

This checklist is used before any experiment execution in the MOGT project.

## Criteria

| Check                                                                                      | Pass/Fail | Notes |
| ------------------------------------------------------------------------------------------ | --------- | ----- |
| Objective and claim mapping defined                                                        |           |       |
| Methodology profile exists (`experiments/<experiment-key>/methodology.md`)                 |           |       |
| Protocol terms are anchored in `definitions/DEFINITIONS-INDEX.md`                          |           |       |
| Baseline comparison policy is explicit                                                     |           |       |
| Objective vector and decision-state unit are explicit                                      |           |       |
| Context bundle path is declared (`experiments/<experiment-key>/context.md`)                |           |       |
| Hypothesis or success criteria are measurable                                              |           |       |
| Required data schema fields are defined                                                    |           |       |
| Metadata fields are complete (`experiment_id`, `run_id`, `timestamp`, `model`, `operator`) |           |       |
| Source requirements are explicit and pinnable                                              |           |       |
| Inventory entry-type requirements are explicit                                             |           |       |
| Disconfirming outcome is explicit                                                          |           |       |
| Analysis path is declared                                                                  |           |       |
| Claim-to-paper traceability section is present                                             |           |       |

## Decision

- PASS: all required checks pass.
- NEEDS-REVISION: non-critical checks fail.
- BLOCKED: measurable criteria, objective definitions, or schema requirements are missing.
