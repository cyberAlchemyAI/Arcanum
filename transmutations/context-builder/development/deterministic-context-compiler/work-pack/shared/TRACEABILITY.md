# Traceability

| Requirement Or Rule | Architecture Anchor | SWU | Witness |
| --- | --- | --- | --- |
| FR-01 request schema | Request Validator | SWU-DCC-001 | malformed and duplicate-ID mutants |
| FR-02 exact source binding | Source Snapshotter | SWU-DCC-002 | DCC-FIX-003, DCC-FIX-006 |
| FR-03 cache key | Content-Addressed Store | SWU-DCC-002 | DCC-FIX-001 |
| FR-04 safe cache reuse | Content-Addressed Store | SWU-DCC-006 | stale/corrupt cache mutants |
| FR-05 deduplication | Covering-Set Selector | SWU-DCC-003 | DCC-FIX-002 |
| FR-06 deterministic covering set | Covering-Set Selector | SWU-DCC-003 | DCC-FIX-004, DCC-FIX-008 |
| FR-07 fail-closed blockers | Decision Flow | SWU-DCC-003 | DCC-FIX-005, DCC-FIX-007 |
| FR-08 stable renders | Pack Renderer And Validator | SWU-DCC-004 | DCC-FIX-011 |
| FR-09 one injected payload | Runtime Adapter | SWU-DCC-004 | DCC-FIX-012 |
| FR-10 proved base/delta | Runtime Adapter | SWU-DCC-006 | DCC-FIX-010 |
| FR-11 evidence-separated measurements | Usage receipt interface | SWU-DCC-005 | DCC-FIX-009 |
| FR-12 public/private boundary | Data Lifecycle Extension | SWU-DCC-007, SWU-DCC-008 | public hygiene scan |
| R-007 compiler cannot promote sigil | Sigil Development interface | SWU-DCC-008 | lifecycle-owner receipt |

Every row recomposes into the [Define acceptance criteria](../../SPEC.md) and
[Design witness contracts](../../WITNESS-CONTRACTS.md).
