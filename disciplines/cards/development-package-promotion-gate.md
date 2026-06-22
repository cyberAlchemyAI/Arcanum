# Development Package Promotion Gate

Status: active-pattern
Steward: Artifact Constitution and GitHub Project Issue Loop

## Purpose

Require every development/run package to be classified in the local repository
before it enters a commit or pull request. Raw refinement, invoke, task-session,
runtime, and observability outputs stay local unless repository guidelines
explicitly promote a distilled artifact as source or durable evidence.

## Boundary

This discipline names the review practice for development package promotion. It
does not own a consuming repository's local discipline catalog, Artifact
Constitution, gitignore policy, lifecycle sigils, task-session receipts,
project-board state, or product implementation changes. It also does not forbid
canonical source, tests, templates, docs, or curated durable evidence just
because they were produced during development.

Mutation belongs to the artifact owner:

- framework artifact-class rules route to the Artifact Constitution;
- generated-path enforcement routes to the artifact constitution validator;
- issue-loop delivery behavior routes to `github-project-issue-loop`;
- repository-specific promotion decisions route to the local repository owner.

## Evidence

- [Artifact Constitution](../../framework/ARTIFACT-CONSTITUTION.md) - classifies generated artifacts as ignored by default unless explicitly promoted to durable evidence.
- [Artifact Constitution validator](../../tools/validate-artifact-constitution.sh) - provides the existing enforcement surface for generated and local-runtime artifact visibility.
- [GitHub Project Issue Loop](../../arcana/github-project-issue-loop/SKILL.md) - creates refinement, invoke, task-session, PR, and telemetry evidence during issue delivery, so it needs a commit-surface gate before publishing.
- [Discipline Governance](../../arcana/discipline-governance/SKILL.md) - requires consuming-repository local discipline handling before public Arcanum promotion when evidence is local.
- [Runtime boundary discipline](runtime-boundary.md) - keeps canonical source, generated install surfaces, and local runtime state separate across consuming repositories.

## Validation

- Mode: prose-review
- Check: catalog validator plus PR changed-file review for unpromoted development package paths before commit/push.
- Latest result: pass (catalog validation and five open issue-loop PR cleanup checks on 2026-06-22).

## Quality Bar

A useful development package promotion gate must:

- inspect the intended commit surface before publishing a PR;
- check or create the consuming repository's local discipline surface before promoting a generalized Arcanum rule;
- classify each run-created artifact as source, durable evidence, generated output, or local runtime state;
- keep raw `development/refinement-runs/**`, `development/invoke-runs/**`, `development/task-sessions/**`, runtime folders, and observability logs out of product PRs unless explicitly promoted;
- promote only the smallest distilled artifact that repository guidelines name as canonical or durable evidence;
- keep tests, source changes, docs, schemas, and curated examples when they are the real deliverable;
- summarize non-committed run evidence in PR text or telemetry without bundling the raw package;
- compare the final changed-file set against the dependency map and affected-only hypothesis.

## Promotion Guardrail

This discipline can recommend validator, gitignore, local discipline, or
issue-loop contract changes, but it cannot itself promote development packages,
registry entries, ontology, glossary, sigil, spell, or repository product
artifacts. Promotion beyond `active-pattern` requires a deterministic validator
that covers the known issue-loop package paths, an explicit durable-evidence
allowlist, and evidence that at least one consuming repository handled the rule
locally before framework promotion.
