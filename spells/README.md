# Spells

Spells are localized workflow compositions that combine multiple sigils into a coherent run.

A sigil is an atomic capability. A spell is a recipe: it defines which sigils run, in what order, what state they share, which artifacts move between phases, what gates can stop the workflow, and how the overall run is observed.

## How Spells Differ From Sigils

Sigils define reusable behaviors such as inventory maintenance, context synthesis, decision gating, or implementation layering.

Spells compose those behaviors for a specific class of work. They do not copy sigil internals. They reference sigils by name and define orchestration around them.

## Use Spells When

- several sigils are more useful together than alone,
- a repository needs a repeatable local workflow,
- outputs from one sigil should become inputs to another,
- the workflow needs gates, handoffs, and shared state,
- users need a guided path instead of choosing each sigil manually.

## Avoid Spells When

- one sigil already handles the task clearly,
- the sequence is experimental and not worth preserving,
- the workflow has no shared artifacts or gates,
- the spell would duplicate sigil instructions instead of referencing them,
- local project details would make the composition unusable elsewhere.

## Library Spells And Local Spells

This folder contains reusable first-party spells. A consuming repository may install and adapt a spell locally under:

```text
.arcanum/spells/
```

Local spells can bind project-specific paths, thresholds, gate policies, and harness choices without changing the upstream sigils.

## Names And Aliases

Each spell has one stable canonical ID in kebab-case, such as `repository-harness`. This ID is used for filenames, registry links, automation, and validation.

Spells may also define aliases: memorable names, local nicknames, or branded invocation names. For example, a local repository may invoke `repository-harness` as `Repository Codex` while keeping the canonical file and registry entry stable.

`Ontology Harness` is the spell for ontology governance, vault-like knowledge, session distillation, premise review, branch-aware business/system mapping, and bridge validation.

`Necronomicon` is the persistent repository harness. Use `necronomicon` when a repository should keep durable session memory, route first through selected local sigils and spells, offer Arcanum fallback candidates, and update the selected capability set with an audit trail.

Alias rules:

- aliases must resolve to exactly one canonical spell,
- aliases should be listed in the spell registry and spell file,
- aliases are case-insensitive for lookup,
- local aliases may override library aliases only inside the consuming repository,
- automation should store both the alias used and the canonical spell ID in run reports.

## Authoring Help

Use [spellcraft](../arcana/spellcraft/) to design, install, validate, observe, or revise spells.

Active spell development packs live inside each spell folder under `spells/<canonical-id>/development/` until Spellcraft validation and release approval promote canonical spell changes. `invoke` may prepare the spec, design bundle, or work-pack for a spell, but Spellcraft remains the lifecycle authority for spell composition.

For multi-mode spells, keep one canonical contract file as `README.md` inside the spell folder and place mode-specific contracts in sibling files. Example:

```text
spells/invoke/README.md
spells/invoke/define.md
spells/invoke/design.md
```

The root file should keep cross-mode identity, gates, shared state, and handoff policy, while mode files carry mode-specific phases and output details.

Start with the [Spell Registry](../registry/SPELLS.md) for available first-party spells.
