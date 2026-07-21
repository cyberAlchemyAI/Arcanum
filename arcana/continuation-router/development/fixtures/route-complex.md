# Fixture: route-complex

## Request

Route a flagged review receipt whose evidence could require either a blocker-level decision or more target refinement. A prior continuation receipt also shows an unchanged Task Session fingerprint.

## Expected behavior

- Rank no more than three probable routes.
- Keep the unresolved owner routes visible.
- Select neither ambiguous route.
- Reject unchanged Task Session re-entry.
- Perform no dispatch.
