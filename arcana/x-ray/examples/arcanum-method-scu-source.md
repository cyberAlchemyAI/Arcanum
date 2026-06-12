# Arcanum Method SCU X-Ray Source Notes

This source packet supports `arcanum-method-scu.html` and `arcanum-method-scu.lanes.json`.

## Reader Goal

Teach a newcomer how Arcanum arrives at the SCU concept instead of assuming they already know it.

The explanation should show the method pressure step by step:

1. Vague intent needs a governed authoring front door.
2. Invoke turns intent into define, design, plan, handoff, refresh, and work-pack artifacts before lifecycle execution.
3. Work-packs and SWUs make execution boundaries explicit enough for Task Session or runtime handoff.
4. Implementation layering asks what minimum working proof unlocks the next decision.
5. Distill asks what smallest unit still has responsibility, inputs, outputs, closure, and recomposition.
6. SCU is the convergence point: smallest enough to execute or reason about, coherent enough to preserve meaning.
7. Refine keeps the loop honest when the target is vague, incomplete, or needs critique and repair before execution.

## Source-Backed Evidence

- `framework/CYBERALCHEMY-METHOD.md` defines the CyberAlchemy method as converting vague intent and discovered evidence into governed artifacts.
- `framework/CYBERALCHEMY-METHOD.md` lists the method loop as Orient, Discover, Shape, Stabilize, and Evolve.
- `framework/CYBERALCHEMY-METHOD.md` defines Smallest Coherent Unit as the smallest unit that still has meaning, responsibility, inputs, outputs, and recomposition in the current context.
- `framework/CYBERALCHEMY-METHOD.md` names Layered Proof Progression as an evolution primitive: start with a minimum working unit and add bounded layers when each unlocks a distinct decision.
- `spells/invoke/README.md` says Invoke turns vague development intent into governed authoring artifacts and owns intent-to-artifact authoring, including define, design, plan, work-pack creation, and handoff context.
- `spells/invoke/plan.md` says plan mode converts approved design outputs into a governed work-pack and implementation-layering artifact without executing implementation work.
- `spells/invoke/plan.md` says medium and high complexity work-packs require Smallest Working Units with goal, dependencies, write scope, done criteria, acceptance evidence, and verification.
- `transmutations/implementation-layering/SKILL.md` defines Layer 0 as the smallest end-to-end minimum working unit proof that shows the target concept can work.
- `arcana/distill/SKILL.md` selects the smallest coherent concept unit by checking responsibility, inputs and outputs, abstraction level, recomposition, hidden glue, and meaning loss.
- `arcana/refine/SKILL.md` describes Refine as a discovery/design loop for vague targets, design concerns, repository areas, and existing work-packs before next routes.
- `arcana/task-session/SKILL.md` executes one bounded task or SWU end to end, with context building, gates, validation, and synchronized evidence.

## Inferences

- SCU is easier to teach as the meeting point between two questions: "what is the smallest proof that teaches us something?" and "what is the smallest concept that still holds together?"
- Work-packs are not bureaucracy in this story. They are the bridge from a conceptual SCU to an executable SWU, because they preserve write scope, validation, source anchors, and acceptance evidence.
- Refine should appear after the first method pass as a repair loop, not as a mysterious prelude. A reader can understand it once they have seen where vagueness, overlarge units, and premature execution create risk.

## Evidence Boundaries

This example explains the Arcanum method from current repository contracts. It does not prove that every installed runtime adapter is operational. Runtime readiness remains outside this x-ray boundary.
