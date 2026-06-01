# Refine Seed Proposal: Constitution Governance

## Target

Create a canonical Arcanum sigil for modular constitution lifecycle governance.

## Source Context

- User concern: one large constitution file will lose effect when too much governance context is loaded.
- User framing: constitutions should enforce patterns for structure/form.
- Recent example: chart rendering line-break rule added to Artifact Constitution and validator.
- Existing surfaces: `framework/ARTIFACT-CONSTITUTION.md`, `tools/validate-artifact-constitution.sh`, Context Builder, Decision Gate, Invoke, Sigil Development.

## Write Scope

Allowed:

- `arcana/constitution-governance/**`
- `registry/SIGILS.md`
- `arcana/README.md`

Already touched related surfaces:

- `framework/ARTIFACT-CONSTITUTION.md`
- `framework/ARTIFACT-AUTHORING-MEMORY.md`
- `tools/validate-artifact-constitution.sh`

## Done Criteria

- New sigil package exists.
- Contract answers whether Context Builder alone is enough.
- Contract defines creation, rule addition, selection, composition, validation, split, and promotion modes.
- Templates exist for constitution, composition pack, and validation adapter.
- Registry is updated.

## Research Decision

No external research. Local Arcanum governance surfaces are sufficient for initial source-contract creation.
