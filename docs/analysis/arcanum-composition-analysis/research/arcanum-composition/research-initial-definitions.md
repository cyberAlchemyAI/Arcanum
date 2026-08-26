# Research Initial Definitions — Arcanum Composition

## Context

Arcanum provides capabilities and workflow compositions for making agent work
bounded, inspectable, evidence-backed, and connected to the objectives and
artifacts that give it meaning. Its repository contains distinct owners for
project state, lifecycle authoring, bounded execution, consequential decisions,
continuation, and autonomous work progression.

The current public explanation needs a faithful account of how those parts and
their artifacts relate. The existing contracts describe several handoffs and
ownership boundaries, but it is not yet established which relations are direct,
which depend on a coordinator, which are implemented or observed, and which are
only intended. Without that distinction, an explanation may mischaracterize the
role of state as a phase, imply automatic integration, or present a proposed
improvement as current behavior.

## Purpose

This document establishes the informational baseline for research that will
inform the Arcanum composition analysis and later decisions about how that
composition should be explained or improved. It separates confirmed constraints,
existing repository evidence, and unresolved knowledge before the research is
designed or conducted.

## Research Question (Can be refined)

### Program boundary

**RQ-0.** What composition, if any, is presently supported by Arcanum's
capabilities and artifacts for turning intent into bounded, governed work and
maintaining coherence across preparation, decisions, execution, and
continuation?

**Why this question is necessary:** it defines the overall knowledge boundary
without assuming that the repository already implements one unified or linear
composition.

### Scope and ownership

**RQ-1.** Which capabilities and artifacts are materially part of that
composition, and what responsibility, state, or result does each one own?

**Why this question is necessary:** claims about relationships cannot be precise
until capabilities are distinguished from their artifacts and each ownership
boundary is established.

### Meaning of communication and composition

**RQ-2.** Which operational meanings of capability communication and
composition are supported by current Arcanum authority, and what boundary does
each meaning impose on claims made in the analysis?

**Why this question is necessary:** communication and composition are
load-bearing terms in the analysis, but the current baseline does not establish
a shared meaning precise enough to constrain what can honestly be claimed.

### Cross-capability relations

**RQ-3.** Which material relations currently connect the in-scope capabilities
and artifacts, and what information, artifact, authority, or state crosses each
boundary?

**Why this question is necessary:** naming adjacent capabilities does not
establish a relation, and different transferred objects can support materially
different kinds of composition.

### Relation activation and coordination

**RQ-4.** For each material relation, who or what detects the need, invokes the
owner, supplies the required context, and applies or records the result?

**Why this question is necessary:** an interface or documented handoff does not
establish whether its activation and completion are automatic, caller-mediated,
or explicitly user-gated.

### Preparation for bounded execution

**RQ-5.** What makes a unit of work ready for Task Session, and what role, if
any, do definitions, specifications, designs, plans, and work packs authored by
Invoke play in establishing that readiness?

**Why this question is necessary:** the current explanation can describe bounded
execution without explaining the artifact-mediated preparation that may precede
it, while the repository may not require that same preparation for every task.

### Craft and consequential decisions

**RQ-6.** What operational binding, if any, connects Craft-backed ledger state
to Decision Gate inputs and outcomes?

**Why this question is necessary:** the current baseline describes caller
routing and ledger write-back responsibilities, but it does not establish that
Decision Gate directly consumes or mutates the Craft ledger.

### State transition and write-back

**RQ-7.** How, if at all, do state changes produced through Task Session,
Decision Gate, Invoke Refresh, or Goal become proposed, approved, or recorded in
Craft-backed state?

**Why this question is necessary:** native capability results and durable
project-state mutation have different owners, so producing an outcome does not
by itself establish a ledger transition.

### Evidential status

**RQ-8.** For each claimed relation, what status can the repository evidence
support: documented contract, implemented binding, or observed execution?

**Why this question is necessary:** an honest account must not present intended
or generated behavior as implemented and exercised integration.

### Source authority

**RQ-9.** Which source governs each relationship when a README, skill contract,
registry, schema, generated surface, and runtime implementation disagree?

**Why this question is necessary:** evidential classification cannot resolve a
source conflict by silently choosing the surface that supports the preferred
account.

### Improvement boundary

**RQ-10.** Which incomplete or ambiguous relationships materially limit
Arcanum's documented purposes, and which separations are deliberate ownership
boundaries under current authority?

**Why this question is necessary:** the analysis must identify improvement
opportunities without treating every separation of responsibility as a defect
or deciding in advance whether the architecture should change.

## Confirmed Product Constraints

- The analysis will live at
  `docs/analysis/arcanum-composition-analysis/analysis.md`.
- The research supporting the analysis will remain inside
  `docs/analysis/arcanum-composition-analysis/research/`.
- The analysis itself will remain one document; at most one separate review
  document may be added later.
- The analysis must serve both as an explanation of the current state and as an
  evidence-backed account of improvement opportunities.
- Current behavior, inferred relationships, open gaps, and proposed improvements
  must remain distinguishable even when presented in the same analysis document.
- The existing introduction is not to be changed as part of this research or
  scaffold task.
- `findings.md` must implement the DomainSpec research-question coverage contract
  imported from `../domainspec/.claude/skills/research/SKILL.md`: the coverage
  section precedes the candidate matrix; every registered RQ receives an explicit
  row; statuses are limited to `answered`, `unresolved`, `deferred`, or `retired`;
  and each answer records addressable evidence, contrary evidence or material
  uncertainty, and its boundary. Evidence support must be labelled as
  `documentary assertion`, `executable observation`, `independent recomputation`,
  or `formal proof` without treating those classes as interchangeable.

## Current Evidence Baseline

- [`README.md`](../../../../../README.md) describes Arcanum's method, capability
  model, lifecycle work, and the high-level roles of Invoke and Task Session.
- [`framework/CYBERALCHEMY-METHOD.md`](../../../../../framework/CYBERALCHEMY-METHOD.md)
  establishes objective, output artifact, discovery, tension, and route as
  visible anchors of governed work, and separately requires trace to be
  preserved.
- [`arcana/craft/SKILL.md`](../../../../../arcana/craft/SKILL.md) defines Craft as
  the owner of a project-local, file-backed ledger for contexts, blockers,
  decisions, gaps, evidence, next moves, and related state. It also states that
  native capabilities retain ownership of their own results.
- [`spells/invoke/README.md`](../../../../../spells/invoke/README.md) assigns
  intent-to-artifact authoring for definition, design, planning, work-pack
  creation, and handoff context to Invoke, and separately defines a refresh mode
  for evidence-backed artifact deltas and routing.
- [`arcana/task-session/SKILL.md`](../../../../../arcana/task-session/SKILL.md)
  assigns execution of one bounded task or smallest working unit to Task Session
  and declares context, blocker, decision, validation, and closeout obligations.
- [`arcana/decision-gate/SKILL.md`](../../../../../arcana/decision-gate/SKILL.md)
  defines a gate for blocker-level decisions with multiple admissible options
  before consequential work continues.
- Task Session declares routes to Decision Gate for consequential blockers and
  to Invoke Refresh for bounded closeout synchronization, while Craft declares
  that decisions resolved by another capability should be recorded back into
  the owning ledger context.
- [`spells/goal/README.md`](../../../../../spells/goal/README.md) defines one
  explicit composition that reads a Craft-backed frontier, routes bounded work,
  uses Decision Gate for approval or blocker decisions, and applies ledger
  changes only through an approval-gated path.
- These artifacts establish documented responsibilities and intended handoffs.
  They do not by themselves prove that every relation has a universal runtime
  integration or has been exercised successfully.

## Known Gaps

- The exact boundary of the composition to be analyzed is unresolved, including
  which adjacent capabilities are necessary to explain the core relations.
- It is not yet established which documented relations are implemented, which
  have observed execution evidence, and which remain contractual intent.
- No single shared definition of capability communication or composition has yet
  been identified in the available baseline.
- The distinctions needed to describe cross-capability relationships without
  overstating integration remain unresolved.
- The authoritative source for each relationship is not yet reconciled when a
  README, skill contract, registry, schema, generated surface, and runtime
  implementation differ.
- It is not yet clear how specifications, design artifacts, planning artifacts,
  and Task Session readiness relate across ownership boundaries.
- It is unclear whether the general Craft-to-Decision-Gate path has a universal
  operational binding or only caller-specific coordination and write-back rules.
- It is unresolved how outcomes from Task Session, Decision Gate, Invoke
  Refresh, or Goal become proposed, approved, or recorded as Craft-backed state
  changes, when they do.
- It is unresolved who detects the need for each capability, who invokes it, how
  its context is assembled, and which routes are automatic, caller-mediated, or
  explicitly user-requested.
- The current baseline does not establish which apparent relationship weaknesses
  are improvement opportunities and which are deliberate ownership boundaries.
