# Craft Recursive Ledger Implementation Layering

## Purpose

Keep the next Craft recursive-ledger work small enough to refine safely before implementation.

This companion artifact exists because Invoke plan mode requires layer boundaries for work-pack planning. It does not authorize runtime, registry, command, sigil, or spell mutation.

## Layer Summary

| Layer | Question | Scope | Promotion Evidence |
| --- | --- | --- | --- |
| L0 | Can the type/lane model explain real ledger examples? | Create example rows for contexts, blockers, gates, enablers, lanes, and role hints. | `CRAFT-LEDGER-TYPE-EXAMPLES.md` passes review against current define/type artifacts. |
| L1 | Can the examples stabilize a minimal ledger schema? | Define the Markdown-first ledger shape for contexts, relations, typed items, and optional indexes. | `CRAFT-RECURSIVE-LEDGER-DESIGN.md` includes fields, validation rules, and example mapping. |
| L2 | Can the schema be validated and refined? | Add validation checklist, conflict policy, and lane/type review criteria. | Future validation artifact or refined design pass. |
| L3 | Can Craft expose this as reusable operational machinery? | Runtime, command, scoring, automation, or canonical promotion. | Deferred; requires explicit approval. |

## Active Layer Window

`L0-L1`

The immediate work is refinement-only:

1. Refine examples.
2. Refine schema.

No execution automation or source-code implementation belongs in this work-pack.

## Deferrals

| Deferred Item | Reason |
| --- | --- |
| Priority scoring | Requires stable typed examples and conflict policy first. |
| Runtime command integration | File-backed MVP should prove value before command mutation. |
| JSON/YAML parser implementation | Schema shape should be validated in Markdown first. |
| Canonical Craft promotion | Requires architecture, validation, and explicit approval. |

## Gate

- Status: `pass`
- Reason: The two refinement tasks are bounded, local to `development/craft/`, and do not require implementation mutation.
