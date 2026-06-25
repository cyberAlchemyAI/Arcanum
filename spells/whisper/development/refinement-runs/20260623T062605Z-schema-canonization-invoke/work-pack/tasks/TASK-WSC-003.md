# TASK-WSC-003 - Canonical Schema Package Creation

- Layer: L1 package creation
- Status: complete
- Parent work-pack: `../../WORK-PACK.md`

## Objective

Create the stable Whisper schema package under `arcanum/spells/whisper/schemas/`
from reviewed field contracts and example fixtures.

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Validation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-WSC-003 | Create canonical schema package files. | SWU-WSC-002 complete in `../../CANONICAL-SCHEMA-PACKAGE-SPEC.md` | `arcanum/spells/whisper/schemas/**` only. | README, base schema contract, and examples exist. | YAML parse; validator compatibility checks; path-reference scan. | task-session |

## Implementation Detail

Do not copy the development substrate wholesale. Extract stable field contracts
from reviewed evidence and move article-specific values into examples.

Base schema candidates:

- `text_intent_substrate.metadata`
- `transport_schema`
- `scu_candidate_set`
- `pareto_tournament`
- `composition_parts`
- `draft_artifact`
- `validation`
- `learning_residue`
- optional `readability_dynamics`

Example-only candidates:

- article title,
- author source context,
- reference candidates,
- Draft 02 sequence relation,
- exact body parts for one post.

## Gate Evidence

The package specification is complete in
`../../CANONICAL-SCHEMA-PACKAGE-SPEC.md`.

Use the exact package shape, field ownership, example policy, validation
commands, and non-goals defined there. Do not refresh
`arcanum/spells/whisper/README.md` in this SWU.

## Completion

`SWU-WSC-003` completed on 2026-06-23.

Acceptance evidence:

- `arcanum/spells/whisper/schemas/README.md`
- `arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml`
- `arcanum/spells/whisper/schemas/examples/substack-language-ai.yaml`
- `arcanum/spells/whisper/schemas/examples/substack-object-first-abstraction.yaml`
- `arcanum/spells/whisper/schemas/examples/readability-dynamics.yaml`
- `../../TASK-SESSION-CONTEXT-SWU-WSC-003.md`
- `../../TASK-SESSION-SWU-WSC-003-REPORT.md`

The next Task Session unit is `SWU-WSC-004`.
