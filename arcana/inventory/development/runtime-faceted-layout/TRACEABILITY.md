# Requirement Traceability

| Acceptance | SWU | Evidence |
| --- | --- | --- |
| unrelated working directory | 002, 007 | `session-evidence/SWU-IFR-002/receipt.json`, `session-evidence/SWU-IFR-007/receipt.json` |
| clean and one-new-warning deltas | 002, 007 | `session-evidence/SWU-IFR-002/receipt.json`, `session-evidence/SWU-IFR-007/receipt.json` |
| repeated dry-run | 001R, 002, 007 | `session-evidence/SWU-IFR-001R/receipt.json`, `session-evidence/SWU-IFR-002/receipt.json`, `session-evidence/SWU-IFR-007/receipt.json` |
| no-op and conflict | 002 | `session-evidence/SWU-IFR-002/receipt.json` |
| partial mutation is visible | 003 | `session-evidence/SWU-IFR-003/receipt.json` |
| faceted path and maps | 004, 005 | `session-evidence/SWU-IFR-004/receipt.json`, `session-evidence/SWU-IFR-005/receipt.json` |
| legacy preserved | 004, 005 | `session-evidence/SWU-IFR-004/receipt.json`, `session-evidence/SWU-IFR-005/receipt.json` |
| generated sync safety | 006, 007 | `session-evidence/SWU-IFR-006/receipt.json`, `session-evidence/SWU-IFR-007/receipt.json` |
| public/private boundary | 006, 007, VERIFY | `session-evidence/SWU-IFR-006/receipt.json`, `session-evidence/SWU-IFR-007/receipt.json`, `session-evidence/TASK-IFR-VERIFY/audit.md` |
