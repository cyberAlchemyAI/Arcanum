# Implementation Layering - Whisper Schema Canonization

- Module: `whisper-schema-canonization`
- Status: plan
- Target owner: `whisper` spell lifecycle
- Planning owner: `invoke`
- Lifecycle owner next: `spellcraft`

## Layer Decision Table

| Layer | Question Answered | Outcome | Promotion Evidence | Deferred Work |
| --- | --- | --- | --- | --- |
| L0 review | What schema artifacts exist, which are evidence, which are candidates, and which fields are stable enough to promote? | Complete artifact inventory and canonicalization matrix. | Review report citing concrete paths, field families, current validation behavior, and candidate/authority classification. | No canonical file moves. |
| L1 canonical package | Can Whisper expose a stable schema home without copying development-run assumptions? | `arcanum/spells/whisper/schemas/` with README, schema contract, and example fixtures. | YAML/JSON validation, validator compatibility checks, and owner-reviewed field selection. | Runtime mirror regeneration and broader transport examples. |
| L2 contract refresh | Do Whisper README, validator docs, and refresh artifacts point at the canonical schema home? | Canonical spell contract references schema home; development refresh artifacts become provenance, not live authority. | README diff, validator checks, and path-reference scan showing no development-only schema dependency for canonical behavior. | Renderer/review HTML schema integration. |
| L3 promotion evidence | Is the canonical schema package reusable across transports and future posts? | Experiment evidence over at least main Substack substrate, Object sequel substrate, and readability fixture. | Experiment Harness report or equivalent fixture matrix with pass/flag/block outcomes and residue ledger. | Registry/runtime install claims if broader exposure is requested. |

## Active Window

The first executable unit is L0 only:

`SWU-WSC-001`: inventory and classify Whisper schema artifacts.

This avoids creating canonical files before review distinguishes stable schema
contracts from run-specific evidence.

## Promotion Rules

- Development artifacts may seed canonical schemas but must not be copied
  wholesale.
- Article-specific fields may become examples, not base schema requirements.
- Optional `readability_dynamics` remains candidate-stable until broader fixture
  evidence exists.
- Canonical schema package creation requires Spellcraft acceptance before
  mutation.
- Runtime generated surfaces are regenerated only after canonical README or
  skill contract changes, never hand-edited as source authority.

## Validation Strategy

| Layer | Required Checks |
| --- | --- |
| L0 | `rg` inventory, YAML parses for candidate substrates, validator pass on existing Draft 02 substrate, report completeness review. |
| L1 | Schema package files parse; examples validate; old development substrates still validate; canonical examples do not depend on development-only paths. |
| L2 | Whisper README path references are current; validator help/docs mention canonical schema home; no stale `.agents` or development-run authority claims. |
| L3 | Experiment report covers main substrate, Object sequel substrate, and readability fixture; residue names transport gaps and promotion limits. |

## Layer Exit Criteria

- L0 exits when the audit matrix names every schema-bearing artifact and assigns
  one of: canonical-source-candidate, example-candidate, provenance-only,
  generated, or superseded.
- L1 exits when a canonical schema package exists and passes validation.
- L2 exits when the spell contract and validator documentation consume the new
  package without stale development-only authority.
- L3 exits when reusable evidence exists and Spellcraft decides the promotion
  status.
