# Experiment Harness Generalization Design

Status: design candidate for Spellcraft and Sigil Development integration.

## Concept Layer Optimizer Result

- Target context: generalize `experiment-harness` so it becomes the shared validation loop for both `spellcraft` and `sigil-development`.
- Objective and output artifact: produce a design and plan for making reusable spells and sigils start with executable experiments, live loops, observability, and promotion evidence. The output artifact is this design plus the implementation plan in `GENERALIZATION-IMPLEMENTATION-PLAN.md`.
- Mode and budget: Standard; one proposal track, Proposer/Balancer role simulation, two recursive rounds.
- Proposal tracks: one shared-kernel design with two lifecycle adapters.
- Recursive rounds: 2 / 2.
- Verdict: pass.
- Current smallest coherent unit: lifecycle experiment profile.
- Optimization point: a lifecycle experiment profile is small enough to generate from `init-harness.sh`, but large enough to describe what Spellcraft and Sigil Development need without baking their internal lifecycle logic into Experiment Harness.

## Role Conversation Trace

| Role | Claim Or Objection | Reconciliation |
| --- | --- | --- |
| Proposer | Generalize the harness by adding a shared profile contract that any lifecycle authority can request. | Accepted. The profile is the closed unit. |
| Balancer | Do not make Experiment Harness own spell or sigil meaning; it should only own experiment mechanics. | Accepted. Spellcraft and Sigil Development provide lifecycle-specific scenarios and pass criteria. |
| Proposer | Add Spellcraft and Sigil Development starter profiles directly to the harness initializer. | Revised. The initializer should expose profile hooks and starter profiles, but authority-specific prompts remain adapter-owned or generated from lifecycle contracts. |
| Balancer | A single profile may underfit future capability types. | Deferred with an extension boundary: profile schema includes `artifact_type`, `lifecycle_owner`, and `scenario_pack`, but only `spell` and `sigil` are implemented first. |

## Concept Layer Map

```text
Reusable capability lifecycle evidence
  -> Experiment Harness as shared validation loop
    -> Lifecycle experiment profiles
      -> Spellcraft profile
      -> Sigil Development profile
        -> Test case: Sigil Development creates/updates an experiment harness and validates the produced work
```

## Closed System Boundary

The generalized unit is not a new orchestration spell. It is a profile layer inside Experiment Harness.

Inputs:

- artifact path,
- artifact type,
- lifecycle owner,
- desired profile,
- target contract path,
- optional live-loop budget.

Outputs:

- starter validation experiment,
- task matrix,
- fixtures,
- example prompts,
- live regime definitions,
- wrapper scripts,
- validation report shape,
- observability-compatible reports.

Owned by Experiment Harness:

- generated harness layout,
- experiment profile schema,
- loop execution mechanics,
- validation/report/observe mechanics,
- generated evidence boundaries.

Owned by Spellcraft:

- what a spell must prove,
- phase and sigil-composition scenarios,
- spell-specific gates and failure policy.

Owned by Sigil Development:

- what a sigil must prove,
- lifecycle authoring/update/observe/reflect scenarios,
- sigil-specific Quality Bar, Anti-Patterns, and promotion gates.

## Evolution Profile

Expected evolution:

- spell and sigil profiles first,
- local repository profile overrides later,
- additional capability families only after repeated use,
- richer semantic judging after observer judging exists,
- real Codex loop promotion once live execution budget is approved.

Smallest extension boundary:

- a `profile` value and profile-specific generated starter files,
- no new global registry until at least one spell and one sigil profile run produces evidence,
- no new profile plugin system until more than two artifact families need it.

## Deferred Complexity

- Profile plugins are deferred; generated profile files are enough for `spell` and `sigil`.
- Semantic AI judging is deferred; current validators continue to use structural and contract checks.
- Automatic promotion is deferred; the harness prepares evidence but lifecycle owners decide promotion.
- Cross-repository profile registry is deferred; external repository support can use copied starter profiles first.

## Technique Pack Trace

| Technique | Result |
| --- | --- |
| abstraction-level guard | pass; the selected unit is profile generation, not a new lifecycle authority. |
| recomposition proof | pass; profiles recompose into Spellcraft and Sigil Development by providing evidence they already require. |
| evolution profile | pass; extension points are concrete and minimal. |
| boundary-object check | pass; the profile is the boundary object between harness mechanics and lifecycle meaning. |
| cognitive-load check | pass; one profile contract is easier to learn than separate harness forks. |
| premortem pass | pass; likely failure is profile drift from lifecycle contracts, guarded by validation against `SKILL.md` sections. |
| navigable-result check | pass; next route is implementation layering and then the Sigil Development test case. |

## Frame Expiry Note

Revisit this design if Experiment Harness begins validating non-Arcanum artifacts whose lifecycle owners do not expose `SKILL.md`, Quality Bar, Anti-Patterns, or lifecycle authority boundaries.

## Navigation Guide

Start with the shared profile schema and a sigil profile because `sigil-development` already requires experiment harness initialization. Then add the spell profile and update Spellcraft to request it when designing reusable spells. Only after both paths validate should runtime adapters expose profile selection as a stable user-facing option.

The concrete profile boundary is defined in [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md). Implementation should follow that contract before expanding runtime adapters or lifecycle-owner docs.

Next route: implementation-layering.
