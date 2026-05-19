# TASK-CLO-002: Author SKILL Contract

## Goal

Create `arcana/concept-layer-optimizer/SKILL.md` as the executable sigil contract.

## Layer

L0 Candidate Package

## Micro-Layers

- L0.2 SKILL Execution Contract
- L0.3 Balance And Complexity Contract
- L0.4 Navigation Closeout

## Source Contracts

- [../../SIGIL-HANDOFF.md](../../SIGIL-HANDOFF.md)
- [../../MODE-TECHNIQUE-SURFACE-DESIGN.md](../../MODE-TECHNIQUE-SURFACE-DESIGN.md)
- [../../techniques/README.md](../../techniques/README.md)
- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)

## Inputs

- README draft from TASK-CLO-001,
- approved handoff and surface design,
- TechniqueSpec index and individual technique files,
- local glossary.

## Output Artifact

- `arcana/concept-layer-optimizer/SKILL.md`

## Implementation Steps

1. Create a Codex skill contract with name, description, and metadata.
2. Define trigger conditions and non-trigger conditions.
3. Encode the first action: confirm design intent, target context, output artifact, budget, and recursion depth.
4. Define the discovery baseline: what context must be gathered before proposing layers.
5. Define mode resolution for Compact, Standard, Tournament, Deep, and Validate.
6. Specify the Proposer/Balancer loop, including default two-role behavior and optional tournament behavior.
7. Add recursion and cycle guards: max rounds, stop condition, recomposition proof, and no infinite reduction.
8. Add the complexity balance rule: complexity is allowed only for named tension, concrete failure mode, or confirmed evolution pressure.
9. Add technique activation rules and trace requirements.
10. Add the output contract with objective-output pair, concept layers, smallest coherent unit, recomposition proof, tensions, verdict, and next route.
11. Add the navigable result closeout: start-here, artifact use, decisions, unresolved tensions, and next action.

## Edge Cases

- Do not require true subagents in the skill contract; role simulation must be valid.
- Do not let the Balancer add complexity for elegance alone.
- Do not omit the evolution-profile prompt when future scale is discussed.
- Do not mark a result as pass if it cannot be navigated by a future user or agent.

## Smallest Working Units

| SWU | Micro-Layer | Work | Acceptance |
| --- | --- | --- | --- |
| SWU-CLO-003 | L0.2 | Draft SKILL core process. | Process includes setup, discovery, Proposer/Balancer, techniques, verdict, and handoff. |
| SWU-CLO-004 | L0.3 | Add quality bar, anti-patterns, complexity balance, and output contract. | Reviewable success/failure criteria and complexity exception rule exist. |
| SWU-CLO-005 | L0.4 | Add navigable result closeout to SKILL. | Closeout requires start-here, artifact use, decisions, unresolved tensions, and next action. |

## Verification

```bash
rg -n "objective-output|Proposer|Balancer|Technique|output-contract" arcana/concept-layer-optimizer/SKILL.md
rg -n "<quality-bar>|<anti-patterns>|complexity|evolution profile|<output-contract>" arcana/concept-layer-optimizer/SKILL.md
rg -n "Navigable|start-here|next action|unresolved" arcana/concept-layer-optimizer/SKILL.md
```

## Done When

- SKILL is self-contained enough for manual execution.
- SKILL can produce a valid first-turn confirmation and Standard-mode run envelope.
- SKILL preserves finite recursion and trace requirements.
- SKILL routes lifecycle work instead of executing implementation.
