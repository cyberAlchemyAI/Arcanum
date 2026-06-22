# TASK-GOAL-VERIFY-EVIDENCE

## Objective

Prove reusable behavior and generated-runtime readiness after the runtime path
exists. This task closes the evidence gap; it does not advance registry status
by itself.

## Layer And Slice Mapping

- Layer: L3
- Slice: S-004
- Wave: W3
- Gate status: ready-after-implementation

## Source Contracts

- `arcanum/spells/goal/README.md` Validation Examples and Registry Readiness
- `../20260620T202601Z-goal-spec-definitions/SPEC.md` Validation Matrix
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/SCHEMAS.md`

## Dependencies

- SWU-GOAL-008 pass.
- Runtime behavior exists for Experiment Harness scenarios.

## Blocker And Gap State

| ID | State | Handling |
| --- | --- | --- |
| B-GOAL-PROMOTION-EVIDENCE | active | Build Experiment Harness evidence before registry readiness. |
| generated-surface boundary | active | Use runtime installer only; do not hand-author generated outputs. |

## Implementation Detail

### Inputs

- Implemented runtime behavior.
- Validation scenarios for low-risk, medium-risk, protected mutation, gap
  discovery, and approval-token behavior.
- Runtime installer or bootstrap path selected by Spellcraft.

### Outputs

- Experiment Harness report.
- Telemetry evidence.
- Runtime installer dry-run or approved apply evidence.
- No-leak and diff-hygiene evidence.

### Ordered Rules

1. Build scenario set from README validation examples.
2. Include protected-mutation and approval-required cases.
3. Check gap discovery termination.
4. Check telemetry signal shape.
5. Run public-boundary scan.
6. Generate runtime surface only through installer dry-run or approved installer
   path.
7. Keep registry readiness as review evidence, not automatic status change.

### Edge Cases And Failure Modes

- Scenario passes only because no protected case exists: block evidence.
- Telemetry missing but hidden: flag or block.
- Installer output is hand-authored: block.
- Private profile content appears in public output: block.

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-GOAL-009 | Build reusable behavior evidence through Experiment Harness. | SWU-GOAL-008 | `arcanum/spells/goal/development/experiment-runs/` or equivalent evidence path | Low, medium, protected-mutation, approval, and gap-discovery scenarios are reported. | Experiment Harness report. | experiment-harness validation scenario set. | manual | Runtime evidence is input; reusable proof is separate. |
| SWU-GOAL-010 | Verify generated runtime package readiness through installer path. | SWU-GOAL-009 | generated runtime outputs through installer only | Runtime package generation is dry-run or approved installer result; no hand-authored generated surface. | Installer evidence and diff hygiene. | runtime installer validation plus public-boundary scan. | manual | Do not edit generated `SKILL.md` directly. |

## Smallest Working Unit Exemption

This is a verification/evidence task. It still has SWUs because the evidence
and generated-readiness checks have distinct owners and gates.

## Expected Result Shape

```yaml
swu_id: SWU-GOAL-009
result: pass | flag | block | interrupted
capability_ref: experiment-harness
receipt_kind: native-stage
receipt_artifact: <path or none>
files_touched:
  - <path>
validation:
  - <command or review check and result>
blockers:
  - <blocker or none>
residue:
  - <residue or none>
reroute: <next owner or none>
handoff_note: <what the parent coordinator needs next>
```

## Synchronization Rules

- SWU-GOAL-010 cannot claim readiness if SWU-GOAL-009 blocks.
- Registry readiness requires owner review after evidence; do not mutate
  registry state from this task.

## Completion Evidence

Pending.
