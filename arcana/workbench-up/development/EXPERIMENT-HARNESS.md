# Workbench Up Experiment Harness

This harness keeps Workbench Up honest while it is still a local operating sigil.

## Fixtures

| Fixture | Purpose | Expected Result |
| --- | --- | --- |
| `check-healthy` | Server is already running on `127.0.0.1:8765`. | `--check` reports HTTP 200 and does not start a duplicate server. |
| `start-cold` | No server is listening on the default port. | `--start` launches `npm run start`, waits for `/demo/l0`, and reports the URL. |
| `available-request` | Operator wants a task ready for manual polling. | `--available` prepares, approves, marks ready, and stops before claim. |
| `smoke-loop` | Developer wants a bridge contract proof. | `--smoke` prepares, approves, marks ready, claims, records synthetic result, and reports proof limits. |
| `bad-port` | Port is occupied by a non-workbench process or unreachable route. | Returns `BLOCK` with concrete URL and startup/check evidence. |

## Manual Test Script

1. Run `[$workbench-up] --start`.
2. Open the reported URL and confirm the workbench renders.
3. Run `[$workbench-up] --available --task "Change the logo of the presentation" --skill whisper`.
4. In a separate session, poll with the manual bridge CLI or API and confirm the ready response exposes only an opaque handle before claim.
5. Claim the request from the separate session and confirm the task and skill appear only after successful claim.
6. Run `[$workbench-up] --smoke --task "Workbench bridge smoke" --skill decision-gate --agent-ref openrouter.local-session`.
7. Confirm the closeout says the smoke proves the bridge loop, not real skill execution.

## Promotion Gate

Promotion readiness requires:

- at least three successful runs across `--start`, `--available`, and `--smoke`,
- one cold-start run,
- one unclaimed availability run consumed by a separate polling session,
- one failed-port or failed-route negative control,
- no overclaim language in closeouts.

## Known Limits

- No automatic worker is created.
- No browser-control API is added.
- No remote deployment or tunnel is created.
- No provider credentials are read.
- Real skill execution remains outside this sigil's proof boundary.
