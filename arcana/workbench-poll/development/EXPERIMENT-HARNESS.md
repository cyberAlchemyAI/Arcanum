# Workbench Poll Experiment Harness

This harness validates the session-side half of the manual bridge.

## Fixtures

| Fixture | Purpose | Expected Result |
| --- | --- | --- |
| `no-ready-request` | No request is currently marked ready. | `--ready` reports no available request without guessing task content. |
| `ready-handle` | One approved request is ready. | `--ready` returns only an opaque `request_handle`. |
| `claim-reveal-and-run` | A ready handle is claimed by the intended active session. | `--claim` returns the execution packet, resolves the requested skill, runs it, and submits a bound result. |
| `claim-only` | A transport-level diagnosis needs the execution packet without running work. | `--claim-only` returns the packet and leaves the claim active without a result. |
| `claim-loser` | Another session tries to claim an already claimed handle. | Loser receives conflict and no execution packet. |
| `result-bound` | Claimed work is completed and submitted. | `--result` returns admitted receipt with the claimant agent ref. |
| `interrupt-bound` | Claimed work cannot complete. | `--interrupt` records interrupted state and does not release the claim automatically. |

## Manual Blind Test

1. In the operator context, run `[$workbench-up] --available --task "<hidden task>" --skill <skill>`.
2. In the intended session, run `[$workbench-poll] --ready`.
3. Confirm the ready output has an opaque handle and does not include task or skill.
4. Run `[$workbench-poll] --claim --request-handle <id> --agent-ref codex.current-session`.
5. Confirm the task and requested skill appear only after successful claim.
6. Confirm the active session resolves and reads the requested skill without another operator command.
7. Confirm the task executes under that skill and `--claim` submits the bound result.
8. Confirm the receipt is kernel-admitted before claiming pass.
9. Repeat with `--claim-only` and confirm no skill execution or result submission occurs.

## Promotion Gate

Promotion readiness requires:

- one no-ready negative control,
- one ready-without-disclosure proof,
- one successful claim-reveal-execute-result run,
- one explicit claim-only run,
- one losing concurrent claim proof,
- one admitted result,
- one interruption and operator-release recovery proof,
- no durable state bypass.

## Known Limits

- Same-session execution still depends on an active agent invocation; the workbench cannot wake an inactive session.
- No background polling.
- No operator-side prepare or approval.
- No remote bridge origin.
- No attestation that the claimant is really the named agent; assurance remains `unattested`.
