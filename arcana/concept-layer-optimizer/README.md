# Concept Layer Optimizer

Status: candidate Arcana sigil, in development.

Concept Layer Optimizer is an interactive planning sigil for finding the best optimization point between a tiny working unit and the larger context a user is trying to reason about.

It helps design a model, architecture, plan, workflow, or implementation shape by recursively reducing an initial seed into coherent concept layers, testing whether smaller units still make sense, and recomposing the selected unit back into the upper design.

The goal is not to make the smallest possible fragment. The goal is to find the smallest coherent unit that still has meaning, responsibility, inputs, outputs, and a recomposition path in the user's target context.

## Start Here

For users and future agents:

1. Read this README to understand when the sigil is useful.
2. Read [development/SIGIL-HANDOFF.md](development/SIGIL-HANDOFF.md) for the full design contract.
3. Read [development/IMPLEMENTATION-LAYERING.md](development/IMPLEMENTATION-LAYERING.md) for the development layer plan.
4. Read [development/IMPLEMENTATION-PLAN.md](development/IMPLEMENTATION-PLAN.md) for task and SWU handoff.
5. Use `development/examples/` and `development/VALIDATION.md` when they are created during validation.

The executable `SKILL.md` is planned in the implementation work-pack. Until it exists, this README is an orientation surface, not the runtime contract.

## Use When

Use Concept Layer Optimizer when:

- an idea, model, architecture, design, or plan feels too broad to implement responsibly,
- a system needs to be decomposed without losing the meaning of the whole,
- the user needs a planning process before committing to one solution,
- a proposed solution may be overbuilt, underbuilt, or prematurely optimized,
- multiple possible designs need to be compared before convergence,
- the work needs a clear relationship between concept layers, smallest coherent unit, and next implementation route.

## Do Not Use

Do not use this sigil when:

- the user already has a small, well-scoped implementation task,
- a deterministic check or direct code change would solve the problem,
- the work only needs a summary, not a concept optimization,
- the user does not need role-based critique or recursive reduction,
- the expected output artifact is unclear and the user is not ready to clarify it.

## First Turn Shape

The sigil should begin by confirming intent and budget before decomposition:

```text
I understand the design intent as: <seed point>.
Target context: <context size and purpose>.
Expected Output Artifact: <data model, architecture design, implemented code structure,
plan, decision record, research map, technique spec, or other concrete result>.
Optimization goal: <clarity, scope, architecture, planning depth, model quality,
implementation readiness, or other explicit goal>.
Recommended budget: Standard - one proposal track, two role conversations
(Proposer and Balancer), two recursive rounds, then reconciliation.
Do you want Compact, Standard, Tournament, or Deep?
```

If the user does not choose a budget, the default is Standard.

## Modes

| Mode | Use When | Shape |
| --- | --- | --- |
| Compact | The user wants a quick bounded pass. | One proposal track, one recursive round, always-on gates only. |
| Standard | Default planning depth is enough. | One Proposer, one Balancer, two recursive rounds, one reconciliation pass. |
| Tournament | Multiple possible designs should compete. | Several proposal tracks, each balanced, followed by evidence-based pitch-off. |
| Deep | The context is high-risk, broad, or strategically important. | More rounds, stronger cycle checks, triggered techniques, premortem, and possible human gates. |
| Validate | An existing design needs review. | Balancer-led critique with optional Proposer repair and readiness verdict. |

All modes must keep finite proposal tracks, finite recursive rounds, cycle guards, and a recorded reason for skipped techniques.

## Output Artifact

Every run should name the concrete result it is optimizing toward. Examples:

- data model structure,
- architecture design,
- implementation plan,
- implemented code structure,
- decision record,
- research map,
- technique spec.

The output artifact is a guide, not a prison. If discovery shows that another artifact shape would solve the objective better, the sigil should rename the output artifact and record why.

## How It Works

Concept Layer Optimizer uses a role loop:

- Proposer builds a candidate concept decomposition or design path.
- Balancer challenges premature complexity, brittle minimalism, wrong abstraction level, missing recomposition, and unsupported assumptions.
- Orchestrator reconciles the proposal and objections into a selected optimization point or a routed blocker.

The core process:

1. Confirm seed point, target context, output artifact, optimization goal, and budget.
2. Build a discovery baseline from available evidence, constraints, unknowns, and assumptions.
3. Identify the broad concept layer that contains the user's frame.
4. Ask what smaller concepts must combine to make that layer work.
5. Test each candidate unit for responsibility, inputs, outputs, abstraction level, evolution profile, and recomposition.
6. Stop reduction when splitting further removes meaning, repeats a prior state, exceeds budget, or creates hidden glue.
7. Select the optimization point where the unit is small enough to work with and large enough to remain meaningful.
8. Produce a navigable result with tensions, deferred complexity, proof of recomposition, and next route.

## Technique Pack

The sigil uses techniques as internal instruments, not as separate modes.

Core techniques include:

- abstraction-level guard,
- recomposition proof,
- evolution profile,
- frame-expiry note,
- cognitive load check,
- requisite variety check,
- boundary-object check,
- concept-vs-knowledge status,
- premortem pass,
- set-based tournament,
- navigable result check.

See [development/techniques/README.md](development/techniques/README.md) for the current TechniqueSpec index.

## Complexity Balance

The sigil should not introduce complexity because it is elegant, reusable, or theoretically complete.

Complexity is justified only when the current context has a named tension that the simpler unit cannot responsibly handle. Future scale is in scope only when the evolution profile is concrete, such as expected variants, repeated integrations, growing policy rules, multiple actors, scaling volume, migration needs, or governance review.

When the evolution profile is unknown, preserve a clear boundary and defer the heavier mechanism.

## Expected Result Shape

A complete run should produce a result shaped like:

```markdown
## Concept Layer Optimizer Result

- Target context: <context summary>
- Objective and output artifact: <objective; artifact shape>
- Mode and budget: <compact | standard | tournament | deep | validate>
- Proposal tracks: <count and role summary>
- Recursive rounds: <count completed / budget>
- Verdict: pass | flag | block
- Current smallest coherent unit: <unit name and responsibility>
- Optimization point: <why this unit is the best size for the target context>
- Concept layer map: <broad layer to selected unit>
- Technique pack trace: <techniques run, skipped, triggered, and outcomes>
- Closure and recomposition proof: <how the unit closes and recomposes upward>
- Evolution profile: <expected evolution and smallest extension boundary>
- Deferred complexity: <what was deferred and why>
- Tension ledger: <resolved and unresolved tensions>
- Navigation guide: <where to start, what changed, what remains unresolved, and how to use the result>
- Next route: implementation-layering | robot-talks | decision-gate | invoke design | invoke plan | task-session | deferred
```

## Next Routes

Concept Layer Optimizer does not execute the implementation itself. It routes the result to the next lifecycle owner:

- [implementation-layering](../../transmutations/implementation-layering/) when the selected unit needs phased implementation planning,
- [robot-talks](../robot-talks/) when cross-layer tensions need independent investigation,
- [decision-gate](../decision-gate/) when a blocker choice prevents selecting an optimization point,
- [invoke design](../../spells/invoke/) or [invoke plan](../../spells/invoke/) when the result needs governed lifecycle authoring,
- [task-session](../task-session/) when the work is scoped enough to execute.

## Development Status

Current development artifacts:

- [development/SIGIL-HANDOFF.md](development/SIGIL-HANDOFF.md)
- [development/MODE-TECHNIQUE-SURFACE-DESIGN.md](development/MODE-TECHNIQUE-SURFACE-DESIGN.md)
- [development/techniques/README.md](development/techniques/README.md)
- [development/IMPLEMENTATION-LAYERING.md](development/IMPLEMENTATION-LAYERING.md)
- [development/IMPLEMENTATION-PLAN.md](development/IMPLEMENTATION-PLAN.md)
- [development/WORK-PACK.md](development/WORK-PACK.md)
- [development/PLAN-TRANSPORT.md](development/PLAN-TRANSPORT.md)

Planned validation artifacts:

- `development/examples/`
- `development/VALIDATION.md`

Planned package artifact:

- `SKILL.md`

## Next

The next implementation step is to author the executable `SKILL.md`, then build validation examples and a validation report before runtime adapter or registry promotion work begins.
