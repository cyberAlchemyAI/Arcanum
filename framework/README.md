# Arcanum Framework

The Arcanum framework defines how sigils are authored, validated, composed, observed, and maintained.

Use this folder when you are changing the rules of the system rather than adding one reusable capability to the registry.

## Framework Documents

- [CyberAlchemy Method](CYBERALCHEMY-METHOD.md) - governed synthesis method for creating and working with agent capabilities.
- [Quality Bar](QUALITY-BAR.md) - observable completion criteria for sigil execution.
- [Anti-Patterns](ANTI-PATTERNS.md) - failure modes and misuse boundaries.
- [Validation Experiment Protocol](VALIDATION-EXPERIMENT-PROTOCOL.md) - repeatable release-gate experiments for spells, sigils, and canonical templates.
- [Experiment Harness Standard](EXPERIMENT-HARNESS-STANDARD.md) - artifact-local test harness layout for fixtures, prompts, outputs, runs, and promotion evidence.
- [Development To Canonical Promotion](DEVELOPMENT-TO-CANONICAL-PROMOTION.md) - process for turning development evidence into owner-gated canonical artifact patches.
- [Sigil Development Workflow](SIGIL-DEVELOPMENT-WORKFLOW.md) - lifecycle from candidate capture through maintenance.
- [Sigil Template](templates/sigil-template.md) - base `SKILL.md` structure.
- [Validation Experiment Template](templates/validation-experiment.md) - starter validation experiment for any spell or sigil.
- [Validation Report Template](templates/validation-report.md) - starter validation evidence report.
- [Observability](observability/) - telemetry, hook, runtime package, observed-run, hook-ledger, and reflection conventions.

## Disciplines

[Disciplines](../disciplines/) are framework-adjacent source artifacts for recurring Arcanum practices that cross capability boundaries.

Use them when a practice is too broad to live only inside one sigil, spell, or development package, but should not become a registry entry. Discipline entries preserve evidence, steward boundaries, status, and next hardening moves for practices such as Craft, planning, schema governance, validation, observability, evidence, decisions, and runtime boundaries.

## Tier Ontology

The framework classifies sigils by epistemic nature:

- [Formulae](../formulae/) - deterministic operational sigils.
- [Transmutations](../transmutations/) - bounded cognitive synthesis sigils.
- [Arcana](../arcana/) - autonomous orchestration sigils.

## Local Runtime

Arcanum keeps the consuming-repository runtime path as `.arcanum/` for compatibility.

Use `.arcanum/` for repository-local installed spells, observability ledgers, inventory entries, aliases, and run reports. The Arcanum repository defines the framework; the consuming repository owns its local runtime data.

## Registry Boundary

Framework changes alter how sigils are created or judged. Registry changes add, remove, rename, or revise reusable sigils and spells.

Use the [Arcanum Registry](../registry/) to browse available artifacts.
