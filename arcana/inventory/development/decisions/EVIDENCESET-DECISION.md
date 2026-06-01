# Decision Gate: EvidenceSet Candidate

## Target Scope

Inventory EvidenceSet candidate after first evidence-card POC.

## Consequential Work Blocked

Canonicalizing `EvidenceSet` as an Inventory artifact would affect schema, index, retrieval, handoff, validator, and docs behavior. That should not proceed without an explicit decision.

## Context Evidence

| Evidence | Signal |
| --- | --- |
| `decisions/POC-GATES-DECISION.md` | Five of six POC gates pass; retrieval value is flagged only because second-slice reuse is not yet proven. |
| `POC-VALIDATION.md` | EvidenceSet is candidate-only and should continue only if grouped evidence proves reusable. |
| `pilot-retrieval.json` | First retrieval produced 6 selected cards, 3 excluded matches, and a candidate EvidenceSet with 4 included cards and 2 excluded cards. |
| `pilot-handoff-ontology.json` | Ontology handoff reused a related card group with non-authority language. |
| `pilot-handoff-definitions.json` | Definitions handoff reused term/card groups with non-authority language. |
| `POC-CANDIDATES.md` | Craft selected sections are the strongest second-pass EvidenceSet stressor. |
| `validate-evidence-card-fixtures.sh` | Current fixtures pass agent/runtime validation. |

## Decision Question

What should Inventory do with `EvidenceSet` after the first POC?

## Options

### Option 1: Promote EvidenceSet Now

- Benefit: gives Inventory a durable grouped-evidence artifact immediately.
- Cost/Risk: one pilot slice is not enough evidence; may create ceremony or duplicate Context Builder packs.
- Choose when: the team already accepts grouped evidence as a core Inventory primitive.
- Downstream impact: requires schema, templates, validator rules, index behavior, docs, and handoff updates.

### Option 2: Keep Candidate And Run Craft Stressor

- Benefit: preserves the promising idea while testing it against nested contexts, artifacts, gates, blockers, enablers, and recomposition.
- Cost/Risk: one more POC pass before canonicalization.
- Choose when: current evidence is promising but not sufficient for a schema commitment.
- Downstream impact: adds one bounded second-pass fixture/query before promotion, drop, or redesign.

### Option 3: Drop EvidenceSet Into Retrieval Output Only

- Benefit: avoids adding an artifact family.
- Cost/Risk: may lose reusable grouped context that appears useful for handoff assembly.
- Choose when: card groups are one-off and do not need stable IDs or lifecycle.
- Downstream impact: retrieval keeps selected/excluded cards, but no stored set artifact exists.

## Recommended Option

Option 2: keep candidate and run Craft stressor.

## Selected Option

Option 2: keep candidate and run Craft stressor.

Source of decision: user invoked `task-session` after the small refine and decision gate on 2026-05-27.

## Result

`BLOCK` for canonical EvidenceSet promotion.

`PASS` for bounded second-pass exploration.

`PASS` for completed Craft stressor validation.

## Remaining Blockers

No blocker remains for the Craft stressor.

One blocker remains for canonical promotion: EvidenceSet needs a minimal schema/design task before production behavior changes.

## Deferred Decisions

- Human UI for EvidenceSet review remains deferred.
- Final naming can be revisited after the Craft stressor if Option 2 is selected.
