# TASK-CLO-007: Prepare Registry Candidate

## Goal

Prepare registry and docs updates for explicit approval.

## Layer

L3 Registry Candidate

## Micro-Layers

- L3.1 Candidate Metadata
- L3.2 Routing And Link Check
- L3.3 Promotion Decision

## Blocker

- B-CLO-002: registry promotion requires explicit approval.

## Source Contracts

- validated package README and SKILL,
- validation report,
- runtime evidence,
- local registry and docs conventions.

## Inputs

- package artifacts from L0,
- validation evidence from L1,
- runtime and observability evidence from L2,
- explicit user or lifecycle owner approval to prepare registry candidacy.

## Output Artifacts

- registry candidate metadata,
- docs/package links,
- link validation notes,
- `arcana/concept-layer-optimizer/development/REGISTRY-PROMOTION.md` or equivalent promotion record.

## Implementation Steps

1. Confirm runtime and validation evidence exist.
2. Prepare candidate metadata: name, purpose, route, tier, dependencies, lifecycle owner, and validation links.
3. Add or stage docs links without silently making the sigil canonical.
4. Run link and route checks for README, SKILL, examples, validation, and runtime adapter.
5. Record promotion status: promote, hold, or revise.
6. Capture approval state and any remaining risks.

## Edge Cases

- Do not promote without explicit approval.
- Do not promote global glossary terms as part of registry work.
- Do not hide broken links behind a promotion decision.
- If runtime evidence is absent, prepare a hold/revise record instead of promotion.

## Smallest Working Units

| SWU | Micro-Layer | Work | Acceptance |
| --- | --- | --- | --- |
| SWU-CLO-015 | L3.1 | Prepare registry/docs candidate metadata. | Candidate entry and package links exist behind approval. |
| SWU-CLO-016 | L3.2 | Run routing and link check. | README, SKILL, examples, validation, and adapter links are reachable. |
| SWU-CLO-017 | L3.3 | Record promotion decision. | Decision names promote, hold, or revise with evidence and approval status. |

## Verification

```bash
rg -n "concept-layer-optimizer|Concept Layer Optimizer" registry README.md framework arcana 2>/dev/null
```

Use local link review when registry/docs paths differ.

## Done When

- Candidate entry is reviewable.
- Link validation passes.
- Approval status is explicit.
