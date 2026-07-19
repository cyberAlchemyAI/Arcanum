# Workbench Poll

Workbench Poll is an Arcana sigil for the session side of the ide-extension manual bridge.

Workbench Up makes a request available. Workbench Poll is what an interested local session runs after the operator says "poll": it checks for an opaque ready handle, claims it, reveals the task only after a successful claim, runs the revealed skill in the current session, and records either a result or an interruption.

## When To Use

Use this sigil when:

- the operator has made a workbench request ready for open polling,
- the user wants the current Codex session to claim the hidden task,
- a blind test must prove the task and requested skill are not known before claim,
- the session needs to submit a kernel-admitted result or interruption after work.

Do not use it as a background worker, scheduler, or queue lease. It can continue execution only inside the active agent session that invoked it; it cannot wake an inactive session when the browser marks work available.

## Common Invocations

Check whether a request is ready:

```text
[$workbench-poll] --ready
```

Claim a ready handle, execute the revealed skill, and submit its result:

```text
[$workbench-poll] --claim --request-handle <id> --agent-ref codex.current-session
```

Claim without executing, for protocol diagnosis or an explicit handoff:

```text
[$workbench-poll] --claim-only --request-handle <id> --agent-ref codex.current-session
```

Submit a result after the requested work is actually done:

```text
[$workbench-poll] --result --claim-id <id> --input <result.json>
```

Submit an interruption when the session cannot complete:

```text
[$workbench-poll] --interrupt --claim-id <id> --input <interrupt.json>
```

## Blind-Test Boundary

Before claim, the poller may know only:

- whether a ready request exists,
- the opaque `request_handle`,
- local bridge status.

After successful claim, the poller may know:

- task,
- requested skill,
- grants,
- context,
- claim identifiers needed for result or interrupt.

If `ready` returns no request, the correct outcome is `no_ready_request`, not guessing or scanning durable state.

## Relationship To Workbench Up

`workbench-up --available` is the operator-side half: start workbench, prepare, approve, and mark ready.

`workbench-poll --ready` and `--claim` are the session-side half: discover the opaque handle, claim it, execute the revealed request in the active session, and return the admitted result. The two sigils deliberately meet only through the local bridge API.

## Lifecycle Status

Status: local operating sigil with same-session claim continuation.

The transport bridge is locally witnessed. Same-session continuation is now the default contract; background wake-up and unattended worker execution remain explicitly outside this sigil.
