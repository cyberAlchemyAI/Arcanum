---
name: sync-user-stories
description: Generate story-driven STORIES from DomainSpec aspect docs with mandatory slice coverage and a concept-coverage matrix.
metadata:
  tier: arcana
  status: draft
  scope: repository-local
---

# Sigil: Sync User Stories

<objective>
Turn a feature's DomainSpec aspect docs into capability-scoped user stories with a coverage matrix that flags any concept not yet covered by a story.
</objective>

<logic-type>
Arcana: spec→story derivation with mandatory-slice coverage accounting.
</logic-type>

<applicability>
Use when a feature has a DomainSpec `SPEC.md` + aspect docs and you need traceable user stories whose coverage of the domain is auditable. M2-C5 of the DomainSpec capability pipeline.
</applicability>

<inputs>
- feature `SPEC.md` (capabilities + Concept Registry),
- aspect docs (operations/queries/interfaces/states/events),
- canonical vocabulary (`definitions/DEFINITIONS.md` DS-D1/D2).
</inputs>

<process>
1. For each capability, derive stories in Classic ("As a … I want … so that …") and BDD (Given/When/Then) forms.
2. Enforce the **mandatory slice taxonomy** — every capability must produce, where applicable:
   - a public/happy-path journey,
   - an admin/ops journey,
   - a cross-feature integration journey,
   - an error/edge journey.
   Mark any slice that does not apply as explicitly N/A with reason (do not silently omit).
3. Link each story's acceptance checks to the concept IDs and aspect anchors they exercise.
4. Build a **Story Coverage Matrix**: rows = Concept Registry IDs, columns = stories; flag any concept with zero covering stories as a coverage gap.
5. Emit `STORIES.md` + the coverage matrix. Do not invent concepts absent from the SPEC.
</process>

<anti-patterns>
Avoid:
- omitting a mandatory slice without an explicit N/A reason,
- stories that reference concepts not in the Concept Registry,
- acceptance checks with no concept/aspect anchor,
- reporting coverage without flagging unmapped concepts.
</anti-patterns>

<output-contract>
Return:

```markdown
## User Stories Sync

- Feature: <name>
- Capabilities covered: <n>
- Stories: <count> (Classic + BDD)
- Mandatory slices: public <y/n/na> · admin <y/n/na> · integration <y/n/na> · error <y/n/na>
- Concept coverage: <covered>/<total> (unmapped: <ids>)
- Output: STORIES.md + coverage matrix
- Follow-ups: <gaps>
```
</output-contract>
