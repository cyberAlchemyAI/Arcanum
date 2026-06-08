---
module: inventory-whole-arcanum
task: TASK-WAI-004
swu: SWU-WAI-008
status: built
layer: L2
createdAt: 2026-06-01
docType: task-session-context
---

# Context Pack: SWU-WAI-008 Arcana Capability Cards

## Selected Scope

`SWU-WAI-008` expands the `arcana/` capability family into inventory cards.
The write scope is limited to:

- `arcana/inventory/development/whole-arcanum/cards/arcana/`

## Controlling Sources

- `arcana/inventory/development/whole-arcanum/WORK-PACK.md`
- `arcana/inventory/development/whole-arcanum/work-pack/tasks/TASK-WAI-004-expanded-capability-waves.md`
- `arcana/inventory/development/whole-arcanum/source-manifest.json`
- `arcana/inventory/development/whole-arcanum/SOURCE-POLICY.md`
- Representative `arcana/*/SKILL.md` contracts

## Constraints

- Use tracked source selectors and small line spans.
- Do not ingest generated observability or runtime paths.
- Preserve owner boundaries; cards may summarize capability families but must
  not redefine the canonical skill contracts.
- Record intentional omissions and duplicate/overlap risks in a coverage note.
- Validate the slice with the slice-aware evidence card validator.

## Decision Pack

No blocker-level decision is visible for this SWU. The non-blocking
implementation choice is the card granularity:

| Option | Consequence | Decision |
| --- | --- | --- |
| One card per `arcana/` package | Broad coverage, slower agent retrieval, higher maintenance churn. | Rejected for this first L2 slice. |
| Clustered high-value capability cards | Faster retrieval and clearer ownership boundaries, with explicit coverage gaps. | Selected. |

## Gate Verdict

Proceed. W1 validation is complete, the implementation completion gate says no
blocker-level decisions remain, and the write scope is narrow enough to mutate.
