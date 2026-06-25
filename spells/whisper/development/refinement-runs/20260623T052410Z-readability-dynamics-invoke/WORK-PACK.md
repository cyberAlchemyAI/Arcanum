---
module: whisper-readability-dynamics
version: current
status: draft
updatedAt: 2026-06-23
docType: work-pack
---

# WORK-PACK: Whisper Readability Dynamics

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Spellcraft accepted L0 execution in `SPELLCRAFT-RESULT.md`; promotion remains blocked until experiment evidence exists. |
| complexity | low | L0 execution scope is one SWU with two write-scope paths. Later layers are deferred. |
| outputMode | single-file | Low-complexity L0 plan only. |
| executionPackRef | n/a | Not required for L0. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | Layering companion present. |
| dispatchTechniqueTrace | inline | See Dispatch Technique Trace. |
| distillValidationStatus | pass-with-owner-gate | SCU/SWU boundary passes; owner gate remains. |
| activeLayerWindow | L0 | Validator-only proof. |
| lastUpdatedAt | 2026-06-23 | Initial Invoke plan packet. |
| readinessProfile | pilot | Proof before promotion. |

## Objective Summary

Objective: prepare the first executable SWU for Whisper readability dynamics:
add a non-breaking schema section and validator-only checks for paragraph
density, abstraction load, scan anchors, and discourse movement.

Success condition: a later Task Session can execute `SWU-WHISPER-READABILITY-001`
without reopening design discovery, after Spellcraft accepts the lifecycle route.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Optional readability schema plus validator checks. | L0 | Spellcraft acceptance of lifecycle route. | YAML parse, validator regression, readability flag fixture. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-WR-001 | Add optional readability dynamics schema and validator-only checks. | L0 | low | `DEFINE.md`, `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, `SPELLCRAFT-RESULT.md`, `TASK-SESSION-READABILITY-REPORT.md` | pass | complete |
| TASK-WR-VERIFY | Verify non-breaking behavior and readability flags. | L0 | low | validator and fixture evidence in `TASK-SESSION-READABILITY-REPORT.md` | pass | complete |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WHISPER-READABILITY-001 | TASK-WR-001 | `arcanum/spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/RUNTIME-HANDOFF.md`, `arcanum/spells/whisper/tools/validate-whisper-draft.py`, one target substrate fixture | `DEFINE.md`, `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, `SPELLCRAFT-RESULT.md`, `TASK-SESSION-READABILITY-REPORT.md` | none | `arcanum/spells/whisper/tools/validate-whisper-draft.py`; one existing or new Whisper test substrate under `arcanum/spells/whisper/development/refinement-runs/` | Optional `readability_dynamics` config is supported; old schemas still validate; readability findings report paragraph indexes and configured limits. | `TASK-SESSION-READABILITY-REPORT.md` records old draft validation unchanged plus `readability-dynamics-fixture.yaml` producing paragraph-indexed readability flags. | `python3 arcanum/spells/whisper/tools/validate-whisper-draft.py --schema <schema> --draft <draft>` and `python3 -m py_compile arcanum/spells/whisper/tools/validate-whisper-draft.py` | local-fallback | complete |

## Implementation Detail: TASK-WR-001

Purpose: add validator-only readability governance without changing rendered HTML.

Inputs:

- Loaded Whisper schema mapping.
- Markdown draft text.
- Existing `prose_paragraphs` output.
- Optional `readability_dynamics` mapping.

Outputs:

- Existing blocking errors remain unchanged.
- New readability warnings/flags are emitted when the optional layer exists.
- Validator prints a flag-style status when only readability findings exist.

Algorithm sketch:

1. Load schema as today.
2. Run existing Pareto, opening contract, required-term, word-count, and
   character-count checks first.
3. Read `schema.get("readability_dynamics")`.
4. If absent, return existing behavior.
5. If present, compute per-paragraph word count and simple signal terms:
   paragraph index, sentence count, configured scan-anchor terms, configured
   abstract/internal terms where supplied, and configured example markers.
6. Emit warnings for:
   - paragraph over max words,
   - consecutive dense paragraphs over limit,
   - scan-anchor spacing gap,
   - abstraction-without-example gap when configured terms appear.
7. Treat warnings as `flag` unless a configured rule says `block`.
8. Preserve existing exit behavior for hard errors.

Edge cases:

- Missing PyYAML stays an environment block as today.
- Empty draft still blocks as today.
- Invalid `readability_dynamics` type flags or blocks with a clear message.
- Old schemas do not emit readability findings.

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| B-WR-001 | lifecycle | RESOLVED for L0 execution by `SPELLCRAFT-RESULT.md`; promotion still requires experiment evidence. | Spellcraft | Route `SWU-WHISPER-READABILITY-001` to Task Session. |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| `sequence` | define -> design -> layering -> work-pack -> owner handoff | Later artifacts consume explicit earlier artifacts. | pass |
| `scu_swu_reduction` | L0 boundary | First SWU is schema plus validator only. | pass |
| `recomposition_proof` | L0 -> full readability layer | Validator proof recomposes into renderer and browser layers later. | pass |
| `validation_loop` | SWU acceptance | Each acceptance claim has a command or reviewable check. | pass |
| `owner_boundary_check` | Invoke vs Spellcraft vs Task Session | Direct mutation remains blocked until Spellcraft accepts lifecycle route. | pass |
| `handle_handoff` | downstream execution | Handoff uses artifact paths and source anchors, not copied context. | pass |
| `residue_ledger` | deferred SWUs and threshold tuning | Future renderer/browser/experiment gaps remain visible. | pass |
| `execution_receipt_handoff` | later Task Session | Expected result shape is command evidence plus touched paths. | pass |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit or SWU boundary | pass | `SWU-WHISPER-READABILITY-001` is bounded to optional schema plus validator checks. |
| Recomposition proof | pass | L0 proves the governance layer before renderer and browser work. |
| Hidden acceptance-critical gaps | pass | Spellcraft lifecycle acceptance is recorded in `SPELLCRAFT-RESULT.md`; promotion evidence remains deferred but does not block L0 execution. |
| Deferred complexity | pass | Renderer, browser validation, and experiment harness are deliberately deferred. |
| Navigation to first executable unit | pass | Start at `SWU-WHISPER-READABILITY-001` after owner gate. |

## Future SWUs Not Execution-Ready In This Work-Pack

- `SWU-WHISPER-READABILITY-002`: renderer support for rhythm units.
- `SWU-WHISPER-READABILITY-003`: regenerate and browser-check review HTML.
- `SWU-WHISPER-READABILITY-004`: consume review comments for targeted revision.

These remain roadmap items until L0 evidence exists.

## Expected Task Session Receipt

```yaml
runtime: codex
source_swu: SWU-WHISPER-READABILITY-001
result: pass | flag | block | interrupted
files_touched:
  - arcanum/spells/whisper/tools/validate-whisper-draft.py
  - <one Whisper substrate fixture path>
validation:
  - python3 -m py_compile arcanum/spells/whisper/tools/validate-whisper-draft.py
  - python3 arcanum/spells/whisper/tools/validate-whisper-draft.py --schema <schema> --draft <draft>
remaining_blockers:
  - <blocker or none>
lifecycle_owner_next_step: validate | observe | reflect | iterate | promote
```

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-23 | Initial Invoke work-pack for readability dynamics L0. | Codex |
| 2026-06-23 | Completed `SWU-WHISPER-READABILITY-001` with validator support, a readability fixture, compatibility validation, and task-session evidence. | Codex |
