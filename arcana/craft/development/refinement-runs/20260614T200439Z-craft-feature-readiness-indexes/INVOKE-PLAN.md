# Invoke Plan: Craft Feature Readiness Indexes

## Plan Identity

- Spell: `invoke`
- Mode: `plan`
- Target artifact: Craft execution-readiness index update.
- Target owner: `arcana/craft` lifecycle owner.
- Phase status: `pass`
- Complexity: `medium`
- Output mode: `split`
- Next route: `sigil-development` or maintainer-approved `task-session`

## Planning Summary

This plan turns the design into a bounded Craft maintenance work-pack. The first executable slice is schema-only and additive. Later slices update contract text, examples, validation, generated surfaces, and publication checks.

## Source Design References

- `INVOKE-DESIGN.md`
- `GLOSSARY-CONSISTENCY.md`
- `IMPLEMENTATION-LAYERING.md`
- `REFINE-SEED-PROPOSAL.md`
- Current Craft canonical files under `arcana/craft/`

## Delivery Boundary

In scope:

- optional `indexes.execution_readiness` contract;
- optional row-level readiness fields when linked to existing artifacts or next moves;
- status/export guidance;
- public-safe examples or fixtures;
- generated runtime surface synchronization after source mutation.

Out of scope:

- executing work-pack SWUs;
- mutating Invoke, Refine, Workflow Reflect, or Spellcraft contracts;
- committing or pushing submodule or parent changes;
- publishing private workspace evidence.

## Task Breakdown

| Task | Layer | Goal | Contract |
| --- | --- | --- | --- |
| `TASK-CFR-001` | L0 | Add schema/index contract. | `work-pack/tasks/TASK-CFR-001.md` |
| `TASK-CFR-002` | L1 | Update Craft skill and README wording. | `work-pack/tasks/TASK-CFR-002.md` |
| `TASK-CFR-003` | L2 | Add public-safe example/fixture coverage. | `work-pack/tasks/TASK-CFR-003.md` |
| `TASK-CFR-004` | L2/L3 | Add validation and status/export checks. | `work-pack/tasks/TASK-CFR-004.md` |
| `TASK-CFR-005` | L3 | Regenerate surfaces and prepare publication gates. | `work-pack/tasks/TASK-CFR-005.md` |

## Smallest Working Units

| SWU | Parent Task | Goal | Execution Owner | Verification |
| --- | --- | --- | --- | --- |
| `SWU-CFR-001` | `TASK-CFR-001` | Add optional readiness index schema contract. | local-fallback | YAML parse and targeted grep. |
| `SWU-CFR-002` | `TASK-CFR-001` | Confirm existing examples remain compatible. | local-fallback | YAML parse examples. |
| `SWU-CFR-003` | `TASK-CFR-002` | Update `SKILL.md` linking/all-status guidance. | local-fallback | Grep contract terms. |
| `SWU-CFR-004` | `TASK-CFR-002` | Update `README.md` package summary. | local-fallback | Grep README terms. |
| `SWU-CFR-005` | `TASK-CFR-003` | Add public-safe readiness example or fixture. | local-fallback | YAML parse and privacy scan. |
| `SWU-CFR-006` | `TASK-CFR-004` | Add reviewable validation checklist. | local-fallback | Checklist commands pass. |
| `SWU-CFR-007` | `TASK-CFR-005` | Regenerate runtime surfaces after canonical edits. | local-fallback | Generated copies include new contract. |
| `SWU-CFR-008` | `TASK-CFR-005` | Run submodule-safe publication checks. | manual | `git diff --check`; `make bump-check` before parent publication. |

## Execution Rule

Select one SWU before execution. Do not run a whole task bundle as one mutation unless the executor has explicit maintainer approval.

## Validation Strategy

- JSON validation for this planning packet.
- YAML parse for `ledger.schema.yml` and touched examples.
- Grep checks for readiness contract terms in canonical and generated surfaces.
- Public-boundary scan for private workspace names or local-only product paths before any public commit.
- `git diff --check`.
- `make bump-check` only when publication or parent gitlink movement is requested.
