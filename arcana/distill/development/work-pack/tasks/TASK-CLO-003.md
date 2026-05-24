# TASK-CLO-003: Build Validation Examples

## Goal

Create validation examples that prove expected sigil behavior before runtime adapter work begins.

## Layer

L1 Behavior Validation

## Micro-Layers

- L1.1 Golden Runs
- L1.2 Technique Trigger Runs
- L1.3 Drift And Failure Runs

## Source Contracts

- [../../SIGIL-HANDOFF.md](../../SIGIL-HANDOFF.md)
- [../../IMPLEMENTATION-PLAN.md](../../IMPLEMENTATION-PLAN.md)
- `arcana/distill/README.md`
- `arcana/distill/SKILL.md`

## Inputs

- completed README and SKILL from L0,
- output contract from the SKILL,
- technique pack specs,
- known failure cases from design review.

## Output Artifacts

- `arcana/distill/development/examples/`
- example index or runbook inside the examples directory

## Implementation Steps

1. Create the examples directory.
2. Add golden examples that show normal successful behavior.
3. Add technique-trigger examples that show when a technique activates, what it contributes, and when it is deferred.
4. Add negative examples for blocked or flagged outcomes.
5. Make every example include a prompt, relevant input context, expected output body, expected verdict, and acceptance notes.
6. Keep expected outputs realistic enough that TASK-CLO-004 can validate the SKILL against them.

## Required Examples

- Standard mode pass.
- Compact mode pass or a documented reason Compact is covered by Standard-mode simplification.
- Tournament mode pass.
- Technique-trigger cases for Cynefin, TRIZ, morphological analysis, set-based design, Wardley mapping, and navigable result check where relevant.
- Validate mode flag.
- Infinite reduction block.
- Premature complexity flag.
- Missing evolution profile flag.
- Lost recomposition block.
- Objective-output artifact drift.
- Navigable-result downgrade.

## Edge Cases

- Do not write examples as summaries only; include real expected output bodies.
- Do not activate every technique in a single example just to show coverage.
- If a technique is not relevant to a case, the example should say why it remains deferred.
- Negative examples must give repair guidance, not just failure labels.

## Smallest Working Units

| SWU | Micro-Layer | Work | Acceptance |
| --- | --- | --- | --- |
| SWU-CLO-006 | L1.1 | Create golden passing examples. | Standard and Compact or Tournament examples include real expected outputs. |
| SWU-CLO-007 | L1.2 | Create technique trigger examples. | Technique examples show activation reason, contribution, and deferral/deactivation when relevant. |
| SWU-CLO-008 | L1.3 | Create negative and drift examples. | Infinite reduction, objective-output drift, premature complexity, missing evolution profile, and navigation downgrade examples exist. |

## Verification

```bash
rg -n "Expected Verdict|Prompt|Expected Output|Technique|pass|flag|block" arcana/distill/development/examples
```

## Done When

- Example files include prompts and real expected output bodies.
- Each example states expected verdict.
- Each technique-trigger example states activation reason and contribution.
- Examples cover objective-output and navigability contracts.
