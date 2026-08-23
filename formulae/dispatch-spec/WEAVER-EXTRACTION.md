# Weaver Extraction For Arcanum Dispatch

Source copied locally for inspection: `/tmp/weaver-spec`.

Primary source files inspected:

- `/tmp/weaver-spec/README.md`
- `/tmp/weaver-spec/docs/ARCHITECTURE.md`
- `/tmp/weaver-spec/docs/GLOSSARY.md`
- `/tmp/weaver-spec/docs/LIFECYCLE.md`
- `/tmp/weaver-spec/docs/INTEGRATION_MAP.md`
- `/tmp/weaver-spec/docs/INVARIANTS.md`
- `/tmp/weaver-spec/docs/BOUNDARIES.md`
- `/tmp/weaver-spec/examples/multi_agent_orchestration.md`
- `/tmp/weaver-spec/contracts/json/*.schema.json`

## Useful Weaver Concepts

Weaver is a contract repository, not a runtime. Its value for Arcanum is the disciplined split between route selection, authorized execution, safe result framing, orchestration, and audit.

The central lifecycle is:

```text
route -> call -> interpret -> answer -> execute
```

For Arcanum, this becomes:

```text
operator intent
  -> bounded sigil/spell menu
  -> selected route or dispatch graph
  -> gated sigil/spell execution
  -> safe frame and artifact handles
  -> next route, synthesis, or final answer
  -> observed trace for reflection
```

## Extracted Contract Lessons

### Bounded routing

Weaver uses a `ChoiceCard` containing `SelectableItem` objects so an LLM chooses from a small menu rather than an unbounded tool list. Arcanum should copy the principle, not the exact product names:

- present 3-7 viable sigil/spell options when routing is ambiguous,
- avoid injecting full sigil internals into the prompt,
- record the selected item and rationale as route evidence,
- keep candidate capability labels safe and short.

### Capability references

Weaver models executable units as named versioned capabilities. Arcanum can map this to:

- `sigil_id`,
- `spell_id`,
- `mode`,
- `runtime_adapter`,
- optional version or profile,
- ownership boundary.

The dispatch document should reference capabilities by stable id and mode instead of copying their internal instructions.

### Safe frames

Weaver's `Frame` concept is the strongest fit for Arcanum handoffs. A dispatch step should not pass raw internal output by default. It should pass:

- summary,
- structured data,
- artifact handles,
- redaction or residue notes,
- next-route hints.

This fits Arcanum's no-promotion guardrails: a step can emit a candidate, gap, or artifact handle without claiming canonical authority.

### Handles

Weaver's `Handle` is a controlled pointer to raw artifacts. Arcanum can use handles for:

- generated HTML explanation pages,
- work-packs,
- validation reports,
- toy-game outputs,
- research appendices,
- decision records,
- Necronomicon checkpoint material.

The dispatch should say which handles are produced and who can consume them.

### Audit traces

Weaver requires `TraceEvent` records for execution. Arcanum already has observability packages, signal observer, workflow reflect, and observed invocation loops. The missing connective tissue is:

```text
dispatch_id + parent_dispatch_id + step_id
```

These fields let sibling sigils in a fan-out or tournament be analyzed as one run later.

### DAG orchestration

Weaver's ChainWeaver executes deterministic DAG flows while delegating actual tool execution. Arcanum's equivalent is a Spellcraft/Necronomicon route graph:

- Spellcraft owns reusable spell composition.
- Necronomicon owns active repository route memory.
- Task Session owns bounded execution tasks.
- Experiment Harness owns repeatable validation mechanics.
- Dispatch Spec validates the graph shape.

## Invariants Worth Adapting

| Weaver Invariant | Arcanum Adaptation |
| --- | --- |
| Raw tool output does not enter LLM context by default. | Sigil outputs cross steps as frames or handles, not uncontrolled raw blobs. |
| Every execution is authorized and auditable. | Every dispatch step has a gate result and trace event. |
| Routing does not require full schema injection. | Route menus contain short capability cards, not copied skill bodies. |
| Core contracts are minimal and stable. | Dispatch core should stay small; Arcanum-specific metadata belongs in extensions. |
| ChainWeaver delegates execution. | Dispatch Spec validates; it does not execute sigils. |

## What Not To Import Directly

Do not import Weaver's repository split as Arcanum structure. Arcanum already has tiers:

- Formulae for deterministic checks,
- Transmutations for bounded synthesis,
- Arcana for autonomous orchestration,
- Spells for composition.

Do not make dispatch shapes a closed enum forever. Arcanum needs an open poetic/operator surface, but the first schema should still name common starter patterns so validators and examples have traction.
