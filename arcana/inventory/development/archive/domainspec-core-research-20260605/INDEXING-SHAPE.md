---
module: inventory-domainspec-core
version: 0.1.0
status: draft
updatedAt: 2026-06-05
docType: research-lane-output
lane: indexing-shape
dispatch: domainspec-core-tagging-indexing-20260605
---

# Indexing Shape

## Purpose

Define how repository-wide Inventory indexes should be structured for
`domainspec-core`.

This is a shape proposal for lookup and future ingest/backfill work. It does not
create source-backed cards yet.

## Index Layers

Use five layers.

```text
repository index
  -> zone indexes
    -> slice indexes
      -> evidence-card indexes
        -> retrieval fixtures / EvidenceSets
```

## Proposed Package Layout

Recommended generated Inventory package:

```text
arcana/inventory/development/domainspec-core/
  REPOSITORY-TAGGING-INDEXING-RESEARCH-STRATEGY.md
  DOMAIN-SPEC-CORE-TAGGING-INDEXING-DISPATCH.json
  ZONE-AUTHORITY-MAP.md
  EXISTING-KNOWLEDGE-SURFACES.md
  TAG-TAXONOMY.md
  INDEXING-SHAPE.md
  PILOT-SLICE-BACKLOG.md
  RESEARCH-SYNTHESIS.md
  indexes/
    repository-index.json
    zone-index.json
    tag-index.json
    surface-index.json
  slices/
    <slice-id>/
      cards.json
      index.json
      retrieval.json
      COVERAGE.md
  evidence-sets/
    evidence-sets.json
  lint/
    latest.md
```

Only the strategy artifacts are created in this run. The `indexes/`, `slices/`,
and `evidence-sets/` folders should be created by the first approved Inventory
ingest/backfill task.

## Repository Index

Purpose:

- list top-level zones,
- classify source status,
- point to zone index entries,
- expose exclusions.

Minimum fields:

```json
{
  "repo_root": "/home/vrondelli/projects/domainspec-core",
  "updated_at": "2026-06-05",
  "zones": [
    {
      "zone_id": "implementation-domainspec",
      "path": "implementation/domainspec",
      "authority_class": "submodule-source",
      "authority_owner": "domainspec-implementation",
      "default_source_policy": "read-only",
      "index_ref": "indexes/zones/implementation-domainspec.json",
      "tags": [
        "zone:implementation-domainspec",
        "source:submodule",
        "authority:domainspec-implementation"
      ],
      "residue": []
    }
  ],
  "excluded_by_default": [
    ".git",
    ".arcanum",
    ".codex",
    ".data",
    "output",
    "node_modules"
  ]
}
```

## Zone Index

Purpose:

- map each zone's primary surfaces,
- record source selectors,
- identify nested inventory/index surfaces,
- point to slice candidates.

Minimum fields:

```json
{
  "zone_id": "research",
  "path": "research",
  "authority_class": "research-source",
  "primary_surfaces": [
    {
      "path": "research/registry/PROJECT-INDEX.md",
      "role": "project-index",
      "source_class": "canonical",
      "tags": [
        "zone:research",
        "artifact:registry",
        "source:canonical"
      ]
    }
  ],
  "existing_inventory_surfaces": [
    "research/projects/domainspec/inventory",
    "research/projects/mars/inventory"
  ],
  "slice_candidates": [
    "research-project-contracts"
  ],
  "exclusions": []
}
```

## Tag Index

Purpose:

- support shell/JQ lookup,
- prevent tag sprawl,
- show tag families and meanings.

Minimum fields:

```json
{
  "tag": "risk:authority-conflict",
  "family": "risk",
  "meaning": "Multiple surfaces claim or imply authority over the same behavior, lifecycle, definition, or relation.",
  "owner": "inventory",
  "promotion_guardrail": "Does not decide the conflict; routes to decision-gate or owner capability.",
  "related_tags": [
    "handoff:decision-gate",
    "authority:unknown"
  ]
}
```

## Surface Index

Purpose:

- register existing docs, inventories, registries, glossaries, vaults, source
  digests, and project indexes before creating new inventory cards.

Minimum fields:

```json
{
  "surface_id": "root-asset-ownership-policy",
  "path": "ops/ASSET-OWNERSHIP-POLICY.md",
  "surface_type": "policy",
  "zone_id": "ops",
  "authority_owner": "root-governance",
  "source_class": "canonical",
  "tags": [
    "zone:ops",
    "artifact:policy",
    "authority:root-governance",
    "domain:automation-assets"
  ],
  "lookup_use": "Classify Type A, Type B, and Type C automation asset ownership.",
  "do_not_use_for": [
    "runtime execution evidence",
    "implementation source changes"
  ]
}
```

## Slice Index

Purpose:

- keep each Inventory slice task-shaped,
- avoid whole-folder summaries,
- tie cards to retrieval value.

Minimum fields:

```json
{
  "slice_id": "sigils-library-arcanum-authority",
  "retrieval_question": "Which source should an agent use when deciding whether a reusable capability belongs to Arcanum or sigils-library?",
  "source_anchors": [
    "arcanum/README.md",
    "arcanum/registry/SIGILS.md",
    "sigils-library/README.md"
  ],
  "expected_outputs": [
    "cards.json",
    "index.json",
    "retrieval.json",
    "COVERAGE.md"
  ],
  "stop_conditions": [
    "Block if the slice starts deciding authority rather than describing the conflict."
  ]
}
```

## Evidence-Card Index

Purpose:

- provide selector-level evidence for future lookup,
- preserve source authority,
- expose residue.

Use the existing Inventory evidence-card contract from
`arcana/inventory/SKILL.md` and existing templates under
`arcana/inventory/development/templates/`.

Required index behavior:

- every card appears in the slice `index.json`,
- every card has tags from `TAG-TAXONOMY.md`,
- every material claim has `source_refs`,
- relation/definition/ontology-like claims carry non-authority language,
- generated/runtime state requires a source promotion note or is excluded.

## Retrieval Fixtures

Each slice should include one realistic retrieval fixture:

```json
{
  "query": "What source owns automation asset propagation policy?",
  "selected_cards": [
    {
      "card_id": "ops-asset-ownership-policy",
      "reason": "Defines Type A, Type B, Type C ownership and propagation rules."
    }
  ],
  "excluded_cards": [
    {
      "card_id": "implementation-domainspec-readme",
      "reason": "Explains DomainSpec but does not own root automation propagation policy."
    }
  ],
  "fallback_searches_required": []
}
```

## Indexing Stop Conditions

Stop and route before writing cards when:

- a slice requires reading a whole high-count zone,
- a tag encodes canonical meaning,
- two zones claim source authority over the same capability,
- a generated/runtime artifact is needed but lacks durable promotion evidence,
- a project-local inventory would be overwritten by parent Inventory,
- a nested Git/submodule source would be mutated from parent Inventory.

## First Index Creation Recommendation

Do not create `repository-index.json` first by sweeping all files.

Create it after the first approved pilot slice proves:

- the tag taxonomy is usable,
- source selectors are precise enough,
- retrieval fixtures can answer real agent questions,
- duplicate inventory risks are manageable.
