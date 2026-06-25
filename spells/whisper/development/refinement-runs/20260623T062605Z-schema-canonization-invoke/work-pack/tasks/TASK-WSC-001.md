# TASK-WSC-001 - Schema Artifact Inventory And Classification

- Layer: L0 review
- Status: complete
- Parent work-pack: `../../WORK-PACK.md`
- Selected SWU: `SWU-WSC-001`

## Objective

Inventory every Whisper schema-bearing artifact and classify whether it is a
canonical source candidate, example candidate, provenance-only evidence,
generated artifact, or superseded artifact.

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Validation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-WSC-001 | Produce `SCHEMA-ARTIFACT-AUDIT.md`. | none | This invoke run folder only. | Audit matrix cites every relevant artifact and classifies field families. | `rg`, `find`, YAML parses, draft validator compatibility check. | task-session |

## Implementation Detail

1. Inventory candidate files under `arcanum/spells/whisper/` using `find` and
   `rg` for `schema`, `substrate`, `pareto_tournament`, `composition_parts`,
   `readability_dynamics`, and `refresh`.
2. Parse candidate YAML substrates.
3. Record field families:
   - base metadata,
   - transport schema,
   - SCU candidate set,
   - Pareto tournament,
   - composition parts,
   - draft/review/validation/learning residue,
   - readability dynamics.
4. Classify each artifact:
   - `canonical-source-candidate`,
   - `example-candidate`,
   - `provenance-only`,
   - `generated`,
   - `superseded`.
5. Name which fields must stay example-only because they are article-specific.

## Acceptance Evidence

- `SCHEMA-ARTIFACT-AUDIT.md`
- `TASK-SESSION-CONTEXT.md`
- `TASK-SESSION-WORKPACK-REPORT.md`
- Command output summary for inventory and YAML parse checks.
- Compatibility check against the current Draft 02 substrate.

## Completion

`SWU-WSC-001` completed on 2026-06-23. The L0 audit is done; downstream package
design remains blocked until Spellcraft accepts or revises the L1
package-specification route.
