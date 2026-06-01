# Craft MVP Implementation Layering

## Purpose

Plan the first usable YAML-backed Craft recursive-ledger MVP without promoting Craft into a canonical sigil, spell, command, or runtime surface.

This companion artifact exists for Invoke plan mode and is grounded in [CRAFT-MVP-DEFINE.md](CRAFT-MVP-DEFINE.md) and [CRAFT-MVP-DESIGN.md](CRAFT-MVP-DESIGN.md). It supersedes neither [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) nor [WORK-PACK.md](WORK-PACK.md); those remain the completed refinement slice for examples and schema.

## MVP Boundary

The MVP is a file-backed recursive ledger under `development/craft/` that proves a YAML schema can represent:

- nested project/context rows,
- owned artifacts,
- cross-context blockers and enablers,
- gates with validator, QA, and auditor review lanes,
- blocker refinement before resolution,
- waiver decisions for blockers that cannot be refined before closure.

The MVP does not implement scoring, command dispatch, automation, runtime integration, canonical registry promotion, or role delegation execution.

## Layer Summary

| Layer | Question | Scope | Promotion Evidence |
| --- | --- | --- | --- |
| L0 | Can the YAML schema instantiate a readable ledger fixture? | Create `LEDGER.md` using `CRAFT-LEDGER-SCHEMA.yml` and example rows. | Ledger contains contexts, artifacts, relations, typed items, and decisions with stable IDs. |
| L1 | Can blocker refinement prevent false closure? | Add raw, typed, refined, resolution-proposed, resolved, and waived blocker examples. | Validation review catches direct raw-to-resolved closure unless a waiver decision exists. |
| L2 | Can humans validate the ledger without runtime tooling? | Create `LEDGER-VALIDATION.md` with manual checks and review outcomes. | Checklist maps every schema rule to pass, flag, or block evidence. |
| L3 | Can the ledger become reusable operational machinery? | Runtime commands, generated indexes, scoring, role delegation, and package promotion. | Deferred until the file-backed MVP passes review and Craft architecture is approved. |

## Active Layer Window

`L0-L2`

The next work should produce the first usable ledger fixture and a manual validation artifact. Runtime and automation stay deferred.

## Refine Trigger Policy

No new refine run is required before starting this MVP plan. Use a small `/refine` only if execution exposes one of these blocker-level ambiguities:

| Trigger | Refine Target | Reason |
| --- | --- | --- |
| A schema row cannot represent a required example without inventing a new field. | [CRAFT-RECURSIVE-LEDGER-DESIGN.md](CRAFT-RECURSIVE-LEDGER-DESIGN.md) | Schema ambiguity affects acceptance. |
| A blocker waiver cannot be represented by the decision row shape. | [CRAFT-RECURSIVE-LEDGER-DESIGN.md](CRAFT-RECURSIVE-LEDGER-DESIGN.md) | Waiver policy must be refined before closure is trusted. |
| Type plus lane cannot indicate a reasonable role hint in the fixture. | [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md) | Delegation semantics are unclear even before automation. |

## Deferrals

| Deferred Item | Reason |
| --- | --- |
| Priority scoring | Requires several real ledger states before ranking rules are meaningful. |
| Generated `ledger-index.json` | YAML schema and Markdown fixture should pass manual validation first. |
| Command integration | Runtime work is split to the refine/runtime thread and should not be hidden inside Craft MVP execution. |
| Automatic role delegation | Type plus lane hints need more examples before dispatch rules are safe. |
| Canonical Craft promotion | Requires architecture, validation, and explicit user approval. |

## Gate

- Status: `pass`
- Reason: Existing examples and schema are sufficient to plan a file-backed MVP. Any deeper ambiguity is routed through the refine triggers above.
