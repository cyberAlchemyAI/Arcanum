# SWU-NEO-001 Context Pack

## Session

- Task session: `SWU-NEO-001`
- Workflow profile: `iterative-refinement`
- Work pack: `spells/necronomicon/development/WORK-PACK.md`
- Target artifact: `spells/necronomicon/README.md`
- Runtime: local Codex task session
- Coverage status: strict pass

## Local Evidence Baseline

| Source | Coverage | Relevant contract |
| --- | --- | --- |
| `spells/necronomicon/development/WORK-PACK.md` | covered | `SWU-NEO-001` rewrites canonical README around substrate-first MVP; generated command snapshots require explicit approval. |
| `spells/necronomicon/development/DEFINE.md` | covered | MVP is `Inventory And Ontology Substrate Loop`; routing/setup/research/maintenance are support layers; no-promotion guardrails are mandatory. |
| `spells/necronomicon/development/DESIGN.md` | covered | Design starts from knowledge authority, inventory retrieval, evidence capture, authority classification, gaps, and handoffs. |
| `spells/necronomicon/README.md` | covered | Canonical README contained old harness/routing-first framing and needed contract sync. |

## Required Contract

- README must state the MVP is `Inventory And Ontology Substrate Loop`.
- README must state routing, setup profiles, active interaction state, bounded research, checkpoints, and maintenance are support layers.
- README must explicitly preserve no-promotion guardrails.
- README must not revive stale `Session Memory Router` MVP language.

## Gaps

- No blocking source gaps for this SWU.
- Generated command snapshots are intentionally out of scope until explicitly approved after the canonical README edit.
- L0 schemas, fixtures, and adapter proof remain separate SWUs.

## Fallback Search Status

- Broad fallback search was not needed.
- Local context coverage was sufficient from the work-pack, define document, design document, and current README.

## Handoff Notes

- Next recommended SWU: `SWU-NEO-002` for L0 state shape contracts.
- Do not start `SWU-NEO-004` adapter or generated command snapshot updates until canonical README approval and L0 evidence are available.
