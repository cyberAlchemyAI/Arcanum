# Readiness: Inventory Evidence-Card POC

## Status

Static POC package readiness: pass. The first executable validator surface is implemented for agents; the human UI surface remains deferred.

## Acceptance Checklist

| Gate | Evidence | Status |
| --- | --- | --- |
| Production schema exists | `arcana/inventory/templates/evidence-card-schema.md` | pass |
| Authoring template exists | `arcana/inventory/templates/evidence-card.md` | pass |
| Lint contract exists | `arcana/inventory/templates/evidence-card-lint.md` | pass |
| Index/retrieval contract exists | `arcana/inventory/templates/index.md` | pass |
| Pilot card fixture parses | `arcana/inventory/development/pilot/evidence-card/pilot-cards.json` | pass |
| Pilot fixture has required card mix | 11 cards: 2 source-summary, 3 concept, 1 method, 4 claim, 1 question | pass |
| Pilot index/retrieval fixtures parse | `pilot-index.json`, `pilot-retrieval.json` | pass |
| Retrieval references existing card IDs | 11 referenced IDs, no missing references | pass |
| Handoff examples parse | `pilot-handoff-ontology.json`, `pilot-handoff-definitions.json` | pass |
| Handoff examples include non-authority language | both handoff packets include `non_authority_notice` and `source_refs` | pass |
| README/SKILL expose evidence-card behavior | `arcana/inventory/README.md`, `arcana/inventory/SKILL.md` | pass |
| Executable validator language | `VALIDATOR-SURFACE-DECISION.md` | pass for agent surface; user UI deferred |
| Agent/runtime validator script | `arcana/inventory/scripts/validate-evidence-card-fixtures.sh` | pass |
| Invalid examples fixture | `arcana/inventory/development/pilot/evidence-card/invalid-examples.json` | pass |
| Validator runtime contract | `arcana/inventory/development/VALIDATOR-RUNTIME.md` | pass |
| Candidate EvidenceSet schema exists | `arcana/inventory/templates/evidence-set-schema.md` | pass |
| Candidate EvidenceSet authoring template exists | `arcana/inventory/templates/evidence-set.md` | pass |
| Stored EvidenceSet fixture validates | `arcana/inventory/development/pilot/evidence-card/evidence-sets.json` | pass |

## POC Decision State

The evidence-card POC can proceed to review with the current static artifacts.

The `EvidenceSet` candidate should remain candidate-only. The pilot retrieval and Craft stressor now show enough grouped-evidence reuse to justify a minimal candidate schema and fixture, but not enough to canonicalize production behavior.

## Validator Surface Decision

| Surface | Runtime | Status | Rationale |
| --- | --- | --- | --- |
| Agent/runtime | shell plus `jq` | selected | Inventory must be fast for agents to query, validate, and compose with local command flows. |
| Human/user interface | deferred | later | A richer review UI can be designed after the fast agent path proves useful. |

## Next Route

The shell plus `jq` agent/runtime validator is implemented and passes against the pilot fixture package, including EvidenceSet reference validation across the pilot and Craft card pools.

Run:

```sh
bash arcana/inventory/scripts/validate-evidence-card-fixtures.sh arcana/inventory/development/pilot/evidence-card
```

The validator checks:

- required fields,
- controlled vocabularies,
- selector shape,
- full/minimal profile rules,
- `promotion_owner` and terminal status pairing,
- relation candidate non-authority notices,
- EvidenceSet required fields, controlled vocabularies, unique IDs, and card ID references,
- handoff packet source refs and non-authority text.

## Remaining Deferred Surface

Human UI remains deferred-not-blocking. Revisit it only after the agent/runtime validator proves useful or its output becomes hard for humans to inspect.

## Remaining Design Blocker

Canonical `EvidenceSet` promotion remains deferred. The candidate schema is designed and checked against both current candidate sets; promotion now needs evidence that stored sets stay useful beyond the current POC slices.
