# Invoke Design Production Process Definition

## Objective

Define the machine-first process that converts complete, exact Design inputs
into one coherent candidate Design artifact and deterministic human views.
This process closes the `SWU-WIR-007` contract boundary without claiming Plan,
acceptance, execution, publication, or deployment evidence.

## Core Separation

The process has two distinct author-owned machine sources:

1. `DESIGN-INPUT-CLOSURE.json` states what the Design must respect. It closes approved
   Define outputs, current-state evidence, adjacent contracts, constraints,
   invariants, prior decisions, ownership, exclusions, and evolution context.
2. `DESIGN-SOURCE.json` states the proposed architecture. It binds the exact
   input-closure receipt and selection result, applies every input obligation,
   declares typed architecture facts once, and indexes those facts into the six
   required Design views.

The two sources must not be collapsed. Input evidence cannot silently become
an architectural decision, and an authored architecture cannot rewrite its
own input boundary.

## Monotonic Artifact Chain

```text
approved Define bundle
  -> DesignInputBoundaryApproval
  -> DESIGN-INPUT-CLOSURE.json
  -> DesignInputClosureReceipt
  -> DesignScopeManifest
  -> DesignDenominatorReceipt
  -> DesignSelectionResult
  -> DesignInputProductionReceipt
  -> DesignProfile
  -> DESIGN-SOURCE.json
  -> staged DESIGN.json
  -> DesignCoherenceReceipt
  -> DesignCandidateProductionReceipt
  -> DESIGN-BUNDLE-CLOSURE.json + independently passing Distill evidence
  -> deterministic human and transport views
  -> Invoke Design stage receipt v2
  -> independent byte-equal replay admission receipt
  -> capability-status artifact_authored admission
```

Each edge consumes exact refs and digests from its predecessor. A later
artifact cannot repair, reinterpret, or replace an earlier authority-bearing
input. A semantic change supersedes the affected predecessor and restarts from
the earliest changed edge.

## Stage Ownership

| Stage | Owner | Responsibility | Must not claim |
| --- | --- | --- | --- |
| Boundary approval | Target owner | Approve the finite roots, rules, required classes, exact exclusions, visibility, and observation epoch. | Repository-global completeness or architecture choice. |
| Input closure | Design input author | Declare the discovery boundary, complete evidence, authority roles, constraints, and evolution baseline. | Architecture choice or validation PASS. |
| Input-closure validation | Independent Invoke Design input validator | Inspect the declared boundary, classify missing, stale, conflicting, excluded, and prior-Design evidence, and issue a failure-capable closure receipt. | Concern selection or architecture choice. |
| Scope projection | Invoke Design input producer | Derive or prove total equality with `DesignScopeManifest`. | Concern selection. |
| Denominator extraction | Existing independent scope extractor | Inspect exact selectors and enumerate the denominator. | Companion selection or Design completeness. |
| Selection | Existing selection validator | Bind every signal to one concern and obtain the fixed point. | Authored architecture or Plan evidence. |
| W1 atomic closure | Invoke Design input producer | Publish the closure receipt, manifest, denominator, selection, and production receipt in one directory replacement. | Six-view Design, final Design stage PASS, or capability admission. |
| Design authoring | Design author | Propose one typed architecture model, six ID-based view projections, and total input application. | Self-validation, policy selection, or upstream mutation. |
| Staging compilation | Invoke Design candidate producer | Compile a normalized candidate `DESIGN.json` against the installed process, public profile, and policy without publishing the final bundle. | Coherence PASS or final stage PASS. |
| Coherence validation | Independent Invoke Design coherence validator | Check total coverage, cross-view integrity, preserved contracts, and exact supersession evidence against the staged artifact. | Acceptance, execution, final publication, or Plan evidence. |
| W2 candidate closure | Invoke Design candidate producer | Publish `DESIGN.json`, the independent coherence receipt, and the candidate production receipt in one atomic directory replacement. | Human views, final stage PASS, admission, or Plan entry. |
| Atomic bundle closure (W3) | Invoke Design producer | Validate exact W2 and Distill bindings, derive deterministic views, and publish fourteen payloads plus the v2 stage receipt atomically. | Registry release or runtime readiness. |
| Bundle admission (W3) | Independent Design bundle validator | Validate all fifteen files, replay the compiler from the bound closure, and require byte equality without editing submitted bytes. | Any later capability axis. |
| Artifact admission | Capability resolver | Admit only an exact current v2 stage receipt plus its independent replay receipt. | Any later capability axis. |

## Design Coherence

A Design is coherent only when all of the following are true:

- every mandatory input has exactly one legal application disposition;
- excluded and conditionally excluded inputs are explicit N/A applications with
  their exact W1 evidence and no architecture facts;
- every authored Design element traces to applicable input or selection evidence;
- component, interface, state, workflow, decision, dependency, and owner identities
  are declared once and every view reference resolves to the correct registry;
- every one of the thirteen W1 signal classes is projected without field loss;
  workflow operators resolve specifically to an actor or component while other
  generic graph endpoints resolve to a registered fact;
- preserved contracts and invariants remain unchanged;
- a changed contract or invariant carries an exact owner decision ref;
- every required selected output has authored content and no unselected
  companion is presented as required;
- glossary identities remain consistent with the exact Define bundle;
- an evolution Design binds one prior Design artifact and expresses a total
  delta rather than creating an untracked parallel architecture;
- blocking contradictions and unknowns are empty.

JSON Schema establishes structural closure. The coherence validator owns these
cross-document and cross-view semantic checks.

## Failure Policy

- Missing, stale, escaping, or duplicate input refs block before scope projection.
- Unknown authority, unresolved conflict, or an uncovered mandatory input blocks.
- Manifest/input coverage drift blocks; neither side is silently preferred.
- A blocking or changed-pass-two selection result blocks Design compilation.
- Cross-view identity, ownership, interface, workflow, or invariant conflict blocks.
- Discovery activation may close input evidence but cannot issue a normal
  W2 candidate or `design-stage-pass` receipt.
- W1 producer or late-stage validation failure publishes no success directory;
  a governed failure issues only the separate failure-capable attempt receipt.
- W2 producer, independent coherence, or late output-closure failure publishes
  no success directory; a governed failure issues only its separate candidate
  attempt receipt.
- Evolution accepts exactly one live W3 v2 predecessor bundle whose target,
  producer, receipt digest, `DESIGN.json`, and complete output inventory pass
  independent validation. Historical, synthetic, ambiguous, or mismatched
  predecessors block.
- Historical Design prose and selection evidence remain readable but cannot
  establish a new producer-backed Design PASS.

## Evidence Ceiling

W1 may prove approved-boundary-relative input closure, deterministic manifest
projection, denominator compatibility, fixed-point selection, and exact atomic
input-bundle closure. W2 may additionally prove exact normal-W1 binding, total
authored application, lossless signal projection, installed-profile six-view
coherence, deterministic candidate projection, independent policy validation,
and atomic three-file candidate closure. W3 adds deterministic complete-bundle
production, exact W1/W2/Distill binding, independent replay admission,
capability `artifact_authored`, and real v2 predecessor evidence. It does not
prove Plan evidence, registry release, mutation readiness, owner acceptance,
execution, publication, deployment, or external effect.
