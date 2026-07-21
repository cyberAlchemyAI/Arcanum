# Continuation Router

Continuation Router is an Arcana sigil for the boundary between one terminal capability run and its next owner. It turns a receipt into visible probable routes, checks exact authorization, dispatches at most one owner capability, joins that owner's receipt, and returns the next route.

It exists because route advice and route execution are different contracts. A blocked Task Session can correctly name `invoke-refresh`, yet a later run may still repeat the blocked task when the handoff is only free text. The router makes that handoff typed and auditable without expanding Task Session into a general workflow engine.

## Use When

- a terminal receipt names or implies a next owner,
- the source capability should not be repeated with unchanged evidence,
- one to three probable routes should be visible before dispatch,
- one exact capability and mode may be authorized for a bounded hop,
- the selected owner must return a separate receipt.

## Do Not Use When

- there is no terminal receipt,
- several independent routes should run in parallel,
- the target needs broad discovery or design,
- a multi-node Craft graph belongs to Goal,
- the caller expects recursive continuation.

## One-Hop Boundary

```text
terminal source receipt
  -> continuation-router ranks 1-3 owner routes
  -> exact authorization and owner gates
  -> at most one owner dispatch
  -> joined owner receipt
  -> returned next route, not auto-executed
```

The router may run in one bounded helper or subagent so the parent receives a clean route result. The helper is an execution strategy, not an authority boundary. The selected owner still owns all semantic work and mutation.

## Authorization

Use an exact route tuple:

```text
--authorize-route invoke:refresh:apply-approved
```

That grant authorizes only that capability, mode, and mutation mode for the declared target and write scope. It does not authorize a different owner, recursive continuation, destructive cleanup, or a broader mutation.

Without exact authorization, the router may still return probable routes, but it does not dispatch a consequential route.

## Common Routes

- planning drift -> `invoke:refresh`;
- blocker-level human choice -> `decision-gate:blocker`;
- one ready task or SWU -> `task-session:execute`;
- vague target -> `refine:standard` or an Invoke authoring mode;
- broad Craft graph -> `goal:execute`;
- missing evidence or unsafe scope -> `stop:user-input`.

These are candidate patterns only. Installed owner contracts and the source receipt remain authoritative.

## Artifacts

- [SKILL.md](SKILL.md) defines routing, authorization, dispatch, and receipt behavior.
- [continuation-route.schema.json](continuation-route.schema.json) defines the durable machine receipt.
- `development/` holds Experiment Harness evidence and route-specific fixtures.

## Why This Is Arcana

Continuation Router coordinates evidence, authority, dispatch, helper lifecycle, and owner receipts across capabilities. It is not a deterministic formatter and it does not perform the selected owner's work.
