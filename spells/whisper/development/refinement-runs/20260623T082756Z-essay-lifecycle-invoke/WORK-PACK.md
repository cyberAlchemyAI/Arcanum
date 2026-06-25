---
module: whisper-essay-lifecycle
version: current
status: draft
updatedAt: 2026-06-23
docType: work-pack
---

# WORK-PACK: Whisper Essay Lifecycle Type Model

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass-for-L1-contract-refresh | Spellcraft accepted the route; canonical mutation still needs bounded Task Session execution. |
| complexity | medium | Touches writing artifact identity, canonical schema guidance, Whisper README, and future validation. |
| outputMode | split | This packet separates review, model, layering, dispatch, Invoke result, and Spellcraft result. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | Defines L0-L3 promotion sequence. |
| dispatchRef | `PLAN-DISPATCH.json` | Cross-capability route from Invoke to Spellcraft and Task Session. |
| distillValidationStatus | pass-with-coordination-flag | SCU is essay identity vs draft state; coordinate with `SWU-WSC-004`. |
| activeLayerWindow | L1-contract-refresh | Next mutation-capable work is contract/schema refresh coordinated with `SWU-WSC-004`. |
| readinessProfile | lifecycle-extension | Add optional type model before physical publication reshaping. |

## Objective Summary

Add a Whisper lifecycle/type model that distinguishes public essay identity from
development draft state, so a series can promote `DRAFT-SUBSTACK-002.md` as
`essay-001` and relate `DRAFT-SUBSTACK-003.md` as `essay-002` without using draft
numbers as public sequence identifiers.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-WEL-001 | Review and type model. | L0 | current drafts and Whisper contract | Review cites concrete draft and contract gaps. |
| S-WEL-002 | Canonical contract/schema extension. | L1 | Spellcraft acceptance; coordinate with `SWU-WSC-004` | YAML parse, README path scan, schema package review. |
| S-WEL-003 | Essay 01/02 example mapping or series registry proposal. | L2 | S-WEL-002 | Example parse and review against model. |
| S-WEL-004 | Reusable evidence and promotion decision. | L3 | S-WEL-003 | Fixture or experiment matrix. |

## Task Status Board

| Task ID | Goal | Layer | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| TASK-WEL-001 | Review draft/essay sequence ambiguity and propose model. | L0 | `WRITING-SEQUENCE-REVIEW.md`, `ESSAY-LIFECYCLE-TYPE-MODEL.md` | complete | complete |
| TASK-WEL-002 | Add optional essay lifecycle/type fields to Whisper contract and schema guidance. | L1 | `ESSAY-LIFECYCLE-TYPE-MODEL.md`, `IMPLEMENTATION-LAYERING.md`, `SPELLCRAFT-RESULT.md` | ready-via-SWU-WSC-004 | not-started |
| TASK-WEL-003 | Create example mapping for Essay 01 and Essay 02. | L2 | L1 contract/schema fields | blocked-until-L1 | not-started |
| TASK-WEL-004 | Validate reusable behavior and promotion scope. | L3 | L2 examples | blocked-until-L2 | not-started |

## SWU Manifest

| SWU ID | Parent Task | Goal | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WEL-001 | TASK-WEL-001 | Review sequence ambiguity and define type model. | none | This refinement-run folder. | Review, type model, layering, dispatch, Invoke result, and Spellcraft result exist. | `WRITING-SEQUENCE-REVIEW.md`; `ESSAY-LIFECYCLE-TYPE-MODEL.md`; `INVOKE-RESULT.md`; `SPELLCRAFT-RESULT.md`. | Markdown review, dispatch validation. | invoke/spellcraft | complete |
| SWU-WEL-002 | TASK-WEL-002 | Add optional essay lifecycle fields to canonical Whisper docs/schema guidance. | SWU-WEL-001; Spellcraft acceptance; coordinate with SWU-WSC-004 | `arcanum/spells/whisper/README.md`; `arcanum/spells/whisper/schemas/**` if needed. | Whisper names `essay_artifact`, `draft_artifact`, `essay_revision`, and `series_relation` without requiring them for all transports. | Task Session receipt for docs/schema update. | YAML parse, path scan, validator compatibility checks. | task-session | ready-via-SWU-WSC-004 |
| SWU-WEL-003 | TASK-WEL-003 | Add examples for `essay-001` and `essay-002` identity mapping. | SWU-WEL-002 | Example/evidence artifacts only. | Example maps Draft 02 to Essay 01 and Draft 003 to Essay 02 with sequel relation. | Example parse and review. | YAML parse and model checklist. | task-session | blocked |
| SWU-WEL-004 | TASK-WEL-004 | Validate promotion readiness. | SWU-WEL-003 | Evidence artifacts only. | Evidence says whether lifecycle fields stay optional, become base for series transports, or remain local examples. | Fixture matrix or experiment report. | Validator matrix and Spellcraft decision. | experiment-harness/spellcraft | blocked |

## Coordination With Schema Canonization

`SWU-WSC-004` is already the next ready unit in the schema-canonization
work-pack. Because it refreshes the Whisper README and validator guidance, this
essay lifecycle model should be consumed there or immediately after it. Avoid
two independent edits to the same canonical contract.

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| `sequence` | review -> type model -> Spellcraft acceptance -> Task Session | Later artifacts consume earlier decisions. | pass |
| `artifact_contract_bridge` | draft files to essay model | Development draft paths are provenance, not public identity. | pass |
| `owner_boundary_check` | Invoke vs Spellcraft vs Task Session | Invoke authors, Spellcraft accepts, Task Session mutates. | pass |
| `state_namespace_boundary` | draft state vs essay identity | File revision and essay sequence remain separate namespaces. | pass |
| `validation_loop` | every canonical mutation | Parser, path scan, or review evidence required. | pass |
| `residue_ledger` | deferred publish directory and validator checks | Future work remains explicit. | pass |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit | pass | Separate essay identity from draft state. |
| Recomposition proof | pass | Supports public title, sequence, bridge, revision, and publication readiness. |
| Hidden acceptance-critical gaps | flag | Must coordinate with `SWU-WSC-004` before editing Whisper README. |
| Deferred complexity | pass | Physical publishing directory and executable checks are deferred. |

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-23 | Initial Invoke/Spellcraft packet for essay lifecycle type management. | Codex |
| 2026-06-23 | Spellcraft accepted route and marked lifecycle model ready as an input to `SWU-WSC-004`. | Codex |
