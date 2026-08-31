# Fixture: INV-PLAN-ATOMICITY-BLOCK-001

## Scenario

A medium-complexity work-pack has complete SWU fields but its first SWU is a
task-shaped bundle.

## User Request

Plan a responsive operator workbench from approved design outputs.

## Inputs

- Approved design and source references: present.
- Work-pack output mode: split.
- First SWU goal: build semantic shell, desktop grid, mobile navigation, and a
  user-facing state mapper while preserving behavior.
- Candidate child units: semantic shell, desktop grid, mobile navigation, state
  mapper; each has an independent browser or unit acceptance check.
- Split analysis: omitted.

## Expected

- Phase status: `block`
- SWU atomicity: `block`
- First-unit narrowness: `block`
- Next route: `plan repair`
