# Arcanum

**Arcanum** is a framework for creating reusable agent capabilities through governed synthesis.

It provides a method, lifecycle, quality bar, observability model, and capability structure for turning vague intent into artifacts that humans and agents can understand, reuse, validate, and improve.

The center of Arcanum is the [CyberAlchemy Method](framework/CYBERALCHEMY-METHOD.md): a way of working that keeps objective, output artifact, discovery, tension, trace, and lifecycle ownership visible throughout the work.

## Start Here

- Start with the [CyberAlchemy Method](framework/CYBERALCHEMY-METHOD.md) to understand the working philosophy.
- Start with the [Framework](framework/) when authoring, reviewing, validating, or maintaining capabilities.
- Start with [Disciplines](disciplines/) when a recurring Arcanum practice appears across capabilities and needs framework-level shape without becoming a sigil or spell.
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
- observability emission through `observe-harness.sh`.

The harness pairs with observability: validation proves whether a capability satisfies its contract in controlled examples, while observability records how it behaves in actual use.

## The Framework

The [framework](framework/) is the operating model for Arcanum capabilities.

The Method, Observability Layer, and Experiment Harness are highlighted above. The supporting framework references are:

- [Quality Bar](framework/QUALITY-BAR.md) - observable criteria for successful execution.
- [Anti-Patterns](framework/ANTI-PATTERNS.md) - known misuse cases and failure modes to avoid.
- [Sigil Development Workflow](framework/SIGIL-DEVELOPMENT-WORKFLOW.md) - lifecycle from candidate capture through maintenance.
- [Validation Experiment Protocol](framework/VALIDATION-EXPERIMENT-PROTOCOL.md) - release-gate experiments for spells, sigils, and templates.
- [Sigil Template](framework/templates/sigil-template.md) - base structure for new `SKILL.md` files.

## Canonical Definitions

Arcanum-wide terminology authority lives in [Definitions](definitions/). Use
[Canonical Definitions](definitions/DEFINITIONS.md) for normative meanings and
[Definitions Index](definitions/DEFINITIONS-INDEX.md) for lookup aliases.

Local glossaries may explain bounded project or capability vocabulary, but they
should reference project-level definition IDs instead of redefining global terms.

## Capability Model

Arcanum capabilities are organized by how they reason and how much governance they need.

```text
arcanum/
  framework/       method, lifecycle, templates, observability, and quality rules
  disciplines/     cross-capability operating practices and evidence-backed discipline catalog
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

For Codex discovery, repository skills are exposed through `.agents/skills/`. In this repository that directory uses symlinked skill folders so the tiered Arcanum folders remain canonical while Codex can discover the skills from the official repo-scoped location.

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

## Disciplines

[Disciplines](disciplines/) formalize cross-capability operating practices that appear throughout Arcanum, such as Craft, planning, schema, validation, observability, evidence, decision gating, and runtime boundaries.

Use disciplines when a practice is broader than one sigil or spell but should not become a bloated framework document. Discipline entries cite evidence, name stewards, define boundaries, and identify the next hardening move. They do not register capabilities or claim promotion authority for sigils, spells, ontology, definitions, or inventory.

## Registry

The [registry](registry/) is the catalog of reusable Arcanum artifacts.

- [Sigil Registry](registry/SIGILS.md) - quick-reference index of available sigils.
- [Spell Registry](registry/SPELLS.md) - quick-reference index of offered spell compositions.
- [Packs](registry/PACKS.md) - future grouping model for curated bundles.

Registry promotion is governed. A candidate capability should not become listed merely because it exists; it needs a clear contract, validation evidence, and lifecycle approval.

## Using Arcanum With Codex

Codex reads repository skills from `.agents/skills/` in the current working directory or parent directories up to the repository root. Arcanum exposes its reusable sigils there as symlinks to canonical capability folders:

```text
.agents/skills/experiment-harness -> ../../arcana/experiment-harness
.agents/skills/context-builder -> ../../transmutations/context-builder
.agents/skills/observability-setup -> ../../formulae/observability-setup
```

Invoke skills explicitly with `$skill-name`, or let Codex choose them implicitly when the request matches the `description` in `SKILL.md`.

The older `.codex/commands/` files are compatibility adapters for slash-command-style experiments. They are not the canonical Codex skill surface. Prefer repository skills for normal Codex use.

## Installing Arcanum Into Another Repository

For local Codex use in another repository, install repo-scoped Codex skills with the bootstrap profile:

```bash
tools/bootstrap_arcanum.sh --target ../my-repo --profile repo-codex --sigils all --spells none
```

For a fresh Codex, Claude Code, and GitHub project, install repo-scoped Codex skills, Claude Code skills, repo-local deterministic tool/runtime config, GitHub Copilot instructions, and observability skeleton together:

```bash
tools/bootstrap_arcanum.sh --target ../my-repo --profiles repo-codex,claude,repo-local,github-copilot,observability --sigils all --spells all
```

From GitHub, use the installer wrapper:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles repo-codex,claude,repo-local,github-copilot,observability --sigils all --spells all
```

For Claude Code only:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles claude,repo-local --sigils all --spells all
```

See [FRIEND-INSTALL-TUTORIAL.md](FRIEND-INSTALL-TUTORIAL.md) for a shareable walkthrough.

Generated Codex skill installs use short alias names by default so the skill picker does not show both `refine` and `arcanum-refine`. Use `--prefixed-skill-packages` only when you intentionally need `arcanum-*` compatibility packages.

Use `--profile personal-codex --codex-home "$HOME/.codex"` only when you want to install generated skills into a personal Codex home. Use `--legacy-codex-commands` only when a repository still needs deprecated `.codex/commands/` compatibility, and `--clean-legacy-codex-commands` to remove generated legacy command files while preserving unknown local command files.

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

Arcanum is source-available under the [PolyForm Noncommercial License 1.0.0](LICENSE).

You may use, study, modify, and share Arcanum for noncommercial purposes. You may
not sell Arcanum or use it for commercial purposes without separate written
permission from Cyber Alchemy AI.

Copyright (c) 2026 Cyber Alchemy AI.
