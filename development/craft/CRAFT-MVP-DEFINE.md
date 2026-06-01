# Craft Recursive Ledger MVP Define

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: Craft recursive ledger MVP
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: `development/craft/CRAFT-MVP-DEFINE.md`
- Template selection: local candidate define artifact for a file-backed operational MVP
- Decisions: define the MVP as a YAML schema contract plus Markdown recursive ledger fixture and manual validation; preserve completed refine artifacts as source evidence; defer scoring, generated indexes, runtime integration, and role delegation automation
- Unresolved gaps: waiver behavior still needs proof in a real ledger row; broader Craft method architecture remains outside this MVP
- Next route: design

## Purpose

Define the first executable Craft recursive-ledger MVP after the type/lane examples and schema refinement work.

This artifact gives [CRAFT-MVP-DESIGN.md](CRAFT-MVP-DESIGN.md) and [CRAFT-MVP-WORK-PACK.md](CRAFT-MVP-WORK-PACK.md) a stable define baseline. It does not replace the earlier recursive-ledger define artifact; [CRAFT-RECURSIVE-LEDGER-DEFINE.md](CRAFT-RECURSIVE-LEDGER-DEFINE.md) remains the broader feature definition.

## Source Context

Primary source artifacts:

- [CRAFT-RECURSIVE-LEDGER-DEFINE.md](CRAFT-RECURSIVE-LEDGER-DEFINE.md)
- [CRAFT-RECURSIVE-LEDGER-GLOSSARY.md](CRAFT-RECURSIVE-LEDGER-GLOSSARY.md)
- [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md)
- [CRAFT-LEDGER-TYPE-EXAMPLES.md](CRAFT-LEDGER-TYPE-EXAMPLES.md)
- [CRAFT-RECURSIVE-LEDGER-DESIGN.md](CRAFT-RECURSIVE-LEDGER-DESIGN.md)

## Problem

Craft has a refined schema and examples, but not yet a usable operational ledger artifact. Without a concrete ledger fixture, the recursive-ledger idea remains a design claim rather than a working artifact that can track nested contexts, blockers, gates, enablers, decisions, and cross-context dependencies.

## MVP Objective

Create a YAML-backed, file-backed recursive ledger that can be reviewed, edited, and validated without runtime tooling.

The MVP should prove that Craft can represent:

- projects inside projects as recursive contexts,
- artifacts owned by those contexts,
- blockers and enablers between contexts,
- gates that require QA, validator, or auditor evidence,
- blocker refinement before resolution,
- explicit waiver decisions when a blocker is not refined before closure.

## In Scope

| Capability | MVP Requirement |
| --- | --- |
| Schema contract | Define valid row families, fields, enums, and validation rules in [CRAFT-LEDGER-SCHEMA.yml](CRAFT-LEDGER-SCHEMA.yml). |
| Recursive contexts | Represent parent-child context rows with lifecycle stage, gate, and next move. |
| Artifact ownership | Represent source artifacts, work-packs, validation artifacts, and handoffs as context-owned rows. |
| Cross-context relations | Represent contains, blocks, enables, depends_on, informs, and supersedes relations. |
| Typed items | Represent blockers, gates, and enablers with condition type, lane, role hint, status, closure condition, and evidence. |
| Blocker refinement | Prevent direct raw-to-resolved blocker closure unless a waiver decision exists. |
| Manual validation | Record schema and lifecycle validation in a reviewable Markdown artifact. |

## Out Of Scope

| Deferred Capability | Reason |
| --- | --- |
| Priority scoring | Needs multiple real ledger states before ranking rules are meaningful. |
| Generated index | YAML schema and Markdown fixture should be validated first. |
| Runtime command integration | Belongs to the separate runtime/refine interface thread. |
| Automatic role delegation | Type plus lane should remain a hint until more examples exist. |
| Canonical Craft promotion | Requires architecture, validation, and explicit approval. |

## Glossary Baseline

| Term | Definition For MVP |
| --- | --- |
| recursive context | A project-like unit that may contain child contexts, artifacts, blockers, gates, and enablers. |
| ledger fixture | The first concrete `LEDGER.md` file that instantiates the schema against current Craft state. |
| typed item | A blocker, gate, or enabler row with type, lane, role hint, status, evidence, and closure semantics. |
| blocker refinement | The lifecycle step that turns a raw blocker into an owned, typed, evidence-backed condition before resolution. |
| waiver decision | A decision row that explicitly permits bypassing normal blocker refinement or closure evidence. |
| operational lane | A responsibility lane such as business, tech, QA, validator, auditor, planner, or blocker_refiner. |

## Decisions

| Decision | Selected | Rationale | Status |
| --- | --- | --- | --- |
| Schema source of truth | YAML `CRAFT-LEDGER-SCHEMA.yml` | The schema should be structured and machine-readable before ledger fixtures or indexes rely on it. | accepted |
| Ledger fixture | Markdown `LEDGER.md` | The first ledger instance should remain durable and inspectable for human review. | accepted |
| Validation artifact | `LEDGER-VALIDATION.md` | Manual validation keeps the MVP reviewable without generated indexes. | accepted |
| Runtime integration | defer | Runtime strategy is being handled in another thread and should not pollute Craft MVP acceptance. | accepted |
| Role delegation | defer automation | The MVP can preserve role hints without delegating work automatically. | accepted |
| Waiver behavior | include in MVP | The user explicitly identified blocker refinement as important before resolution. | accepted |

## Acceptance Criteria

1. `CRAFT-LEDGER-SCHEMA.yml` exists and defines context, artifact, relation, typed-item, and decision row families.
2. `LEDGER.md` exists and instantiates the YAML schema as a human-readable fixture.
3. The ledger can represent nested Craft contexts and cross-context blockers/enablers.
4. Every blocker includes refinement status and closure condition.
5. A resolved blocker has refinement evidence or a linked waiver decision.
6. `LEDGER-VALIDATION.md` reviews every schema validation rule from the YAML contract.
7. The package state identifies the MVP ledger as the active next Craft artifact after validation.

## Gaps

| Gap | Severity | Route |
| --- | --- | --- |
| Waiver row shape is designed but unproven in a real ledger fixture. | medium | Prove in `CRAFT-MVP-002`; refine schema only if representation fails. |
| Current MVP does not decide the final Craft method architecture. | low | Route after ledger MVP validation. |
| Runtime/orchestrator work is split out. | medium | Keep linked as side-thread context only. |

## Next Route

`invoke design` for the MVP architecture/design bundle.
