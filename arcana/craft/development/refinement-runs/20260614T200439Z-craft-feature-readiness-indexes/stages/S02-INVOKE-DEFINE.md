# Stage S02: Invoke Define

## Invoke Result

- Mode: define.
- Spell: invoke.
- Canonical ID: invoke.
- Scope: library.
- Phase status: pass.
- Mode contract: `spells/invoke/define.md`.
- Outputs: this stage artifact, `GLOSSARY-CONSISTENCY.md`, `IMPLEMENTATION-LAYERING.md`, `PLAN-TRANSPORT.md`.
- Template selection: Craft sigil maintenance packet, using existing Craft canonical schema and package sources.
- Decisions: additive readiness index family; no canonical glossary promotion; no direct source mutation in the refine loop.
- Unresolved gaps: no blocker-level define gaps; implementation requires SWU selection.
- Next route: design.

## Defined Intent

Craft should be updated so ledgers that already point to work-packs can expose execution-readiness handles:

- current execution target;
- work-pack gate status;
- ready SWU IDs;
- approval record;
- execution mode;
- product worktree;
- blocked mutation scope;
- blocked publication scope;
- owner route.

## Source Contracts

- `arcana/craft/SKILL.md` owns the portable Craft operating contract.
- `arcana/craft/templates/ledger.schema.yml` owns field/index schema vocabulary.
- `arcana/craft/README.md` owns package navigation.
- `WORK-PACK.md` owns future execution boundaries.

## Define Verdict

Pass. The define baseline is stable enough for design because the update is additive, bounded to Craft, and does not require product-specific decisions.
