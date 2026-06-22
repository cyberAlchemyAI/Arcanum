# Verification: SWU-GOAL-001

## Required Evidence

The validation report must cover:

- `arcanum/spells/goal/README.md`
- `arcanum/spells/goal/decision-profile.schema`
- `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/SPEC.md`
- `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/DEFINITIONS.md`
- `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/ARCHITECTURE.md`
- `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md`
- `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md`
- `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/SCHEMAS.md`
- `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md`
- `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/PLAN-DISPATCH.json`

## Review Questions

1. Does the packet preserve `goal` as router-only?
2. Are public/private boundaries explicit and sufficient?
3. Are generated runtime surfaces installer-owned?
4. Are runtime SWUs gated behind lifecycle validation?
5. Are schema-home and Craft-sync gaps owned without authorizing mutation?

## Validation Surface

Primary surface:

```text
spellcraft validate arcanum/spells/goal
```

If no direct Spellcraft runner is available, use a reviewable lifecycle
validation report with the same evidence, verdict, blockers, residue, and next
route fields.

## Minimum Receipt

```yaml
swu_id: SWU-GOAL-001
result: pass | flag | block | interrupted
capability_ref: spellcraft
receipt_kind: native-stage
receipt_artifact: <path or none>
files_touched:
  - <path or none>
validation:
  - <command or review check and result>
blockers:
  - <blocker or none>
residue:
  - <residue or none>
reroute: <next owner or none>
handoff_note: <what the parent coordinator needs next>
```
