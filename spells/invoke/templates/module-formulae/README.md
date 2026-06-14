# Module Formulae Template Pack

> **Partially deprecated (2026-06-14).** The invoke `define` baseline is now the **DomainSpec
> template** (`../domainspec-spec/`) — do not start new *specs* from this pack's `module-spec.md`.
> **Still in active use:** `architecture-bundle.md` (design-stage six-view profile, composed by
> `design.md`) and `execution-pack.md` (plan-stage wave planning, composed by `plan.md` /
> `work-pack.md`) — the DomainSpec family has no equivalents yet. Full removal is blocked on:
> (1) authoring DomainSpec design-stage + plan-stage templates, (2) regenerating the 9 invoke
> validation fixtures, (3) the `mogt-agentic-conversation` project's own `module-formulae/` dir
> (out of scope). See keystone-closeout TASK-MF-REMOVE-2.

This pack provides a neutral, module-first documentation model that preserves structured governance semantics without framework-specific wording.

## Goal

Use these templates when you need:

- concept-first design,
- evidence-linked contracts,
- explicit governance gates,
- deterministic handoffs from definition to design to execution planning.

## Included Templates And Companions

| Template | Purpose |
| --- | --- |
| module-spec.md | Canonical module contract with capabilities, concept index, and relationship map. |
| glossary-ontology.md | Plain-language and formal terminology contract for business and system language. |
| concept-model.md | Structural model for records, value types, and enumerations. |
| operations.md | Action contract for rules, calculations, transitions, and outcomes. |
| flows-policies.md | Multi-step flow orchestration and policy decision contracts. |
| interfaces.md | External and internal integration contract mapping. |
| research-brief.md | Evidence-first discovery and decision framing before design. |
| architecture-bundle.md | Required architecture view set with assumptions, risks, and decisions. |
| [../implementation-layering.md](../implementation-layering.md) | Standalone invoke layering companion composed from the implementation-layering transmutation. |
| [../work-pack.md](../work-pack.md) | Canonical invoke executable planning manifest that maps objectives, slices, waves, tasks, and SWUs. |
| observability.md | Signal derivation and alert contract tied to source artifacts. |
| execution-pack.md | Phased implementation planning, gates, and closure obligations. |
| bundle-profile.md | Composable profile selection for discovery, architecture, implementation, and full runs. |
| vocabulary-map.md | One-to-one translation from source terms to Module Formulae terms. |

## Usage Contract

1. Keep structure; only adapt naming and examples.
2. Keep evidence links and source references in every major table.
3. Keep deterministic gates for approvals, blockers, and closure.
4. Keep traceability from concept definitions to execution tasks.
5. Keep business and system terminology synchronized through the glossary.

## Integration Notes

- These templates are intended for local inventory-first usage.
- A consuming workflow can select a subset, but the full pack is the default for high-complexity work.
- The glossary template is the terminology authority for all generated artifacts.
- The standalone companion [../implementation-layering.md](../implementation-layering.md) is the default layering artifact for invoke plan/full/validate outputs.
- The standalone companion [../work-pack.md](../work-pack.md) is the canonical executable plan manifest between implementation-layering and execution-pack.

## Related Invoke Families

Dedicated family scaffolds live beside this pack and remain separate from Module Formulae ownership:

- [../generic/](../generic/)
- [../research/](../research/)
- [../architecture/](../architecture/)
- [../spell/](../spell/)
- [../sigil/](../sigil/)
- [../ux-plan/](../ux-plan/)

## Composable Bundle Profiles

Use [bundle-profile.md](bundle-profile.md) to compose templates by intent:

- discovery profile,
- architecture profile,
- implementation profile,
- full profile.
