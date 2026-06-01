# Goal Handoff: EvidenceSet Schema Refinement

## Objective

Refine the Inventory `EvidenceSet` candidate into a minimal schema design proposal and non-executed next-route plan.

## Constraints

- Do not canonicalize `EvidenceSet`.
- Do not edit production templates or runtime scripts.
- Preserve shell plus `jq` as the preferred fast agent surface.
- Keep human UI deferred.
- Keep `EvidenceSet` subordinate to evidence cards and downstream handoff packets.

## Stage Dispatch Contract

Each command-backed stage resolves through:

```sh
tools/arcanum --resolve <command>
```

and, where runnable, dispatches through:

```sh
tools/arcanum --exec --output <stage-output> <command> <stage-request>
```

## Blocked Fields

None at seed time. If command execution fails, record the failed stage with exact command output and continue only with stage-owned blocked evidence.

## Goal Status

Prepared only. No native `/goal` execution requested for this refine run.
