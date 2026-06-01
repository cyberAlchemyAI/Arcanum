# WORK-PACK: Craft Recursive Ledger Refinement

## Purpose

Create the smallest work-pack needed to refine the next two Craft recursive-ledger steps:

1. typed examples for blockers, gates, enablers, lanes, and role hints;
2. a minimal recursive-ledger schema shaped by those examples.

This work-pack is an Invoke plan artifact. It prepares refinement tasks only; it does not execute them.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for `/refine` over the two selected tasks. |
| complexity | low | Two documentation/design tasks, no code mutation. |
| outputMode | single-file | Split task files are unnecessary for this refinement slice. |
| executionPackRef | n/a | Not needed for low complexity. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | Required Invoke plan companion. |
| activeLayerWindow | L0-L1 | Examples first, schema second. |
| readinessProfile | pilot | Candidate Craft development artifact. |

## Objective Summary

- Objective: refine the recursive ledger examples and schema enough to decide the next Craft development step.
- Primary inputs: [CRAFT-RECURSIVE-LEDGER-DEFINE.md](CRAFT-RECURSIVE-LEDGER-DEFINE.md), [CRAFT-RECURSIVE-LEDGER-GLOSSARY.md](CRAFT-RECURSIVE-LEDGER-GLOSSARY.md), [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md).
- Success condition: two refined artifacts exist or return clear blockers that can guide the next decision.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Realistic type/lane examples demonstrate nested and cross-context ledger behavior. | L0 | Existing type system | Review examples against acceptance criteria in this work-pack. |
| S-002 | Minimal recursive ledger schema reflects the examples and keeps future scoring/delegation possible. | L1 | S-001 | Review schema fields against examples and gate rules. |

## Task Status Board

| Task ID | Goal | Layer | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| CRAFT-REFINE-001 | Refine typed examples for blockers, gates, enablers, operational lanes, and role hints. | L0 | [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md) | pass | completed |
| CRAFT-REFINE-002 | Refine the minimal recursive-ledger schema from the examples. | L1 | [CRAFT-RECURSIVE-LEDGER-DEFINE.md](CRAFT-RECURSIVE-LEDGER-DEFINE.md) | pass | completed |

## Task Contracts

### CRAFT-REFINE-001

Goal:

Create [CRAFT-LEDGER-TYPE-EXAMPLES.md](CRAFT-LEDGER-TYPE-EXAMPLES.md) with a small but meaningful example set.

Required examples:

- root Craft context,
- child recursive-ledger context,
- at least one cross-context blocker,
- at least one enabler,
- at least one gate using `qa`, `validator`, or `auditor`,
- at least one `business` lane item,
- at least one `tech` lane item,
- at least one example where `type + lane -> role` is obvious,
- at least one example where multiple lanes require coordination,
- at least one blocker that starts raw and must go through `blocker_refiner` before resolution.

Done criteria:

- examples use stable local IDs,
- examples include `kind`, `base_type`, `primary_lane`, optional `secondary_lanes`, `status`, `source_id`, `target_id`, `reason`, and `evidence`,
- examples identify what would be delegated later but do not execute delegation,
- examples show that blockers cannot move to `resolved` until refined or explicitly waived,
- examples expose any confusing type/lane choices as open questions.

Validation:

- manual review against [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md) validation rules.

Recommended `/refine` target:

```text
/refine development/craft/WORK-PACK.md --task CRAFT-REFINE-001
```

### CRAFT-REFINE-002

Goal:

Create [CRAFT-RECURSIVE-LEDGER-DESIGN.md](CRAFT-RECURSIVE-LEDGER-DESIGN.md) defining the minimal ledger schema.

Required schema sections:

- context rows,
- artifact rows,
- relation rows,
- typed blocker/gate/enabler rows,
- operational lane fields,
- role-hint fields,
- status and gate values,
- blocker refinement lifecycle,
- validation rules,
- open conflict policy for multiple lanes or multiple types,
- future scoring placeholders without scoring weights.

Done criteria:

- schema can represent every example from `CRAFT-REFINE-001`,
- schema distinguishes condition type, lane, and role hint,
- schema includes `refinement_status` and `closure_condition` for blockers,
- schema keeps work-pack as an owned artifact, not the whole ledger,
- schema does not require runtime command integration.

Validation:

- manual trace from each example row in [CRAFT-LEDGER-TYPE-EXAMPLES.md](CRAFT-LEDGER-TYPE-EXAMPLES.md) to a schema field.

Recommended `/refine` target:

```text
/refine development/craft/WORK-PACK.md --task CRAFT-REFINE-002
```

## Blockers And Gaps

| ID | Scope | Description | Severity | Next Action |
| --- | --- | --- | --- | --- |
| GAP-001 | CRAFT-REFINE-001 | Lane names may change after examples. | low | Record proposed changes in the example artifact. |
| GAP-002 | CRAFT-REFINE-002 | Markdown-only versus Markdown plus structured index remains undecided. | medium | Let examples drive the schema decision. |
| GAP-003 | future | Priority scoring remains deferred. | low | Revisit after schema examples are stable. |

## Gate Checks

1. Work stays under `development/craft/`.
2. No canonical registry, runtime, command, sigil, or spell mutation.
3. `/refine` should process one task at a time.
4. CRAFT-REFINE-002 should consume the output or blockers from CRAFT-REFINE-001.
5. If examples cannot make lane/type distinctions clear, stop before schema design and revise the type model.
6. Any blocker marked resolved without refinement evidence should fail review unless an explicit waiver decision is recorded.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-05-27 | Minimal refinement work-pack created for examples and schema. | Codex |
| 2026-05-27 | CRAFT-REFINE-001 completed; examples artifact created. | Codex |
| 2026-05-27 | CRAFT-REFINE-002 completed; schema design artifact created. | Codex |
