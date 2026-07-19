---
surface_kind: canonical-sigil
runtime: generic
name: workbench-up
description: "Use when: starting or checking the ide-extension local workbench, making a request available for open-poll bridge testing, or running a bounded local bridge smoke."
argument-hint: "[--start|--check|--available|--smoke] [--port <port>] [--task <text>] [--skill <skill>] [--agent-ref <id>] [--session-ref <id>]"
tier: arcana
domain: local-workbench-operations
version: 0.1.0
origin: created from ide-extension open-poll bridge pilot on 2026-07-17
allowed-tools: Read, Write, Grep, Bash
---

# Sigil: Workbench Up

<objective>
Bring the local ide-extension HTML workbench online, report a usable URL, and optionally create or exercise one approval-gated open-poll bridge request.
</objective>

<logic-type>
Arcana: local operating loop with readiness checks, approval boundary preservation, optional bridge evidence, and honest proof limits.
</logic-type>

<flags>
- `--start`: start the local workbench if it is not already responding, then report the URL.
- `--check`: check the current workbench route only; do not start a server or create requests.
- `--available`: start or verify the workbench, prepare one task envelope, approve it, and mark it ready for open polling. Do not claim it.
- `--smoke`: start or verify the workbench, prepare one task envelope, approve it, mark it ready, claim it, and submit a synthetic admitted result.
- `--port <port>`: override the default port `8765`.
- `--task <text>`: task text for `--available` or `--smoke`. Default: `Workbench bridge smoke`.
- `--skill <skill>`: requested skill slug for the prepared request. Default: `decision-gate`.
- `--agent-ref <id>`: claimant identity for `--smoke`. Default: `openrouter.local-session`.
- `--session-ref <id>`: caller-generated session reference for `--smoke`.
</flags>

<applicability>
Use this sigil when:

- the user asks to run, reopen, or demo the local workbench,
- the workbench must be available for a ResonantOS or augmentor demonstration,
- a manual polling request needs to be made available without revealing the task before claim,
- the bridge needs a quick L0 contract smoke before real work starts.

Do not use this sigil for remote deployment, browser-extension control, model-provider integration, or real skill execution attestation.
</applicability>

<inputs>
Expected inputs, if available:

- repository root, resolved from the current working directory,
- ide-extension project at `projects/ide-extension`,
- desired mode: `--start`, `--check`, `--available`, or `--smoke`,
- optional task text,
- optional requested skill slug,
- optional claimant identity for smoke mode.
</inputs>

<process>
## Step 1 - Resolve Workbench Project

1. Resolve the repository root from the current working directory.
2. Confirm `projects/ide-extension/package.json` exists.
3. Confirm its `start` script is `node src/server.mjs` or an equivalent local server command.
4. Build the base URL as `http://127.0.0.1:<port>`, defaulting to port `8765`.
5. Build the workbench URL as `<base-url>/demo/l0`.

## Step 2 - Check Readiness

1. Request the workbench URL with a short timeout.
2. If it returns HTTP 200, report `Server: running`.
3. If the user selected `--check` and the route is not available, return `BLOCK` with the failed URL and do not start anything.
4. If the route is not available and the mode allows startup, run `npm run start` from `projects/ide-extension` as a long-running local server command.
5. Poll the workbench URL until it returns HTTP 200 or the startup timeout expires.
6. If startup fails, return `BLOCK` with the command, port, and latest connection error.

## Step 3 - Prepare Availability

Run this step only for `--available` and `--smoke`.

1. Prepare one envelope with `POST /api/envelopes/prepare`.
2. Use the supplied task text or `Workbench bridge smoke`.
3. Use the supplied requested skill or `decision-gate`.
4. Preserve the approval boundary: the prepared request must still be approved before it is ready.
5. Approve the prepared request with `POST /api/approvals/<approval_id>/approve`.
6. Mark the approved envelope ready with `POST /api/bridge/requests/<envelope_id>/ready`.
7. Confirm `GET /api/bridge/requests/ready` returns one opaque `request_handle`.
8. For `--available`, stop here and report the envelope ID, approval ID, and ready handle. Do not claim the request.

## Step 4 - Run Optional Smoke

Run this step only for `--smoke`.

1. Claim the ready request with `POST /api/bridge/requests/<request_handle>/claim`.
2. Bind the claim to `agent_ref`, defaulting to `openrouter.local-session`.
3. Use a caller-generated `session_ref` when one is not provided.
4. Confirm the successful claim reveals the task, requested skill, grants, and context.
5. Submit one synthetic result with `POST /api/bridge/claims/<claim_id>/result`.
6. Use `status: "passed"` and `result_type: "skill.execution"` only for the local smoke, and state that this does not attest real skill execution.
7. Confirm `/api/state` shows the envelope in a terminal passed state and the ready handle cleared.

## Step 5 - Close Honestly

1. Report the workbench URL prominently.
2. State which mode ran.
3. State whether the server was already running or started during the run.
4. State whether an available request was created.
5. State whether a claim/result smoke was run.
6. If any step failed, preserve the exact failing endpoint or command.
</process>

<quality-bar>
- Workbench URL is loopback and concrete.
- Server readiness is checked with the actual `/demo/l0` route.
- `--available` leaves the request unclaimed and ready for a separate polling session.
- `--smoke` binds any result to a successful claim and a named `agent_ref`.
- Pre-claim output does not reveal task or requested skill beyond what the operator already supplied.
- The closeout separates "bridge loop proved" from "real skill executed".
</quality-bar>

<anti-patterns>
- Claiming that smoke mode proves Codex, Claude, OpenRouter, or a named skill actually executed.
- Starting duplicate servers when the route is already healthy.
- Using a non-loopback URL by default.
- Skipping approval and marking an unapproved request ready.
- Claiming an `--available` request in the same run.
- Hiding failed curl, CLI, or API responses.
- Mutating workbench state files directly instead of using the local API.
</anti-patterns>

<observability>
When `.arcanum/observability/` exists, emit post-run telemetry for:

- mode,
- server state,
- workbench URL,
- prepared envelope ID when present,
- claim ID and `agent_ref` when smoke mode claims a request,
- validation commands or endpoints checked,
- proof boundary and any overclaim risk.
</observability>

<output-contract>
Return:

```markdown
## Workbench Up Result
- Mode:
- Server:
- URL:
- Availability:
- Prepared envelope:
- Claimant:
- Receipt:
- Validation:
- Proof boundary:
- Follow-up:
```
</output-contract>
