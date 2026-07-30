---
artifact: goal-decision-frontier-experiment-invoke-package
status: pass
stages: define-design-plan
lifecycle_owner: spellcraft
authority_effect: none
---

# Goal Decision Frontier Experiment

This directory is the governed Invoke package for a fixture-only experiment
that tests whether a Wayfinder-style decision DAG can improve Goal without
collapsing decision discovery into implementation execution.

The package is planning evidence only. It changes no canonical Craft schema,
Goal runtime, Invoke contract, tracker, or lifecycle state. No SWU is selected.

## Route

```text
Discovery
  -> Invoke Define
  -> Invoke Design
  -> Invoke Plan
  -> Spellcraft review
  -> explicit SWU selection, if approved
```

The intended implementation target is
`spells/goal/development/decision-frontier-experiment/`, but this Invoke run
does not create it.

## Entry Points

- [Discovery](DISCOVERY.md)
- [Specification](SPEC.md)
- [Architecture](ARCHITECTURE.md)
- [Work pack](WORK-PACK.md)
- [Invoke result](INVOKE-RESULT.md)
