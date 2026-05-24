# Skill-Aware Observation Bridge Design

## Invoke Design Context

- Mode: design
- Target artifact: Arcanum observability package
- Design objective: add deterministic observability for explicit Codex skill invocations such as `$distill`.
- Source architecture: [ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md)
- Primary runtime surface: `.agents/skills/<skill-name>/SKILL.md`
- Compatibility runtime surface: `.codex/commands/<command>.md`
- Observer authority: `framework/observability/scripts/observe-invocation.sh`
- Telemetry derivation: [DERIVE-INVOCATION-TELEMETRY-DESIGN.md](DERIVE-INVOCATION-TELEMETRY-DESIGN.md)
- Delayed feedback attribution: [CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md](CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md)
- Phase status: flag-ready-for-L0-L3; architecture is coherent, but feature readiness still depends on derivation, observer preservation, route regression, and docs sync.

## 1. Context View

Arcanum has shifted toward Codex repository skills under `.agents/skills/`, but the deterministic observability bridge still primarily watches `.codex/commands/`.

The current command path is deterministic:

1. `UserPromptSubmit` detects `/command`.
2. It resolves `.codex/commands/<command>.md`.
3. It opens a pending envelope under `.arcanum/observability/runs/arcanum-hooks/`.
4. `PostToolUse` records tool evidence.
5. `Stop` closes the envelope and calls `observe-invocation.sh`.

The direct skill path is not equally deterministic yet:

1. User invokes `$skill-name`.
2. Codex loads `.agents/skills/<skill-name>/SKILL.md`.
3. No current hook opens a skill envelope unless a legacy command is also present.

The design goal is to extend the existing hook pipeline to explicit skill invocations without creating a second observer system.

## 2. High-Level Structure View

```text
User prompt
  |
  v
.codex/hooks/arcanum-user-prompt-submit.sh
  |
  |-- command route: /invoke -> .codex/commands/invoke.md
  |
  |-- skill route: $distill -> .agents/skills/distill/SKILL.md
  |
  v
pending-envelope.json
  |
  v
.codex/hooks/arcanum-post-tool-use.sh
  |
  v
.codex/hooks/arcanum-stop.sh
  |
  v
framework/observability/scripts/derive-invocation-telemetry.sh
  |
  v
framework/observability/scripts/observe-invocation.sh
  |
  v
.arcanum/observability/signals/sigil-invocations.jsonl
```

The command route remains unchanged. The skill route uses the same pending envelope and Stop-hook closeout. Before append, `derive-invocation-telemetry.sh` enriches the envelope from tool events, final message, and optional skill-local telemetry profiles.

Tool evidence is partial by design. Codex hook coverage can vary by tool handler, especially around filesystem writes, so `PostToolUse` evidence must improve telemetry when present without becoming the only proof path. The bridge must tolerate empty `tool-events.jsonl` or missing changed-file evidence and still close a truthful envelope.

## 3. Low-Level Components View

### Skill Detection

Add deterministic explicit-skill detection to `arcanum-user-prompt-submit.sh`.

Accepted forms:

- `$skill-name` as the first meaningful token,
- `use $skill-name ...` near the beginning of the prompt,
- Markdown-link style skill references where the display text starts with `$`, such as `[$invoke](...)`.

Rejected forms:

- arbitrary `$VARIABLE` tokens not resolving to `.agents/skills/<name>/SKILL.md`,
- implicit skill usage with no explicit `$skill-name` token,
- unknown skill names.

### Skill Resolution

Resolve against:

```text
.agents/skills/<skill-name>/SKILL.md
```

Resolution must follow symlinks naturally through the filesystem but store the repository-facing `.agents/skills/...` path in the envelope for navigability.

### Frontmatter Extraction

Read only simple YAML frontmatter fields:

- `name`
- `description`
- `tier`
- `domain`

Minimum implementation can use shell-safe line extraction because current Arcanum `SKILL.md` frontmatter is simple key-value metadata. If frontmatter parsing grows more complex, route that to a later parser-hardening task.

### Capability Classification

Classification rule:

| Evidence | capability.kind | capability.tier |
| --- | --- | --- |
| `tier: arcana`, `formulae`, or `transmutations` | `sigil` | tier value |
| canonical path under `spells/` | `spell` | `spell` |
| no Arcanum tier/path evidence | `skill` | `runtime` |

Because `.agents/skills/*` may be symlinked, classification should prefer frontmatter tier first and canonical resolved path second.

### Envelope Shape

Skill route pending envelope should preserve the existing observer schema:

```json
{
  "sigil": "distill",
  "tier": "arcana",
  "mode": "skill",
  "capability": {
    "id": "distill",
    "kind": "sigil",
    "tier": "arcana",
    "mode": "skill",
    "alias": null
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
  "target_artifact": ".agents/skills/distill/SKILL.md"
}
```

The `sigil` field stays for legacy compatibility with the central observer. New consumers should use `capability`.

## 4. Workflow Process View

1. User submits a prompt.
2. `arcanum-user-prompt-submit.sh` tries command detection first for backwards compatibility.
3. If no command matches, it tries explicit skill detection.
4. If a skill token is found, the hook resolves `.agents/skills/<name>/SKILL.md`.
5. If the skill file exists, the hook extracts frontmatter and builds a pending envelope.
6. `arcanum-post-tool-use.sh` records tool events when a pending envelope exists.
7. `arcanum-stop.sh` writes the final assistant message into the run bundle.
8. `derive-invocation-telemetry.sh` reads the pending envelope, tool events, final message, and optional skill-local telemetry profile, then writes an enriched `envelope.json`.
9. `observe-invocation.sh` validates, normalizes, dedupes, appends, indexes, updates counters, and emits closeout fields.
10. A later continuation-feedback layer can attribute the user's next-turn corrections back to the linked run when the useful signal appears after closeout.

## 4A. Telemetry Data Contract

The skill-aware bridge records **run metadata and behavioral signals**, not full conversation memory. Telemetry must be enough to answer:

- what capability was invoked,
- why it was invoked,
- whether it completed,
- what evidence it produced,
- whether observation found quality, workflow, or contract issues,
- whether reflection should run.

### Capture Points

| Phase | File | Captured Data | Purpose |
| --- | --- | --- | --- |
| prompt submit | `pending-envelope.json` | timestamp, run id, session id, skill token, skill path, capability metadata, request summary/raw prompt | Open an auditable run boundary. |
| tool use | `tool-events.jsonl` | tool name, tool input, tool response metadata, failure state when hook events are available | Preserve execution evidence for closeout without assuming complete write coverage. |
| stop | `final-message.md` | bounded final assistant output | Preserve closeout evidence for derivation. |
| derive | `envelope.json`, `derived-telemetry.json` | final status, validation notes, output references, workflow gaps, anti-pattern hits, quality status | Convert raw run evidence into observer-ready telemetry. |
| observe | `signals/sigil-invocations.jsonl` | normalized capability event with observer status and recommendation | Central source of truth for capability behavior. |
| observe | `by-sigil/*.jsonl`, `by-capability/*/*.jsonl` | compact references to central ledger rows | Rebuildable lookup indexes. |
| observe | `reflection-state.json` | counters by repository, sigil, and capability | Threshold-backed reflection routing. |
| observe | `hooks/hook-operations.jsonl`, `hooks/dedupe.jsonl` | observer operation status and dedupe keys | Infrastructure audit trail, not capability telemetry. |

### Pending Envelope Fields

The UserPromptSubmit hook should create:

```json
{
  "timestamp": "2026-05-23T00:00:00Z",
  "run_id": "arcanum-hook-<turn-id>",
  "session_id": "<codex-session-id>",
  "sigil": "distill",
  "tier": "arcana",
  "mode": "skill",
  "capability": {
    "id": "distill",
    "kind": "sigil",
    "tier": "arcana",
    "mode": "skill",
    "alias": null
  },
  "skill": {
    "name": "distill",
    "file": ".agents/skills/distill/SKILL.md",
    "domain": "planning-optimization",
    "description": "Use when optimizing a model, architecture, design, implementation plan, or workflow..."
  },
  "skill_detection": {
    "source": "explicit-dollar-token",
    "token": "$distill",
    "confidence": "high"
  },
  "request": {
    "raw": "$distill analyze this architecture",
    "summary": "Codex skill distill",
    "intent": "$distill analyze this architecture"
  },
  "execution": {
    "status": "partial",
    "outputs": [],
    "files_changed": [],
    "validation": ["codex UserPromptSubmit hook opened skill observer envelope"],
    "notes": "pending skill closeout"
  },
  "observer": {
    "quality_bar_status": "partial",
    "anti_pattern_hits": [],
    "workflow_gaps": [],
    "output_contract_drift": false,
    "reflection_trigger": "none",
    "recommendation": "pending-closeout"
  },
  "target_artifact": ".agents/skills/distill/SKILL.md"
}
```

### Final Ledger Event Fields

`derive-invocation-telemetry.sh` produces the enriched envelope. `observe-invocation.sh` then normalizes that envelope into one ledger event. The implementation must preserve optional skill-specific telemetry from the pending envelope; otherwise the final ledger can prove that a capability ran in `mode: "skill"` but loses how the skill route was detected.

```json
{
  "timestamp": "2026-05-23T00:00:10Z",
  "run_id": "arcanum-hook-<turn-id>",
  "session_id": "<codex-session-id>",
  "sigil": "distill",
  "tier": "arcana",
  "mode": "skill",
  "capability": {
    "id": "distill",
    "kind": "sigil",
    "tier": "arcana",
    "mode": "skill",
    "alias": null
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
  "request": {
    "raw": "$distill analyze this architecture",
    "summary": "Codex skill distill",
    "intent": "$distill analyze this architecture"
  },
  "execution": {
    "status": "completed",
    "outputs": ["framework/observability/development/SKILL-AWARE-OBSERVATION-DESIGN.md"],
    "files_changed": ["framework/observability/development/SKILL-AWARE-OBSERVATION-DESIGN.md"],
    "validation": [
      "codex UserPromptSubmit hook opened skill observer envelope",
      "codex PostToolUse hook recorded tool evidence when available",
      "codex Stop hook closed observer envelope"
    ],
    "notes": "tool_events=3; tool_failures=0"
  },
  "observer": {
    "quality_bar_status": "pass",
    "anti_pattern_hits": [],
    "workflow_gaps": [],
    "output_contract_drift": false,
    "reflection_trigger": "none",
    "recommendation": "none"
  },
  "target_artifact": ".agents/skills/distill/SKILL.md",
  "dedupe_key": "arcanum-hook-<turn-id>:signal-observer:0.1.0",
  "observer_version": "0.1.0"
}
```

`execution.outputs` and `execution.files_changed` should only name paths or summaries that the hook can derive from deterministic tool evidence or explicit safe closeout metadata. If the hook cannot derive changed files deterministically, keep `files_changed: []` rather than guessing from the final assistant message. Missing write-tool events are a degraded evidence condition, not an implementation failure by themselves.

### Derived Index Event

Indexes store references, not full duplicate telemetry:

```json
{
  "timestamp": "2026-05-23T00:00:10Z",
  "run_id": "arcanum-hook-<turn-id>",
  "session_id": "<codex-session-id>",
  "dedupe_key": "arcanum-hook-<turn-id>:signal-observer:0.1.0",
  "ledger": "signals/sigil-invocations.jsonl",
  "line": 42,
  "sigil": "distill",
  "capability": {
    "id": "distill",
    "kind": "sigil",
    "tier": "arcana",
    "mode": "skill",
    "alias": null
  },
  "execution_status": "completed",
  "reflection_trigger": "none",
  "recommendation": "none",
  "target_artifact": ".agents/skills/distill/SKILL.md"
}
```

### Reflection Counters

Each recorded event updates counters such as:

- `meaningful_executions`,
- `generated_outputs`,
- `related_workflow_gaps`,
- `severe_workflow_gaps`,
- `quality_bar_failures`,
- `output_contract_drift_events`,
- per-sigil counters under `by_sigil`,
- per-capability counters under `by_capability`.

### What Must Not Be Stored

- secrets, credentials, tokens, or private keys,
- large raw conversation excerpts,
- full generated files,
- full tool outputs unless already safe and intentionally summarized,
- hook operation rows in the capability ledger.

The telemetry should prefer summaries, file paths, status values, counts, and compact gap evidence. Raw request text may be stored only when it is short and safe; otherwise set `request.raw` to `null` or a redacted excerpt and preserve `request.summary`.

### Later Feedback Telemetry

Some of the most valuable quality signals appear only after the run, when the user corrects, clarifies, or redirects in the next one or two prompts. That signal does not belong in the original closeout envelope because it did not exist yet.

Continuation feedback attribution handles this later evidence:

```text
observed run closes
  -> active-run-context.json points to the recent run
next user turn arrives
  -> classify correction / clarification / continuation / route miss
  -> link feedback to prior run_id
  -> append continuation-feedback event
```

The detailed design lives in [CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md](CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md).

## 5. Decision Flow View

```text
Does first explicit route match .codex/commands?
  yes -> use existing command envelope
  no
    |
    v
Does prompt contain an explicit $skill-name route?
  no -> no Arcanum envelope; return {}
  yes
    |
    v
Does .agents/skills/<skill-name>/SKILL.md exist?
  no -> no Arcanum envelope; return {}
  yes
    |
    v
Can basic frontmatter be read?
  yes -> classify from metadata
  no -> classify as kind=skill, tier=runtime, flag metadata gap in envelope notes
```

Command detection wins when a prompt starts with a legacy `/command`; this avoids changing existing slash behavior.

## 6. Dependency Interface View

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| `.agents/skills/<name>/SKILL.md` | Codex skill install/symlink layer | UserPromptSubmit hook | Must contain readable `SKILL.md`; simple frontmatter preferred. |
| `pending-envelope.json` | UserPromptSubmit hook | PostToolUse and Stop hooks | Must match required observer fields enough for Stop hook to close. |
| `tool-events.jsonl` | PostToolUse hook | Stop hook and human diagnostics | One JSON object per observed tool event. |
| `envelope.json` | Stop hook | `observe-invocation.sh` | Must include timestamp, capability, mode, request, execution, observer fields. |
| `sigil-invocations.jsonl` | `observe-invocation.sh` | `workflow-reflect`, indexes, maintainers | Central source of truth. |

## Design Decisions

| Decision | Outcome | Rationale |
| --- | --- | --- |
| D-OBS-001 | Observe explicit `$skill-name` only. | Hooks cannot reliably know implicit skill selection without platform metadata. |
| D-OBS-002 | Reuse `observe-invocation.sh`. | Prevents a second telemetry append authority. |
| D-OBS-003 | Keep `.codex/commands` route first. | Preserves existing slash-command behavior and compatibility telemetry. |
| D-OBS-004 | Store `.agents/skills/.../SKILL.md` as `target_artifact`. | Makes skill-native runs navigable. |
| D-OBS-005 | Use simple frontmatter extraction for L0/L1. | Current skill metadata is simple; parser hardening can be deferred until needed. |
| D-OBS-006 | Preserve `skill` and `skill_detection` in the normalized ledger event. | Keeps final telemetry explainable after pending envelopes are compacted or removed. |
| D-OBS-007 | Do not infer changed files from assistant prose. | Keeps deterministic telemetry separate from narrative closeout. |
| D-OBS-008 | Split derivation from append. | Keeps semantic extraction in `derive-invocation-telemetry.sh` and deterministic ledger mutation in `observe-invocation.sh`. |
| D-OBS-009 | Attribute later user corrections as continuation feedback, not as original closeout evidence. | Captures quality signals that only become visible after the skill run is over. |

## Risks And Guardrails

| Risk | Guardrail |
| --- | --- |
| False positive `$VARIABLE` detection | Only open envelopes for tokens that resolve to `.agents/skills/<name>/SKILL.md`. |
| Duplicate observation for prompts containing both `/command` and `$skill` | Command route wins; skill route runs only when no command matched. |
| Symlink path confusion | Store repo-facing `.agents/skills/...` path; use resolved path only for classification fallback. |
| Frontmatter parsing misses quoted values | Treat missed metadata as non-blocking and classify as `skill/runtime`; parser hardening is a later task. |
| Implicit skill usage remains unobserved | Document as a known limitation until Codex exposes structured skill-use metadata. |

## Glossary Consistency

| Term | Meaning In This Design |
| --- | --- |
| Skill surface | `.agents/skills/<name>/SKILL.md`, the current Codex discovery path. |
| Command surface | `.codex/commands/<name>.md`, the legacy slash-command adapter path. |
| Observer authority | `observe-invocation.sh`, the single script that appends capability telemetry. |
| Explicit skill route | A user prompt containing `$skill-name` or equivalent markdown skill token. |
| Implicit skill route | Codex selects a skill based on description without a visible `$skill-name` token. Deferred. |

## Handoff To Plan

Recommended next route: invoke plan.

Required plan outputs:

- implementation layering artifact,
- work-pack with task/SWU boundaries,
- validation strategy for hook detection, envelope shape, and observer append,
- migration note for docs that still describe command-first observability.
