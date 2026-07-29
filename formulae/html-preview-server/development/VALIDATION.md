# Validation

- Latest report: `runs/2026-07-29-initial-validation.md`
- Status: flag
- Deterministic lifecycle helper: pass
- Profile-aware harness structure: pass
- Browser navigation: pass on the bounded Body War HTML fixture
- Generated runtime mirror comparison: pass
- Promotion readiness: hold until repeated runtime/telemetry evidence exists

## Checks

- Harness layout and `sigil-development` profile exist.
- Fixture pairs and prompts cover low, medium, and complex lifecycle cases.
- Dynamic open verifies exact target bytes.
- Same-target start reuses one managed process.
- Status does not start or stop.
- Explicit root/port conflicts block without duplicate startup.
- Concurrent starts converge through a per-target lock.
- Encoded paths, relative assets, dotfiles, traversal, and symlink escape are
  checked.
- Same-basename targets receive distinct identities.
- Stop is authenticated and idempotent.
- The canonical package and selectively generated Codex/Claude mirrors match the
  disposable bootstrap output.
- Shared Chromium navigation reached the exact managed URL with HTTP 200, the
  expected title, no console errors, and no horizontal overflow.
- Repeated meaningful usage telemetry remains required before this report can
  advance beyond `flag`.
