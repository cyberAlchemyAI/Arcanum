# Invoke Design Input Authoring Guide

Start with the unified [Design authoring guide](design-authoring-guide.md) for
the complete path from admitted Define evidence through Design admission. This
guide expands only W1 input-boundary and input-closure authoring.

## Purpose

W1 closes the inputs that a later Design must respect. It does not infer
architecture from prose or code, decide which source outranks another, or claim
that the whole repository was searched. Its completeness claim is limited to
the roots and discovery rules that the target owner approved.

## Authoritative Documents

Author two machine documents:

1. `DESIGN-INPUT-BOUNDARY-APPROVAL.json` records the owner-approved target,
   visibility, observation epoch, roots, discovery rules, required input
   classes, and permitted exact exclusions.
2. `DESIGN-INPUT-CLOSURE.json` catalogs the discovered whole files, records
   authority and applicability, resolves every conditional and conflict, binds
   prior-Design status, authors typed signals, and states the selection
   predicates.

Markdown is explanatory evidence or a human view. It is not a substitute for
either schema-valid machine source.

## Authoring Sequence

1. Name the target owner and visibility.
2. Choose the smallest complete roots. In the boundary authoring request, bind
   each root object through `evidence_paths` with `kind: directory`; the CLI
   derives the deterministic tree digest and total byte size.
3. Add one or more discovery rules. Each rule binds `rule_id`, `root_id`, one
   input class, and explicit include globs. W1 has no implicit exclusion globs.
4. Record exact permitted exclusions. Every exclusion must name one discovered
   path and exact evidence; the closure exclusion set must equal the approved
   set.
5. Leave `boundary_digest` and `approval_digest` out of the authoring request.
   The CLI derives both from the validated material.
6. Catalog applicable files with canonical `file:<repo-relative-path>`
   selectors. Use regular whole files only; absolute paths, traversal,
   non-normal paths, duplicate normalized paths, and symlinks block.
7. Resolve every conditional input and conflict. An excluded conditional still
   requires an approved exact exclusion.
8. For greenfield, bind an exact determination that names the same target,
   epoch, owner, and zero applicable prior Design paths. For evolution, bind
   exactly one applicable prior Design and a valid producer-backed stage
   receipt. W1 never selects among multiple predecessors.
9. Author the thirteen scope-signal arrays. Every record names one
    `source_input_id`; the projector supplies its source path and digest.
10. For every authored concern, author exactly one predicate assertion. The
    asserted value must equal the authored concern and the final selection
    predicate.
11. Leave `closure_digest` out of the authoring request. The CLI derives it
    from the complete validated closure.

## Activation

Normal activation requires a current Define v3 stage receipt and its drift-free
Define admission v1. W1 validates both installed identities, their exact
agreement, output inventory, source/context target, and exactly one applicable
`define-artifact` catalog entry for the admitted `DEFINITIONS.json`.

Discovery activation still requires boundary approval. A PASS routes only to
`input-review`; it cannot enter normal W2/W3 Design production.

## Run

```text
tools/arcanum invoke design author boundary \
  --request BOUNDARY-AUTHORING-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-INPUT-BOUNDARY-APPROVAL.json

tools/arcanum invoke design author input-closure \
  --request CLOSURE-AUTHORING-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-INPUT-CLOSURE.json

tools/arcanum invoke design produce input-bundle \
  --closure DESIGN-INPUT-CLOSURE.json \
  --repo-root ROOT \
  --output ABSENT_DIRECTORY
```

A PASS atomically publishes exactly five files. A governed BLOCK removes
staging, leaves the success directory absent, returns exit `1`, and reports the
typed blocker in the CLI command result. Invocation/interface failure returns
exit `2` without fabricating evidence.

## Example

The historical public example starts at
[examples/design-input-v1/DESIGN-INPUT-CLOSURE.json](examples/design-input-v1/DESIGN-INPUT-CLOSURE.json).
It remains validate-only guidance for discovery activation. Inspect the current
successor stages and request schemas with `tools/arcanum invoke design describe`.

## Evidence Ceiling

W1 PASS proves approved-boundary-relative input closure, deterministic manifest
projection, frozen denominator compatibility, fixed-point selection, and exact
atomic W1 output closure. It does not prove repository-global semantic
completeness, architectural coherence, evolution against a real W3-produced
predecessor, six-view Design production, final Design stage PASS, capability
admission, mirror parity, Plan evidence, acceptance, execution, publication,
deployment, or external effect.
