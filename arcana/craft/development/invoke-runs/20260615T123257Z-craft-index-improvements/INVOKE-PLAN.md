# Invoke Plan: Craft Index Improvements

## Objective

Implement Craft readiness indexes plus generated JSON/CSV projection support in
one governed execution sequence, while preserving YAML authority and public
submodule safety.

## Planning Decisions

- Complexity: medium.
- Output mode: split work-pack.
- Selected execution unit for Codex Goal conversion: `TASK-CII-ONEGO`.
- Execution style: one native Codex goal session with ordered SWUs and hard
  stop conditions.
- Publication: out of scope unless explicitly approved after validation.

## Execution Sequence

1. L0 contract update.
   - Add readiness/projection contracts to schema/docs/SKILL.
   - Preserve source-of-truth language and non-execution boundary.

2. L1 public-safe fixture.
   - Add synthetic fixture covering live row families, links, evidence, gaps,
     receipts, recomposition, and readiness fields.
   - Add expected JSON/CSV outputs or fixture expectations.

3. L2 deterministic tooling.
   - Add `craft-index build`.
   - Add `craft-index validate`.
   - Integrate all-status fast-path expectations without trusting stale output.

4. L3 import dry-run and runtime refresh.
   - Add `import-csv --dry-run`.
   - Refresh generated runtime mirrors only after canonical checks pass.
   - Run public-boundary scan and submodule discipline checks.

## Validation Strategy

- Parse schema and fixtures with Python/YAML.
- Parse generated JSON with `python3 -m json.tool`.
- Validate CSV headers and row counts.
- Run stale-source and unsupported-family checks.
- Run targeted `rg` checks for readiness and projection language.
- Run `git -C arcanum diff --check -- arcana/craft`.
- Run parent `make bump-check` only before parent gitlink publication.

## Blockers And Gaps

- CSV writeback remains blocked until dry-run fixture proof passes.
- Generated runtime refresh remains blocked until canonical source validation
  passes.
- Commit, push, PR, and parent gitlink movement are blocked until explicitly
  requested after submodule-first checks.

## Next Route

Use the private Codex Goal profile generated from `TASK-CII-ONEGO`.
