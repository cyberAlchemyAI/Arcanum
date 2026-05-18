# Invoke Design Bundle: Observed Invocation Loop Remaining Items

## Source Contracts

| Ref | Source | Role |
| --- | --- | --- |
| RD-001 | `spells/observed-invocation-loop/development/REMAINING-DEFINE-SPEC.md` | approved follow-up define source |
| RD-002 | `framework/observability/scripts/observe-invocation.sh` | append, dedupe, threshold recommendation |
| RD-003 | `framework/observability/scripts/reflect-invocation-signals.sh` | non-mutating reflection report runner |
| RD-004 | `tools/arcanum` | managed command wrapper closeout |
| RD-005 | `.codex/hooks/arcanum-stop.sh` | Codex hook closeout |

## Six Views

### 1. Context View

The remaining work sits inside the existing OIL runtime path. The observer remains the source of telemetry append and recommendation. Managed closeout layers execute reflection policy because they know whether the invocation is a full managed run and can preserve the primary result.

### 2. High-Level Structure View

| Component | Responsibility |
| --- | --- |
| Generic observer | Validate envelope, append telemetry, update counters, emit recommendation. |
| Dedupe recorder | Check duplicate keys before append and commit keys only after success. |
| Reflection runner | Analyze scoped signal ledger and write non-mutating reports. |
| Managed command wrapper | Honor `OBSERVED_REFLECT` after observer closeout. |
| Codex Stop hook | Close hook envelope, derive status, and honor `OBSERVED_REFLECT`. |
| Migration check | Verify legacy rows summarize through capability fallback. |

### 3. Low-Level Components View

| Component | Inputs | Outputs |
| --- | --- | --- |
| `record-hook-operation.sh` | hook action, dedupe key, dedupe mode | hook row and optional committed dedupe key |
| `observe-invocation.sh` | envelope and observability dir | ledger row, indexes, counters, recommendation |
| `reflect-invocation-signals.sh` | ledger, state, optional scope | reflection report and updated `last_reflection_at` |
| `tools/arcanum` reflection closeout | observer output and env controls | reflection status fields |
| Stop hook reflection closeout | observer output and env controls | hook additional context and reflection output file |
| `check-observability-migration.sh` | ledger | anonymous-group migration result |

### 4. Workflow Process View

1. Managed invocation writes or closes an envelope.
2. Observer checks dedupe without committing it.
3. Observer evaluates thresholds against signals since `last_reflection_at`, with severe gaps evaluated from the current event.
4. Observer appends ledger row, writes indexes, updates counters, then commits dedupe.
5. Managed closeout checks `OBSERVED_REFLECT`.
6. If enabled and recommended, closeout calls `reflect-invocation-signals.sh`.
7. Reflection report updates `last_reflection_at`, cooling ordinary thresholds.
8. Closeout returns primary result plus observation and reflection status.

### 5. Decision Flow View

| Decision | Rule |
| --- | --- |
| Should reflection run? | `off` never runs, `auto` runs on `reflect-now`, `always` runs regardless and may skip with reason. |
| Should threshold trigger? | Count ordinary thresholds since last reflection; severe-gap checks current event immediately. |
| Should dedupe suppress? | Suppress only committed dedupe keys. |
| What status should Stop report? | Tool failure means failed; existing blocked/interrupted/partial is preserved unless final assistant output supports completion. |
| Can legacy rows summarize? | Use `capability.id/kind` when present, otherwise `sigil` and default kind fallback. |

### 6. Dependency Interface View

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| `OBSERVED_REFLECT` | environment | wrappers/hooks | `off`, `auto`, or `always`; default `auto` |
| observer machine output | observer | wrappers/hooks | `OBSERVATION`, `REFLECTION_TRIGGER`, `RECOMMENDATION`, `DEDUPE_KEY` |
| reflection machine output | reflector | wrappers/hooks | `REFLECTION`, `REASON`, `SIGNALS_ANALYZED`, `REPORT`, `STATE` |
| migration summary | migration check | maintainers/validation | no anonymous capability groups |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Reflection report loops on same threshold. | Noise and stale reports. | Scope analysis since `last_reflection_at`. |
| Dedupe check rows look like signal emissions. | Confusing hook operations. | Append commit row is the authoritative emitted-signal row. |
| Hook status inference misses a runtime failure. | Over-optimistic telemetry. | Prefer explicit tool failure and preserved pending status over blind completion. |
| Legacy rows remain mixed-shape. | Summary drift. | Migration check validates fallback grouping. |

## Design Result

- Phase status: pass
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Implementation layering: L0 reflection route, L1 threshold scoping, L2 atomic dedupe, L3 status and migration
- Work-pack: required
- Next route: plan
