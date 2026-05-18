# Invoke Design Transport: Necronomicon

## Source Context

- Define spec: `spells/necronomicon/development/DEFINE.md`
- Glossary: `spells/necronomicon/development/GLOSSARY.md`
- Canonical spell contract: `spells/necronomicon/README.md`
- UX vision: `spells/necronomicon/development/USAGE-VISION.md`
- Knowledge substrate: `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md`

## Design Outputs

- Architecture bundle: `spells/necronomicon/development/DESIGN.md`
- Glossary consistency report: `spells/necronomicon/development/GLOSSARY-CONSISTENCY.md`
- Transport report: `spells/necronomicon/development/INVOKE-DESIGN-TRANSPORT.md`

## Six-View Coverage

| View | Status |
| --- | --- |
| Context view | pass |
| High-level structure view | pass |
| Low-level components view | pass |
| Workflow process view | pass |
| Decision flow view | pass |
| Dependency interface view | pass |

## Design Decisions

- File-backed state remains the first implementation architecture.
- Turn classifier is deterministic and ordered before any adaptive routing.
- Side notes are first-class non-derailing input.
- Related unblockers can run or queue when small, safe, and blocking.
- Full scheduler/parallel orchestration is deferred.

## Design Gaps

- Exact schemas for active interaction, side notes, routes, gaps, and checkpoints.
- Fixture set for turn classification and workbench queue behavior.
- Plan-layer breakdown for L0-L4 implementation slices.

## Design-Carried Decisions

- Schema strictness: JSON schema drafts in plan; typed validator deferred.
- Side-note processing: checkpoint plus user-triggered processing selected; automatic thresholds deferred.
- Unblocker execution: run or queue when narrow and blocking; full side-task orchestration deferred.
- Research extraction: keep as Necronomicon mode for MVP; reusable sigil extraction deferred.

## Next Route

`invoke plan`
