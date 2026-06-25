---
module: whisper-schema-canonization
version: current
status: draft
updatedAt: 2026-06-23
docType: work-pack
---

# WORK-PACK: Whisper Schema Canonization

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass-for-L2-contract-refresh | `SWU-WSC-003` created the canonical schema package; contract refresh is the next ready SWU. |
| complexity | medium | Canonical promotion touches spell contract, schema package, validator docs, and evidence review. |
| outputMode | split | Task contracts live under `work-pack/tasks/`; execution order lives in `EXECUTION-PACK.md`. |
| executionPackRef | `EXECUTION-PACK.md` | Required for medium-complexity plan. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | Defines L0-L3 promotion sequence. |
| dispatchRef | `PLAN-DISPATCH.json` | Cross-capability route from Invoke to Spellcraft, Task Session, and Experiment Harness. |
| distillValidationStatus | pass-with-owner-gate | SCU is schema authority separation; first SWU is L0 inventory. |
| activeLayerWindow | L2-contract-refresh | Canonical schema package exists and validates; next unit may refresh Whisper contract/docs. |
| readinessProfile | promotion-review | Stable canonical version requires evidence, not direct copy. |

## Objective Summary

Create a governed plan to canonize Whisper schema artifacts that currently live
inside `development/refinement-runs/`. The plan must produce a stable canonical
schema route while preserving the distinction between development evidence,
examples, generated runtime mirrors, and canonical spell authority.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-WSC-001 | Complete schema artifact inventory and canonicalization matrix. | L0 | none | Review report cites concrete paths and classifications. |
| S-WSC-002 | Design canonical schema package surface. | L1 | S-WSC-001, Spellcraft acceptance | Proposed path map and file contracts. |
| S-WSC-003 | Create canonical schema package and examples. | L1 | S-WSC-002 | YAML/JSON parse, validator compatibility, example validation. |
| S-WSC-004 | Refresh Whisper contract and validator docs. | L2 | S-WSC-003 | Path-reference scan and validator checks. |
| S-WSC-005 | Record reusable promotion evidence. | L3 | S-WSC-004 | Experiment or fixture matrix evidence. |

## Task Status Board

| Task ID | Goal | Layer | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-WSC-001](work-pack/tasks/TASK-WSC-001.md) | Inventory and classify schema-bearing artifacts. | L0 | `CONTEXT-PACK.md`, `SPELLCRAFT-RESULT.md`, `SCHEMA-ARTIFACT-AUDIT.md` | complete | complete |
| [TASK-WSC-002](work-pack/tasks/TASK-WSC-002.md) | Specify canonical schema package surface. | L1 | `IMPLEMENTATION-LAYERING.md`, `SCHEMA-ARTIFACT-AUDIT.md`, `SPELLCRAFT-PACKAGE-SPEC-RESULT.md`, `CANONICAL-SCHEMA-PACKAGE-SPEC.md` | complete | complete |
| [TASK-WSC-003](work-pack/tasks/TASK-WSC-003.md) | Create canonical schema files and examples. | L1 | `CANONICAL-SCHEMA-PACKAGE-SPEC.md`, `TASK-SESSION-SWU-WSC-003-REPORT.md` | complete | complete |
| [TASK-WSC-004](work-pack/tasks/TASK-WSC-004.md) | Refresh Whisper contract and validator documentation. | L2 | canonical schema package; `../20260623T082756Z-essay-lifecycle-invoke/ESSAY-LIFECYCLE-TYPE-MODEL.md` | ready | not-started |
| [TASK-WSC-005](work-pack/tasks/TASK-WSC-005.md) | Validate reusable evidence and promotion readiness. | L3 | canonical package and refreshed contract | blocked-until-L2 | not-started |

## SWU Manifest

| SWU ID | Parent Task | Goal | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WSC-001 | TASK-WSC-001 | Inventory schema-bearing artifacts and classify authority status. | none | New L0 review artifact under this run folder. | Every relevant schema/development/refresh artifact is classified as canonical-candidate, example-candidate, provenance-only, generated, or superseded. | `SCHEMA-ARTIFACT-AUDIT.md`; `TASK-SESSION-WORKPACK-REPORT.md`; `SPELLCRAFT-RESULT.md` accepts L0 execution. | `rg`, `find`, YAML parse checks, validator compatibility check, report review. | task-session | complete |
| SWU-WSC-002 | TASK-WSC-002 | Propose canonical schema package contract. | SWU-WSC-001, Spellcraft acceptance | New package spec under this run folder. | Target files, field ownership, examples, and validation commands are specified. | `CANONICAL-SCHEMA-PACKAGE-SPEC.md`; `TASK-SESSION-SWU-WSC-002-REPORT.md`. | Review against `README.md`, validator behavior, and L0 matrix; path-scope check. | task-session | complete |
| SWU-WSC-003 | TASK-WSC-003 | Create `arcanum/spells/whisper/schemas/` package. | SWU-WSC-002 | `arcanum/spells/whisper/schemas/**` only. | README, base schema contract, and example fixtures exist and parse. | `TASK-SESSION-SWU-WSC-003-REPORT.md`; package files under `arcanum/spells/whisper/schemas/**`. | YAML parse, draft validator against examples, path-reference scan. | task-session | complete |
| SWU-WSC-004 | TASK-WSC-004 | Refresh Whisper README and validator docs to reference canonical schema home and accepted optional essay lifecycle/type model. | SWU-WSC-003 | `arcanum/spells/whisper/README.md`; validator doc/help if needed; schema guidance if needed; generated mirrors only through regeneration. | Canonical contract names stable schema home, does not cite development runs as runtime authority, and distinguishes essay identity from draft state for series artifacts. | Path-reference scan and validation report; essay lifecycle model review. | `rg "development/refinement-runs"`, validator checks, YAML parse, optional bootstrap dry run. | task-session | ready |
| SWU-WSC-005 | TASK-WSC-005 | Run reusable evidence pass over main, sequel, and readability fixtures. | SWU-WSC-004 | Experiment/evidence artifacts only. | Evidence matrix says pass/flag/block for all current fixtures and names residue. | Experiment Harness or equivalent fixture report. | Validator matrix and Spellcraft promotion decision. | experiment-harness/spellcraft | blocked |

## Completed Executable Unit

`SWU-WSC-001` completed the L0 audit and classification pass.

Actual receipt:

```yaml
runtime: codex
source_swu: SWU-WSC-001
result: pass
files_touched:
  - arcanum/spells/whisper/development/refinement-runs/20260623T062605Z-schema-canonization-invoke/SCHEMA-ARTIFACT-AUDIT.md
  - arcanum/spells/whisper/development/refinement-runs/20260623T062605Z-schema-canonization-invoke/TASK-SESSION-CONTEXT.md
  - arcanum/spells/whisper/development/refinement-runs/20260623T062605Z-schema-canonization-invoke/TASK-SESSION-WORKPACK-REPORT.md
validation:
  - rg/find inventory commands
  - YAML parse checks for candidate substrates
  - validator pass on current Draft 02 substrate
remaining_blockers:
  - Spellcraft acceptance required before canonical package mutation
lifecycle_owner_next_step: spellcraft
```

## Completed Package-Spec Unit

`SWU-WSC-002` completed the canonical package specification in
`CANONICAL-SCHEMA-PACKAGE-SPEC.md`.

## Next Executable Unit

`SWU-WSC-004` is next in sequence. Its write scope is limited to
`arcanum/spells/whisper/README.md`, validator docs/help if needed, and schema
guidance if needed. It should also consume the accepted essay lifecycle/type
model in `../20260623T082756Z-essay-lifecycle-invoke/`.

## Blockers And Gaps

| Gap ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| GAP-WSC-001 | lifecycle | RESOLVED for L2 contract refresh by `TASK-SESSION-SWU-WSC-003-REPORT.md`; promotion evidence remains downstream-gated. | Task Session | Run `SWU-WSC-004` to refresh the Whisper contract and validator guidance. |
| GAP-WSC-002 | evidence | `readability_dynamics` has L0 validator evidence but not broad reusable promotion evidence. | Experiment Harness | Validate across fixture matrix before full promotion. |
| GAP-WSC-003 | source separation | Development-run schema includes article-specific source context. | Task Session | Separate base schema contract from examples during canonical package creation. |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| `sequence` | L0 review -> L1 package -> L2 contract refresh -> L3 evidence | Each layer consumes prior evidence. | pass |
| `scu_swu_reduction` | first unit | First unit is audit/classification only. | pass |
| `recomposition_proof` | canonical package route | Canonical package recomposes from proven development artifacts without copying run-local assumptions. | pass |
| `validation_loop` | every slice | Each SWU names validation surface. | pass |
| `owner_boundary_check` | Invoke vs Spellcraft vs Task Session | Invoke plans; Spellcraft accepts lifecycle mutation; Task Session executes SWUs. | pass |
| `handle_handoff` | downstream execution | Handoff uses artifact paths and one selected SWU. | pass |
| `residue_ledger` | blocked future work | Readability promotion and generated runtime sync remain visible. | pass |
| `state_namespace_boundary` | canonical vs development vs generated | Source roots and generated mirrors stay separate. | pass |
| `execution_receipt_handoff` | later Task Session | Expected receipt fields are defined. | pass |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit | pass | `SWU-WSC-001` is review-only inventory/classification. |
| Recomposition proof | pass | Inventory feeds schema package design, package creation, contract refresh, and experiment evidence. |
| Hidden acceptance-critical gaps | pass | Package spec exists; README refresh and promotion evidence remain explicitly deferred. |
| Deferred complexity | pass | Runtime mirror sync, renderer schema integration, and broad transport coverage are deferred. |
| Navigation to next executable unit | pass | `SWU-WSC-004` is ready for Task Session. |

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-23 | Initial Invoke plan for Whisper schema canonization. | Codex |
| 2026-06-23 | Spellcraft accepted L0 audit execution while keeping canonical package mutation blocked. | Codex |
| 2026-06-23 | Task Session completed `SWU-WSC-001` audit and left the workpack blocked at L1 owner gate. | Codex |
| 2026-06-23 | Spellcraft accepted the L1 package-spec lane and made `SWU-WSC-002` ready. | Codex |
| 2026-06-23 | Task Session completed `SWU-WSC-002` package specification and made `SWU-WSC-003` ready. | Codex |
| 2026-06-23 | Task Session completed `SWU-WSC-003` canonical schema package creation and made `SWU-WSC-004` ready. | Codex |
| 2026-06-23 | Added accepted essay lifecycle/type model as an input to `SWU-WSC-004`. | Codex |
