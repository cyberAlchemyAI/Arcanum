# Execution Pack

## Choreography

| Wave | Owner route | SWUs | Gate |
| --- | --- | --- | --- |
| W0 | `sigil-development` for Task Session | `SWU-PEP-001`, `SWU-PEP-002` | contract and read-bounded classifier pass |
| W1 | `sigil-development` for Continuation Router and Task Session | `SWU-PEP-003`, `SWU-PEP-004` | one-hop join, authorization, idempotency, and resume pass |
| W2 | `spellcraft` for Invoke and Implementation Readiness | `SWU-PEP-005` | handoff state is non-contradictory; plan-once reuse passes |
| W3 | owner-routed integration | `SWU-PEP-006` | regression, canary, public scan, and generated parity pass |

All waves are sequential. No parallel write lane is safe because later owner contracts consume the exact receipts and schemas produced by earlier waves.

## Handoff rule

The implementation dispatch requires separate lifecycle receipts from Sigil Development and Spellcraft. Task Session may execute bounded implementation only within the write scope of the selected SWU. No SWU is selected by this package.
