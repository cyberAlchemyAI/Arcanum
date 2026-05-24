# Invoke Define Transport: Necronomicon

## Source

- Observed capability: `invoke`
- Invoke mode: `define`
- Target artifact: `necronomicon`
- Target owner: Necronomicon spell development cycle

## Inputs

- Existing Necronomicon development pack.
- User correction: Necronomicon should start with ontology and inventory handling.
- Existing knowledge substrate rationale in `KNOWLEDGE-SUBSTRATE-FLOW.md`.

## Outputs

- Spec: `spells/necronomicon/development/DEFINE.md`
- Glossary: `spells/necronomicon/development/GLOSSARY.md`

## Transport Summary

Define mode re-centered Necronomicon around the Inventory And Ontology Substrate Loop. The MVP is now the authority-preserving flow from inventory retrieval and session evidence into candidates, gaps, and owner-correct handoffs.

## Decisions

| Decision | Status |
| --- | --- |
| MVP starts with substrate handling, not route/bootstrap proof. | selected |
| Necronomicon may create candidates and gaps but not promote them. | selected |
| Inventory retrieval precedes broad source search for durable knowledge questions. | selected |
| Bootstrap configures the substrate after L0 proof. | selected |

## Gaps

| Gap | Owner | Next Route |
| --- | --- | --- |
| Exact L0 state schemas need plan detail. | Necronomicon | invoke plan |
| Canonical README needs synchronization after development pack approval. | Necronomicon | task-session |
