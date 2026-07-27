# Glossary: Distill Runtime-Event Emission

| Term | Meaning | Status |
| --- | --- | --- |
| runtime event | One non-authoritative role/process evidence record conforming to the accepted Invoke-side schema | existing |
| event ledger | Append-only JSONL sequence for one Distill run | existing |
| runtime emitter | Distill-owned producer that writes one boundary event through the accepted append contract | proposed |
| evidence-gated run | Distill execution whose downstream handoff requires validator-resolvable evidence | proposed |
| evidence-emission status | Producer closeout status: `complete`, `partial`, `failed`, `not-required`, or `not-configured` | proposed |
| execution-evidence status | Whether the request, event, receipt, and validator references are complete, partial, or unavailable | existing |
| telemetry status | Whether Signal Observer recorded the invocation summary | existing |
| direct telemetry | Distill-owned signal with no parent lineage | proposed |
| invoked telemetry | Caller-owned Distill child signal with parent lineage | existing |

## Non-Equivalence Rules

- Runtime events are not usage telemetry.
- Usage telemetry is not a validator result.
- Evidence-emission status is not execution-evidence status.
- No event, receipt, or telemetry row grants mutation authority.
