# Glossary Consistency: Craft Schema Stack

## Verdict

Pass with target-artifact gaps. The proposed schema terms are consistent with
current Craft language, but several concepts are not yet canonical schema
surfaces.

## Term Checks

| Term | Current Source | Consistency |
| --- | --- | --- |
| Source ledger | `SKILL.md`, `README.md`, `ARCHITECTURE.md` | Consistent: `.craft/ledger.yml` remains authority. |
| Human view | `SKILL.md`, `README.md`, examples | Consistent: `CRAFT.md` is derived and linked. |
| Generated index | `SKILL.md`, refine/index proposal | Consistent but underspecified: `.craft/index.json` needs schema. |
| Embedded indexes | `ledger.schema.yml`, examples | Consistent but shallow: key list exists, object shape missing. |
| Projection | refine/index proposal, row-update design | Candidate: not canonical yet. |
| Row update planner | row-update architecture | Candidate: dry-run planner only, no apply mode. |
| Route handoff | interaction draft, Body War example | Candidate but evidence-backed. |
| Receipt | interaction draft, Body War example | Candidate but evidence-backed. |
| Route event | interaction draft only | Candidate-local until example coverage exists. |
| Recomposition | `SKILL.md`, examples | Canonical behavior, missing formal row schema. |
| Definition | `SKILL.md`, examples | Local-candidate only; canonical-definition promotion remains outside Craft. |
| Gap | `SKILL.md`, examples | Canonical behavior, missing formal row schema. |

## Conflicts Or Drifts

| Drift | Impact | Resolution |
| --- | --- | --- |
| `SKILL.md` names descriptions, definitions, gaps, and recomposition, but `ledger.schema.yml` does not formalize them. | Source schema cannot validate live examples fully. | P0 schema split should promote these row families. |
| Generated `.craft/index.json` is named as rebuildable but not shaped. | Tools cannot safely rely on freshness or lookup contracts. | P0 index schema should define metadata and lookup groups. |
| `CRAFT.md` requirements are prose-only. | Renderers and reviewers lack a stable interface contract. | P1 interface schema should validate anchors and required sections. |
| Route handoffs/receipts are present in drafts and one example but not canonical. | Receipt-backed workflows remain informal. | P1 route-exchange schema after source/index schemas. |
| Projection and row updater designs depend on schemas not yet present. | CSV/import work risks schema drift. | P2 projection and row-update schemas after P0/P1 coverage. |

## Glossary Decision

Do not promote new canonical definitions from this invoke run. Treat this bundle
as a target-artifact design gap inventory and route implementation through
Craft maintenance.
