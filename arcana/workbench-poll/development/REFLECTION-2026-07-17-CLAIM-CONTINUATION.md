# Workbench Poll Claim Continuation Reflection

## Signal Summary

- `--ready` returned an opaque handle without task or skill disclosure.
- `--claim` atomically bound the request and revealed `task-session` as the requested skill.
- The sigil stopped after claim because version 0.1.0 treated full execution as optional.
- The operator expected claiming to start the approved work and corrected that behavior explicitly.

## Observer Pass

Mode: local fallback; no subagent mechanism was available in this runtime.

Finding: severe workflow gap. The bridge contract was sound, but the orchestration contract made the ordinary `--claim` path stop before delivering user value. The distinction between transport claim and active-session execution was hidden behind wording rather than an explicit mode.

## Proposed Changes

- Make `--claim` continue into the revealed skill and submit the bound result by default.
- Add `--claim-only` for protocol inspection, handoff, and diagnostic use.
- Preserve late disclosure, claim binding, human gates, and kernel-admitted terminal receipts.
- Record whether requested-skill resolution and execution continuation occurred.

## Rejected Changes

- Do not claim that this creates a background worker.
- Do not make the browser wake an inactive Codex session.
- Do not bypass the revealed skill's human gates or completion criteria.
- Do not submit synthetic evidence for real requested work.

## Applied Decision

Targeted update accepted. The core bridge remains one-shot and claim-bound; the active session now owns continuation after successful claim unless `--claim-only` is explicit.

## Next Trigger

Review after five meaningful claim executions, or immediately if a claim cannot preserve a requested skill's human gate or result evidence.
