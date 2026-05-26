# Arcanum Dispatch Synthesis

## Core Idea

The operator should be able to write Arcanum-fluent sentences that name sigils, techniques, and composition patterns:

```text
Use dialectics to explore/exploit, then distill, x-ray the architecture, run toy games, and use a Pareto-aware decision process to find the best abstraction for this problem.
```

Necronomicon interprets the sentence into Arcanum vocabulary, Dispatch Spec validates the resulting route, Spellcraft turns recurring routes into spells, and Observed Invocation Loop ties the steps together with one `dispatch_id`.

The dispatch object is the missing middle between poetic operator language and executable sigil sequences.

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

### 5. SRU/SWU Reduction

Find the smallest responsible unit before planning or execution.

```text
craft SRU reasoning -> distill optimization point -> implementation-layering -> task-session SWU
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
Run Necronomicon to recover local vocabulary, use context-builder for evidence, distill to the SRU, then invoke design and plan only if the recomposition proof passes.
```

```text
Use robot-talks for cross-layer tensions, synthesize with distill, run toy games through experiment-harness, and send blocker choices to decision-gate before Spellcraft turns the route into a reusable spell.
```

```text
Use x-ray to expose the current workflow, architecture-pattern-inventory to name reusable patterns, residuality-spec to stress the selected design, then task-session to execute the first SWU.
```

```text
Use Whisper to extract the text intent substrate, run an SRU candidate tournament, draft the artifact, then checkpoint learning residue into Necronomicon without promoting glossary terms.
```

```text
Use Craft to select the SRU/SWU boundary, Invoke to define/design/plan the artifact, Experiment Harness to run controlled tests, and Workflow Reflect to decide whether the spell needs revision.
```

## How Whisper, Craft, And Invoke Interconnect

### Whisper

Whisper is a spell-level example of dispatch composition:

```text
structured-interview-kits
  -> distill text_intent_substrate
  -> distill tournament over SRU candidate sets
  -> Whisper composition plan
  -> draft/review
  -> learning residue
```

Dispatch Spec can represent this as a sequence with one tournament step and one residue ledger. Necronomicon can store the learning residue as session evidence or inventory candidate, but not promote it.

### Craft

Craft supplies the deeper method vocabulary:

- SRU is the smallest coherent/responsible unit.
- SWU is the executable planning case of SRU.
- Residue is the material left unresolved by translation or execution.
- Recomposition proves the small unit still belongs to the larger artifact.

Dispatch Spec should use Craft vocabulary to make step boundaries honest:

```text
each execution step should name its SRU/SWU, validation surface, residue policy, and recomposition target
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
    "arcanum_vocabulary": ["dialectic", "distill", "x-ray", "toy_game", "Pareto", "SRU", "spell"]
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

