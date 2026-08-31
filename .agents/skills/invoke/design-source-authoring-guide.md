# Invoke Design Source v2 Authoring Guide

Start with the unified [Design authoring guide](design-authoring-guide.md) for
the complete path from admitted Define evidence through Design admission. This
guide expands only W2 source and candidate authoring.

## Purpose

`DESIGN-SOURCE.json` is the sole authored machine authority for a W2 Design
candidate. It does not discover repository inputs, select concerns, validate
itself, execute witnesses, or create a final Design stage PASS. W1 owns the
approved input denominator; W2 states how every item in that denominator is
applied to one coherent typed model.

The installed public profile is
`invoke.generic-design-baseline.v1`. Do not substitute a private architecture
profile, an historical Markdown template, or prose inferred from code.

## Required Upstream Boundary

Author only from one exact normal W1 PASS directory containing:

- `DESIGN-INPUT-CLOSURE-RECEIPT.json`;
- `DESIGN-SCOPE-MANIFEST.json`;
- `DESIGN-DENOMINATOR-RECEIPT.json`;
- `DESIGN-SELECTION-RESULT.json`;
- `DESIGN-INPUT-PRODUCTION-RECEIPT.json`.

Bind each file by repository-relative path, SHA-256, and byte size. Bind the
canonical closure at its original repository path. W2 rejects discovery
activation, copied payloads outside the W1 receipt directory, stale digests,
wrong producer identity, a different target, and a non-fixed-point selection.

## Authoring Order

1. Bind the exact installed profile and W1 family.
2. Copy the W1 application denominator as typed `(subject_kind, subject_id)`
   pairs. Add each pair exactly once.
3. Declare each architectural fact once in `facts`.
4. Make provenance reciprocal: every application fact ID must name a fact whose
   `requirement_refs` contains the same typed pair, and vice versa.
5. Project fact IDs into the six views allowed by the installed profile.
6. Bind selection concerns, selected outputs, companion facts, glossary terms,
   and planned witnesses without changing W1 meanings.
7. Record gaps, layering, template selection, Dispatch techniques, Distill
   contract, transport policy, the W2 next route, and `authority_effect: none`.
8. Leave fixed fields, producer identities, and `source_digest` out of the
   authoring request. The CLI validates the authored decisions, derives exact
   evidence hashes, fills fixed fields, and computes the digest.

## Application Denominator

The exact denominator includes:

- every W1 catalog input, including excluded and conditional inputs;
- every conditional resolution;
- constraints and invariants;
- prior decisions and resolved conflicts;
- every signal in all thirteen `scope_signals` arrays;
- every selection concern and selected output;
- every planned witness requirement;
- the Design kind and, for evolution, every declared delta.

An applicable item must bind authored facts. An excluded or conditionally
excluded catalog item uses `not-applicable-with-evidence`, has no fact IDs, and
includes its exact W1 exclusion evidence ref. N/A is not permission to discard
an inconvenient input. A `block` application makes the candidate ineligible.

## Typed Facts and Edges

Use only fact kinds in the installed profile. The profile currently requires at
least one `system`, one `component`, and one `contract`; other kinds are
evidence-driven. W1 signals map field-for-field to their profile fact kinds.
The producer may reorder set-valued arrays deterministically but may not omit,
rename, or reinterpret a signal field.

Every internal edge must resolve to a registered fact. Component parents must
be components and component contracts must be contracts. Workflow operators
must be actors or components; workflow successors must be workflow steps; state
successors must be states. Relationship endpoints, state subjects, decision
successors, and dependency endpoints deliberately accept any registered fact
kind and are therefore checked for existence, not narrowed by inference.

## Six Views

The six required IDs, in installed profile order, are:

1. `view:context`;
2. `view:high-level-structure`;
3. `view:low-level-components`;
4. `view:workflow-process`;
5. `view:decision-flow`;
6. `view:dependency-interface`.

Views contain fact IDs only. Each ID must resolve and its kind must be legal for
that view. Evidence-backed N/A is allowed only when no authored fact of an
allowed kind exists; it is not a shortcut around missing required facts.

## Selection, Glossary, and Witnesses

Preserve the complete selection concern trace. N/A concerns have no fact IDs;
required concerns cannot be discarded. `selected_outputs` equals the W1 set.
`architecture` covers the complete fact registry; every companion output covers
exactly the facts declared in its companion record.

Glossary mappings bind exact Define/W1 terms to existing fact IDs. Unmapped
terms block. Planned witnesses preserve their W1 identity, claim, concern, and
`planned-contract` state. Their application covers exactly their target facts.
They remain unexecuted Plan contracts and never count as Plan PASS evidence.

## Greenfield and Evolution

Greenfield binds the exact W1 no-prior-Design determination. Evolution binds
one current Design v3 stage receipt and its admission v2. Historical v1/v2
stages, admission v1, prose, and synthetic receipts cannot activate evolution.

## Compile

The [historical Design source example](examples/design-source-v1/README.md)
remains validate-only guidance. Use the current stage description and request
schema for new authoring.

```text
tools/arcanum invoke design author source \
  --request DESIGN-SOURCE-AUTHORING-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-SOURCE.json

tools/arcanum invoke design produce candidate \
  --source DESIGN-SOURCE.json \
  --repo-root ROOT \
  --output ABSENT_DIRECTORY
```

Every output is an explicit absent target confined to the repository. PASS
atomically publishes exactly
`DESIGN.json`, `DESIGN-COHERENCE-RECEIPT.json`, and
`DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json`. A governed BLOCK leaves the success
directory absent and returns typed diagnostics with exit `1`. Exit `2` means
the command could not evaluate the request.

## Evidence Ceiling

W2 PASS proves exact normal-W1 binding, total authored input application,
lossless signal projection, installed-profile six-view coherence, fixed
selection preservation, independent policy validation, deterministic candidate
projection, and atomic three-file output closure. It does not prove final
Design stage PASS, human-view production, real predecessor evolution, Plan
evidence, capability admission, acceptance, execution, publication, or
deployment.
