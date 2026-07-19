---
surface_kind: canonical-sigil
runtime: generic
name: workbench-poll
description: "Use when: polling the ide-extension manual session bridge, claiming and executing one ready request in the current session, or submitting a claimant-bound result or interruption."
argument-hint: "[--ready|--claim|--claim-only|--result|--interrupt] [--base-url <url>] [--request-handle <id>] [--claim-id <id>] [--agent-ref <id>] [--session-ref <id>] [--input <json-file|->]"
tier: arcana
domain: local-workbench-operations
version: 0.2.0
origin: created from ide-extension manual session bridge protocol on 2026-07-17
allowed-tools: Read, Write, Grep, Bash
---

# Sigil: Workbench Poll

<objective>
Let a local session poll the ide-extension bridge, claim one ready request, expose task details only after atomic claim, execute the revealed skill in the current session by default, and submit a claimant-bound result or interruption.
</objective>

<logic-type>
Arcana: session-side bridge loop with blind pre-claim boundary, one-shot commands, claim binding, and honest result admission.
</logic-type>

<flags>
- `--ready`: run one readiness poll and return an opaque request handle if one exists.
- `--claim`: claim one request handle, invoke the revealed skill in the current session, execute the task, and submit the bound result by default.
- `--claim-only`: claim one request handle and return the execution packet without invoking the revealed skill.
- `--result`: submit one bound result after the requested work has actually been completed.
- `--interrupt`: submit one bound interruption when the session cannot complete the request.
- `--base-url <url>`: override the default loopback origin `http://127.0.0.1:8765`.
- `--request-handle <id>`: opaque handle returned by `--ready`; required for `--claim`.
- `--claim-id <id>`: claim identifier returned by `--claim`; required for `--result` or `--interrupt`.
- `--agent-ref <id>`: claimant identity for `--claim`. Default: `codex.current-session`.
- `--session-ref <id>`: caller-generated local session reference for `--claim`. Generate one if absent.
- `--input <json-file|->`: result or interrupt JSON for `--result` and `--interrupt`.
</flags>

<applicability>
Use this sigil when:

- the operator says `poll` after making a workbench request available,
- a blind test needs to prove the session does not know task or skill until claim,
- a local session needs to claim a ready request and run the requested skill in the same turn,
- a claimed request needs a terminal result or explicit interruption.

Do not use this sigil to start the workbench, prepare operator approvals, wake an inactive agent session, loop forever, or inspect durable state directly.
</applicability>

<inputs>
Expected inputs, if available:

- repository root, resolved from the current working directory,
- ide-extension bridge CLI at `projects/ide-extension/scripts/session-bridge.mjs`,
- base URL, defaulting to `http://127.0.0.1:8765`,
- request handle for claim mode,
- claim ID and JSON input for result or interrupt mode,
- optional `agent_ref` and `session_ref`.
</inputs>

<process>
## Step 1 - Resolve Bridge Client

1. Resolve the repository root from the current working directory.
2. Confirm `projects/ide-extension/package.json` exists.
3. Confirm the bridge CLI is available through `npm run bridge:session -- <command>`.
4. Use only a loopback HTTP base URL. Reject HTTPS, paths, remote hosts, and non-loopback origins.
5. Do not read or mutate `.ide-extension/state` directly.

## Step 2 - Ready Poll

Run this step for `--ready`.

1. Execute:

   ```text
   npm run bridge:session -- ready --base-url <base-url>
   ```

2. If exit code is `0`, report the returned opaque `request_handle`.
3. Do not infer, reveal, or guess the task, requested skill, grants, or context from a ready response.
4. If exit code is `3` with `no_ready_request`, report `Availability: none` without treating it as a failure.
5. If exit code is `4`, report that the workbench bridge is unreachable and recommend `workbench-up --start`.

## Step 3 - Claim And Continue

Run the claim portion of this step for `--claim` and `--claim-only`.

1. Require `--request-handle`.
2. Generate `session_ref` if absent, using a stable local shape such as `session-<timestamp>-<short-random>`.
3. Execute:

   ```text
   npm run bridge:session -- claim --request-handle <id> --session-ref <session-ref> --agent-ref <agent-ref>
   ```

4. If the claim succeeds, report the execution packet:
   - task,
   - requested skill,
   - grants,
   - context summary,
   - claim ID,
   - claim attempt ID,
   - envelope ID,
   - run ID,
   - approval ID,
   - session ref.
5. For `--claim-only`, stop after reporting the execution packet. Do not invoke the requested skill or submit a result.
6. For `--claim`, treat successful claim as authorization to continue the already-approved request in the current session:
   - resolve the revealed requested skill from the installed runtime skills,
   - read its complete `SKILL.md` before task actions,
   - execute the revealed task under that skill's process and boundaries,
   - preserve any human gate or blocker required by the requested skill,
   - assemble a result only from actual execution evidence.
7. If the requested skill cannot be resolved, execution cannot safely continue, or the requested skill reaches a real blocker, report the blocker and submit a bound interruption when the claim cannot remain usefully active.
8. Do not submit a passing result until the requested work has actually completed.

## Step 4 - Result

Run this step automatically after successful `--claim` execution, or explicitly for `--result` when resuming an already completed claim.

1. Require `--claim-id` and `--input`.
2. Confirm the input JSON contains the claim binding fields returned by claim:
   - `claim_id`,
   - `claim_attempt_id`,
   - `envelope_id`,
   - `run_id`,
   - `approval_id`,
   - `session_ref`,
   - `requested_skill`.
3. Execute:

   ```text
   npm run bridge:session -- result --claim-id <claim-id> --input <json-file|->
   ```

4. Report the admitted result and receipt only if the command exits `0`.
5. Never tell the user the task passed unless the local kernel admits the result.
6. Include the requested skill's real validation and evidence references; do not use placeholder hashes or synthetic evidence for a real run.

## Step 5 - Interrupt

Run this step for `--interrupt`.

1. Require `--claim-id` and `--input`.
2. Confirm the input JSON carries the claim binding fields and a reason.
3. Execute:

   ```text
   npm run bridge:session -- interrupt --claim-id <claim-id> --input <json-file|->
   ```

4. Report the interrupted claim state and preserve the reason.
5. State that only the operator may release and retarget an interrupted claim.
</process>

<quality-bar>
- `--ready` reveals only an opaque handle and no task details.
- `--claim` binds the request to an explicit `agent_ref` and `session_ref`.
- Claim output is the first point where task and requested skill are revealed.
- `--claim` continues into the revealed skill by default; only `--claim-only` stops after transport-level claim.
- Result and interrupt submissions are bound to the claim identifiers.
- Terminal success is reported only after kernel-admitted result output.
- No background polling process is left running.
- No durable state files are read to bypass the bridge API.
</quality-bar>

<anti-patterns>
- Polling repeatedly in a background loop.
- Guessing the requested skill before claim.
- Reading workbench state files to discover task content.
- Submitting a result before running the requested skill or work.
- Stopping after a successful `--claim` without `--claim-only`, a required human gate, or a named blocker.
- Claiming same-session continuation is a background worker or autonomous wake-up mechanism.
- Reporting chat completion as bridge completion without an admitted receipt.
- Claiming a request in `--ready` mode.
- Preparing or approving operator-side requests from this sigil.
</anti-patterns>

<observability>
When `.arcanum/observability/` exists, emit post-run telemetry for:

- mode,
- base URL,
- ready handle presence without task disclosure,
- claim ID and claimant refs when claimed,
- requested skill resolution and execution continuation status,
- result or interruption receipt when submitted,
- proof boundary,
- overclaim or blind-boundary violations.
</observability>

<output-contract>
Return:

```markdown
## Workbench Poll Result
- Mode:
- Base URL:
- Availability:
- Request handle:
- Claim:
- Requested skill:
- Task:
- Execution:
- Receipt:
- Validation:
- Proof boundary:
- Follow-up:
```
</output-contract>
