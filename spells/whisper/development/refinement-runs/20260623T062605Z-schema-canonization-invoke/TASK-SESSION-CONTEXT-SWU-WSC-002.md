# Task Session Context - SWU-WSC-002

- Task: `SWU-WSC-002`
- Mode: standard
- Files selected: 10 evidence groups
- Snippets selected: 20 selectors
- Obligation coverage: 100 percent
- Noise ratio: low
- Output markdown: `TASK-SESSION-CONTEXT-SWU-WSC-002.md`
- Output index: none
- Handoff pack: none
- Session evidence path: this refinement-run folder
- Strict coverage: pass
- Blockers: 0 for package-spec execution

## Selected Unit

`SWU-WSC-002` writes the canonical Whisper schema package specification. It is a
design/review artifact only. It must not create `arcanum/spells/whisper/schemas/`
or refresh the Whisper README.

## Obligations

| Obligation | Evidence | Status |
| --- | --- | --- |
| Select exactly one ready SWU. | `WORK-PACK.md` marks `SWU-WSC-002` ready and later SWUs blocked. | covered |
| Preserve write scope. | `TASK-WSC-002.md` and `SPELLCRAFT-PACKAGE-SPEC-RESULT.md` restrict writes to this refinement-run folder. | covered |
| Produce package spec. | Expected artifact is `CANONICAL-SCHEMA-PACKAGE-SPEC.md`. | covered |
| Name target files. | Candidate package shape in `TASK-WSC-002.md`; stable home accepted by Spellcraft. | covered |
| Name field ownership. | `SCHEMA-ARTIFACT-AUDIT.md` field-family classification. | covered |
| Name example policy. | Audit separates full example, partial compatibility example, readability optional fixture, generated outputs, and provenance-only artifacts. | covered |
| Name validation commands. | `validate-whisper-draft.py`, YAML parse checks, path-scope checks, and audit validation evidence. | covered |
| Avoid canonical mutation. | `SPELLCRAFT-PACKAGE-SPEC-RESULT.md` still blocks schemas creation, README refresh, and generated mirror edits. | covered |

## Included Context

| Source | Selectors | Use |
| --- | --- | --- |
| `WORK-PACK.md` | control fields, SWU manifest, gap table | Determine ready unit and next blocked units. |
| `work-pack/tasks/TASK-WSC-002.md` | objective, write scope, done criteria, candidate package shape | Task contract. |
| `SPELLCRAFT-PACKAGE-SPEC-RESULT.md` | accepted boundary, forbidden write scope, expected receipt | Owner gate and constraints. |
| `SCHEMA-ARTIFACT-AUDIT.md` | executive finding, classification matrix, field-family classification, proposed boundary, validation evidence | Main evidence for package spec. |
| `arcanum/spells/whisper/README.md` | shared state, artifact lifecycle, review HTML contract, SCU core model | Canonical spell lifecycle contract. |
| `IMPLEMENTATION-LAYERING.md` | L1 package expectations and promotion rules | Layer boundary and future validation. |
| `EXECUTION-PACK.md` | W1 ready state, W2 blocked state | Execution order. |
| `tools/validate-whisper-draft.py` | YAML load behavior, Pareto checks, opening contract, readability dynamics | Current executable validation semantics. |
| `tools/build-whisper-review-html.py` | schema loading, composition part lookup, review payload | Deferred review surface consumer. |
| Candidate YAML fixtures | main substrate, Object sequel substrate, readability fixture | Example policy and validation tiers. |

## Key Findings

1. The canonical package should be a human-readable contract plus YAML fixtures
   first, not a standalone JSON Schema package, because the current executable
   validator consumes YAML substrates directly.
2. The main language-AI substrate is the only full current draft-validator
   fixture.
3. The Object sequel substrate is a partial compatibility fixture until it is
   augmented with `pareto_tournament`, `composition_parts`, and a draft artifact.
4. The readability fixture is an optional extension fixture that should produce
   expected `FLAG` behavior, not base-schema pass behavior.
5. Review payload schema should remain deferred to a later package decision.

