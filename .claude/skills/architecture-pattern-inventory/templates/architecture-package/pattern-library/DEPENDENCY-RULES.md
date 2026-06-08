# Dependency Rules

Use this document to record import, call, data-flow, and runtime dependency constraints.

## Dependency Direction

| From | May Depend On | Must Not Depend On | Enforcement |
| ---- | ------------- | ------------------ | ----------- |
| `{layer or module}` | `{allowed targets}` | `{forbidden targets}` | `{lint/test/review/manual}` |

## Boundary Contracts

| Boundary | Contract | Evidence | Verification |
| -------- | -------- | -------- | ------------ |
| `{boundary}` | `{what crosses and how}` | `{paths}` | `{check}` |

## Import Rules

| Rule | Rationale | Example Allowed | Example Blocked |
| ---- | --------- | --------------- | --------------- |
| `{rule}` | `{why}` | `{example}` | `{example}` |

## Drift Signals

Record signals that suggest dependency drift:

- unexpected import direction,
- duplicated boundary logic,
- runtime calls bypassing an interface,
- tests that require forbidden internals,
- shared types leaking across ownership boundaries.
