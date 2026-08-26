# Research Initial Definitions — Unified Skill Model

## Context

Arcanum organizes reusable agent capabilities as skills whose canonical packages currently live under three named directories: `formulae/`, `transmutations/`, and `arcana/`. The repository documentation presents these directories as epistemic tiers, while Codex discovers the resulting capabilities through repo-scoped skill adapters under `.agents/skills/`.

The current separation has become difficult to apply consistently. The documented tier taxonomy assigns behavioral meaning to directory placement, while parts of the publication path derive category directly from that placement rather than from a validated capability contract. This matters because terminology, authoring rules, installation, discovery, and governance can drift even when every runtime artifact is ultimately exposed as a skill.

## Purpose

This document establishes the informational baseline for deciding whether Arcanum should replace the three named capability directories with one unified skill model. The later study should inform a product and repository decision about the canonical unit, its required schema, its creation lifecycle, and any categories that remain necessary.

## Research Questions (Can be refined)

### Program question

**RQ-00.** What current properties and behaviors define an Arcanum skill across its creation, representation, governance, distribution, and execution, and which of them must remain distinguishable if canonical packages are consolidated into one skill model?

### Creation and lifecycle

1. **RQ-01.** Which current entry point, if any, is authoritative for initiating the creation of a new skill?
2. **RQ-02.** Which lifecycle states of a skill are recognized by current authoritative artifacts and executable consumers?
3. **RQ-03.** Which conditions, if any, make a lifecycle-state transition effective?
4. **RQ-04.** Which guarantees of the documented lifecycle are enforced executably, and which depend only on documentary convention?
5. **RQ-05.** What propagation rule, if any, governs when a derived repository artifact reflects a change to its canonical skill contract?

### Contract and schema

6. **RQ-06.** What precedence resolves a conflict among canonical location, frontmatter, the body of `SKILL.md`, sidecars, agent metadata, dependency manifests, registries, and generated packages?
7. **RQ-07.** Which identity and routing properties are common minimum requirements across supported runtimes?
8. **RQ-08.** Which semantic elements of the `SKILL.md` body are required for a capability to be recognized as an Arcanum-governed skill?
9. **RQ-09.** What normative role, if any, does `SKILL.md.artifact.yml` exercise over its associated skill?
10. **RQ-10.** Which differences, if any, are permitted between a canonical skill package and a generated projection of it?
11. **RQ-11.** Where, if anywhere, is compliance with the skill contract enforced?

### Categories, identity, and compatibility

12. **RQ-12.** Which observable repository behaviors currently depend on the identity `formulae`, `transmutations`, or `arcana`?
13. **RQ-13.** Which property or combination of properties, if any, supplies a capability's stable identity across its current surfaces?
14. **RQ-14.** Which externally observable references to a canonical skill, if any, function as compatibility contracts?

## Confirmed Product Constraints

- The study concerns the Arcanum repository rooted at `C:\Users\victo\Arcanum`.
- The user wants to evaluate eliminating the names `Formulae`, `Transmutations`, and `Arcana` and consolidating their contents as skills, not merely correcting individual folder placement.
- Existing capabilities, runtime discovery, dependency closure, and installation behavior must not be treated as disposable merely because the taxonomy may change.
- Claims about the current process, schemas, and categories must be grounded in repository artifacts or executable behavior.
- This baseline may register no more than 15 research questions, counting the program question and all supporting questions.
- Research artifacts belong beneath this topic folder; implementation changes require separate authorization after the study.

## Current Evidence Baseline

- `README.md` defines a sigil as one reusable agent capability and assigns sigils to the three directories according to epistemic nature.
- `framework/SIGIL-DEVELOPMENT-WORKFLOW.md` describes a lifecycle containing candidate capture, tier classification, contract authoring, validation, trial execution, promotion, observation, and maintenance.
- `framework/templates/sigil-template.md` provides a common skill-contract skeleton with a `logic-type` distinction for the three current tiers.
- `.agents/README.md` states that repo-scoped skill folders point to canonical capability folders under `arcana/`, `formulae/`, and `transmutations/`.
- `registry/README.md` and `registry/SIGILS.md` describe availability and entry requirements for reusable sigils.
- `tools/build-skill-registry.py` discovers packages by directory, extracts metadata from `SKILL.md` or falls back to `README.md`, and assigns the directory name as the published tier.

## Known Gaps

- No unambiguous authority for initiating skill creation is established across the current, partially overlapping entry points.
- The lifecycle states recognized by documentary and executable authorities are not represented as one coherent state model.
- The conditions that make lifecycle transitions effective are distributed across gates, validation, trials, registration, generation, and installation.
- The boundary between executably enforced lifecycle guarantees and documentary convention is unclear.
- No consistent rule establishes when a derived repository artifact must reflect a change to its canonical skill contract.
- No single precedence rule resolves disagreement among the current schema-bearing surfaces.
- The identity and routing properties common to all supported runtimes are not established as one minimum contract.
- The required semantic structure of the `SKILL.md` body is unclear because templates, real contracts, and validators differ.
- The normative authority of `SKILL.md.artifact.yml` is unclear and its presence is not uniform across canonical packages.
- The permitted and prohibited differences between canonical packages and their generated projections are not established.
- The locations at which compliance with the skill contract is enforced have not been reconciled.
- The operational consumers of the three current category identities, including dependency resolution and distribution behavior, have not been fully delimited.
- The property or combination of properties supplying stable identity across a capability's current surfaces is unresolved.
- The compatibility significance of externally observable references to canonical skills is unknown.
