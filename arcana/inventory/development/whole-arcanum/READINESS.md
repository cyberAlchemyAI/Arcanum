---
module: inventory-whole-arcanum
version: 0.1.0
status: ready-for-agent-poc
updatedAt: 2026-06-03
docType: readiness-report
---

# Readiness Report: Whole Arcanum Inventory

## Verdict

The whole-Arcanum Inventory package is ready for an agent-facing POC using the
selected shell plus `jq` surface.

It is not yet promoted as a canonical repository-wide knowledge system. The
current state is a validated development package with source boundaries,
evidence-card slices, candidate EvidenceSets, coverage reports, and a repeatable
validation command.

The runtime proof path is now native/generated skill packages plus canonical
source contracts. Legacy `.codex/commands` files are excluded from the live
Inventory proof unless a future migration explicitly promotes one as durable
evidence.

## Evidence Summary

| Area | Status | Evidence |
| --- | --- | --- |
| Source boundary | pass | `source-manifest.json` and `SOURCE-POLICY.md` define included source families and exclusions. |
| Inventory self-slice | pass | `cards/inventory/` validates. |
| Governance slice | pass | `cards/governance/` validates. |
| Lifecycle slice | pass | `cards/lifecycle/` validates. |
| Arcana capability slice | pass | `cards/arcana/` validates and has `COVERAGE.md`. |
| Composition slice | pass | `cards/composition/` validates and has `COVERAGE.md`. |
| Runtime support slice | pass | `cards/runtime/` validates and has `COVERAGE.md`; legacy command-file proof is excluded. |
| Candidate EvidenceSets | pass | `evidence-sets/evidence-sets.json` references known cards. |
| Operational validation contract | pass | `OPERATIONAL-COMMANDS.md` and `scripts/validate-whole-arcanum-inventory.sh` exist. |
| Validation suite | pass | `validate-whole-arcanum-inventory.sh` returns `RESULT: pass`. |
| Native install smoke | pass | Temporary target installed `inventory`, `invoke`, `task-session`, and `orchestrate` under `.agents/skills/` with zero `.codex/commands` files. |

## Validation Command

Run from the repository root:

```bash
bash arcana/inventory/development/whole-arcanum/scripts/validate-whole-arcanum-inventory.sh
```

Latest observed result on 2026-06-03: `RESULT: pass`.

The Artifact Constitution validator still reports pre-existing benchmark
generated-artifact warnings, but it returns `result: pass`. These warnings are
not blockers for this Inventory POC.

## Current Query Surface

The inventory is usable by agents through direct `jq` commands over card slices.
Examples are documented in `OPERATIONAL-COMMANDS.md`.

Minimum useful query paths:

- list cards: `cards/*/cards.json`,
- select by tag: `cards/*/cards.json`,
- inspect retrieval fixtures: `cards/*/retrieval.json`,
- inspect candidate sets: `evidence-sets/evidence-sets.json`.

## Promotion Gate

Promotion from development package to broader reusable Inventory surface should
wait until these conditions are met:

1. At least one real implementation task uses the inventory first, before broad
   source search.
2. The task records which cards or EvidenceSets were useful and which were
   missing.
3. A second validation run after that real use still returns `RESULT: pass`.
4. Candidate EvidenceSets are either promoted, split, or rejected based on reuse
   evidence.
5. Any new schema-shaped machine-readable artifacts follow Schema Constitution
   `.schema.yml` rules.

## Deferred Decisions

| Decision | Status | Revisit Trigger |
| --- | --- | --- |
| Human UI | deferred | Revisit after shell plus `jq` queries become too hard for humans to inspect. |
| EvidenceSet promotion | deferred | Revisit after repeated task-session reuse shows stable value. |
| Native package integration | deferred | Revisit when generated native runtime packages should expose whole-inventory validation directly. |
| Fine-grained card expansion | deferred | Revisit when a concrete task needs omitted package-level cards. |

## Remaining Gaps

- The current cards are high-value clustered slices, not exhaustive package
  coverage.
- Retrieval is file-based `jq`; there is no dedicated native wrapper yet.
- EvidenceSets are candidate-level and should not be treated as canonical
  context-builder contracts.
- Coverage reports name omissions but do not yet create backlog items for every
  omitted artifact.

## External Repository Test

Use the native profile install path in a target repository:

```bash
bash tools/bootstrap_arcanum.sh --target <repo> --sigils inventory,task-session --spells invoke --profiles repo-codex,repo-local --clean-legacy-codex-commands --force --no-necronomicon
```

Smoke evidence from a temporary target:

- `tools/arcanum --resolve inventory` -> `.agents/skills/inventory/SKILL.md`,
- `tools/arcanum --resolve invoke` -> `.agents/skills/invoke/SKILL.md`,
- default adapter -> `native-skill`,
- legacy command files -> `0`.

## Next Recommended Use

Use this inventory in a real Arcanum implementation task, preferably in the
target repository after native-profile install:

1. Run the full validation command.
2. Query relevant cards and candidate EvidenceSets before opening broad source
   files.
3. Execute the implementation task.
4. Record which cards shortened retrieval, which cards were stale or missing,
   and whether a new EvidenceSet should be promoted or split.
