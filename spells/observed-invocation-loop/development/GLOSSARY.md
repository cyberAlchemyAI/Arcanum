# Glossary: Observed Invocation Loop

| Term | Definition | Status |
| --- | --- | --- |
| Arcanum-managed invocation | A skill, sigil, or spell run through an Arcanum adapter, orchestrator, wrapper, or generated command. | linked |
| Invocation envelope | Safe structured summary of a completed, blocked, or failed capability run. | linked |
| Capability telemetry | One append-only JSONL signal describing behavior, quality, validation, and reflection recommendation for a capability invocation. | linked |
| Hook operation | Operational audit row for observer or hook mechanics. It is not capability telemetry. | linked |
| Central signal ledger | `.arcanum/observability/signals/sigil-invocations.jsonl`. | linked |
| Reflection state | `.arcanum/observability/reflection-state.json`, storing counters since last reflection. | linked |
| Reflection threshold | Configured count or severity rule that turns accumulated signals into `reflect-now`. | linked |
| Dedupe key | Stable key preventing repeated telemetry appends for the same run and observer version. | linked |
| Strict telemetry mode | Runtime policy where failure to append telemetry blocks the spell result. | candidate |

