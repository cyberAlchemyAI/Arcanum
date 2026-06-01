# Craft Validation And Recomposition Guide

## Purpose

This guide validates Craft method examples without reopening architecture discovery.

It is local to `development/craft/` and candidate until a later promotion route explicitly says otherwise. It reviews the example suite, architecture interface rules, recomposition evidence, and deferred boundaries.

## Source Contracts

| Source | Use |
| --- | --- |
| `CRAFT-VALIDATION-EXAMPLES.yml` | Structured authority for validation examples. |
| `CRAFT-VALIDATION-EXAMPLES.md` | Human-readable walkthrough. |
| `CRAFT-ARCHITECTURE.md#Dependency And Interface Rules` | Rule checklist R-001 through R-007. |
| `CRAFT-ARCHITECTURE.md#Gate Result` | Architecture pass/follow-up boundary. |
| `LEDGER-VALIDATION.md` | Prior validation style and blocker lifecycle evidence. |

## Validation Result Vocabulary

| Result | Meaning |
| --- | --- |
| `pass` | Evidence supports the claim at the current Craft layer. |
| `flag` | Evidence is useful but has residue that must be routed, deferred, or reviewed before stronger claims. |
| `block` | A required claim lacks evidence or violates a boundary. Stop before dependent work. |
| `waived` | A blocker or strict requirement is explicitly bypassed with decision evidence. |
| `deferred` | Work is intentionally outside the current layer and has an owner, evidence requirement, or future route. |

## Example Coverage Checklist

| Example | Claim | Required Review | Current Expected Result |
| --- | --- | --- | --- |
| EX-001 | SCU selection | Does the selected unit preserve recomposition while shrinking scope? | pass |
| EX-002 | SWU planning | Does every SWU have dependencies, write scope, done criteria, validation, and handoff notes? | pass |
| EX-003 | Residue classification | Is unclosed runtime evidence routed as side-thread residue rather than hidden? | flag |
| EX-004 | Recomposition | Does completed child work unlock or update the correct parent context? | pass |
| EX-005 | Blocker refinement gate | Is a raw blocker prevented from direct resolution? | pass |
| EX-006 | Cross-context relation | Is a relation across branches explicit and evidence-backed? | pass |
| EX-007 | Route boundary | Does Craft call an existing route without taking over its authority? | pass |
| EX-008 | Runtime side-thread boundary | Are runtime/interface gaps visible and non-blocking? | pass |
| EX-009 | Promotion decision | Does local validation lead to review without automatic promotion? | flag |
| EX-010 | Role-hint review | Are type plus lane mappings treated as review hints before automation? | pass |

## Architecture Rule Checklist

| Rule | Validation Question | Pass Evidence | Failure Mode |
| --- | --- | --- | --- |
| R-001 | Does the artifact cite required source contracts? | Source contract table or task-local source list. | Claim is unsupported or cannot be audited. |
| R-002 | Does every unit have a recomposition path before execution? | Recomposition target or parent-context update is named. | Completed work cannot reconnect to its parent context. |
| R-003 | Are raw blockers prevented from direct resolution? | Blocker is refined, waived, or still active/raw. | Raw blocker is marked resolved without evidence. |
| R-004 | Are work-packs represented as context-owned artifacts, not ledger roots? | Ledger artifact row or work-pack ownership note. | Work-pack becomes the whole context and hides relations. |
| R-005 | Do candidate glossary terms stay local until promotion? | Local glossary status remains candidate/deferred/validated-by-mvp. | Term is treated as canonical without promotion review. |
| R-006 | Are runtime/interface changes side-threaded? | Runtime owner artifacts are cited; no runtime mutation is claimed. | Craft architecture claims runtime integration is solved. |
| R-007 | Is deferred automation evidence-gated? | Scoring, generated indexes, and role automation require examples and decision evidence. | Automation starts from preference instead of evidence. |

## Recomposition Checklist

A Craft unit is closed only when all applicable questions pass:

| Check | Question |
| --- | --- |
| Parent context | Which parent context, architecture section, work-pack slice, or route does this unit return to? |
| Evidence | What validation, review, command, or decision proves the unit's claim? |
| Residue | What mismatch, ambiguity, or deferred scope remains after validation? |
| Route | Does residue close locally, route to refine/decision-gate/task-session/workflow-reflect, or become a side-thread dependency? |
| Boundary | Did the unit avoid mutating runtime, registry, promotion, scoring, generated index, or role automation surfaces unless explicitly authorized? |
| Next move | What is now enabled, blocked, flagged, or deferred? |

## Classification Rules

| Situation | Classification |
| --- | --- |
| All required evidence exists and boundaries hold. | `pass` |
| Evidence exists but side-thread, promotion, or automation residue remains. | `flag` or `deferred`, depending on whether a dependent claim is being made. |
| Required evidence is missing for the current claim. | `block` |
| A blocker is bypassed with explicit decision evidence. | `waived` |
| A future capability is named but intentionally out of scope. | `deferred` |

## Evidence Requirements For Task Session Runs

Every task-session that executes Craft architecture hardening should record:

| Evidence | Required For |
| --- | --- |
| Context pack summary | Every task or SWU. |
| Source contracts | Every task or SWU. |
| Files updated | Every mutation-capable task. |
| Validation command or review substitute | Every task. |
| Recomposition target | Every completed task. |
| Residue classification | Every flag, blocker, deferral, or waiver. |
| Synchronization notes | Any task that updates README, session ledger, work-pack status, or package state. |

## Non-Goals

This guide does not authorize:

- runtime integration,
- command route mutation,
- registry mutation,
- sigil or spell promotion,
- canonical glossary promotion,
- priority scoring implementation,
- generated index implementation,
- role delegation automation.

## Current Guide Verdict

`pass`

The guide can classify examples `EX-001` through `EX-010`, architecture rules `R-001` through `R-007`, recomposition evidence, and deferred boundaries. It is ready to feed `CRAFT-ARCH-004`.
