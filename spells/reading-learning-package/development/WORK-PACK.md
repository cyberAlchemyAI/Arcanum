# WORK-PACK: Reading Learning Package

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | flag | Ready for Spellcraft review; implementation must wait for lifecycle owner acceptance. |
| complexity | medium | Cross-capability spell with source intake, interview, Whisper composition, renderer checks, and validation fixtures. |
| outputMode | split-ready | Single development bundle now; task files may split during Task Session. |
| defineRef | `arcanum/spells/reading-learning-package/development/DEFINE.md` | Source definition. |
| designRef | `arcanum/spells/reading-learning-package/development/DESIGN.md` | Source design. |
| layeringArtifactRef | `arcanum/spells/reading-learning-package/development/IMPLEMENTATION-LAYERING.md` | Layering source. |
| dispatchRef | `arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json` | Route validation source. |
| nextOwner | `spellcraft` | Invoke stops at handoff. |

## Objective

Prepare a Spellcraft-ready candidate spell that creates personalized PDF learning
packages from research towers and source artifacts using `research-tower` and
`whisper`.

## Task Status Board

| Task ID | Goal | Layer | Gate Status | Status |
| --- | --- | --- | --- | --- |
| T-RLP-001 | Draft Spellcraft contract from this package. | L0 | blocked-until-spellcraft-accepts | ready |
| T-RLP-002 | Implement tower/source intake and preset-profile artifacts. | L0 | ready-after-T-RLP-001 | planned |
| T-RLP-003 | Implement example-driven core interview and Whisper substrate bridge. | L0 | ready-after-T-RLP-002 | planned |
| T-RLP-004 | Implement manuscript and source-trace assembly. | L1 | ready-after-T-RLP-003 | planned |
| T-RLP-005 | Implement HTML/PDF assembly and renderer fallback. | L2 | ready-after-T-RLP-004 | planned |
| T-RLP-006 | Add validation fixtures and experiment harness examples for all presets. | L3 | ready-after-T-RLP-005 | planned |
| T-RLP-VERIFY | Verify spellcraft readiness, no-promotion boundaries, and docs. | L3 | ready-after-T-RLP-006 | planned |

## Smallest Working Units

| SWU ID | Parent Task | Goal | Write Scope | Acceptance Evidence | Verification | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-RLP-001 | T-RLP-001 | Create candidate spell contract from handoff without copying full sigil bodies. | `arcanum/spells/reading-learning-package/README.md` or Spellcraft-selected local path. | Spell contract has phases, gates, outputs, observability, and referenced sigils. | Spellcraft validate/review. | spellcraft |
| SWU-RLP-002 | T-RLP-002 | Add tower intake checks and `source-context.md`/gap behavior. | Spell runtime implementation and fixtures. | Missing tower blocks; valid tower emits source-context handles. | Fixture over one existing tower. | task-session |
| SWU-RLP-003 | T-RLP-002 | Add `preset-profile.yaml` schema and starter presets. | Spell runtime docs/schema. | Deep, quick, and medium presets parse and expose defaults. | Schema/example review. | task-session |
| SWU-RLP-004 | T-RLP-003 | Add one-question preset menu and example-driven SCU core interview. | Spell runtime/interview contract. | Each core records accepted/rejected example evidence. | Interview fixture transcript. | task-session |
| SWU-RLP-005 | T-RLP-003 | Bridge preset profile to Whisper `text_intent_substrate`. | Spell runtime/Whisper adapter. | Substrate includes resonance, relevance, trajectory, source handles, validation checks. | Whisper substrate validation fixture. | task-session |
| SWU-RLP-006 | T-RLP-004 | Build `composition-plan.md`, `manuscript.md`, and `source-trace.md`. | Spell runtime/output templates. | Load-bearing claims map to tower/source paths or residue. | Source-trace review fixture. | task-session |
| SWU-RLP-007 | T-RLP-005 | Build HTML/PDF assembly with renderer detection and blocked fallback. | Spell runtime renderer adapter. | PDF produced when renderer exists; otherwise HTML plus explicit renderer gap. | Renderer command or fallback fixture. | task-session |
| SWU-RLP-008 | T-RLP-006 | Add preset fixtures for deep, quick, and medium outputs. | `arcanum/spells/reading-learning-package/development/fixtures/` or experiment-harness path. | Three fixture prompts produce expected pass/flag/block summaries. | Experiment harness report. | experiment-harness |
| SWU-RLP-009 | T-RLP-VERIFY | Validate no-promotion, owner boundaries, docs, and observability. | Spell docs and validation reports. | Spellcraft validation report names pass/flag/block. | `check_markdown_links` plus Spellcraft review. | spellcraft |

## Implementation Detail Notes

### Tower Intake

Required checks:

1. `tower_root` exists.
2. At least one final learning artifact exists, preferably `FINAL-LEARNING-PACK.md`.
3. Source claim evidence exists, preferably `tracks/paper-claim-ledger.md` or an equivalent ledger.
4. Source record exists or the package records a source-record gap.
5. Open residue is copied only as a reference/handle, not as hidden claim text.

### Preset Interview

The interview must produce `preset-profile.yaml` before Whisper drafting. It must
not silently infer all cores from the preset id. The preset id only seeds defaults.

### PDF Assembly

Renderer strategy order:

1. If `pandoc` and a PDF engine are available, render Markdown/HTML to PDF.
2. Else if a browser print route is available, render HTML to PDF through that route.
3. Else emit `learning-package.html`, keep `learning-package.pdf` absent, and mark
   the validation report `flag` with a renderer gap.

No implementation task may mark PDF pass without a deterministic command or
reviewable artifact.

## Validation Strategy

| Validation | Required Evidence |
| --- | --- |
| Link validation | Markdown links in development package pass. |
| Dispatch validation | `reading-learning-package.dispatch.json` validates. |
| Tower fixture | Valid tower fixture passes intake; missing tower fixture blocks. |
| Preset fixture | All three starter presets produce usable preset profiles. |
| Whisper fixture | Substrate and composition plan include all SCU cores. |
| Source-trace fixture | Manuscript sections cite tower/source artifacts. |
| PDF fixture | PDF is rendered or renderer gap is explicit. |

## Blockers And Gaps

| Gap | Severity | Owner | Repair |
| --- | --- | --- | --- |
| Spell contract is not installed yet. | blocker for runtime | spellcraft | Consume `SPELL-HANDOFF.md` and create candidate spell file. |
| Renderer availability unknown. | flag for PDF completion | task-session | Implement renderer detection/fallback. |
| No preset fixtures yet. | blocker for promotion readiness | experiment-harness | Add three example fixtures after spell contract exists. |
| Custom preset persistence policy undecided. | non-blocking design gap | spellcraft | Decide local-output vs `.arcanum` state after L0. |

## Distill Validation

Verdict: `flag`

Reason: the smallest coherent unit is clear and recomposes into the design, but
mutation-capable work must wait for Spellcraft lifecycle acceptance and the PDF
renderer decision.

## Next Route

1. `spellcraft design reading-learning-package --from arcanum/spells/reading-learning-package/development/SPELL-HANDOFF.md`
2. After Spellcraft accepts, execute `SWU-RLP-001`.
3. Use `task-session` one SWU at a time for implementation.
4. Use `experiment-harness` before declaring reusable spell readiness.
