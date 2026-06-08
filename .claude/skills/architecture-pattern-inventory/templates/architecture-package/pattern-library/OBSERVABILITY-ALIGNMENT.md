# Observability Alignment

Use this document to connect architecture patterns to operational signals.

## Signal Strategy By Layer

| Layer | Signals | Purpose | Evidence |
| ----- | ------- | ------- | -------- |
| `{layer}` | `{logs/metrics/traces/events/health}` | `{why it matters}` | `{paths}` |

## Pattern Observability

| Pattern | Expected Signals | Existing Evidence | Gaps |
| ------- | ---------------- | ----------------- | ---- |
| `{pattern}` | `{signals}` | `{paths}` | `{gaps}` |

## Relationship Observability

| Relationship | Expected Signals | Existing Evidence | Gaps |
| ------------ | ---------------- | ----------------- | ---- |
| `{relationship}` | `{signals}` | `{paths}` | `{gaps}` |

## Drift Signals

- critical workflow has no success/failure signal,
- boundary crossing has no trace or event,
- retries or fallbacks are invisible,
- dashboards do not map to architecture concepts,
- operational alerts cannot identify owning layer or pattern.
