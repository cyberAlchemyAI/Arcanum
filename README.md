# Arcanum

**Arcanum** is a framework for creating reusable agent capabilities through governed synthesis.

It provides a method, lifecycle, quality bar, observability model, and capability structure for turning vague intent into artifacts that humans and agents can understand, reuse, validate, and improve.

The center of Arcanum is the [CyberAlchemy Method](framework/CYBERALCHEMY-METHOD.md): a way of working that keeps objective, output artifact, discovery, tension, trace, and lifecycle ownership visible throughout the work.

## Start Here

- Start with the [CyberAlchemy Method](framework/CYBERALCHEMY-METHOD.md) to understand the working philosophy.
- Start with the [Framework](framework/) when authoring, reviewing, validating, or maintaining capabilities.
- Start with the [Sigil Registry](registry/SIGILS.md) when you need one reusable capability.
- Start with the [Spell Registry](registry/SPELLS.md) when you need a composed workflow.
- Start with [Sigil Development](arcana/sigil-development/) when creating or revising a sigil.
- Start with [Spellcraft](arcana/spellcraft/) when creating or revising a spell.

## What Arcanum Is

Arcanum is for agent work that should become more than a one-off response.

It helps define:

- how a capability should be named and bounded,
- when an agent should ask, research, propose, challenge, validate, or stop,
- what artifact should exist at the end of a run,
- what quality and failure boundaries apply,
- how repeated usage should produce evidence for improvement,
- which lifecycle authority owns the next step.

Arcanum is not just a prompt library. A prompt can say what to do once. An Arcanum capability should explain when to use it, when not to use it, how it reasons, how it fails, what it outputs, how it is observed, and how it evolves.

## The Method

The [CyberAlchemy Method](framework/CYBERALCHEMY-METHOD.md) treats agent work as governed synthesis.

Every serious run should keep five anchors visible:

| Anchor | Question |
| --- | --- |
| Objective | What are we trying to solve? |
| Output artifact | What should exist when this work is done? |
| Discovery | What must we learn before the artifact can responsibly close? |
| Tension | What could make the artifact brittle, oversized, misleading, or unsafe? |
| Route | Who or what owns the next lifecycle step? |

The method is recursive but bounded. It favors research and discovery, structured tension, clear artifacts, ergonomic navigation, observability, and lifecycle routing. It does not reward complexity for being elegant; it introduces structure when the current context has a named tension that the simpler unit cannot responsibly handle.

## Observability Layer

Arcanum already includes an implemented repository-local observability layer.

The observability layer turns runs into evidence. It stores invocation signals, run envelopes, lookup indexes, hook operation records, reflection state, and reflection reports under `.arcanum/observability/`. This lets a capability improve from actual usage instead of relying on memory or vibes.

Implemented pieces include:

- central invocation ledger: `.arcanum/observability/signals/sigil-invocations.jsonl`,
- lookup indexes by sigil and capability under `.arcanum/observability/by-sigil/` and `.arcanum/observability/by-capability/`,
- run envelopes under `.arcanum/observability/runs/`,
- hook operation evidence under `.arcanum/observability/hooks/`,
- reflection state and reports under `.arcanum/observability/reflection-state.json` and `.arcanum/observability/reflections/`,
- framework guidance in [Observability](framework/observability/), [Repository Observability Package](framework/observability/REPOSITORY-PACKAGE.md), and [Sigil Observability Hook](framework/observability/SIGIL-OBSERVABILITY-HOOK.md).

This layer is part of the framework's governance model: if a sigil repeatedly drifts, blocks, misses its output contract, or creates confusing handoffs, observability gives the system a traceable reason to reflect and revise.

## Experiment Harness

Arcanum also includes an implemented experiment harness for validating reusable spells and sigils before promotion.

The [Experiment Harness](arcana/experiment-harness/) gives each artifact a local test loop: realistic fixtures go in, real user-facing outputs come out, and promotion decisions are based on inspectable evidence rather than contract prose alone.

Implemented harness support includes:

- artifact-local validation layout from the [Experiment Harness Standard](framework/EXPERIMENT-HARNESS-STANDARD.md),
- fixture and expected-output checks,
- bounded Codex example runs,
- generated example prompts and captured example outputs,
- validation reports under each artifact's `development/runs/`,
- observability emission through `observe-harness.sh`,
- command adapters such as `experiment-next`, `experiment-run`, `experiment-validate`, and `experiment-observe`.

The harness pairs with observability: validation proves whether a capability satisfies its contract in controlled examples, while observability records how it behaves in actual use.

## The Framework

The [framework](framework/) is the operating model for Arcanum capabilities.

The Method, Observability Layer, and Experiment Harness are highlighted above. The supporting framework references are:

- [Quality Bar](framework/QUALITY-BAR.md) - observable criteria for successful execution.
- [Anti-Patterns](framework/ANTI-PATTERNS.md) - known misuse cases and failure modes to avoid.
- [Sigil Development Workflow](framework/SIGIL-DEVELOPMENT-WORKFLOW.md) - lifecycle from candidate capture through maintenance.
- [Validation Experiment Protocol](framework/VALIDATION-EXPERIMENT-PROTOCOL.md) - release-gate experiments for spells, sigils, and templates.
- [Sigil Template](framework/templates/sigil-template.md) - base structure for new `SKILL.md` files.

## Capability Model

Arcanum capabilities are organized by how they reason and how much governance they need.

```text
arcanum/
  framework/       method, lifecycle, templates, observability, and quality rules
  registry/        indexes of reusable sigils, spells, and future packs
  formulae/        deterministic operational sigils
  transmutations/  bounded cognitive synthesis sigils
  arcana/          autonomous orchestration sigils
  spells/          reusable workflow compositions
  research/        proofs, experiments, and validation evidence
```

### Sigils

A **sigil** is one reusable agent capability.

Sigils live in the tier that best matches their epistemic nature:

- [Formulae](formulae/) - deterministic operational sigils.
- [Transmutations](transmutations/) - bounded cognitive synthesis sigils.
- [Arcana](arcana/) - autonomous orchestration sigils.

Each sigil folder should include:

- `README.md` - human-facing explanation, use cases, non-use cases, and tier fit.
- `SKILL.md` - executable agent instruction contract.
- `templates/` - optional reusable artifacts.
- `development/` - in-progress design, validation, planning, and reflection artifacts when needed.

### Spells

[Spells](spells/) compose multiple sigils into a workflow.

A spell defines which capabilities run, in what order, what state they share, which artifacts move between phases, what gates can stop the workflow, and how the overall run is observed.

Use spells when several sigils are more useful together than alone. Do not copy sigil internals into a spell; reference the owning capabilities and define orchestration around them.

## Lifecycle Work

Development is artifact-local. Each capability owns its own `development/` folder while it is being defined, designed, planned, validated, or revised.

Use:

- [invoke](spells/invoke/) to prepare governed definition, design, plan, and handoff artifacts.
- [sigil-development](arcana/sigil-development/) to create, validate, observe, reflect on, and iterate sigils.
- [spellcraft](arcana/spellcraft/) to design, install, validate, observe, and revise spells.
- [implementation-layering](transmutations/implementation-layering/) to choose the smallest responsible implementation layer and promotion evidence.
- [task-session](arcana/task-session/) to execute a bounded task after planning is ready.

`invoke` may prepare lifecycle handoff context, but it should not absorb the lifecycle authority of sigil-development, spellcraft, or task-session.

## Registry

The [registry](registry/) is the catalog of reusable Arcanum artifacts.

- [Sigil Registry](registry/SIGILS.md) - quick-reference index of available sigils.
- [Spell Registry](registry/SPELLS.md) - quick-reference index of offered spell compositions.
- [Packs](registry/PACKS.md) - future grouping model for curated bundles.

Registry promotion is governed. A candidate capability should not become listed merely because it exists; it needs a clear contract, validation evidence, and lifecycle approval.

## Installing Arcanum Into Another Repository

Use the [Arcanum Bootstrap](spells/arcanum-bootstrap/README.md) spell or the bootstrap script to install Arcanum into a consuming repository:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --sigils all --spells all --runtime github-copilot
```

When working from a local checkout, use the repository bootstrap script directly:

```bash
tools/bootstrap_arcanum.sh --target <repo> --sigils all --spells all --runtime github-copilot
```

Both paths install runtime support under `.arcanum/`, with observability under `.arcanum/observability/` and runtime adapters under `.arcanum/runtimes/`. GitHub Copilot, Claude, and Codex may still require small discovery bridges in their platform-specific folders, but canonical local runtime behavior lives inside `.arcanum/runtimes/`.

Use `--sigils <comma-separated-list>` and `--spells <comma-separated-list>` to choose which runtime commands are generated.

When a runtime is selected, bootstrap installs the general `arcanum-orchestrate` adapter and individual adapters for selected sigils and spells. Prefixed names such as `arcanum-sigil-<id>` and `arcanum-spell-<id>` remain stable compatibility names, while bare aliases such as `invoke` and `interrogation` are preferred when no collision exists.

For Codex-style local invocation, use the repository command surface:

```bash
tools/arcanum /invoke define a new sigil
tools/arcanum --exec invoke define a new sigil
tools/arcanum --list
```

The command surface resolves `.codex/commands/<alias>.md` into the canonical adapter under `.arcanum/runtimes/codex/commands/`. With `--exec`, it runs the Codex CLI and appends Observed Invocation Loop telemetry under `.arcanum/observability/`.

## Research And Proofs

[Research](research/) contains proof runs, framework experiments, and validation evidence.

- [Ontology Vault Branching Proof](research/proofs/ontology-vault-branching/) demonstrates business ontology, system ontology, bridge edges, traceability, and drift reporting with a neutral sample vault.

## Contribution And Governance

To add or revise a reusable sigil:

1. Follow the [Sigil Development Workflow](framework/SIGIL-DEVELOPMENT-WORKFLOW.md).
2. Draft from the [Sigil Template](framework/templates/sigil-template.md).
3. Assign the sigil to `formulae/`, `transmutations/`, or `arcana/` based on epistemic nature.
4. Keep in-progress development artifacts under `<tier>/<canonical-id>/development/`.
5. Include a [Quality Bar](framework/QUALITY-BAR.md), [Anti-Patterns](framework/ANTI-PATTERNS.md), and validation evidence.
6. Register promoted sigils in [registry/SIGILS.md](registry/SIGILS.md).

To add or revise a reusable spell:

1. Create or update the spell development pack under `spells/<canonical-id>/development/`.
2. Use `invoke` when the work needs a governed spec, glossary, architecture bundle, or work-pack.
3. Use [spellcraft](arcana/spellcraft/) for spell design, validation, observability, and reflection.
4. Promote the canonical spell file to [spells](spells/) only after validation passes.
5. Register promoted spells in [registry/SPELLS.md](registry/SPELLS.md).

## License

Copyright © 2026 Cyber Alchemy AI.
