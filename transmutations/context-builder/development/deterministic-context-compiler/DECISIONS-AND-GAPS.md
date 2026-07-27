# Decisions And Gaps

## Decisions

| ID | Status | Decision | Rationale |
| --- | --- | --- | --- |
| D-001 | accepted for authoring | Build a deterministic compiler around Context Builder rather than replace semantic obligation formation. | Mechanical work is reproducible; semantic sufficiency remains judgment. |
| D-002 | accepted for authoring | Store excerpt objects by exact admitted input and content hashes. | Git revision alone does not bind dirty or later-created bytes. |
| D-003 | accepted for authoring | Keep cache state non-authoritative and consumer-local. | Reuse must not become promotion or freshness authority. |
| D-004 | accepted for authoring | Persist required evidence formats but inject one declared runtime payload. | Persistence and runtime prompt composition are separate concerns. |
| D-005 | accepted for authoring | Use deterministic cost-aware covering-set selection, not an unproved global-optimum claim. | Global minimum set cover is not required to establish reproducibility or savings. |
| D-006 | accepted for authoring | Treat token reduction as a hypothesis until paired runtime receipts exist. | Bytes and tokenizer estimates are not provider usage. |
| D-007 | accepted for authoring | Leave implementation SWU selection unset. | Define/Design/Plan authoring is not execution authorization. |

## Gaps

| ID | Severity | Gap | Owner | Route |
| --- | --- | --- | --- | --- |
| G-001 | medium | No compiler, schemas, or deterministic fixtures exist. | Sigil Development | planned implementation SWUs |
| G-002 | medium | Current packs do not require per-selected-excerpt hashes or cache receipts. | Sigil Development | contract update after proof |
| G-003 | medium | No exact tokenizer/runtime usage baseline is recorded. | Experiment Harness | paired baseline and candidate runs |
| G-004 | low | Provider-specific cache behavior is intentionally unspecified. | Runtime adapter owner | optional future adapter |
| G-005 | medium | Reusable behavior and promotion readiness are unproven. | Sigil Development | experiment and lifecycle validation |
