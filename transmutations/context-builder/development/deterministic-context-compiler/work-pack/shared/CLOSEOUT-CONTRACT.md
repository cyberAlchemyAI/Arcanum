# Task Session Closeout Contract

## Purpose

Define one stable reconciliation protocol for every mutation-capable SWU.
Task-specific files still declare exact target inventories and successors.

## Baseline Binding

Before mutation, the selected Task Session writes:

```text
session-evidence/<SWU-ID>/baseline.json
```

The baseline contains:

- `swu_id`;
- the exact declared target inventory in plan order;
- for each target: `exists`, `kind`, and SHA-256 for an existing file;
- repository-relative paths only;
- the scoped porcelain status for the exact target inventory;
- the canonical JSON digest of all preceding fields.

Missing future targets are recorded with `exists: false`; they are not replaced
by globs. The Task Session blocks if its requested write is outside the exact
inventory.

## Terminal Source Receipt

The executor writes:

```text
session-evidence/<SWU-ID>/task-session-receipt.json
```

Required fields:

- `swu_id`, `session_id`, `status`, and `selected_swu`;
- baseline digest and exact target inventory;
- observed delta for each target;
- validation commands, exit codes, and evidence paths;
- residual blockers and unrelated pre-existing changes;
- `authority_effect: none`;
- proposed successor eligibility without selection.

Only `pass` with no undeclared target mutation can enter owner closeout.

## Owner Receipt

Sigil Development validates the terminal source receipt and writes:

```text
session-evidence/<SWU-ID>/owner-receipt.json
```

Required fields:

- `swu_id`, `owner: sigil-development`, and source receipt digest;
- `validation_result`, exact validated targets, and validation evidence;
- admitted delta classes and residual blockers;
- `successor_eligible`, `successor_id`, and `successor_selected: false`;
- `lifecycle_effect` and `authority_effect`.

An owner receipt may reconcile evidence and mark the completed SWU. It cannot
select or execute a successor, authorize unrelated mutation, publish, deploy,
approve cost/risk, or promote the canonical sigil.

## Delta Classes

Allowed classes are:

- `artifact_added`
- `artifact_changed`
- `evidence_added`
- `status_changed`
- `route_changed`

Each task file narrows this set. Deletion, unrelated cleanup, authority change,
publication, deployment, and consumer-private export are never admitted.

## Successor Rule

A successor is eligible only when:

1. the source and owner receipts pass;
2. all predecessor dependencies are complete;
3. no blocker affects the successor acceptance boundary; and
4. the successor ID exactly equals the task-local declaration.

Eligibility is not selection. Every successor begins with
`successor_selected: false`.
