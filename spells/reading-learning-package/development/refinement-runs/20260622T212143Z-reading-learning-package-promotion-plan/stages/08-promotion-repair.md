# Stage 08: Promotion Repair Validation

Status: pass
Owner: `distill`
Mode: validate

## Repaired Scope

The promotion scope is repaired to this sequence:

1. Registry row.
2. Bootstrap temporary-target proof.
3. Generated surface synchronization, if expected by validated profiles.
4. Validation bundle.
5. Promotion receipt.
6. Public submodule commit and push.
7. Parent bump-check and gitlink publication.

## Validation

The sequence is small enough to execute as a promotion bundle and large enough
to preserve the meaning of promotion. It avoids both under-promotion (registry
only) and overreach (new runtime features or renderer implementation).

## Remaining Flags

- Generated mirrors require live target validation during execution.
- Parent publication depends on unrelated dirty state being isolated from the
  requested promotion scope.

