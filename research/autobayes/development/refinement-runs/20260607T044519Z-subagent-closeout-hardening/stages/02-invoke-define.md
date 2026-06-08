---
profile: autobayes-research
name: Invoke Define - Subagent Closeout Hardening
description: Definition artifact for hardening subagent lifecycle closeout in AutoBayes research task sessions.
type: invoke-define
status: pass
last_updated: 2026-06-07
---

# Invoke Define

## Capability Handle

`subagent-lifecycle-ledger`

## Definition

A subagent lifecycle ledger is a task-session-owned record that proves every delegated research lane has one final lifecycle state:

```text
not_spawned | spawned_pending | joined | timed_out | blocked | closed
```

A parent Task Session or Dispatch Spec research route may not report `PASS` for delegated research until the ledger proves:

- every attempted spawn has an agent id or a blocked reason;
- every spawned agent has a join result, timeout record, or explicit continuation handoff;
- every completed or timed-out agent has a closeout status;
- every thread-cap failure is recorded as residue with a reroute.

## Why This Exists

AutoBayes research runs already produced useful full-mode artifacts, but one lane was blocked by thread cap and closeout was managed manually. Full-AFK research needs this as a hard gate.

## Owner Boundary

- Task Session owns the execution gate and report.
- Dispatch Spec owns route shape and receipt requirements.
- Observability owns telemetry after the run.
- Native Codex Goal owns continuation across turns.

