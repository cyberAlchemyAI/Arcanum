# Definitions Governance

Definitions Governance is an Arcana sigil for keeping critical terminology authoritative, interpretable, indexed, and traceable across a repository.

It maintains one canonical definition source, keeps lookup artifacts synchronized, separates normative wording from explanatory intuition, and audits downstream drift where terms are reused.

Definitions Governance is the maintainer process, not the place where a
project's definitions live. When the sigil is installed or copied into another
repository, it must resolve that repository's project-level definition authority
before reading or writing terms.

## Problem It Solves

Projects drift when critical terms are redefined in papers, plans, specs, implementation notes, or presentations. A term may look familiar while its meaning silently changes across artifacts.

Definitions Governance prevents that by treating definitions as a governed authority layer with traceable downstream consumers.

## Use When

- a gate-critical or high-impact term is added or revised,
- formulas, notation, or formal constructs need stable interpretation,
- downstream documents reference canonical terms,
- narrative summaries risk redefining normative semantics,
- definition drift needs to be audited.

## Do Not Use When

- the term is local to one feature glossary,
- the wording is informal and non-critical,
- the task is only to rename a label,
- the repository is not ready to own definition governance.

If there is no canonical definitions source but the repository is ready to own
one, use this sigil to initialize a project-level source instead of writing into
the sigil folder.

## Authority Model

The consuming repository should identify:

- canonical definitions source,
- lookup or index layer,
- narrative consumers,
- protocol or process consumers,
- validation checks,
- drift remediation targets.

Default project-level convention when the repository has no existing authority
source:

```text
definitions/
  DEFINITIONS.md
  DEFINITIONS-INDEX.md
  DEFINITION-DRIFT-AUDIT.md
```

Do not store project definitions in:

- the installed sigil package,
- a copied `.codex/skills` package,
- a `.agents/skills` discovery link,
- `arcana/definitions-governance/`,
- any runtime or generated install surface.

Those locations may contain the Definitions Governance process. They are not the
consuming project's terminology authority unless the repository explicitly says
so.

In this Arcanum repository, the project-level authority source is
[definitions/DEFINITIONS.md](../../definitions/DEFINITIONS.md), with lookup in
[definitions/DEFINITIONS-INDEX.md](../../definitions/DEFINITIONS-INDEX.md).

## Why This Is Arcana

Definitions Governance coordinates authority, interpretation, indexing, drift detection, and remediation routing across many artifacts. It governs semantic consistency over time.
