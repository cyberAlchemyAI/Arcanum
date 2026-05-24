# TASK-CLO-004: Run Manual Validation

## Goal

Create `arcana/distill/development/VALIDATION.md` that reviews examples against the sigil contract.

## Layer

L1 Behavior Validation

## Micro-Layers

- L1.4 Validation Report

## Source Contracts

- [../../SIGIL-HANDOFF.md](../../SIGIL-HANDOFF.md)
- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)
- [../../../../sigil-development/SKILL.md](../../../../sigil-development/SKILL.md)
- [../../../../../framework/QUALITY-BAR.md](../../../../../framework/QUALITY-BAR.md)

## Inputs

- completed README and SKILL,
- validation examples from TASK-CLO-003,
- sigil-development quality bar,
- implementation layering gate rules.

## Output Artifact

- `arcana/distill/development/VALIDATION.md`

## Implementation Steps

1. List every validation example and its expected verdict.
2. Review the example output against the SKILL output contract.
3. Record actual review result: pass, flag, or block.
4. Record micro-layer coverage for L1.1 through L1.4.
5. Identify blocker gaps separately from non-blocker improvement gaps.
6. Decide whether L2 runtime work may begin.
7. If validation reveals contract drift, route the fix back to TASK-CLO-001 or TASK-CLO-002 before promoting.

## Edge Cases

- Do not approve runtime work if examples do not include real output bodies.
- Do not hide output-contract drift as wording polish.
- Do not count a mode as validated if it is only named but not exercised.
- If examples are incomplete but useful, return `flag`, not `pass`.

## Smallest Working Units

| SWU | Micro-Layer | Work | Acceptance |
| --- | --- | --- | --- |
| SWU-CLO-009 | L1.4 | Write validation report. | Report records examples, micro-layer coverage, verdicts, gaps, and L2 promotion decision. |

## Verification

```bash
rg -n "pass|flag|block|L1.1|L1.2|L1.3|L1.4|promotion" arcana/distill/development/VALIDATION.md
```

## Done When

- VALIDATION.md exists.
- Validation report distinguishes blocker and non-blocker gaps.
- Validation report states whether L1.1 through L1.4 are covered.
- Runtime work is either approved or deferred with reason.
