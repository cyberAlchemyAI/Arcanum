---
module: inventory-domainspec-core
version: 0.1.0
status: draft
updatedAt: 2026-06-05
docType: synthesis
dispatch: domainspec-core-tagging-indexing-20260605
---

# Research Synthesis: DomainSpec-Core Tagging And Indexing

## Result

The repository-wide tagging and indexing strategy is executable, but the next
step should still be a gated pilot slice, not broad ingest.

This research pass created:

- `ZONE-AUTHORITY-MAP.md`
- `EXISTING-KNOWLEDGE-SURFACES.md`
- `TAG-TAXONOMY.md`
- `INDEXING-SHAPE.md`
- `PILOT-SLICE-BACKLOG.md`

## Main Findings

### 1. The repository is a governed multi-repo workspace.

Evidence:

- `/home/vrondelli/projects/domainspec-core/README.md`
- `/home/vrondelli/projects/domainspec-core/.gitmodules`
- `/home/vrondelli/projects/domainspec-core/ops/ASSET-OWNERSHIP-POLICY.md`

The parent repository includes nested submodules:

- `arcanum`
- `implementation/domainspec`
- `validation/poker-team`

Inventory should index these as owned source zones, not mutate them from parent
repo work.

### 2. Root governance already defines asset authority.

Evidence:

- `/home/vrondelli/projects/domainspec-core/ops/ASSET-OWNERSHIP-POLICY.md`
- `/home/vrondelli/projects/domainspec-core/ops/REPOSITORY-ORGANIZATION-PLAN.md`

The Type A/B/C asset model is the right authority frame for automation asset
indexing:

- Type A: canonical DomainSpec pack in `implementation/domainspec/copilot`.
- Type B: root research orchestration assets in `.github`, `research`, and
  shared/registry paths.
- Type C: project-local overlays in validation or consumer repos.

### 3. Existing inventories and indexes must be reused.

Evidence:

- `research/projects/*/inventory`
- `arcanum/arcana/inventory/development/whole-arcanum`
- `implementation/domainspec/docs/research/inventory`
- `projects/goldenquill/docs/AGENT_CONTEXT_INDEX.md`
- `projects/goldenquill/docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md`

Parent Inventory should aggregate handles and lookup routes. It should not
rewrite or duplicate project-local inventories.

### 4. The first high-risk ambiguity is Arcanum vs sigils-library authority.

Evidence:

- `arcanum/README.md`
- `arcanum/registry/SIGILS.md`
- `arcanum/registry/SPELLS.md`
- `sigils-library/README.md`

Both zones use capability/sigil authority language. This should be inventoried
as a bounded authority-comparison slice before parent tags assume one canonical
capability source.

### 5. Generated and runtime state is widespread.

Evidence:

- `.arcanum/`
- `.codex/`
- `.data/`
- `output/`
- `implementation/domainspec/.arcanum/`
- `implementation/domainspec/.codex/`
- `implementation/domainspec/node_modules/`
- `arcanum/benchmark/artifacts/`

Default policy: exclude generated/runtime state unless a durable source artifact
promotes it as evidence.

## Proposed Execution Model

Use this sequence:

1. Choose one pilot slice by decision gate.
2. Create slice folder:

   ```text
   arcana/inventory/development/domainspec-core/slices/<slice-id>/
   ```

3. Produce:

   ```text
   cards.json
   index.json
   retrieval.json
   COVERAGE.md
   ```

4. Validate against Inventory evidence-card rules.
5. Only after the first slice works, create repository-level indexes:

   ```text
   indexes/repository-index.json
   indexes/zone-index.json
   indexes/tag-index.json
   indexes/surface-index.json
   ```

## Recommended First Decision

Choose between:

| Option | Slice | Why |
| --- | --- | --- |
| A | Arcanum vs Sigils Library Authority | highest authority risk; directly relevant to current Inventory/Arcanum work |
| B | Root Asset Ownership And Automation Surface | lower-conflict governance slice; clarifies Type A/B/C ownership |
| C | Research Project Contract Index | proves cross-project index reuse without project-internal coupling |

Recommendation:

```text
A. Arcanum vs Sigils Library Authority
```

## Blockers

No blocker remains for strategy execution.

There is still a gate before ingest/backfill mutation:

```text
operator confirms the first slice target
```

## Next Task-Session Handoff

Task:

```text
Create first domainspec-core Inventory pilot slice.
```

Recommended target:

```text
sigils-library-arcanum-authority
```

Expected source anchors:

- `/home/vrondelli/projects/domainspec-core/arcanum/README.md`
- `/home/vrondelli/projects/domainspec-core/arcanum/registry/SIGILS.md`
- `/home/vrondelli/projects/domainspec-core/arcanum/registry/SPELLS.md`
- `/home/vrondelli/projects/domainspec-core/sigils-library/README.md`
- `/home/vrondelli/projects/domainspec-core/sigils-library/arcana/README.md`
- `/home/vrondelli/projects/domainspec-core/sigils-library/formulae/README.md`
- `/home/vrondelli/projects/domainspec-core/sigils-library/transmutations/README.md`

Expected output:

```text
arcana/inventory/development/domainspec-core/slices/sigils-library-arcanum-authority/
  cards.json
  index.json
  retrieval.json
  COVERAGE.md
```

Stop condition:

```text
Do not decide canonical authority. Record evidence, conflict, and decision-gate handoff.
```

## Research Receipt

Dispatch:

```text
domainspec-core-tagging-indexing-20260605
```

Artifacts created:

- `arcana/inventory/development/domainspec-core/ZONE-AUTHORITY-MAP.md`
- `arcana/inventory/development/domainspec-core/EXISTING-KNOWLEDGE-SURFACES.md`
- `arcana/inventory/development/domainspec-core/TAG-TAXONOMY.md`
- `arcana/inventory/development/domainspec-core/INDEXING-SHAPE.md`
- `arcana/inventory/development/domainspec-core/PILOT-SLICE-BACKLOG.md`
- `arcana/inventory/development/domainspec-core/RESEARCH-SYNTHESIS.md`

Validation to run:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py \
  arcana/inventory/development/domainspec-core/DOMAIN-SPEC-CORE-TAGGING-INDEXING-DISPATCH.json --json
```
