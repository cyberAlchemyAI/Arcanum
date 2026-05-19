# TASK-CLO-001: Author README

## Goal

Create `arcana/concept-layer-optimizer/README.md` as the human-facing package entrypoint.

## Layer

L0 Candidate Package

## Micro-Layers

- L0.1 README Surface
- L0.4 Navigation Closeout

## Source Contracts

- [../../SIGIL-HANDOFF.md](../../SIGIL-HANDOFF.md)
- [../../GLOSSARY.md](../../GLOSSARY.md)
- [../../DESIGN-CONTINUATION-REVIEW.md](../../DESIGN-CONTINUATION-REVIEW.md)
- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)

## Inputs

- approved Concept Layer Optimizer design packet,
- local glossary terms,
- CyberAlchemy method principles,
- current implementation layering and task sequence.

## Output Artifact

- `arcana/concept-layer-optimizer/README.md`

## Implementation Steps

1. Create the README as the first human navigation surface for the sigil package.
2. Explain the problem the sigil solves: finding the best optimization point between the smallest working unit and the user's working context.
3. Add `Use When` and `Do Not Use When` sections.
4. Add the first-turn prompt contract: seed point, target context, output artifact, optimization goal, budget, and recursion depth.
5. Summarize modes without duplicating the full SKILL process: Compact, Standard, Tournament, Deep, and Validate.
6. Summarize the technique pack and link to the development technique index.
7. Describe the expected output artifact and final navigable result.
8. Add a `Start Here` section that tells future users and agents which file to read next.
9. Link to the development packet, future examples directory, validation report, and implementation plan.

## Edge Cases

- Do not make the README the executable contract; that belongs in `SKILL.md`.
- Do not present all techniques as mandatory for every run.
- Do not imply registry promotion or runtime availability before those layers pass.
- If examples or validation do not exist yet, link to their planned locations and mark them as planned.

## Smallest Working Units

| SWU | Micro-Layer | Work | Acceptance |
| --- | --- | --- | --- |
| SWU-CLO-001 | L0.1 | Draft README usage surface. | README has purpose, use/do-not-use, mode summary, objective-output artifact, and next route. |
| SWU-CLO-002 | L0.4 | Add README navigation and links. | README includes start-here guidance and links to development packet, examples, validation, and SKILL. |

## Verification

```bash
rg -n "Use When|Do Not Use|Modes|Output Artifact|Next" arcana/concept-layer-optimizer/README.md
rg -n "Start Here|development|examples|SIGIL-HANDOFF|VALIDATION" arcana/concept-layer-optimizer/README.md
```

## Done When

- README exists and is navigable.
- README states the objective-output artifact and start-here path.
- README does not duplicate the full SKILL process.
- README links to the development packet and examples.
