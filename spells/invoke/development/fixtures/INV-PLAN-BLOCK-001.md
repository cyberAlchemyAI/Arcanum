# Fixture: INV-PLAN-BLOCK-001

## Scenario

Blocked plan request with missing approved design references and missing companion status.

## User Request

Plan implementation for an unnamed Mars operations tool without approved design outputs.

## Inputs

- Approved design artifact: missing.
- Source design refs: missing.
- Implementation-layering companion: unknown.
- Work-pack companion: unknown.
- Validation strategy: missing.
- Lifecycle owner approval: absent.

## Expected

- Phase status: `block`
- Complexity: `n/a`
- Work-pack output mode: blocked
- Per-layer planning: blocked
- Next route: `deferred`

