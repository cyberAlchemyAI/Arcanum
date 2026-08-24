# Executable fixture boundary

The contract-level synthetic cases live in
`../../fixtures/synthetic-contract-cases.json`. This source package owns sealed
request/catalog fixtures, exact expected bytes, permutation cases,
uncertainty-monotonicity cases, and Node/browser witness definitions.

No fixture may embed a product path, consumer runtime type, approval, workflow
binding, or effect claim.
