# Local Interrogation: Design Review

Status: flag
Owner: refine fallback synthesis
Reason: `interrogation refine-design-review` command surface resolved, but semantic execution used dry-run evidence only.

## Verdict

The architecture is implementation-ready after one naming repair: avoid field
names that imply runtime execution. `boundary_evidence` is the right top-level
name; `delegation_boundary` is safer than `runtime_adapter_boundary`.

## Required Repairs Before Task Session

- Remove Tandem from source notes and synthesis prose.
- Rename the technique family to `Boundary And Evidence Techniques`.
- Keep `boundary_evidence` optional in the schema to preserve compatibility.
- Add fixtures for pass, flag, and block cases before changing the validator.
- Make receipt absence a flag unless the route explicitly marks the boundary as
  execution-producing and required.
