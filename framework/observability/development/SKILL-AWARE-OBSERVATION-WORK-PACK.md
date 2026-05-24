# WORK-PACK: Skill-Aware Observation Bridge

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | flag-ready-for-L0-L3 | Architecture and planning are coherent enough to start bounded implementation, but the feature is not release-ready until derivation, observer preservation, route regression, and docs sync pass. |
| complexity | high | Touches hook runtime behavior, telemetry derivation, observability schema usage, delayed feedback attribution, docs, and tests/manual fixtures. |
| outputMode | single-file | Scope is navigable without split task files. |
| executionPackRef | n/a | Not required for this medium-small repository-local change. |
| layeringArtifactRef | [SKILL-AWARE-OBSERVATION-LAYERING.md](SKILL-AWARE-OBSERVATION-LAYERING.md) | Layer decisions. |
| activeLayerWindow | L0-L3 | Implement detection, derivation, append, and regression checks before delayed feedback or optional CLI helpers. |
| lastUpdatedAt | 2026-05-23 | Created by invoke plan. |
| readinessProfile | pilot | Target is repository-local deterministic observability. |
| refinementReviewRef | [SKILL-AWARE-OBSERVATION-FULL-REFINEMENT.md](SKILL-AWARE-OBSERVATION-FULL-REFINEMENT.md) | Full iterative refinement verdict and repair notes. |

## Objective Summary

- Objective: make explicit Codex skill invocations such as `$distill` deterministic observability subjects.
- Primary inputs: [SKILL-AWARE-OBSERVATION-DESIGN.md](SKILL-AWARE-OBSERVATION-DESIGN.md), [../ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md), `.codex/hooks/arcanum-*.sh`.
- Success condition: a synthetic `$skill-name` hook flow opens a valid envelope, derives meaningful telemetry, calls `observe-invocation.sh`, and preserves command-route behavior.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-OBS-001 | Explicit skill detection opens pending envelopes. | L0 | W0 | Existing `.agents/skills` symlinks. | Synthetic `UserPromptSubmit` JSON creates pending envelope for `$distill`. |
| S-OBS-002 | Stop hook derives meaningful telemetry before append. | L1 | W1 | S-OBS-001. | `derive-invocation-telemetry.sh` writes enriched `envelope.json` and `derived-telemetry.json`. |
| S-OBS-003 | Generic observer preserves enriched skill telemetry. | L2 | W1 | S-OBS-002. | Ledger row includes `skill`, `skill_detection`, derived execution fields, and observer gaps. |
| S-OBS-004 | Route regression coverage protects command behavior and false positives. | L3 | W2 | S-OBS-001, S-OBS-002, S-OBS-003. | `/invoke` still opens command envelope; `$UNKNOWN` produces `{}`. |
| S-OBS-005 | Documentation reflects skill-aware derivation and observability boundaries. | L3 | W2 | S-OBS-002. | README and architecture overview agree on detection, derivation, append, and continuation feedback limits. |
| S-OBS-006 | Continuation feedback attribution links later corrections. | L4 | W3 | S-OBS-003. | Next-turn correction writes linked continuation feedback event. |
| S-OBS-007 | Optional skill-aware `tools/arcanum` diagnostics. | L5 | W4 | S-OBS-004. | `tools/arcanum --list-skills` and `--resolve-skill` work if implemented. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-OBS-001 | Add explicit skill route detection to UserPromptSubmit hook. | L0 | medium | W0 | [SKILL-AWARE-OBSERVATION-DESIGN.md](SKILL-AWARE-OBSERVATION-DESIGN.md) | ready | not-started |
| TASK-OBS-002 | Add derive invocation telemetry component and Stop hook integration. | L1 | high | W1 | [DERIVE-INVOCATION-TELEMETRY-DESIGN.md](DERIVE-INVOCATION-TELEMETRY-DESIGN.md) | ready-after-TASK-OBS-001 | not-started |
| TASK-OBS-003 | Preserve enriched skill telemetry in observer normalization. | L2 | medium | W1 | [../scripts/observe-invocation.sh](../scripts/observe-invocation.sh) | ready-after-TASK-OBS-002 | not-started |
| TASK-OBS-004 | Add route regression fixtures or documented validation commands. | L2 | medium | W2 | `.codex/hooks/`, `.agents/skills/` | ready-after-TASK-OBS-002-and-TASK-OBS-003 | not-started |
| TASK-OBS-005 | Refresh docs for skill-aware observability boundaries. | L3 | low | W2 | [../ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md) | ready-after-TASK-OBS-004 | not-started |
| TASK-OBS-006 | Design and optionally pilot continuation feedback attribution. | L4 | medium | W3 | [CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md](CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md) | deferred-until-derive-proven | not-started |
| TASK-OBS-007 | Add optional `tools/arcanum` skill diagnostics. | L5 | low | W4 | [../../../tools/arcanum](../../../tools/arcanum) | deferred | not-started |
| TASK-VERIFY | Completion verification and closeout. | L2 | low | W2 | this work-pack | ready-after-implementation | not-started |

## Implementation Detail Specs

### TASK-OBS-001: UserPromptSubmit Skill Detection

Purpose:

- Extend `.codex/hooks/arcanum-user-prompt-submit.sh` so explicit `$skill-name` prompts open observer envelopes.

Inputs:

- Hook JSON from Codex with `.prompt`, `.turn_id`, `.session_id`.
- `.agents/skills/<skill-name>/SKILL.md`.

Implementation rules:

1. Preserve current command detection as the first route.
2. Add a skill route only when command detection does not match.
3. Extract an explicit skill token from accepted prompt forms:
   - first token `$skill-name`,
   - near-start `use $skill-name`,
   - markdown display token `[$skill-name](...)`.
4. Strip leading `$` and reject names containing characters outside `[A-Za-z0-9._-]`.
5. Resolve `.agents/skills/<name>/SKILL.md`.
6. Extract simple frontmatter values for `name`, `description`, `tier`, and `domain`.
7. Classify capability:
   - tier `arcana|formulae|transmutations` -> kind `sigil`,
   - resolved path under `spells/` -> kind `spell`,
   - otherwise kind `skill`, tier `runtime`.
8. Write pending envelope using `mode: "skill"` and `target_artifact: ".agents/skills/<name>/SKILL.md"`.
9. Include `skill_detection` metadata.

Edge cases:

- Unknown skill token returns `{}` and does not create a run directory.
- Prompt with `/invoke ... $distill` uses command route only.
- Missing frontmatter does not block envelope creation when `SKILL.md` exists.

Validation:

```bash
printf '{"prompt":"$distill explain this","turn_id":"skill-test-001","session_id":"manual-test"}' \
  | .codex/hooks/arcanum-user-prompt-submit.sh
test -f .arcanum/observability/runs/arcanum-hooks/arcanum-hook-skill-test-001/pending-envelope.json
jq -e '.capability.id == "distill" and .capability.mode == "skill"' \
  .arcanum/observability/runs/arcanum-hooks/arcanum-hook-skill-test-001/pending-envelope.json
```

### TASK-OBS-002: Derive Invocation Telemetry

Purpose:

- Add `derive-invocation-telemetry.sh` and update Stop hook so raw run evidence becomes meaningful telemetry before append.

Implementation rules:

1. Stop hook writes the final assistant message to `<run-dir>/final-message.md`.
2. Stop hook calls `framework/observability/scripts/derive-invocation-telemetry.sh`.
3. The derivation script reads pending envelope, tool events, final message, and optional skill telemetry profile.
4. The derivation script writes enriched `envelope.json` and `derived-telemetry.json`.
5. Stop hook calls `observe-invocation.sh` only after derivation succeeds or degrades safely.
6. Preserve strict mode behavior and reflection routing behavior.

Validation:

```bash
printf '{"turn_id":"skill-test-001","last_assistant_message":"Skill run completed."}' \
  | .codex/hooks/arcanum-stop.sh
test -f .arcanum/observability/runs/arcanum-hooks/arcanum-hook-skill-test-001/derived-telemetry.json
jq -e 'select(.capability.id == "distill" and .capability.mode == "skill")' \
  .arcanum/observability/signals/sigil-invocations.jsonl >/dev/null
```

### TASK-OBS-003: Observer Skill Telemetry Preservation

Purpose:

- Preserve optional skill-specific metadata when `observe-invocation.sh` normalizes a closed envelope into the central ledger event.

Implementation rules:

1. Preserve `.skill` when present.
2. Preserve `.skill_detection` when present.
3. Do not require these fields for command or legacy sigil envelopes.
4. Do not duplicate the full `SKILL.md` body or large descriptions; keep compact metadata only.
5. Keep `target_artifact` as the navigable skill path.
6. Preserve derived `observer.workflow_gaps`, `observer.anti_pattern_hits`, and `execution.outputs`.

Validation:

```bash
jq -e '
  select(.capability.id == "distill"
    and .capability.mode == "skill"
    and .skill.file == ".agents/skills/distill/SKILL.md"
    and .skill_detection.source == "explicit-dollar-token")
' .arcanum/observability/signals/sigil-invocations.jsonl >/dev/null
```

### TASK-OBS-004: Route Regression Fixtures

Purpose:

- Protect command route behavior, skill route behavior, and false-positive behavior.

Required cases:

| Case | Prompt | Expected |
| --- | --- | --- |
| command | `/invoke define x` | command envelope for `invoke` |
| skill first token | `$distill x` | skill envelope for `distill` |
| skill phrase | `use $experiment-harness to validate x` | skill envelope for `experiment-harness` |
| markdown skill | `[$invoke](path) run design` | skill envelope for `invoke` if skill installed, otherwise no envelope |
| unknown token | `$NOT_A_SKILL x` | no envelope |
| mixed route | `/invoke with $distill` | command envelope for `invoke` |

Validation:

- Use temp or unique `turn_id` values to avoid dedupe collisions.
- Check pending envelope before Stop closeout.
- Check ledger append or dedupe closeout after Stop.
- Treat missing `PostToolUse` write evidence as an expected degraded case; route regression must verify hook routing and ledger fields, not complete changed-file capture.

### TASK-OBS-005: Documentation Refresh

Purpose:

- Keep the architecture docs aligned with implementation.

Docs to update:

- [../ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md)
- [../SIGIL-OBSERVABILITY-HOOK.md](../SIGIL-OBSERVABILITY-HOOK.md)
- [../README.md](../README.md)
- [../../../spells/observed-invocation-loop/README.md](../../../spells/observed-invocation-loop/README.md)

Required content:

- explicit `$skill-name` detection is deterministic,
- implicit skill selection remains deferred,
- `.agents/skills` is the skill discovery surface,
- `.codex/commands` remains compatibility.

### TASK-OBS-006: Continuation Feedback Attribution

Purpose:

- Capture useful quality signals that arrive in the user's next one or two prompts after a run has already closed.

Implementation rules:

1. After observed runs, write or update `.arcanum/observability/active-run-context.json`.
2. On later prompt submit, classify obvious correction, clarification, continuation, route miss, or unrelated fresh work.
3. Link high-confidence continuation feedback to the prior `run_id`.
4. Start with a separate `signals/continuation-feedback.jsonl` ledger.
5. If `.arcanum/necronomicon/` exists, mirror a compact gap entry to Necronomicon session state in a later slice.

Status:

- Deferred until derivation and append are proven.

### TASK-OBS-007: Optional `tools/arcanum` Skill Diagnostics

Purpose:

- Make `tools/arcanum` useful in a skill-first architecture without making it the canonical skill runtime.

Potential commands:

```text
tools/arcanum --list-skills
tools/arcanum --resolve-skill distill
tools/arcanum --print-skill-prompt distill <request>
```

Status:

- Deferred until hook bridge works.

## SWU Execution Handoff

| SWU ID | Parent Task | Source | Dependencies | Write Scope | Done Criteria | Validation | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-OBS-001 | TASK-OBS-001 | design + hook script | none | `.codex/hooks/arcanum-user-prompt-submit.sh` | Explicit skill route creates pending envelope. | synthetic hook input + jq checks | local-fallback | ready |
| SWU-OBS-002 | TASK-OBS-002 | derive design + Stop hook | SWU-OBS-001 | `framework/observability/scripts/derive-invocation-telemetry.sh`, `.codex/hooks/arcanum-stop.sh` | Stop hook derives enriched envelope before append. | derived report + ledger query | local-fallback | ready-after-SWU-OBS-001 |
| SWU-OBS-003 | TASK-OBS-003 | observer script | SWU-OBS-002 | `framework/observability/scripts/observe-invocation.sh` | Ledger preserves `skill`, `skill_detection`, and derived observer fields. | ledger query above | local-fallback | ready-after-SWU-OBS-002 |
| SWU-OBS-004 | TASK-OBS-004 | route matrix | SWU-OBS-001, SWU-OBS-002, SWU-OBS-003 | validation docs or test fixture script | Route matrix passes. | manual commands or fixture script | local-fallback | ready-after-SWU-OBS-003 |
| SWU-OBS-005 | TASK-OBS-005 | docs listed above | SWU-OBS-004 | `framework/observability/*.md`, `spells/observed-invocation-loop/README.md` | Docs reflect implemented boundary. | review links and grep for stale command-only claim | local-fallback | ready-after-SWU-OBS-004 |
| SWU-OBS-006 | TASK-OBS-006 | continuation design | SWU-OBS-003 | `.arcanum/observability/active-run-context.json`, optional feedback ledger | Later corrections can link to prior run. | synthetic next-turn correction creates feedback candidate | local-fallback | deferred |
| SWU-OBS-007 | TASK-OBS-007 | `tools/arcanum` | SWU-OBS-004 | `tools/arcanum` | Skill diagnostics work. | `tools/arcanum --list-skills` | local-fallback | deferred |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-OBS-001 | implicit skill use | Codex does not expose structured skill-use metadata to these hooks. | platform/runtime | Defer implicit observation; observe explicit `$skill-name` only. | n/a |

## Gate Checks

1. `/command` route regression passes.
2. `$skill-name` route creates a pending envelope only for installed skills.
3. Stop hook records skill-mode telemetry with `capability.mode = "skill"`.
4. Derive script runs before append and writes `derived-telemetry.json`.
5. Unknown `$TOKEN` does not create telemetry.
6. `observe-invocation.sh` remains the single append authority.
7. Docs state that implicit skill use is deferred.
8. Later user corrections are represented as continuation feedback, not retroactive mutation of the old invocation row.

## Next Route

- `task-session` for SWU-OBS-001 through SWU-OBS-005, one SWU at a time.
- Defer SWU-OBS-006 and SWU-OBS-007 until derivation and append are proven.
