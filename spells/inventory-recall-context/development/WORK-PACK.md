---
work_pack_id: WP-IRC-L0-001
spell: inventory-recall-context
status: prepared-unselected
active_layer: L0
updated_at: 2026-08-07
authority_effect: none
---

# L0 Work Pack

## Control state

| Field | Value |
| --- | --- |
| work pack | `WP-IRC-L0-001` |
| active layer | L0 only |
| frontier | `SWU-IRC-001`, `SWU-IRC-002`, then closure-only `TASK-IRC-VERIFY` |
| selected unit | none |
| execution owner | Task Session after an explicit selection/admission turn |
| lifecycle owner | Spellcraft |
| mutation authority | none from this document |
| authority effect | none |

## Source contracts

- `../README.md`
- `SPELLCRAFT-ACCEPTANCE.md`
- `IMPLEMENTATION-LAYERING.md`
- `DESIGN-SCOPE-MANIFEST.json`
- `DESIGN-DENOMINATOR-RECEIPT.json`
- `DESIGN-SELECTION-RESULT.json`
- `L0-SCENARIOS.json`

Every implementation session must bind current digests for these inputs. A
stale planning digest blocks admission.

## Global invariants

1. Inventory is a read model, not authority.
2. Current owner-controlled sources outrank indexed summaries.
3. `injectionAllowed` is derived and fail-closed.
4. Only a passing source-bound pack may enter the current task context.
5. Denied outcomes have a receipt and no injectable pack handle.
6. No Inventory, selected source, ontology, definition, registry, generated
   mirror, model state, network target, or host configuration is written.
7. Use Python standard library only; add no package root or runtime dependency.
8. Runtime results are evidence, not promotion or release authority.

## SWU-IRC-001 — Pure gate and typed records

### Goal

Implement a pure evaluator for typed recall evidence and prove that only the
positive case allows injection.

### Exact write scope

- `spells/inventory-recall-context/runtime/inventory_recall_context.py`
- `spells/inventory-recall-context/validation/run-fixtures.py`
- `spells/inventory-recall-context/validation/results/.gitignore`
- `spells/inventory-recall-context/development/work-pack/closeouts/SWU-IRC-001.json`

No other path is admitted.

### Required behavior

- validate request, lookup packet, source-state, pack coverage, safety, and
  budget fields;
- derive a stable reason code and boolean decision;
- reject caller-supplied decision overrides and malformed/unknown predicates;
- consume `development/L0-SCENARIOS.json` in `gate` mode;
- write only run-local validation results and the closeout receipt.

### Validation

From the Arcanum repository root:

```bash
python3 -m py_compile \
  spells/inventory-recall-context/runtime/inventory_recall_context.py \
  spells/inventory-recall-context/validation/run-fixtures.py
python3 spells/inventory-recall-context/validation/run-fixtures.py --phase gate
git diff --check -- spells/inventory-recall-context
```

### Done criteria

- seven scenario inputs are accepted by the fixture runner;
- positive returns `injectionAllowed: true` and `allowed`;
- stale, missing, contradictory, unsafe, over-budget, and blocked-index each
  return `false` with their frozen reason code;
- no imported module beyond the Python standard library;
- no write occurs outside the exact scope;
- closeout receipt binds input/output digests and command results.

### Closeout synchronization

Task Session emits
`development/work-pack/closeouts/SWU-IRC-001.json`, then hands it to
`spellcraft:validate`. Spellcraft alone may update lifecycle state and expose
`SWU-IRC-002` as selectable. Completion does not auto-select its successor.

## SWU-IRC-002 — Current-source verifier and native packet coordinator

### Dependencies

- Spellcraft-reviewed `SWU-IRC-001` closeout with verdict `pass`;
- unchanged Work Pack and scenario digests;
- current Inventory and Context Builder contracts.

### Exact write scope

- `spells/inventory-recall-context/runtime/inventory_recall_context.py`
- `spells/inventory-recall-context/validation/run-fixtures.py`
- `spells/inventory-recall-context/validation/fixtures/**`
- `spells/inventory-recall-context/validation/results/**`
- `spells/inventory-recall-context/development/work-pack/closeouts/SWU-IRC-002.json`

No other path is admitted.

### Required behavior

- resolve paths beneath an explicit allowlisted repository root without path
  escape;
- verify selected bytes and selectors against expected SHA-256 bindings;
- classify current, stale, missing, contradictory, and unsafe evidence;
- validate Inventory lookup and strict Context Builder packet shapes;
- accept child results supplied by the parent-native host; do not invoke a
  nested model CLI;
- return a source-bound pack handle only when the pure gate passes;
- never write Inventory, sources, or child artifacts.

### Validation

```bash
python3 -m py_compile \
  spells/inventory-recall-context/runtime/inventory_recall_context.py \
  spells/inventory-recall-context/validation/run-fixtures.py
python3 spells/inventory-recall-context/validation/run-fixtures.py --phase native
bash spells/inventory-recall-context/development/validate-scenarios.sh
git diff --check -- spells/inventory-recall-context
```

### Done criteria

- all seven native fixtures produce digest-bound receipts;
- all negative/degraded cases deny injection and expose no pack handle;
- the positive case retains request, index, source, pack, and receipt digests;
- before/after digest evidence shows no protected source or Inventory write;
- closeout receipt names residual gaps and exact runtime evidence.

### Closeout synchronization

Task Session emits
`development/work-pack/closeouts/SWU-IRC-002.json`, then hands it to
`spellcraft:validate`. Spellcraft may admit closure work only after reviewing
the live native evidence. No registry or generation action follows implicitly.

## TASK-IRC-VERIFY — L0 closure only

### Exact scope

- read the completed L0 runtime, fixtures, and closeouts;
- write timestamped Experiment Harness run/report evidence beneath
  `development/runs/` and `development/example-runs/`;
- write `development/work-pack/closeouts/TASK-IRC-VERIFY.json`;
- update lifecycle/projection artifacts only through `spellcraft:validate`.

### Validation

```bash
bash spells/inventory-recall-context/development/run-validation-fixtures.sh
bash arcana/experiment-harness/scripts/validate-harness.sh \
  spells/inventory-recall-context
git diff --check -- spells/inventory-recall-context
```

### Done criteria

- live outputs are distinguishable from save summaries;
- the seven scenario verdicts and protected-path checks pass;
- a timestamped harness report binds the executed runtime;
- lifecycle residue is reconciled without claiming registry release or
  promotion.

## Selection rule

This Work Pack selects no unit. A later explicit execution/admission decision
may select exactly one dependency-ready SWU. Selection must be reflected in a
fresh validated execution-entry projection before Task Session begins.

## Deterministic successor policy

- After `SWU-IRC-001` pass: `SWU-IRC-002` becomes eligible but remains
  unselected.
- After `SWU-IRC-001` block/fail: no successor is eligible; return to
  `spellcraft:validate`.
- After `SWU-IRC-002` pass: closure-only `TASK-IRC-VERIFY` becomes eligible.
- After any invariant or boundary failure: stop; do not broaden scope.
