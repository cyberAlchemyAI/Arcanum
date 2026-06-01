# Dispatch Spec Glossary

Status: define-stage local glossary. Candidate terms only; no registry or ontology promotion.

| Term | Definition | Status |
| --- | --- | --- |
| Capability reference | A stable id for a sigil, spell, mode, runtime adapter, or transform that may appear in a dispatch step. | local |
| Dispatch document | A structured route contract containing intent, route menu, steps, gates, observability, and promotion guardrails. | local |
| Dispatch ID | Stable identifier that groups all steps and observed signals belonging to one composed run. | local |
| Frame | Safe summary or structured output from one step, suitable for consumption by later steps. Adapted from Weaver vocabulary. | linked |
| Handle | Controlled reference to a raw or larger artifact, such as a report, work-pack, HTML page, or validation output. Adapted from Weaver vocabulary. | linked |
| Operator sentence | Human-written Arcanum-fluent instruction that can be translated into a dispatch document. | local |
| Pattern | The structural shape of a dispatch step: route, sequential, fanout, dialectic, tournament, distill, xray, decision, validation, toy_game, synthesis, or handoff. | local |
| Promotion guardrail | A rule that prevents candidate outputs from becoming canonical without the owning capability. | linked |
| Route menu | A bounded set of selectable candidate routes or capabilities, inspired by Weaver `ChoiceCard`. | linked |
| Step | One dispatch node with capability reference, pattern, inputs, outputs, gates, and optional convergence criteria. | local |
| Technique | A reusable route-shaping or validation method cited by a dispatch document or step. Technique ids live in `TECHNIQUE-CATALOG.md`. | local |
| Component standard | A reusable field or evidence component with one stable meaning across dispatch documents. Adapted from POLE standards-catalog discipline. | linked |
| Conditional obligation | A validation requirement that applies only when a route context triggers it, such as parallel steps requiring a join policy. Adapted from POLE standards-catalog discipline. | linked |
| Data quality dimension | A cross-cutting validation lens such as accuracy, integrity, timeliness, completeness, conformity, or deduplication. Adapted from POLE standards-catalog discipline. | linked |
| Toy game | A small controlled scenario used to test whether an abstraction behaves before larger commitment. | local |
| Trace event | Observability event tied to dispatch, step, capability, and outcome. Adapted from Weaver vocabulary. | linked |
| Zig zag | Alternating generation/critique or exploration/exploitation route pattern. | local |

## Glossary Notes

- `Frame`, `Handle`, `TraceEvent`, `ChoiceCard`, and `SelectableItem` are not imported as canonical Arcanum terms. They are linked concepts from Weaver used to sharpen handoff thinking.
- `SCU`, `SWU`, `residue`, and `recomposition` remain Craft/Arcanum method vocabulary; Dispatch Spec consumes them as step-boundary annotations rather than redefining them.
- Spell and sigil lifecycle terms remain owned by Spellcraft and Sigil Development.
