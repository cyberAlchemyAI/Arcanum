# Package Validation

## Verdict

Pass for authored development-package integrity. Runtime implementation is not
part of this verdict.

## Final checks

- Dispatch Spec: pass, with no blocks or flags.
- Design selection: pass, 13 concerns, fixed point true, diagnostics empty.
- Package documents: 10 JSON documents and one JSONL stream parse.
- Work Pack: eight unique SWUs, dependency DAG valid, selection null.
- Allowed routes: eight exact per-frontier tuples; each write scope matches its
  SWU; canonical digest
  `a2092630f4115fdc25c8624a9cc1232b5d347021c4f88c8e387911c3d7a20ca2`.
- Markdown navigation: eight package-relative links resolve.
- Distill: request, receipt, and event schemas pass; seven-event semantic
  process resolves; objections and reconciliations are complete.
- Boundary scan: no checkout-specific absolute paths or private umbrella paths.
- Scoped whitespace: no trailing whitespace in package files.

## Replay commands

Design replay requires all 13 repeated `--authored-concern-id` arguments from
`DESIGN-AUTHORED-CONCERNS.json`; omitting them correctly produces an unbound
signal block. The successful replay then runs
`design_selection_validator.py` with the authored concerns, planned witnesses,
and Invoke schema directory.

Dispatch replay:

```text
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  <package>/work-pack-execution-grant.dispatch.json --json
```

The structural package check reparses JSON/JSONL, verifies the SWU DAG and task
coverage, recomputes the allowed-routes digest using sorted compact JSON,
resolves Markdown links, and invokes the canonical Distill semantic validator.

## Evidence ceiling

These checks validate the Plan package and its authoring receipts. They do not
run any command named in an SWU verification field and do not establish runtime,
release, promotion, deployment, or production evidence.
