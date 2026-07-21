# Continuation Router Deterministic Validation Report

- Date: 2026-07-20
- Result: pass
- Promotion posture: fixture-ready; live reusable-behavior review pending

## Evidence

- Sigil Development experiment profile: pass.
- Five required lifecycle regimes: pass.
- Route receipt JSON Schema: pass under Draft 2020-12 validation.
- Route-specific fixtures: 6 of 6 pass.
- Low case: missing apply authorization exposes the Invoke route and does not dispatch.
- Medium case: exact `invoke:refresh:apply-approved` authorization selects one route, requires a joined owner receipt, and returns a Task Session route.
- Complex case: ambiguous Decision Gate and Refine candidates remain visible and unselected.
- Repeated fingerprint: unchanged Task Session re-entry blocks.
- Unknown capability or mode: blocks.
- Legacy receipt: remains readable without gaining silent apply authority.
- Public-boundary scan: pass.
- Markdown links, skill frontmatter, generated runtime parity, and scoped diff hygiene: pass.

## Commands

```bash
arcana/continuation-router/development/run-validation-fixtures.sh
git -C arcanum diff --check -- arcana/continuation-router arcana/task-session registry/SIGILS.md README.md arcana/README.md
```

## Boundary

This report proves the contract and deterministic fixture surface. It does not alone promote live autonomous behavior. The separately joined owner hop is operational evidence for later Sigil Development review.
