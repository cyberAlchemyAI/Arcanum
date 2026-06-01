# Refine Result: Why Not Everything?

Status: pass
Preset: compact
Research: no-research

## Refined Answer

"Everything" is acceptable only if it means a governed candidate bundle.

It is not yet safe if it means final canonical promotion of schema, JSON Schema, profiles, and templates all at once.

The distinction is authority:

- development validation proves the model is coherent enough to continue;
- candidate promotion lets the full bundle travel together for reuse and testing;
- canonical template promotion makes the model an authoring obligation;
- external-system adoption would make Inventory, structured-action-schema, DomainSpec, CyberAlchemy, or future systems responsible for fields they have not accepted.

## Why Not Everything As Final Canonical Authority

The current validation surface is strong, but it is still young in four places:

1. The fixture corpus proves coherence, not long-term completeness.
2. Record-kind profiles are validated, but PromotionRecord companion ownership is still deliberately deferred.
3. DomainSpec is represented by a boundary-preserving pressure fixture, not a DomainSpec-owned package.
4. The future-system fixture is a portability placeholder, not evidence from a real future system.

Promoting everything as final would collapse these different maturities into one authority level.

## Better Option

Add a fifth gate option:

```text
promote-governed-candidate-bundle
```

This option promotes the full bundle as candidate-governed evidence:

- branch vocabulary,
- schema axes,
- record-kind profiles,
- development JSON Schema candidate,
- fixtures,
- validators,
- validation report.

It explicitly does not promote:

- canonical Ontology Vault templates,
- mandatory Inventory fields,
- structured-action-schema mutation,
- DomainSpec-owned package changes,
- CyberAlchemy source ontology mutation,
- future-system obligations.

## Final Recommendation

Use Option E.

It is the clean answer to "why not everything?": take everything forward as a governed candidate bundle, but do not grant final template or external adoption authority yet.

## Gate Patch

The decision gate was updated at:

```text
arcana/ontology-vault/development/schema-validation-plan/decision-gates/OVS-GATE-001-promotion-boundary.md
```

The previous recommendation, `promote-minimal-vocabulary`, was too conservative after the validation pass. The refined recommendation is now `promote-governed-candidate-bundle`.
