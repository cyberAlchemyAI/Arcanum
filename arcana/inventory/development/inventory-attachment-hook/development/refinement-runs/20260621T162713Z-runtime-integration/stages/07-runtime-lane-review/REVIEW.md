---
module: inventory-attachment-hook
runId: 20260621T162713Z-runtime-integration
stage: s7-runtime-lane-review
status: flag
updatedAt: 2026-06-21
docType: runtime-lane-review
---

# Runtime Lane Review

## Verdict

`flag`

All runtime lanes accept the shared contract as a pre-implementation design.
None accepts it as completed runtime proof until chat-invoked skill observation
and fallback receipts have fixtures.

## Receipts

### Codex Runtime Lane

| Field | Value |
| --- | --- |
| agent_id | `019eeb39-fdc8-7611-a6d4-a7f960667eb3` |
| role_id | `codex-runtime-lane` |
| status | `flag` |
| shared contract | acceptable with required Codex-lane clarification |

Findings:

- Inventory Attachment must attach to chat-invoked native `.agents/skills/*`
  skill/spell runs.
- Current hook opens envelopes only for `.codex/commands/<name>.md`.
- Add a skill-aware observation bridge for explicit `$skill-name`.
- Legacy command route is prior evidence only, not a compatibility requirement
  or proof target.

### Claude Code Runtime Lane

| Field | Value |
| --- | --- |
| agent_id | `019eeb39-fe7e-7731-99ac-b98a76669075` |
| role_id | `claude-code-runtime-lane` |
| status | `flag` |
| shared contract | acceptable with Claude-lane acceptance gates |

Findings:

- Execute through Claude Code native skills/subagents and
  `.claude/agents/arcanum-stage-worker.md`.
- Do not use VS Code UI or nested model CLIs as evidence.
- Stage worker receipt must include status, artifacts, validation, observer
  status, blockers, and handoff note.
- Claude mirrors must regenerate from canonical `arcanum` sources.
- `WORK-PACK.md` should later name `.claude/skills` and `.claude/agents` in
  generated mirror acceptance.

### Generic Runtime Lane

| Field | Value |
| --- | --- |
| agent_id | `019eeb3a-01a4-74d1-99cd-fbf0534afa9f` |
| role_id | `generic-runtime-lane` |
| status | `flag` |
| shared contract | acceptable with explicit no-native-hook fallback receipt |

Findings:

- Generic runtimes must resolve capability identity, run id, mode, source ref,
  primary result, durable outputs, validation state, and attachment policy.
- Fallback is acceptable only as a managed runtime receipt, not agent memory.
- No-hook execution must mark hook enforcement as fallback/unavailable rather
  than pretending native hook proof exists.
- `.arcanum/runtime/config.json` enables adapters but does not yet declare
  per-host hook availability or fallback policy.

### Runtime Boundary Reviewer

| Field | Value |
| --- | --- |
| agent_id | `019eeb3a-0647-7ac3-be3f-7766d04b81dd` |
| role_id | `runtime-boundary-reviewer` |
| status | `flag` |
| shared contract | acceptable as pre-implementation shared runtime contract |

Findings:

- Canonical/generated discipline is acceptable with guardrails.
- Public/private boundary is acceptable.
- Observability recursion is acceptable in design, not yet implementation proof.
- Chat-invoked skill proof surface is correctly selected, but current direct
  `$skill-name` invocation lacks deterministic bridge.
- VS Code/editor UI deferral is acceptable.

## Convergence

Accepted:

- shared lifecycle and insertion point;
- candidate-only Inventory authority;
- primary-result preservation;
- warn/skip default failure behavior;
- explicit public-boundary and recursion guards;
- VS Code/editor UI deferral.

Flagged:

- direct Codex `$skill-name` observation bridge is not implemented;
- generic no-native-hook fallback receipt schema needs fixture proof;
- Claude lane needs native receipt/wrapper evidence;
- generated mirror acceptance should include Claude surfaces explicitly.

## Design Repair Applied

The parent design was repaired with:

- proof-strength levels in `RUNTIME-INTEGRATION-MODEL.md`;
- no-native-hook fallback receipt schema in `RUNTIME-INTEGRATION-DESIGN.md`;
- Claude lane acceptance gates;
- explicit flag status until fixtures prove chat skill closeout.
