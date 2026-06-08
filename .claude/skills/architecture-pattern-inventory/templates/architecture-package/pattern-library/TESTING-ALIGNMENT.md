# Testing Alignment

Use this document to connect architecture patterns to verification obligations.

## Testing Strategy By Layer

| Layer | Test Type | What It Proves | Evidence |
| ----- | --------- | -------------- | -------- |
| `{layer}` | `{unit/integration/e2e/contract}` | `{claim}` | `{test paths}` |

## Pattern Verification

| Pattern | Required Checks | Existing Evidence | Gaps |
| ------- | --------------- | ----------------- | ---- |
| `{pattern}` | `{checks}` | `{tests}` | `{gaps}` |

## Relationship Verification

| Relationship | Required Checks | Existing Evidence | Gaps |
| ------------ | --------------- | ----------------- | ---- |
| `{relationship}` | `{checks}` | `{tests}` | `{gaps}` |

## Test Gap Signals

- important architecture rule has no test,
- tests assert implementation details across forbidden boundaries,
- repeated pattern has inconsistent test style,
- integration seams are tested only through mocks,
- failure modes are undocumented or untested.
