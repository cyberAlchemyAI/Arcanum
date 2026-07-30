---
artifact: goal-decision-frontier-experiment-spell-handoff
status: proposal
owner: spellcraft
authority_effect: none
---

# Spell Handoff

## Candidate

- Existing spell: `goal`
- Candidate extension: `decision-frontier-experiment`
- Proposed development root:
  `spells/goal/development/decision-frontier-experiment/`
- Lifecycle owner: Spellcraft

## Capability Boundary

The candidate would add a fixture-only decision frontier reducer and receipts.
It would not change Goal's canonical contract, own Craft state, operate a
tracker, or execute an implementation unit.

## Required Inputs

- [Specification](SPEC.md)
- [Architecture](ARCHITECTURE.md)
- [Witness contracts](WITNESS-CONTRACTS.md)
- [Work pack](WORK-PACK.md)
- Design denominator and selection receipts

## Admission Gate

Spellcraft must:

1. accept the experiment boundary;
2. confirm that Goal development is the correct host;
3. preserve Craft, Invoke, and Task Session ownership;
4. approve exactly one selected SWU, beginning with the narrowest eligible
   candidate if appropriate.

Invoke supplies planning evidence only and makes no lifecycle or execution
decision.

