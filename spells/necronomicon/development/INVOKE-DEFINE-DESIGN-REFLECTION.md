# Invoke Define/Design Reflection For Necronomicon

## Reflection Source

Observed invocation reflection was run for `invoke` after `invoke` produced the Necronomicon define/design package. The content and recommended follow-up belong to the Necronomicon development cycle; the reusable process lesson belongs to the invoke development cycle.

| Field | Value |
| --- | --- |
| Reflected capability | `invoke` |
| Subject artifact | Necronomicon define/design package |
| Subject lifecycle | Necronomicon development cycle |
| Report | `.arcanum/observability/reflections/20260518T142135Z-invoke-reflection.md` |
| Signals analyzed | 2 |
| Thresholds | `output-threshold`, `usage-threshold` |
| Recommendation | targeted update |

## Signal Reading

The generated reflection report is intentionally non-mutating and generic. The useful signal is in the underlying `invoke` telemetry:

| Signal | Evidence | Meaning |
| --- | --- | --- |
| Research authority gap | Earlier invoke run recorded `research-authority` as a medium gap. | Necronomicon needs an explicit interim owner for bounded research. |
| Schema and fixture gap | Define/design telemetry recorded unresolved plan-layer schemas and fixtures. | The next invoke route should be `plan`, focused on contracts and validation examples. |
| Output threshold | Define/design produced six artifacts. | The development pack now has enough surface area to consolidate before adding more prose. |

## Proposed Changes

### 1. Promote Research Ownership To A Settled MVP Decision

Change status from open question to interim decision:

```text
Research remains a Necronomicon mode for MVP.
Invoke research templates are packet shapes, not route ownership.
Extract a reusable research sigil only after repeated non-Necronomicon reuse.
```

Rationale: this resolves the previous authority gap without over-building a new sigil.

Status: applied to `USAGE-VISION.md`.

### 2. Make Plan The Next Lifecycle Route

Run `invoke plan` next, but keep the plan narrow. It should not implement the harness yet.

Plan should produce:

- state schema drafts,
- classifier fixture matrix,
- side-note and unblocker lifecycle fixtures,
- checkpoint format,
- route record format,
- validation commands or review checks,
- smallest implementation slices for MVP.

Rationale: define/design are now good enough; implementation without schemas would cause drift.

Status: proposed.

### 3. Add A Schema Pack Before Runtime Changes

Create a small schema/design pack before changing adapters:

```text
spells/necronomicon/development/schemas/
  active-interaction.schema.json
  side-note.schema.json
  route-decision.schema.json
  gap.schema.json
  checkpoint.schema.md
  unblocker-task.schema.json
```

Rationale: the main risk is not missing prose; it is incompatible state written by different agents.

Status: proposed.

### 4. Add Classifier Fixtures

Add fixture examples for:

- pending response continues active interaction,
- explicit command interrupts,
- side note captures without derailment,
- unblocker queues or runs,
- fresh route selects capability,
- ambiguous turn asks one question,
- checkpoint summarizes side queues and gaps.

Rationale: classification is the core MVP behavior and should be testable before implementation.

Status: proposed.

### 5. Consolidate Development Docs

Keep `DEFINE.md` and `DESIGN.md` as the lifecycle baseline. Treat `USAGE-VISION.md`, `KNOWLEDGE-SUBSTRATE-FLOW.md`, and `INVOKE-DEFINE-DESIGN-REFLECTION.md` as supporting evidence.

Rationale: output-threshold fired because the pack is growing. The next pass should reduce ambiguity, not add more parallel explanations.

Status: proposed.

## Invoke Meta-Instruction

The reusable invoke-level improvement is provenance clarity.

Invoke should record two layers whenever it authors artifacts for another target:

| Layer | Meaning |
| --- | --- |
| Observed capability | The capability that ran, usually `invoke`. |
| Subject artifact | The module, spell, sigil, feature, or development pack being authored. |

Reflection should then split gaps by owner:

| Gap Type | Owner | Example |
| --- | --- | --- |
| Invoke gap | `invoke` development cycle | Template routing ambiguity, missing output contract field, provenance confusion. |
| Subject gap | Target artifact development cycle | Necronomicon schemas, classifier fixtures, checkpoint format. |

For this run, the subject gaps remain Necronomicon-cycle work. The invoke-cycle improvement is to add target artifact provenance to invoke outputs, transport reports, and telemetry closeout.

Status: applied to `spells/invoke/README.md`.

Detailed rollout plan: [OBSERVABILITY-PROVENANCE-PLAN.md](OBSERVABILITY-PROVENANCE-PLAN.md).

## Recommended Next Action

Run:

```text
invoke plan Necronomicon MVP from DEFINE.md and DESIGN.md, focusing on schemas, classifier fixtures, side-note/unblocker lifecycle, checkpoint format, and smallest implementation slices.
```

Do not start implementation until the plan resolves the schema and fixture gaps.
