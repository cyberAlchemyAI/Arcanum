# Stage 05: Smallest Promotion Unit

Status: pass
Owner: `distill`
Mode: standard

## Selected Unit

The smallest coherent promotion unit is:

> Promote `reading-learning-package` as a discoverable library spell by adding
> registry discoverability, validating runtime-surface generation, recording a
> promotion receipt, and publishing `arcanum` before the parent gitlink.

## Included

- `arcanum/registry/SPELLS.md` row.
- Temporary-target or dry-run bootstrap validation for
  `--spells reading-learning-package`.
- Generated mirror synchronization only when profile validation proves the
  expected output set.
- Validation and public-boundary receipt.
- Submodule-first commit/push plan.

## Rejected Alternatives

| Alternative | Rejection Reason |
| --- | --- |
| Only add a registry row. | Too small; it would not prove runtime surface generation or publish readiness. |
| Add PDF renderer integration. | Too large; renderer work is optional future `task-session` work. |
| Commit parent gitlink immediately. | Unsafe; submodule discipline requires public submodule push first. |
| Add aliases now. | Optional maintainer decision, not needed for default promotion. |

## Recomposition Proof

This unit recomposes into the original learning package objective because it
does not change the runtime behavior. It makes the already validated spell
discoverable and installable while preserving source and composition authority.

