# Research Initial Definitions — Craft Claim–Evidence Strengthening

## Context

Arcanum's Craft capability provides a project-local recursive ledger for keeping development state explicit and navigable. Its canonical package represents contexts, artifacts, descriptions, local definitions, gaps, typed operational items, decisions, relations, next moves, validation, and recomposition, with `.craft/ledger.yml` as the source of truth and generated or human-readable views remaining derived.

A prior governed audit in `domainspec-lean-formalization/research-domainspec/claim-evidence-proof-model/findings.md` established bounded semantic distinctions among claim content, raw grounds, force-bearing relations or inference applications, attributed evaluations, governance, provenance, lifecycle, and operational authorization. The local problem is not to assume that those distinctions belong in Craft, but to determine whether any of the audit's supported results materially strengthen Craft's existing ledger model and justify a later implementation decision.

## Purpose

This document establishes the informational baseline for governed research that will inform a later decision about whether and how the supported results of the claim–evidence–proof audit should affect Craft. It does not select a target model, prescribe a schema, authorize implementation, or change Craft's canonical contracts.

## Research Question (Can be refined)

Which results supported by `domainspec-lean-formalization/research-domainspec/claim-evidence-proof-model/findings.md` are applicable to the current Craft capability and, among those, which provide enough material gain to justify an implementation?

## Confirmed Product Constraints

- The research must begin from the bounded findings in `domainspec-lean-formalization/research-domainspec/claim-evidence-proof-model/findings.md`, not from a stronger reconstruction of the prior conversation or audit.
- Cross-repository references to that source must begin at the repository name `domainspec-lean-formalization`; machine-specific absolute paths must not be used.
- The research is intended to guide a later implementation decision, but it must not assume in advance that Craft needs a new epistemic layer, new row families, or a particular schema.
- The first intended improvement to Craft is conceptual: clarify what information belongs in the ledger and how it is distinguished before pursuing automation or integration changes.
- Craft's current canonical authority remains under `arcana/craft/`. Research artifacts do not mutate or supersede the canonical skill, architecture, templates, examples, or runtime surfaces.
- Claims in the research and any later design must remain no stronger than their cited audit, repository, validation, or implementation evidence.

## Current Evidence Baseline

- `arcana/craft/SKILL.md` defines Craft as a file-backed recursive ledger for contexts, blockers, enablers, decisions, gaps, definitions, next moves, child contexts, validation evidence, and recomposition.
- `arcana/craft/ARCHITECTURE.md` identifies the current canonical row families as contexts, artifacts, descriptions, definitions, gaps, relations, typed items, decisions, and recomposition. It also records route handoffs, receipts, route events, projections, row-update plans, validation reports, and artifact manifests as deferred schema surfaces.
- `arcana/craft/templates/schemas/ledger-core.schema.yml` permits evidence to reference artifact IDs, receipt IDs, paths, selectors, or link objects and defines typed operational and workflow invariants. It does not currently define first-class row families named `ClaimVersion`, `Ground`, or `Evaluation`.
- `domainspec-lean-formalization/research-domainspec/claim-evidence-proof-model/findings.md` supports keeping an immutable identified claim version, raw grounds, force-bearing relations or inference applications, provenance-bearing evaluations, governance disposition, ownership or provenance, and operational authorization distinguishable.
- The same audit rejects treating evidence kind as justificatory force, treating support as generically transitive, collapsing authorization into epistemic standing, or treating a single mutable status as intrinsic truth.
- The audit gives GO only to a semantic boundary and possible future build-from-owned integration. It explicitly gives NO-GO to a v0.1 schema, metamodel mutation, or implementation on the evidence available in that research cycle.

## Known Gaps

- It is not yet established which supported distinctions from the audit correspond to real ambiguities, information loss, unsafe updates, or unmet consumers in current Craft use.
- It is not yet known which audit concepts are already represented adequately by Craft artifacts, evidence references, relations, decisions, statuses, or owner routes.
- It is not yet known whether any needed distinction belongs inside the primary Craft ledger, in a linked artifact or projection, or outside Craft's responsibility boundary.
- No smallest implementation-bearing consumer has yet been established for any proposed addition to Craft.
- The minimum invariants needed to preserve claim identity, evidential force, evaluation history, governance, and authorization without semantic collapse have not been established for Craft.
- Compatibility requirements for existing Craft ledgers, indexes, human views, validators, and project-local workflows have not yet been determined for this subject.
- The boundary between a conceptual improvement to ledger contents and later automation that records or updates those contents remains unresolved.
