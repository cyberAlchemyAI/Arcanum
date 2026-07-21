# Fixture: route-medium

## Request

Route a blocked task receipt to `invoke:refresh:apply-approved`. Exact approval, target inventory, delta scope, and validation are present.

## Expected behavior

- Select exactly one owner route.
- Dispatch through Invoke in one bounded helper.
- Join a separate Invoke receipt.
- Return its Task Session next route without executing it.
