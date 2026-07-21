# Fixture: route-low

## Request

Rank routes for a blocked task receipt that names planning drift. The caller has not authorized application.

## Expected behavior

- Expose `invoke:refresh` as the first probable route.
- Mark `apply-approved` as not authorized.
- Perform no dispatch.
- Preserve the source block.
