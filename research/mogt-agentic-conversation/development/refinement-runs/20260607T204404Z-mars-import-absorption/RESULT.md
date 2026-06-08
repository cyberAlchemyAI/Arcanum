---
run_id: 20260607T204404Z-mars-import-absorption
status: complete
verdict: import-mogt-first
---

# MARS Import and Arcanum Absorption Result

## Decision

Use MARS now, but import it through MOGT-local proof before absorbing it into Arcanum canonical capabilities.

MARS already contains the research-project mechanics that the MOGT harness feasibility check found missing. The right move is to treat MARS as a source framework, not as an immediate replacement for Arcanum's `experiment-harness`.

## Direct MOGT Imports

These are safe to adapt in the next MOGT harness SWU.

| MARS Asset | MOGT Use | Import Mode |
| --- | --- | --- |
| `../implementation/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md` | Preserve experiment-local `methodology.md`, `protocol.md`, `sources.md`, `context.md`, `data/*.jsonl`, and `results/*.md`. | Reference/adapt into MOGT development docs. |
| `../implementation/mars/definitions/MARS-PIPELINE.md` | Use S0-S12 and G0-G4 as the research-runner lifecycle frame. | Adapt gate names to MOGT readiness without claiming full MARS conformance. |
| `../implementation/mars/templates/schema-foundation-template.json` | Starting point for `experiments/schema/mogt-run.schema.json`. | Derive, do not copy unchanged. |
| `../implementation/mars/templates/protocol-foundation-template.md` | Gap-check MOGT protocols for methodology, data schema, source requirements, success criteria, and gates. | Reference/adapt. |
| `../implementation/mars/templates/context-bundle-template.md` | Normalize MOGT experiment context bundles and source conflict logs. | Reference/adapt. |
| `../implementation/mars/templates/methodology-profile-template.md` | Check MOGT methodology files for missing reproducibility metadata and adjudication policy. | Reference/adapt. |
| `../implementation/mars/templates/telemetry-signal-schema-template.md` | Define MOGT fixture/harness telemetry signals. | Reference/adapt. |
| `../research/projects/mars/experiments/MARS-DRY-RUN-E1-foundation/protocol.md` | Example of tabletop gate walkthrough style for S4 readiness. | Example only; do not copy as canonical template. |

## Arcanum Absorption Candidates

These should become Arcanum-native only after MOGT fixture proof.

| MARS Pattern | Likely Arcanum Home | Absorption Condition |
| --- | --- | --- |
| Experiment bundle contract | `arcana/experiment-harness` or a new research-harness sigil | MOGT validates schema and fixtures with no live claims. |
| Methodology profile contract | `transmutations/` or research governance sigil | MOGT methodology gap checks prove reusable. |
| Research knowledge stack | `inventory`, `definitions-governance`, and `context-builder` | MOGT shows source/inventory/context chain is enforceable. |
| Research taxonomy and relationships | `ontology-vault` or research graph support | MOGT graph-to-paper mapping is stable. |
| Paper derivation rules | paper-design or publication workflow sigil | MOGT `PAPER-*` refresh demonstrates reduced ambiguity. |
| Multi-source context pattern | `context-builder` extension | MOGT web/prior-art synthesis uses conflict logs successfully. |
| Telemetry signal schema | `observability-setup` / `signal-observer` extension | MOGT fixture runs emit useful workflow/evidence signals. |

## Keep MARS-Owned

Do not import these as Arcanum canonical material:

- `../research/projects/mars/claims/**`
- `../research/projects/mars/results/**`
- `../research/projects/mars/telemetry/signals.jsonl`
- `../research/projects/mars/experiments/**` except as examples
- MARS-specific DomainSpec project fields such as `domainspec_version`, `feature_id`, and `sample_id`
- Copilot runtime copies unless a separate skill-transcription task is approved

## Next Executable Unit

Execute `SWU-MOGT-HARNESS-001` with MARS as local reference evidence:

1. Create `research/mogt-agentic-conversation/experiments/schema/mogt-run.schema.json`.
2. Create `research/mogt-agentic-conversation/tools/validate-mogt-run-jsonl.*`.
3. Create one passing and one failing synthetic fixture under `research/mogt-agentic-conversation/development/fixtures/`.
4. Record validator output in the task result.

This should be treated as MOGT-local import proof, not Arcanum absorption yet.
