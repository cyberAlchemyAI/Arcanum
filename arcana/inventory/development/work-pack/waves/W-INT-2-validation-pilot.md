---
module: inventory-interface-link-index
version: current
status: blocked
updatedAt: 2026-06-05
docType: wave
wave: W-INT-2
---

# Wave W-INT-2: Validation And Pilot

## Objective

Validate the new link/index discipline and prove it on one interface-driven
pilot slice.

## Entry Gate

- W-INT-1 passes.

## Exit Gate

- Validator checks controlled edges, source refs, card refs, and non-authority
  notices.
- First pilot slice has cards, index, retrieval, coverage, and gap/risk output.

## Tasks

- `TASK-INT-004-validator.md`
- `TASK-INT-005-pilot-slice.md`
