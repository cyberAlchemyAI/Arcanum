# Validation Report

Status: pass for package authoring and existing baseline regressions.

## Package checks

- JSON parse: 10 files, pass.
- Design schemas: scope manifest, denominator receipt, and selection result pass.
- Design selection: 13 extracted signals, 13 total concerns, fixed point true, §design-validator-pass§.
- Distill schemas, seven-event runtime sequence, and semantic validation: pass.
- SWU manifest: six unique units, valid dependencies/successors, selected unit null.
- Markdown links: pass.
- Dispatch Spec: pass.
- Scoped whitespace: pass.
- Public-boundary scan: pass for private project paths, identifiers, and ontology names.
- Invoke and child Distill observability: recorded at central ledger lines 536 and 535 respectively.

## Existing baseline checks

- Continuation Router lifecycle and six route fixtures: pass.
- Plan-once end-to-end: 1/1 pass, including zero pre-execution Refresh calls.
- Plan-once material admission: 3/3 pass.
- Plan-once governance and single-use admission: 2/2 pass.
- Full Invoke fixture suite: pass, including 28 Design-selection cases and 23 material/handoff cases.

## Evidence interpretation

These checks prove the package is structurally coherent and that its plan-once premise exists in the current local implementation. The new prerequisite schemas, classifier, Router phase, same-attempt resume, adoption changes, and package-local canaries remain planned work.

The Invoke fixture runner emitted §arcanum/spells/invoke/development/runs/20260804T191018Z.md§ as validation evidence.
