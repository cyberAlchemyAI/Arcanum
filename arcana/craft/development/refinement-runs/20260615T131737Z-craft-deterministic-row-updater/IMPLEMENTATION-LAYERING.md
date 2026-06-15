# Implementation Layering: Craft Row Update Planner

## Layer Decision

The row updater should be split out as a planner primitive before broad CSV
writeback.

## Layers

| Layer | Question | Scope | Promotion Evidence |
| --- | --- | --- | --- |
| L0 | Can Craft name the row update planner contract and prove it on a tiny fixture? | schema/docs plus fixture expectations | YAML parse, fixture parse, targeted grep |
| L1 | Can the planner emit deterministic dry-run patch plans for selected fields? | `arcana/craft/scripts/` internal implementation | fixture run, stable JSON report, no-op/block/pass cases |
| L2 | Can CSV import call the planner without owning reconciliation semantics? | `import-csv --dry-run` integration | multi-row dry-run report and stale-source blocking |
| L3 | Can runtime mirrors and publication gates reflect the new behavior safely? | generated mirrors and validation reports | generation check, diff check, public-boundary scan |

## Out Of Scope

- direct YAML apply mode;
- arbitrary nested updates;
- project-local generated projection commit policy;
- parent gitlink movement;
- publication.
