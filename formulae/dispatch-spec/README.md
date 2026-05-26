# Dispatch Spec

Status: draft Formulae package.

`dispatch-spec` is a deterministic contract for describing how Arcanum sigils and spells are chained, fanned out, debated, validated, and handed off inside a larger spell.

It is inspired by Weaver's separation between routing, execution, safe result frames, orchestration, and audit traces. In Arcanum terms, it gives Necronomicon, Spellcraft, Invoke, and runtime adapters a shared object for answering:

- which sigils are being offered or selected,
- what order they run in,
- whether a step is sequential, fan-out, tournament, dialectic, validation, or synthesis,
- which output frame from one step becomes the input substrate for the next,
- what gates, stop conditions, and residue ledgers must exist,
- whether the proposed order should be evaluated before execution.

## Purpose

The package turns user language such as:

```text
use dialectics to explore/exploit, then distill, x-ray the architecture, run toy games, and use a Pareto-aware decision process to find the best abstraction
```

into an inspectable dispatch document:

```text
intent -> capability menu -> selected sequence -> gated execution -> frame handoffs -> synthesis -> evaluation
```

The Formulae role is validation, not interpretation. A synthesizing capability such as Necronomicon, Invoke, Spellcraft, Distill, or Structured Interview Kits may propose a dispatch document. `dispatch-spec` checks whether the document is well formed.

## Weaver Mapping

| Weaver Concept | Arcanum Dispatch Concept |
| --- | --- |
| `SelectableItem` | Candidate sigil/spell/mode offered to the operator |
| `ChoiceCard` | Bounded route menu, usually 3-7 viable next sigils or patterns |
| `RoutingDecision` | Selected sigil, spell, mode, or dispatch pattern |
| `Capability` | Named Arcanum sigil, spell, runtime adapter, or deterministic transform |
| `CapabilityToken` | Permission/approval scope for an execution step |
| `PolicyDecision` | Gate result: allow, deny, ask, defer, or block |
| `Frame` | Safe output summary from a sigil/spell run |
| `Handle` | Reference to a raw artifact, report, HTML page, work-pack, or ledger |
| `TraceEvent` | Observability signal tied to `dispatch_id` and step id |
| ChainWeaver DAG | Spellcraft/Necronomicon dispatch graph |

## Relationship To Arcanum

`dispatch-spec` does not replace the owner capabilities:

- Necronomicon owns repository memory, route selection, and no-promotion guardrails.
- Invoke owns define/design/plan/handoff authoring.
- Spellcraft owns reusable spell composition and lifecycle judgment.
- Distill owns optimization-point selection, tournament reasoning, and recomposition proof.
- Task Session owns bounded execution.
- Experiment Harness owns repeatable validation runs.
- Signal Observer and Workflow Reflect own observed invocation learning.

`dispatch-spec` only validates the shape of a proposed composition.

## Files

| File | Purpose |
| --- | --- |
| [dispatch.schema.json](dispatch.schema.json) | Draft JSON Schema for dispatch documents. |
| [SKILL.md](SKILL.md) | Formulae execution contract for validating a dispatch document. |
| [WEAVER-EXTRACTION.md](WEAVER-EXTRACTION.md) | Extracted useful concepts from `dgenio/weaver-spec`. |
| [ARCANUM-DISPATCH-SYNTHESIS.md](ARCANUM-DISPATCH-SYNTHESIS.md) | Synthesis, taxonomy, sentence grammar, and example sigil sequences. |

## First Integration Target

The first useful integration is Necronomicon route planning:

```text
user intent
  -> Necronomicon extracts Arcanum vocabulary and candidate capabilities
  -> dispatch-spec validates the proposed route graph
  -> Spellcraft uses the route graph when the sequence should become a reusable spell
  -> Invoke emits authoring artifacts when define/design/plan material is needed
  -> Observed Invocation Loop records dispatch_id across all steps
```

