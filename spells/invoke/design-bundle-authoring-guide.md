# Invoke Design Bundle Authoring Guide

Start with the unified [Design authoring guide](design-authoring-guide.md) for
the complete path from admitted Define evidence through Design admission. This
guide expands only W3 bundle closure, final production, and replay admission.

`DESIGN-BUNDLE-CLOSURE.json` v2 is the sole W3 machine input. It does not contain
architecture prose. It exact-binds one passing W2 candidate receipt, the target,
the fixed fifteen-file output contract, and four Distill evidence files.

## Required evidence

- `candidate_receipt_ref` resolves to the receipt inside an unchanged atomic W2
  directory containing exactly `DESIGN.json`, the coherence receipt, and the
  candidate production receipt.
- The candidate binds the current installed Design process, public profile,
  coherence policy, W1 receipt, source, artifact, and coherence validator.
- `distill_evidence` binds a Design-mode request, ordered JSONL event log,
  execution receipt, and independent validation result. The request must review
  the exact candidate artifact and candidate receipt in that order.
- Distill execution and validation must both be clean `pass`; `flag` and `block`
  route to `repair-distill-evidence` and publish no bundle.
- `output_contracts` uses the exact filenames fixed by the closure schema.
- `closure_digest` is SHA-256 over canonical compact JSON with that field
  omitted.

## Produce and admit

```text
tools/arcanum invoke design author bundle-closure \
  --request BUNDLE-CLOSURE-AUTHORING-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-BUNDLE-CLOSURE.json

tools/arcanum invoke design produce final-bundle \
  --closure DESIGN-BUNDLE-CLOSURE.json \
  --repo-root ROOT \
  --output ABSENT_DIRECTORY

tools/arcanum invoke design admit admission \
  --bundle BUNDLE_DIR \
  --repo-root ROOT \
  --output ABSENT_RECEIPT
```

Compiler exit `0` publishes exactly fourteen payloads plus the v3 stage receipt
in one atomic directory replacement. Exit `1` leaves that directory absent and
writes one block-only attempt receipt. Exit `2` means the invocation or installed
contracts prevented valid evidence from being issued.

Admission never edits the submitted bundle. It validates its complete inventory,
replays the compiler from the bound closure into temporary storage, and requires
byte equality before writing the admission receipt outside the bundle.

## Routing and ceiling

Neutral architecture, UX, or research companions route to `plan`; spell-only
ownership routes to `spellcraft`; sigil-only ownership routes to
`sigil-development`; unresolved non-blocking Design gaps route to `deferred`.
Conflicting spell/sigil ownership blocks.

W3 PASS establishes deterministic bundle authorship, exact W1/W2/Distill binding,
independent replay admission v2, and consumable v3 predecessor evidence. It does not
establish Plan evidence, registry release, mutation readiness, acceptance,
execution, publication, deployment, or external effect.

See the [executable W3 example](examples/design-bundle-v1/README.md).
