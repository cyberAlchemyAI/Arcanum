# Cross-Task Decisions: Goal Spell Plan

| Decision ID | Decision | Source | Effect |
| --- | --- | --- | --- |
| D-GOAL-PACKAGE | Package the capability as one composed spell at `spells/goal`. | Existing Craft decision and README status. | Future work stays inside the spell lifecycle unless explicitly routed elsewhere. |
| D-GOAL-PUBLIC-PRIVATE | Public package ships schema and neutral defaults only. | README and decision-profile schema. | Filled profiles stay outside public artifacts. |
| D-GOAL-ROUTER-ONLY | `goal` routes and gates; owners execute their own internals. | ARCHITECTURE and CONTRACTS. | Task SWUs must not reimplement delegated owner behavior. |
| D-GOAL-PROPOSAL-FIRST | Source-changing progress becomes a staged delta before apply. | README, RULES, CONTRACTS. | Active ledger mutation is not a plan-mode output. |
| D-GOAL-EVIDENCE-SPLIT | Runtime execution evidence and reusable behavior evidence are separate. | README Registry Readiness and CONTRACTS. | Experiment Harness evidence is required before registry readiness. |

## Open Decisions

| Decision ID | Question | Owner | Earliest Route |
| --- | --- | --- | --- |
| OD-GOAL-SCHEMA-HOME | Should design schemas move to a stable public `schemas/` location? | spellcraft | SWU-GOAL-001 |
| OD-GOAL-RUNTIME-SOURCE | Which canonical source or implementation files should L1 mutate? | spellcraft | SWU-GOAL-001 or SWU-GOAL-003 |
| OD-GOAL-INSTALLER-TIMING | Should generated runtime package generation be dry-run first or applied after evidence? | runtime installer/spellcraft | SWU-GOAL-010 |
