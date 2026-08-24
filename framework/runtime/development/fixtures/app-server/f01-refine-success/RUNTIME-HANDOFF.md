# Runtime Handoff Fixture: F-01 Refine Stage

## Objective

Replay a synthetic successful App Server lifecycle for one `invoke-design` Refine stage and normalize raw host completion without manufacturing an owner verdict.

## Bindings

- `adapter_id`: app-server-fixture
- `runtime_run_id`: rt-refine-001
- `refine_run_id`: refine-candidate-001
- `stage`: invoke-design
- `input_digest`: sha256:1111111111111111111111111111111111111111111111111111111111111111
- `skill_digest`: sha256:2222222222222222222222222222222222222222222222222222222222222222

## Policy

- `transport`: stdio
- `network`: denied
- `filesystem`: read-only-except-allowlist
- `allowed_write_path`: /fixture/out/design.md
- `turn_limit`: 1
- No outbound connector, realtime, shell, unsandboxed process, or undeclared write.

## Expected Lifecycle

`runtime.created` → `app_server.initialized` → `thread.started` → `turn.started` → `item.started` → `item.completed` → `turn.completed` → normalized host result.

## Authority Stop

Stop after raw host-result normalization. The next required owner is the owner-local stage verdict. Do not advance Refine, admit Task Session work, mutate Craft, control Goal, dispatch Orchestrate, or promote lifecycle state.

## Claim Ceiling

This is synthetic fixture evidence only. It does not launch App Server or a model turn and does not prove live integration, installed-binary parity, semantic acceptance, promotion, publication, release, deployment, or production readiness.
