# Dispatch Spec

Status: draft Formulae package.

`dispatch-spec` is a deterministic contract for describing how Arcanum sigils and spells are chained, fanned out, debated, validated, and handed off inside a larger spell or bounded route.

It is inspired by Weaver's separation between routing, execution, safe result frames, orchestration, and audit traces. In Arcanum terms, it gives Necronomicon, Spellcraft, Invoke, Task Session, and related owner capabilities a shared object for answering:

- which sigils are being offered or selected,
- what order they run in,
- whether a step is sequential, fan-out, tournament, dialectic, validation, or synthesis,
- which output frame from one step becomes the input substrate for the next,
- what gates, stop conditions, and residue ledgers must exist,
- whether the proposed order should be evaluated before execution,
- which dispatch techniques justify the route shape.

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
| `Capability` | Named Arcanum sigil, spell, owner capability, or deterministic transform |
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

## Technique Catalog

[TECHNIQUE-CATALOG.md](TECHNIQUE-CATALOG.md) names reusable route-shaping techniques that dispatch documents may cite through `techniques` at the dispatch or step level.

The catalog currently has three source families:

- Arcanum dispatch synthesis techniques such as sequence, zig zag, dialectic, tournament, SCU/SWU reduction, x-ray, toy-game validation, memory loops, frame/handle handoffs, residue ledgers, Pareto gates, and recomposition proof.
- POLE-inspired standards techniques adapted from the 2023 NPCC / Police Digital Services "Minimum POLE Data Standards Dictionary", such as entity classing, minimum component catalogs, component descriptors, conditional obligations, validation rule catalogs, owner/steward metadata, version/status metadata, data-quality dimensions, and orphan-record checks.
- Boundary and evidence techniques for naming delegation boundaries, route projection, execution receipt handoff, approval semantics mapping, artifact contract bridging, state namespace separation, and memory/promotion splits.

The POLE techniques are used as standards-catalog discipline, not policing-domain semantics. They help `dispatch-spec` keep routes system-agnostic, componentized, validated, and traceable.
Boundary and evidence techniques help dispatch documents describe cross-capability and evidence boundaries without making dispatch-spec an execution engine or granting lifecycle promotion authority.

When a route cites boundary/evidence techniques, it can add an optional
`boundary_evidence` block:

```json
{
  "boundary_evidence": {
    "boundaries": [
      {
        "boundary_id": "b1",
        "kind": "capability_handoff",
        "from_owner": "invoke",
        "to_owner": "task-session",
        "applies_to_steps": ["s2"],
        "contract": "Task Session consumes the handoff and returns validation evidence.",
        "on_violation": "block"
      }
    ],
    "authority": {
      "lifecycle": "dispatch-spec",
      "execution": "task-session",
      "validation": "dispatch-spec",
      "promotion": "owning capability"
    },
    "receipts": [
      {
        "receipt_id": "r1",
        "producer": "task-session",
        "required_fields": ["run_id", "artifacts", "validation_result", "residue"],
        "on_missing": "flag"
      }
    ],
    "promotion_splits": [
      {
        "source": "execution evidence",
        "target": "inventory knowledge",
        "rule": "requires owner review before canonical promotion",
        "on_violation": "block"
      }
    ]
  }
}
```

This block validates boundary claims. It does not perform execution or promote
knowledge.

## Files

| File | Purpose |
| --- | --- |
| [dispatch.schema.yml](dispatch.schema.yml) | Draft JSON Schema for dispatch documents. |
| [SKILL.md](SKILL.md) | Formulae execution contract for validating a dispatch document. |
| [WEAVER-EXTRACTION.md](WEAVER-EXTRACTION.md) | Extracted useful concepts from `dgenio/weaver-spec`. |
| [ARCANUM-DISPATCH-SYNTHESIS.md](ARCANUM-DISPATCH-SYNTHESIS.md) | Synthesis, taxonomy, sentence grammar, and example sigil sequences. |
| [TECHNIQUE-CATALOG.md](TECHNIQUE-CATALOG.md) | Reusable dispatch, POLE-inspired standards, and boundary/evidence techniques. |
| [scripts/validate-dispatch.py](scripts/validate-dispatch.py) | Deterministic schema, route-rule, and technique-catalog validator. |

## Validation

Validate one dispatch document:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py <dispatch.json>
```

Run the package fixtures:

```bash
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

The validator emits `VALIDATION=pass|flag|block` and blocks on schema errors, impossible step dependencies, missing validation evidence, invalid technique references, and false promotion authority claims. It flags weak-but-usable route evidence such as unused technique citations or missing stop conditions.

Technique overlays can be represented with `technique_overlays` when a route needs named profiles such as dialectic review, tournament selection, x-ray explanation, toy-game validation, memory recovery, or protected-context handling. Overlays must name their trigger, techniques, affected steps, and validation expectation.

When a route implies role-bound sibling agents, use `subagent_strategy` to make
the strategy explicit before runtime execution. Dispatch Spec validates the
strategy shape, roles, join policy, receipts, and authorization state; the
orchestrating capability shows the strategy and asks permission before spawning
subagents or running delegated stages.

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
