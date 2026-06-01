# Translate Define

## Invoke Result

- Mode: full authoring package, define slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/translate/`
- Phase status: `pass`
- Mode contract: `spells/invoke/define.md`
- Template/profile selection: sigil candidate family scaffold
- Next route: `sigil-development`

## Objective

Define `translate` as a candidate sigil that maps meaning between vocabularies, domains, and concept frames while preserving target-domain truth and recording mapping limits.

## Intent Record

Translate exists so Guide does not own vocabulary translation internally. Guide should be able to call Translate when it needs to explain architecture in sales terms, a scientific formula in software-engineering terms, or a construction plan in musician terms.

## Scope

In scope:

- translation request schema,
- term map,
- bridge map,
- primitive alignment,
- mapping limits,
- target-domain definition,
- translation receipt,
- user-ledger preference handles.

Out of scope:

- full Guide orchestration,
- subagent dispatch,
- research planning,
- persistent user ledger writes,
- canonical glossary promotion,
- runtime command installation.

## Acceptance Criteria

| Criterion | Evidence |
| --- | --- |
| Translate can map source terms to target terms. | Term-map fixture. |
| Translate can name mapping limits. | Bridge-map fixture includes `maps_well` and `breaks_here`. |
| Translate preserves target truth. | Target-domain definition required in every fixture. |
| Translate reads User handles without owning memory. | Design boundary and receipt field. |
| Translate can be called by Guide later. | Handoff contract and Guide dependency notes. |
