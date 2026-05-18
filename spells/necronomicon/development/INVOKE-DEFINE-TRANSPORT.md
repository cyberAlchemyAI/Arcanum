# Invoke Define Transport: Necronomicon

## Source Context

- `spells/necronomicon/README.md`
- `spells/necronomicon/development/USAGE-VISION.md`
- `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md`
- `spells/necronomicon/development/RESEARCH-DISCOVERY.md`

## Define Outputs

- Spec: `spells/necronomicon/development/DEFINE.md`
- Glossary: `spells/necronomicon/development/GLOSSARY.md`
- Implementation layering seed: existing `spells/necronomicon/development/IMPLEMENTATION-LAYERING.md`

## Template Selection Evidence

- Selected profile: Module Formulae module spec and glossary baseline.
- Reason: Necronomicon now has a product/module boundary, first-class concepts, owned capabilities, external dependencies, and downstream design needs.
- Candidate-template permission: not needed; existing Module Formulae profile is sufficient.

## Define Decisions

- MVP is Session Memory Router.
- Continuation build is Workbench State Manager.
- Side notes are first-class harness input.
- Related unblockers can become bounded side tasks.
- Inventory is the retrieval and durable knowledge surface.
- Ontology promotion remains downstream.
- Invoke is used for lifecycle authoring, not as the default research engine.

## Define Gaps

- `active-interaction.json` schema is not finalized.
- `side-notes.jsonl` and unblocker task schemas are not finalized.
- Inventory install/adoption path may vary by repository.

## Define Deferred Decisions

- Research extraction is deferred. Research remains a Necronomicon mode for MVP until repeated non-Necronomicon reuse justifies a reusable sigil.

## Next Route

`invoke design`
