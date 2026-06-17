# MARS Paper Derivation Rules

Purpose: define an experimental graph-native derivation model for paper-design artifacts in MARS.

Status: pilot-oriented reusable guidance. These rules are not yet a hard gate in the MARS pipeline.

## Why This Exists

MARS can now model papers as typed research graphs.

The next step is to derive a lightweight paper-design contract from that graph so papers can be reviewed before and during evidence integration, rather than only after narrative prose is written.

## Inputs

The derivation model assumes these inputs exist:

- `registry/RESEARCH-GRAPH.md`
- `papers/<paper-file>.md`
- `results/*-EVIDENCE-STATUS.md`
- `sources/REFERENCE-LEDGER.md`
- relevant protocol and result artifacts referenced by the graph

## Derived Outputs

The working output set is:

- `papers/PAPER-SPEC.md`
- `papers/PAPER-STORIES.md`
- `papers/PAPER-TEST-SPEC.md`
- `papers/PAPER-REVIEW.md`

## Derivation Rules

### PDR-01 Section Node Lift

For every `Paper Section` node (`PSEC-*`) in `registry/RESEARCH-GRAPH.md`, create or update one section-registry row in `papers/PAPER-SPEC.md`.

Required fields:

- section node ID
- section title
- synthesis role
- required graph inputs
- current readiness
- current blockers

### PDR-02 Framing And Anchor Lift

Incoming `frames` and `anchors` relations for a paper section become required design inputs in `papers/PAPER-SPEC.md`.

Interpretation:

- `frames` identifies the domain or question context that must be visible in the section.
- `anchors` identifies the methodology or definition authority the section must not drift from.

### PDR-03 Synthesis Obligation Lift

Each `synthesizes` edge from a paper section becomes one paper obligation in `papers/PAPER-TEST-SPEC.md`.

If a section `synthesizes`:

- a `Claim`, the section must make that claim legible.
- an `Experiment`, the section must explain how that experiment contributes.
- an `Analysis Result`, the section may make evidence-backed interpretations.
- an `Evidence Status`, the section may make support-level statements.
- a `Reference`, the section may integrate authority-based framing.

### PDR-04 Citation Obligation Lift

Where a paper section directly `cites` a `Reference`, or where its supporting methodology and protocol artifacts cite references that are essential to the section, record those references as expected authority coverage in `papers/PAPER-TEST-SPEC.md` and `papers/PAPER-REVIEW.md`.

### PDR-05 Evidence Gate Derivation

If a results-facing paper section synthesizes experiment nodes but no matching `Analysis Result` or `Evidence Status` nodes yet exist, mark that section as blocked for evidence-backed publication use in:

- `papers/PAPER-SPEC.md`
- `papers/PAPER-TEST-SPEC.md`
- `papers/PAPER-REVIEW.md`

This keeps design-time structure and empirical readiness separate.

### PDR-06 Story Derivation

Create one section-scoped writing story per `PSEC-*` node in `papers/PAPER-STORIES.md`.

Each story should include:

- a reader-centered outcome
- a short explanation of why the section matters
- a Given / When / Then formulation tied to graph inputs

### PDR-07 Review Derivation

Derive a current verdict in `papers/PAPER-REVIEW.md` from the state of the graph and evidence stack.

Suggested rule:

- PASS: section obligations exist and all required evidence-backed inputs are present
- FLAG: section contract exists but important evidence or authority inputs are incomplete
- BLOCKED: section cannot support its intended role because required graph inputs or evidence updates are missing

### PDR-08 Definition Authority Guard

The paper-design artifacts must never redefine canonical semantics from `definitions/DEFINITIONS.md`.

Paper design files explain synthesis obligations. Definitions remain authoritative elsewhere.

### PDR-09 Result Upgrade Rule

After a live experiment produces results, expand the graph before upgrading the paper:

1. add `Analysis Result` nodes
2. add `analyzes` and `updates` links where applicable
3. update `papers/PAPER-TEST-SPEC.md`
4. refresh `papers/PAPER-REVIEW.md`
5. then revise the relevant narrative paper sections

### PDR-10 Lessons Capture Rule

After a pilot project finishes paper work, record which derivation rules:

- reduced ambiguity
- created overhead
- failed to cover important paper work
- should become canonical automation or gates

## Future Reuse Direction

These rules are designed so MARS can later support graph-derived paper workflows without requiring authors to invent section contracts by hand every time.

The likely evolution path is:

1. pilot manually in one project
2. capture lessons learned
3. create a dedicated paper-design skill
4. automate derivation from `registry/RESEARCH-GRAPH.md`
