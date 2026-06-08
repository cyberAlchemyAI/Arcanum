# Business System Bridge

## Scope

- Repository: {repository}
- Business sources: {business-sources}
- System sources: {system-sources}
- Mapping date: {date}

## Bridge Edges

| Business Claim | Edge Type   | System Evidence    | Bridge Evidence | Status |
| -------------- | ----------- | ------------------ | --------------- | ------ |
| {claim}        | realized_by | {artifact-or-path} | {evidence}      | flag   |

Allowed edge types: realized_by, depends_on, constrained_by, observed_by, tested_by, drifts_from, traced_to.

## Alignment Claims

| Claim             | Business Evidence | System Evidence | Confidence | Gaps  |
| ----------------- | ----------------- | --------------- | ---------- | ----- |
| {alignment-claim} | {business-path}   | {system-path}   | medium     | {gap} |

## Bridge Gaps

- {business claim with no system bridge}
- {system artifact with no business trace}

## Decisions Needed

- {decision}
