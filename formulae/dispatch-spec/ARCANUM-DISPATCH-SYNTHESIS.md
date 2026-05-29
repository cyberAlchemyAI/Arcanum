# Arcanum Dispatch Synthesis

## Core Idea

The operator should be able to write Arcanum-fluent sentences that name sigils, techniques, and composition patterns:

```text
Use dialectics to explore/exploit, then distill, x-ray the architecture, run toy games, and use a Pareto-aware decision process to find the best abstraction for this problem.
```

Necronomicon interprets the sentence into Arcanum vocabulary, Dispatch Spec validates the resulting route, Spellcraft turns recurring routes into spells, and Observed Invocation Loop ties the steps together with one `dispatch_id`.

The dispatch object is the missing middle between poetic operator language and executable sigil sequences.

For reusable technique ids and validation expectations, see [TECHNIQUE-CATALOG.md](TECHNIQUE-CATALOG.md). Dispatch documents may cite those ids at the dispatch or step level through `techniques`.

## Vocabulary Layers

| Layer | Meaning | Examples |
| --- | --- | --- |
| Operator phrase | Natural command using Arcanum language | "zig zag research, then distill" |
| Route pattern | Structural shape of execution | sequence, fanout, dialectic, tournament, validation loop |
| Capability reference | Named owner capability | `distill`, `x-ray`, `decision-gate`, `experiment-harness` |
| Frame handoff | Output from one step used by another | research frame -> distill input |
| Gate | Stop/go/checkpoint rule | human approval, Pareto winner, quality bar |
| Residue | What did not resolve cleanly | contradiction, gap, rejected candidate, route miss |
| Spell candidate | A reusable sequence worth promoting through Spellcraft | "abstraction research spell" |

## Composition Taxonomy

### 1. Sequence

One step feeds the next.

```text
context-builder -> distill -> invoke plan -> task-session
```

Use when the work has a clear lifecycle order.

### 2. Zig Zag

Alternate generation and critique, or exploration and exploitation, until a stop condition.

```text
robot-talks investigate -> structured-interview-kits interrogate -> distill repair -> robot-talks verify
```

Use when early claims are likely to be wrong unless challenged.

### 3. Dialectic

Two or more roles debate a tension while preserving stable disagreement.

```text
Proposer lane: distill candidate A
Balancer lane: residuality-spec stressors
Synthesis: decision-gate or parent synthesis
```

Use when the problem has competing principles, such as speed vs correctness or abstraction vs locality.

### 4. Tournament

Several proposal tracks compete under explicit evidence, option value, and elimination criteria.

```text
distill --mode tournament
  lanes: schema-first, runtime-first, observability-first
  join: Pareto pitch-off
```

Use when there are multiple plausible designs and premature convergence would be expensive.

### 5. SCU/SWU Reduction

Find the smallest coherent unit before planning or execution.

```text
craft SCU reasoning -> distill optimization point -> implementation-layering -> task-session SWU
```

Use when a broad idea is too large to execute safely.

### 6. X-Ray

Expose a system, architecture, workflow, or plan as a navigable explanation surface.

```text
context-builder -> x-ray -> architecture-pattern-inventory -> decision-gate
```

Use when hidden structure is the problem.

### 7. Toy Game / Controlled Test

Create a small artificial scenario to test whether the selected abstraction behaves.

```text
distill selected abstraction -> experiment-harness toy prompt -> residuality-spec stressor -> repair
```

Use when the idea sounds good but needs low-cost falsification.

### 8. Validation Loop

Run fixture, example, or live validation before promotion.

```text
spellcraft design -> experiment-harness -> signal-observer -> workflow-reflect -> spellcraft revise
```

Use when the route should become reusable.

### 9. Necronomicon Memory Loop

Recover, route, execute, checkpoint, and preserve residue without promoting knowledge silently.

```text
necronomicon resume -> inventory lookup -> context-builder -> selected owner -> checkpoint/gap ledger
```

Use when repository memory and route history matter.

## POLE-Inspired Standards Techniques

The 2023 NPCC / Police Digital Services POLE standards dictionary contributes a useful catalog discipline for `dispatch-spec`: separate entity classes from component standards, separate components from validation rules, record owner/steward/version/status metadata, treat conditional obligations explicitly, and evaluate data quality through accuracy, integrity, timeliness, completeness, conformity, and deduplication.

In Arcanum terms, these become route-shaping checks:

- a dispatch step should not be an orphan record; it needs inputs, outputs, and a consumer or parent dispatch,
- minimum required components should be enough to validate the route without copying the owning capability's internals,
- generic components such as frames, handles, gates, ledgers, and trace events should have stable meanings across routes,
- local capability modes can add validation rules without redefining the base dispatch contract,
- draft/live/deprecated or pass/flag/block status should be explicit rather than inferred,
- route evidence should satisfy completeness and conformity before execution or promotion.

These are catalog and validation techniques only. They do not import POLE domain entities into Arcanum.

## Boundary And Evidence Techniques

Dispatch routes sometimes need to describe how a route crosses into another capability, external plan, approval surface, audit surface, state namespace, or evidence system without making that boundary target the lifecycle owner.

In Arcanum terms, these become route boundary checks:

- a delegated step should name target, input contract, ownership boundary, and blocked fallback;
- dispatch-to-plan projection should be marked `preview`, `metadata-only`, or `requires-translation`, not treated as schema equivalence;
- execution receipts should return session/run ids, artifacts, validation results, approval records, and audit references where available;
- approval mappings should distinguish lifecycle approval from execution authorization;
- artifact contract bridges should not imply promotion readiness;
- repository source, generated evidence, workspace state, and `.arcanum/` state should remain separate unless an explicit handoff artifact coordinates them;
- memory visibility should not become Inventory/Ontology promotion without owner review.

These techniques keep dispatch-spec focused on route shape and boundary claims, not execution ownership.

Possible dispatch sentence:

> "Use task-session with a `delegation_boundary`, map human gates through `approval_semantics_map`, require `execution_receipt_handoff`, and keep `state_namespace_boundary` explicit before bounded execution."

Minimal `boundary_evidence` shape:

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
        "contract": "A handoff artifact names write scope, done criteria, and validation surface.",
        "on_violation": "block"
      }
    ],
    "authority": {
      "lifecycle": "dispatch-spec",
      "execution": "task-session",
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
    "state_namespaces": [
      {
        "namespace": "repo-source",
        "owner": "git/worktree",
        "write_policy": "only inside approved task scope"
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

## Sentence Grammar

The human-facing grammar can stay loose, but Dispatch Spec should translate it into structured slots:

```text
use <pattern or technique> with <capability or role set>,
then <capability/mode>,
using <handoff artifact>,
evaluate by <gate>,
if <condition> route to <repair or next owner>,
for <objective>.
```

Examples:

```text
Use dialectics with proposer/balancer lanes, then distill in tournament mode, then x-ray the winning architecture, and gate the result with Pareto decision criteria for this feature design.
```

```text
Run Necronomicon to recover local vocabulary, use context-builder for evidence, distill to the SCU, then invoke design and plan only if the recomposition proof passes.
```

```text
Use robot-talks for cross-layer tensions, synthesize with distill, run toy games through experiment-harness, and send blocker choices to decision-gate before Spellcraft turns the route into a reusable spell.
```

```text
Use x-ray to expose the current workflow, architecture-pattern-inventory to name reusable patterns, residuality-spec to stress the selected design, then task-session to execute the first SWU.
```

```text
Use Whisper to extract the text intent substrate, run an SCU candidate tournament, draft the artifact, then checkpoint learning residue into Necronomicon without promoting glossary terms.
```

```text
Use Craft to select the SCU/SWU boundary, Invoke to define/design/plan the artifact, Experiment Harness to run controlled tests, and Workflow Reflect to decide whether the spell needs revision.
```

## How Whisper, Craft, And Invoke Interconnect

### Whisper

Whisper is a spell-level example of dispatch composition:

```text
structured-interview-kits
  -> distill text_intent_substrate
  -> distill tournament over SCU candidate sets
  -> Whisper composition plan
  -> draft/review
  -> learning residue
```

Dispatch Spec can represent this as a sequence with one tournament step and one residue ledger. Necronomicon can store the learning residue as session evidence or inventory candidate, but not promote it.

### Craft

Craft supplies the deeper method vocabulary:

- SCU is the smallest coherent unit.
- SWU is the executable planning case of SCU.
- Residue is the material left unresolved by translation or execution.
- Recomposition proves the small unit still belongs to the larger artifact.

Dispatch Spec should use Craft vocabulary to make step boundaries honest:

```text
each execution step should name its SCU/SWU, validation surface, residue policy, and recomposition target
```

### Invoke

Invoke is the authoring front door:

```text
invoke define -> invoke design -> invoke plan -> handoff
```

Dispatch Spec can validate the composed route around Invoke:

- Is the user asking for lifecycle authoring?
- Is there enough context to define?
- Does design have a glossary consistency gate?
- Does plan include implementation layering and SWUs?
- Does the next route belong to Task Session, Spellcraft, Sigil Development, or Experiment Harness?

## Suggested Spell Pattern: Abstraction Research Spell

```text
necronomicon route
  -> context-builder evidence pack
  -> robot-talks cross-layer tensions
  -> distill tournament for candidate abstractions
  -> x-ray winning model
  -> residuality-spec stressors
  -> experiment-harness toy games
  -> decision-gate Pareto choice
  -> invoke design/plan or spellcraft compose
  -> observed invocation loop
```

### Dispatch Steps

| Step | Owner | Pattern | Output |
| --- | --- | --- | --- |
| Recover context | `necronomicon` | route | route frame, capability menu |
| Build evidence | `context-builder` | sequential | context frame |
| Explore tensions | `robot-talks` | fanout/dialectic | tension ledger |
| Select abstraction | `distill` | tournament | optimization point |
| Explain structure | `x-ray` | xray | HTML explanation handle |
| Stress behavior | `residuality-spec` | validation | stressor ledger |
| Test small | `experiment-harness` | toy_game | validation report |
| Choose | `decision-gate` | decision | approved route or block |
| Author reusable form | `invoke` or `spellcraft` | handoff | spec/design/plan or spell contract |

## Evaluation Criteria For Suggested Order

The dispatcher should evaluate a proposed sequence before running it:

| Question | Good Signal | Bad Signal |
| --- | --- | --- |
| Does the first step reduce uncertainty? | Starts with context, route, or vocabulary extraction. | Starts with execution before scope exists. |
| Does each step consume a prior frame? | Handoffs are named. | Steps are listed but not connected. |
| Are critique and validation before commitment? | Dialectic/tournament/toy games before plan promotion. | Decision made before alternatives are tested. |
| Are owner boundaries respected? | Spellcraft composes; Invoke authors; Task Session executes. | One capability claims all lifecycle authority. |
| Is residue preserved? | Gaps and rejected candidates are ledgers. | Failed ideas vanish from the trace. |
| Is promotion gated? | Inventory/ontology/glossary promotion routes to owners. | Session output becomes canonical truth automatically. |

## Dispatch Document Example

```json
{
  "dispatch_id": "dispatch-abstraction-research-001",
  "intent": {
    "raw": "use dialectics to explore/exploit, then distill, x-ray, run toy games, and choose the best abstraction",
    "objective": "research the best abstraction for a problem before implementation",
    "target_artifact": "abstraction research spell",
    "arcanum_vocabulary": ["dialectic", "distill", "x-ray", "toy_game", "Pareto", "SCU", "spell"]
  },
  "mode": "mixed",
  "steps": [
    {
      "step_id": "s1",
      "name": "Recover route context",
      "capability_ref": "necronomicon",
      "pattern": "route",
      "inputs": [{"kind": "intent", "ref": "intent.raw"}],
      "outputs": [{"kind": "frame", "ref": "route-frame"}]
    },
    {
      "step_id": "s2",
      "name": "Explore cross-layer tensions",
      "capability_ref": "robot-talks",
      "pattern": "dialectic",
      "parallel": true,
      "roles": ["explorer", "critic", "synthesizer"],
      "inputs": [{"kind": "frame", "ref": "route-frame"}],
      "outputs": [{"kind": "ledger", "ref": "tension-ledger"}],
      "join_policy": "parent_synthesis",
      "convergence_criteria": ["stable tensions named", "unsupported claims separated"]
    },
    {
      "step_id": "s3",
      "name": "Select smallest coherent abstraction",
      "capability_ref": "distill",
      "mode": "tournament",
      "pattern": "tournament",
      "inputs": [{"kind": "ledger", "ref": "tension-ledger"}],
      "outputs": [{"kind": "frame", "ref": "optimization-frame"}],
      "join_policy": "pareto",
      "convergence_criteria": ["recomposition proof passes", "elimination criteria recorded"]
    }
  ],
  "gates": [
    {
      "gate_id": "g1",
      "kind": "promotion_guardrail",
      "owner": "necronomicon",
      "condition": "candidate knowledge is not promoted without owner route",
      "on_fail": "block"
    }
  ],
  "observability": {
    "dispatch_id_required": true,
    "trace_events": ["dispatch_started", "step_completed", "dispatch_completed"],
    "signal_grouping": "dispatch_id"
  }
}
```
