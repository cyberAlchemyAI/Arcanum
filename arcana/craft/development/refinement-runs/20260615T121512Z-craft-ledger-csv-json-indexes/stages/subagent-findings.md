# Subagent Findings

## projection-risk-reviewer

Status: pass with design corrections.

Findings incorporated:

- Embedded ledger indexes currently use positional pointers and can drift after
  row reordering; generated `index.json` should own lookup freshness.
- The initial schema contract does not cover every row family used by current
  examples, so projections must define or flag `descriptions`, `definitions`,
  `gaps`, `route_handoffs`, `receipts`, and `recomposition`.
- CSV projections should be named as generated projections rather than new
  authoritative tables.
- All-status reads should get a `pending_by_node` fast path in `index.json`.
- Decision projections need workflow columns for proposed and selected options.
- Links and evidence should be normalized into references, links in/out, and
  evidence refs.

## process-boundary-reviewer

Status: pass with gate corrections.

Findings incorporated:

- Public Craft fixtures must be synthetic or already public.
- Scan generated JSON and CSV outputs, not only source fixtures.
- Syntax validation is not publication readiness; content-boundary gates remain
  separate.
- Keep source-first and generation-last: schema/docs contract before fixtures,
  fixtures before generated outputs, generated outputs before publication.
- Preserve explicit stage receipts and result status instead of treating a parse
  pass as a lifecycle promotion.
