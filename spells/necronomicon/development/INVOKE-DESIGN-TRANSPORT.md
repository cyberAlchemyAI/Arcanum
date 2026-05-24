# Invoke Design Transport: Necronomicon

## Source

- Observed capability: `invoke`
- Invoke mode: `design`
- Target artifact: `necronomicon`
- Target owner: Necronomicon spell development cycle

## Outputs

- Architecture bundle: `spells/necronomicon/development/DESIGN.md`
- Glossary consistency report: `spells/necronomicon/development/GLOSSARY-CONSISTENCY.md`
- Implementation layering: `spells/necronomicon/development/IMPLEMENTATION-LAYERING.md`

## Transport Summary

Design mode converted the corrected definition into a six-view substrate-first architecture. The design names inventory retrieval, session evidence capture, authority classification, gap ledger writing, and handoff construction as the central components.

## Design Decisions

| Decision | Status |
| --- | --- |
| Use explicit file-backed substrate state. | selected |
| Keep adapter-mediated runtime acceptable for the first proof. | selected |
| Treat missing inventory as a gap with fallback, not a global blocker. | selected |
| Route governance-sensitive claims to ontology owners. | selected |
| Defer setup wizard, route presets, research, and maintenance beyond L0. | selected |

## Target Artifact Gaps

| Gap | Owner | Next Route |
| --- | --- | --- |
| State schemas need executable examples. | Necronomicon | invoke plan / task-session |
| Canonical README and generated command snapshots need sync. | Necronomicon | task-session after approval |

## Invoke Gaps

No invoke-specific blocker found.
