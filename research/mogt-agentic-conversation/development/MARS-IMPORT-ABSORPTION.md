---
name: MARS Import and Arcanum Absorption
description: Decision summary for using MARS assets in MOGT and later absorbing proven patterns into Arcanum.
created: 2026-06-07
status: ready-for-swu
source_run: refinement-runs/20260607T204404Z-mars-import-absorption
---

# MARS Import and Arcanum Absorption

## Decision

Use MARS now through MOGT-local imports. Absorb generalized patterns into Arcanum only after the MOGT fixture path proves them with local validation.

## Use From MARS Immediately

| MARS Asset | MOGT Use |
| --- | --- |
| `../implementation/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md` | Experiment-local `methodology.md`, `protocol.md`, `sources.md`, `context.md`, `data/*.jsonl`, and `results/*.md` discipline. |
| `../implementation/mars/definitions/MARS-PIPELINE.md` | S0-S12 / G0-G4 research lifecycle and gate framing. |
| `../implementation/mars/templates/schema-foundation-template.json` | Starting shape for a MOGT-specific run JSON schema. |
| `../implementation/mars/templates/protocol-foundation-template.md` | Protocol gap-checking for schema, sources, criteria, and gates. |
| `../implementation/mars/templates/context-bundle-template.md` | Context/source conflict log structure. |
| `../implementation/mars/templates/methodology-profile-template.md` | Methodology profile completeness checks. |
| `../implementation/mars/templates/telemetry-signal-schema-template.md` | Fixture/harness telemetry signal structure. |
| `../research/projects/mars/experiments/MARS-DRY-RUN-E1-foundation/protocol.md` | Tabletop gate-walkthrough example only. |

## Absorb Into Arcanum Later

| Pattern | Candidate Arcanum Home | Proof Needed |
| --- | --- | --- |
| Experiment bundle contract | `arcana/experiment-harness` or a new research-harness sigil | MOGT fixture validation passes. |
| Methodology profile contract | research governance transmutation/sigil | MOGT method checks are reusable. |
| Research knowledge stack | `inventory`, `definitions-governance`, `context-builder` | Source/inventory/context chain is enforceable. |
| Research taxonomy and paper derivation | `ontology-vault` plus paper-design workflow | MOGT graph-to-paper refresh proves value. |
| Multi-source context pattern | `context-builder` | MOGT prior-art conflict handling works. |
| Telemetry signal schema | `observability-setup` / `signal-observer` | Fixture runs emit useful signals. |

## Do Not Import As Canonical Arcanum

- MARS project claims, results, telemetry rows, and evidence snapshots.
- MARS project experiment execution files except as examples.
- DomainSpec-specific schema fields such as `domainspec_version`, `feature_id`, and `sample_id`.
- Copilot runtime skill copies without a separate skill-transcription task.

## Next SWU

Run `SWU-MOGT-HARNESS-001` using MARS as reference evidence:

1. Create `experiments/schema/mogt-run.schema.json`.
2. Create a JSONL validator under `tools/`.
3. Add passing and failing synthetic fixtures under `development/fixtures/`.
4. Record validation output in the task result.

Detailed evidence is in `development/refinement-runs/20260607T204404Z-mars-import-absorption/RESULT.md`.
