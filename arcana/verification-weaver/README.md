# Verification Weaver

`verification-weaver` is a candidate public Arcana package for routing
verification targets to the correct evidence owner lanes and joining their
status-qualified outputs into a parent `VERIFICATION-WEAVE` receipt.

The package owns routing, classification, parent receipt shape, public-boundary
checks, and fail-closed recomposition. It does not derive tests, judge UX,
execute experiments, map architecture, or adjudicate research claims.

## Status

- Capability status: candidate package.
- Core verb: `route`.
- Parent receipt: `VERIFICATION-WEAVE`.
- Promotion boundary: owner-gated. A parent receipt can request follow-up; it
  cannot promote an owner output.

## Owner Lanes

| Lane | Owner capability | Parent responsibility |
| --- | --- | --- |
| Formal/spec derivation | `test-derivation` | Route obligations and preserve owner status. |
| Frontend and UX evidence | `ux-evidence-validator` | Record UX residue without upgrading it. |
| Repeatable execution | `experiment-harness` | Require fixture or adapter evidence before pass. |
| Architecture alignment | `architecture-pattern-inventory` | Record source-backed mapping gaps. |
| Research evidence | `research-evidence-harness` | Preserve dry-run and claim-status limits. |

## Target Kinds

- `spec_derivation`
- `frontend_ux`
- `execution_repeatability`
- `architecture_gap`
- `research_evidence`
- `mixed`
- `unsupported`

## Oracle Types

- `deterministic_derivation`
- `fixture_runner`
- `proof_checker`
- `browser_evidence`
- `human_review`
- `research_run_data`
- `explicit_gap`

Targets without an oracle or explicit gap block. Mixed targets must decompose
into owner lane receipts or preserve an explicit gap.

## Public Boundary

The public package uses synthetic fixtures only. It blocks:

- private implementation material;
- copied project fixtures;
- generated run artifacts as source authority;
- local telemetry logs as promotion evidence;
- parent receipts that mark owner outputs as promoted or registry-ready.

## Development

Run the package validation harness from the repository root:

```sh
bash arcanum/arcana/verification-weaver/development/run-validation-fixtures.sh
```

The harness validates fixture shape, owner-lane routing, negative controls,
public-safety fields, and parent promotion boundaries. It writes the current
validation summary to `development/VALIDATION.md` and a timestamped local report
under the ignored local runs directory.
