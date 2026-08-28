# Research Initial Definitions — Current Arcanum

## Context

Arcanum is a repository of capabilities, workflow compositions, runtime
surfaces, state-bearing artifacts, and governance mechanisms intended to make
agent work bounded, inspectable, and evidence-backed. The repository currently
contains canonical owner contracts, derived operational surfaces, and many
Markdown, JSON, YAML, JSONL, and other artifacts whose relationships and
evidential force are not necessarily uniform.

The existing analysis under `docs/analysis/arcanum-migration/` needs a reliable
account of the Arcanum that exists now, including the problems people and
runtime paths encounter when trying to operate it. That account is needed
before any separate discussion of future architecture, additions, removals,
migration, or target requirements can be responsibly opened. The present
quantity and variety of artifacts also make it difficult to tell which
complexity is required by current contracts, which complexity creates an
operational burden, and which complexity is merely unexplained.

## Purpose

This document establishes the informational baseline for research that will
inform a revision of the current-system analysis and, later, a separately
governed migration decision. It fixes the present-system boundary, separates
confirmed constraints from existing evidence and unknowns, and identifies the
questions whose answers must remain no stronger than their proof.
The immediate aim is to understand what exists beyond what is already recorded
in `docs/analysis/arcanum-migration/analysis.md` and to map the current system's
principal problems.

## Research Questions (Can be refined)

### Program question

**RQ-00.** What exists in Arcanum today, how do its material parts and artifacts relate, what does the available evidence establish about their present behavior and principal problems, and what remains unresolved?

### System extent and responsibilities

1. **RQ-01.** Which current components, capabilities, runtimes, state stores, artifacts, projections, and governance mechanisms are materially necessary to explain how Arcanum works today?

2. **RQ-02.** What responsibility, ownership, and authority does each materially relevant part declare or demonstrably exercise?

3. **RQ-03.** To what extent does the existing analysis discover the relevant repository universe rather than only reconcile the entries already declared in its current-system map?

### Artifact surface and complexity

4. **RQ-04.** Which Markdown, JSON, YAML, JSONL, database, log, receipt, fixture, generated, temporary, or other artifacts does each materially relevant part produce, consume, mutate, project, validate, or leave as residue?

5. **RQ-05.** What lifecycle, authority, persistence, source-of-truth status, and downstream consumers does each material artifact have?

6. **RQ-06.** Which artifacts or representations overlap, duplicate, derive from, reconcile with, or drift from one another?

7. **RQ-07.** Which sources of present-system complexity can be described from evidence as necessary contract or governance cost, generated or compatibility cost, accidental duplication or drift, or unresolved complexity?

### Relations and behavior

8. **RQ-08.** Which material relations connect the identified parts, and what inputs, outputs, artifacts, receipts, state transitions, or authority boundaries cross each relation?

9. **RQ-09.** What present behavior occurs when the principal capabilities and runtime surfaces are used together in their material flows?

10. **RQ-10.** Who or what initiates, coordinates, gates, records, or completes each material flow?

11. **RQ-11.** What present relations connect Craft, Task Session, Decision Gate, Invoke or Refresh, Dispatch Spec, Orchestrate, Continuation Router, Goal, readiness, registries or projections, observability, and Experiment Harness, and which other parts are necessary to avoid an incomplete account?

### Evidence and epistemic status

12. **RQ-12.** What evidence supports each material structural or behavioral claim, and what exact scope does that evidence warrant?

13. **RQ-13.** Which claims are supported only as documented, implemented, tested or fixture-backed, observed in execution, partial, not found, contradictory, or unknown?

14. **RQ-14.** Which source is authoritative for a material claim when owner contracts, registries, schemas, generated projections, implementation, tests, fixtures, and runtime evidence disagree?

15. **RQ-15.** Which bounded witnesses have been generalized beyond their demonstrated scope in the existing analysis, if any?

### Current problems and operational impact

16. **RQ-16.** Which current conditions are supported by evidence as operational failures, recurring friction, blocked paths, ambiguous operation, or inability to use a capability reliably?

17. **RQ-17.** Which current inconsistencies, duplicated representations, drift, or complexity have a demonstrated operational or comprehension consequence, and which have no established impact?

18. **RQ-18.** What affected scope, recurrence, severity, and consequence can the available evidence support for each current problem?

19. **RQ-19.** Which supported problems are local to one owner and which arise from interactions, handoffs, or authority boundaries between parts?

20. **RQ-20.** Which manual coordination, workarounds, compatibility paths, or mitigations are presently required, and what is known about their effectiveness and cost?

### Gaps and boundaries

21. **RQ-21.** Which apparent gaps are supported as incomplete implementation, broken behavior, unverified behavior, representational drift, deliberate ownership or authority boundary, or unresolved status?

22. **RQ-22.** Which contradictions and unknowns materially limit a trustworthy explanation of the current system?

23. **RQ-23.** What is the smallest evidenced change to the analysis protocol, map, schema, or validator needed for the analysis to state its own coverage boundary accurately?

## Confirmed Product Constraints

- The subject is only the Arcanum that exists in the repository today.
- Future architecture, additions, removals, migration mechanics, and target
  requirements are outside this research boundary.
- Every claim must remain at or below the strength and scope of its proof.
- A contract does not prove implementation, existing code does not prove
  successful execution, and a fixture does not prove end-to-end integration.
- A bounded witness must not be generalized to the whole system without
  evidence for that wider scope.
- An absent or incomplete relation must not be called a defect without
  distinguishing incomplete implementation, broken behavior, unverified
  behavior, representational drift, deliberate ownership or authority boundary,
  and unresolved status where the evidence permits.
- Artifact count or variety alone must not be treated as proof of unnecessary
  complexity; complexity claims require evidence about purpose, ownership,
  lifecycle, duplication, drift, or operational burden.
- A condition must not be labelled a current problem more strongly than the
  evidence supports. Demonstrated failure or burden, plausible risk, inert
  inconsistency, deliberate cost, and unresolved impact must remain distinct.
- The present analysis must establish the affected scope and consequence of a
  problem before treating it as system-wide or migration-relevant.
- Mapping current problems does not authorize a proposed fix, removal,
  replacement, or migration priority in this research stage.
- The current-system analysis must make the principal parts, their artifacts,
  their relations, principal supported problems, the exact evidence for
  behavior and impact, and unresolved matters distinguishable.
- The existing current-system map and validator are themselves within scope for
  evaluating the analysis's coverage claim.

## Current Evidence Baseline

- [`analysis.md`](../../analysis.md) contains the current narrative analysis,
  including an orientation inventory, a mapping-pass contract, a discovery and
  coverage section, and an evidence boundary.
- [`README.md`](../../README.md) describes the migration-analysis package,
  current position, mapping views, runtime relationship, and current status.
- [`current-system-map.schema.json`](../../contracts/current-system-map.schema.json)
  defines the present machine-readable map contract, while
  [`current-system-map.example.json`](../../contracts/current-system-map.example.json)
  is its checked example.
- [`validate_mapping.py`](../../scripts/validate_mapping.py) is the current
  deterministic validator for the map and related analysis claims.
- The earlier [`findings.md`](../arcanum-composition/findings.md) and
  [`research.md`](../arcanum-composition/research.md) preserve results from an
  investigation of Arcanum composition.
- [`review.md`](../../review/migration-map/review.md) preserves an earlier review
  of the migration map and Craft write-back claims.
- Repository registries, capability contracts, schemas, runtime code, tests,
  fixtures, invocation artifacts, ledgers, and observability records are
  potential evidence surfaces, but their completeness, authority, artifact
  lifecycles, and behavioral force have not been established by this baseline.

## Known Gaps

- The materially relevant repository universe has not been independently
  established, so the completeness of the current inventory remains unknown.
- It is unresolved whether the current map validator establishes discovery
  coverage or only internal reconciliation of declared map entries.
- There is no reconciled inventory of the artifacts each material component
  produces, consumes, mutates, projects, validates, or leaves behind.
- The source-of-truth status, persistence, lifecycle, authority, and downstream
  consumers of many artifacts are not explicit in the current analysis.
- It is not established which apparently similar artifacts are intentional
  projections or compatibility surfaces and which are duplicated, drifting, or
  operationally unexplained.
- The present-system complexity attributable to necessary governance,
  generation, compatibility, duplication, drift, or unknown causes has not
  been distinguished.
- Current operational failures, recurring friction, blocked paths, ambiguous
  operation, and unreliable capability use have not been systematically
  reconciled into one evidence-bounded problem account.
- The affected scope, recurrence, severity, and consequence of suspected
  current problems are not consistently established.
- It is not known which inconsistencies or complexity sources have demonstrated
  operational consequences and which are presently inert or unverified.
- Required manual coordination, workarounds, compatibility paths, and existing
  mitigations have not been reconciled with evidence of their cost or
  effectiveness.
- It is unresolved which current problems belong to one capability owner and
  which emerge only through cross-capability relations or authority boundaries.
- The exact authority hierarchy among canonical contracts, registries, schemas,
  generated projections, implementation, tests, fixtures, and runtime evidence
  is not fully reconciled for the claims in scope.
- The principal cross-capability flows and their real initiators, gates,
  artifacts, state transitions, and completion conditions are not yet covered
  uniformly by evidence.
- It is not yet established which documented relations are implemented, which
  implemented paths have fixture or test support, which have been observed in
  execution, and which remain partial, absent, contradictory, or unknown.
- It is unresolved where the existing analysis generalizes bounded witnesses
  beyond their demonstrated scope.
- Apparent missing integrations have not been consistently distinguished from
  deliberate ownership or authority boundaries.
- The smallest warranted adjustment to the analysis protocol, map, schema, or
  validator cannot be determined from the current baseline alone.
