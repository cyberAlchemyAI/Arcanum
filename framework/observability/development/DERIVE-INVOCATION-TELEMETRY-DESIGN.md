# Derive Invocation Telemetry Design

## Purpose

`derive-invocation-telemetry` is the missing component between runtime closeout and ledger append.

It turns raw run evidence into a structured observer envelope:

```text
pending-envelope.json
tool-events.jsonl
final assistant message
optional skill telemetry profile
  -> derive-invocation-telemetry
  -> enriched envelope.json
  -> observe-invocation.sh
  -> central ledger, indexes, counters
```

`observe-invocation.sh` remains the append authority. It should validate, normalize, dedupe, append, index, and count. It should not become the semantic extractor.

## Problem It Solves

The current Stop hook can see:

- pending envelope metadata,
- tool events,
- tool failure count,
- final assistant message.

But it only writes coarse telemetry:

- execution status,
- quality fallback,
- validation note,
- tool event count,
- final-message excerpt.

That is enough to prove that a run happened. It is not enough to explain what the skill produced, which output contract gaps appeared, whether anti-patterns were hit, or what reflection should do.

## Component Boundary

### Owns

- deterministic extraction from hook evidence,
- conservative output and file-path derivation,
- skill-local telemetry profile loading,
- workflow gap and quality signal derivation,
- enrichment of `execution` and `observer` fields,
- an extraction report for diagnostics.

### Does Not Own

- ledger append,
- dedupe,
- index updates,
- reflection counter updates,
- full semantic judgment without an explicit profile or observer mode,
- direct mutation of skill files or user artifacts.

## Inputs

| Input | Required | Source | Notes |
| --- | --- | --- | --- |
| `pending-envelope.json` | yes | UserPromptSubmit hook | Contains capability, skill, request, initial observer fields. |
| `tool-events.jsonl` | no | PostToolUse hook | Contains observed tool events for the run when hook coverage exists for the tool handler. |
| final assistant message | no | Stop hook input | Used for closeout excerpt and structured marker extraction. |
| skill telemetry profile | no | skill folder | Adds capability-specific quality/gap checks. |
| extraction config | no | env/config | Controls strictness, redaction, and optional AI observer use. |

## Outputs

| Output | Path | Purpose |
| --- | --- | --- |
| enriched envelope | `<run-dir>/envelope.json` | Observer-ready envelope for `observe-invocation.sh`. |
| extraction report | `<run-dir>/derived-telemetry.json` | Diagnostics about what was derived, skipped, or redacted. |
| closeout status | stdout key/value fields | Lets Stop hook report extraction status before append. |

## Proposed CLI

```bash
framework/observability/scripts/derive-invocation-telemetry.sh \
  --pending <run-dir>/pending-envelope.json \
  --output <run-dir>/envelope.json \
  --tool-events <run-dir>/tool-events.jsonl \
  --final-message-file <run-dir>/final-message.md \
  --repo-root <repo-root>
```

Optional:

```bash
  --skill-profile <path>
  --mode deterministic|profile|ai-assisted
  --redact-raw-request
```

Default mode: `profile`.

`profile` means deterministic generic extraction plus deterministic skill-profile checks when a profile exists. It must not call an AI model.

## Derivation Levels

### L0: Generic Runtime Evidence

Always available when hooks ran.

Derived fields:

- `execution.status`: completed, partial, blocked, failed, or interrupted.
- `execution.validation`: hook-opened, tool-evidence-recorded, stop-closed, extraction-ran.
- `execution.notes`: tool event count, tool failure count, extraction mode.
- `observer.quality_bar_status`: fallback from status and tool failures.
- `observer.recommendation`: fallback from status.

This level must stay fully deterministic.

### L1: Tool Evidence Extraction

Parse `tool-events.jsonl` conservatively.

Derived fields:

- `execution.files_changed`: only from known write-capable tool schemas or explicit file paths in tool inputs.
- `execution.outputs`: output paths only when a write tool or explicit command output path makes them clear.
- `observer.workflow_gaps`: tool failure gaps, missing-output gaps, validation failure gaps.

Rules:

- Never infer changed files from assistant prose.
- Unknown tool schemas contribute counts and failures, not file paths.
- Shell command strings are not changed-file evidence unless the command is a known write command and the path is explicit.
- Missing write-tool events are not a failure; they produce empty `files_changed` plus a skipped diagnostic in `derived-telemetry.json`.

### L2: Structured Closeout Extraction

Parse final assistant message for explicit closeout markers only.

Recognized markers:

- `Outputs:`
- `Validation:`
- `OBSERVATION=`
- `REFLECTION_TRIGGER=`
- `RECOMMENDATION=`
- `Next route:`
- `Blocked:` or `Blockers:`

Rules:

- Use marker extraction for summaries and validation notes.
- Do not treat narrative claims as proof of changed files.
- Store only a bounded `closeout_excerpt`.

### L3: Skill-Local Telemetry Profile

If the skill folder contains a telemetry profile, apply it deterministically.

Recommended location:

```text
<skill-folder>/telemetry/profile.json
```

Because `.agents/skills/<name>` may be a symlink, this is also the canonical capability folder:

```text
arcana/distill/telemetry/profile.json
```

Profile example:

```json
{
  "version": "0.1.0",
  "capability": "distill",
  "quality_signals": [
    {
      "id": "has-smallest-coherent-unit",
      "marker": "Current smallest coherent unit",
      "status_when_present": "pass",
      "severity_when_missing": "medium",
      "gap_category": "output-contract"
    },
    {
      "id": "has-recomposition-proof",
      "marker": "Closure and recomposition proof",
      "status_when_present": "pass",
      "severity_when_missing": "high",
      "gap_category": "output-contract"
    }
  ],
  "anti_patterns": [
    {
      "id": "implementation-without-route",
      "marker_absent": "Next route",
      "summary": "Output lacks a navigable next route.",
      "severity": "medium",
      "category": "navigation-efficiency"
    }
  ],
  "reflection_overrides": {
    "severe_gap": "reflect-now"
  }
}
```

Profile rules:

- Profiles are hints, not arbitrary code.
- Use marker, regex, field-presence, and count checks only.
- Missing profile is not a failure.
- Profile results become `observer.workflow_gaps`, `observer.anti_pattern_hits`, and `observer.quality_bar_status`.

### L4: Optional AI-Assisted Extraction

Deferred.

Use only when explicitly enabled, bounded, and privacy-safe. The AI observer should read the run bundle and return an observer JSON object, but the deterministic extractor must still validate and sanitize it before append.

## Enriched Envelope Shape

The output envelope should preserve the pending envelope and update only execution/observer fields:

```json
{
  "timestamp": "2026-05-23T00:00:10Z",
  "run_id": "arcanum-hook-<turn-id>",
  "session_id": "<codex-session-id>",
  "capability": {
    "id": "distill",
    "kind": "sigil",
    "tier": "arcana",
    "mode": "skill"
  },
  "skill": {
    "name": "distill",
    "file": ".agents/skills/distill/SKILL.md",
    "domain": "planning-optimization"
  },
  "skill_detection": {
    "source": "explicit-dollar-token",
    "token": "$distill",
    "confidence": "high"
  },
  "execution": {
    "status": "completed",
    "outputs": [
      "framework/observability/development/SKILL-AWARE-OBSERVATION-DISTILL-REVIEW.md"
    ],
    "files_changed": [],
    "validation": [
      "codex UserPromptSubmit hook opened skill observer envelope",
      "codex PostToolUse hook recorded tool evidence",
      "codex Stop hook received final message",
      "derive-invocation-telemetry ran profile checks"
    ],
    "notes": "tool_events=3; tool_failures=0; extraction_mode=profile"
  },
  "observer": {
    "quality_bar_status": "partial",
    "anti_pattern_hits": [],
    "workflow_gaps": [
      {
        "category": "output-contract",
        "severity": "medium",
        "summary": "Could not verify required marker: Closure and recomposition proof",
        "evidence": "telemetry/profile.json quality signal has-recomposition-proof"
      }
    ],
    "output_contract_drift": false,
    "reflection_trigger": "none",
    "recommendation": "targeted-update",
    "closeout_excerpt": "..."
  },
  "target_artifact": ".agents/skills/distill/SKILL.md"
}
```

`files_changed` is empty in this example because the extractor cannot derive changed files deterministically unless tool events prove them.

## Extraction Report Shape

Write diagnostics to `derived-telemetry.json`:

```json
{
  "version": "0.1.0",
  "status": "completed",
  "mode": "profile",
  "inputs": {
    "pending": "pending-envelope.json",
    "tool_events": "tool-events.jsonl",
    "final_message": "final-message.md",
    "skill_profile": ".agents/skills/distill/telemetry/profile.json"
  },
  "derived": {
    "tool_event_count": 3,
    "tool_failure_count": 0,
    "output_count": 1,
    "files_changed_count": 0,
    "workflow_gap_count": 1,
    "anti_pattern_hit_count": 0
  },
  "skipped": [
    {
      "field": "execution.files_changed",
      "reason": "no deterministic write-path evidence"
    }
  ],
  "redactions": []
}
```

## Stop Hook Integration

Current:

```text
Stop hook mutates pending envelope -> envelope.json
Stop hook calls observe-invocation.sh
```

Target:

```text
Stop hook writes final-message.md
Stop hook calls derive-invocation-telemetry.sh
derive-invocation-telemetry.sh writes envelope.json and derived-telemetry.json
Stop hook calls observe-invocation.sh with envelope.json
```

Stop hook remains responsible for reflection routing after `observe-invocation.sh` returns.

## Skill-Local Telemetry Profile Contract

Recommended profile path:

```text
telemetry/profile.json
```

Optional companion docs:

```text
telemetry/README.md
```

Profile fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `version` | yes | Profile schema version. |
| `capability` | yes | Expected capability id. |
| `quality_signals` | no | Output markers or regex checks that support quality status. |
| `anti_patterns` | no | Deterministic checks for known false-success patterns. |
| `workflow_gaps` | no | Named custom gap checks. |
| `reflection_overrides` | no | Optional trigger/recommendation overrides. |

Allowed check types:

- marker present,
- marker absent,
- regex present,
- regex absent,
- output count threshold,
- validation marker present,
- closeout field present.

Disallowed:

- arbitrary shell commands,
- file writes,
- network calls,
- model calls,
- unbounded regex against large files.

## Privacy Rules

- Redact raw request if configured or if it exceeds a safe length.
- Store bounded closeout excerpts only.
- Never store full tool outputs by default.
- Never store secrets, credentials, tokens, or private keys.
- Prefer paths, counts, statuses, and concise evidence strings.

## Failure Policy

| Failure | Behavior |
| --- | --- |
| missing tool events | continue with L0/L2 extraction |
| incomplete tool hook coverage | continue, leave unprovable write-derived fields empty, and record a skipped diagnostic |
| missing final message | mark status partial unless tool failures prove failed |
| invalid skill profile | add observability workflow gap; continue generic extraction |
| extractor internal failure | Stop hook should preserve pending envelope and either skip observation or block in strict mode |
| observer append failure | handled by existing Stop hook and `observe-invocation.sh` behavior |

## Validation Cases

| Case | Expected |
| --- | --- |
| no profile, successful message | status completed, quality fallback pass, no custom gaps |
| profile requires missing marker | workflow gap added, recommendation targeted-update |
| tool failure present | status failed, quality fail, recommendation inspect-run or reflect-now |
| unknown tool schema | counts preserved, no changed files guessed |
| write happened but no write-tool event exists | status can still complete; `files_changed` remains empty unless another deterministic source proves paths |
| redaction enabled | `request.raw` null or redacted, summary preserved |

## Next Route

1. Add `derive-invocation-telemetry.sh`.
2. Update Stop hook to call it before `observe-invocation.sh`.
3. Add a sample `telemetry/profile.json` for `distill`.
4. Add route and extraction fixtures.
