# Invoke Refresh Implementation Plan

## Objective

Implement `invoke refresh` as a governed invoke mode that turns latest session outputs into scoped artifact refresh proposals or approved updates.

## Layering

| Layer | Decision Question | Minimum Proof | Promotion Evidence |
| --- | --- | --- | --- |
| L0R | Can refresh classify latest outputs into safe delta classes? | Mode contract plus fixture parser expectations. | Pass/no-op/block fixtures validate output shape. |
| L1R | Can refresh produce reviewable patch proposals for workflow artifacts? | Template and patch proposal report. | Fixture expected outputs show evidence-to-delta mapping. |
| L2R | Can refresh safely apply approved deltas and validate artifacts? | Apply mode behind explicit approval. | Local validation and observability closeout. |
| L3R | Can refresh be promoted as a canonical invoke mode? | Command routing, docs, registry/examples. | Validation matrix passes and release gate approves. |

## SWUs

### INV-REFRESH-001: Mode Contract

- Goal: add `spells/invoke/refresh.md`.
- Dependencies: `INVOKE-REFRESH-DESIGN.md`.
- Write scope: `spells/invoke/refresh.md`, `spells/invoke/README.md` mode table/shared state references.
- Done criteria:
  - mode identity, purpose, trigger conditions, inputs, gates, outputs, and observability are documented;
  - authority boundary states refresh does not execute target work;
  - output contract includes pass/flag/block/no-op.
- Validation: markdown review plus link check.
- Status: completed in this session by adding `spells/invoke/refresh.md`.

### INV-REFRESH-002: Refresh Template

- Goal: add a refresh report/proposal template.
- Dependencies: INV-REFRESH-001.
- Write scope: `spells/invoke/templates/refresh/`.
- Done criteria:
  - template records source signals, target artifacts, delta classes, proposed/applied/skipped changes, blockers, next route, and validation;
  - template metadata follows existing invoke template front matter.
- Validation: template metadata review.
- Status: completed in this session by adding `spells/invoke/templates/refresh/`.

### INV-REFRESH-003: Fixtures

- Goal: add validation fixtures for refresh behavior.
- Dependencies: INV-REFRESH-001, INV-REFRESH-002.
- Write scope: `spells/invoke/development/fixtures/`.
- Done criteria:
  - pass fixture: new evidence updates a task/work-pack status;
  - flag fixture: artifact drift exists but approval is required;
  - block fixture: source evidence or target inventory is missing;
  - no-op fixture: latest outputs already match artifacts;
  - expected outputs look like real `## Invoke Result` bodies.
- Validation: invoke validation fixture runner.
- Status: completed in this session for deterministic pass/flag/block/no-op fixture coverage.

### INV-REFRESH-004: Runtime/Command Routing

- Goal: route `/invoke refresh` and `invoke refresh` to the new mode contract.
- Dependencies: INV-REFRESH-003 passing.
- Write scope: command adapter and local command docs.
- Done criteria:
  - router recognizes `refresh`;
  - output contract names mode `refresh`;
  - unknown or missing inputs block clearly.
- Validation: resolver check and fixture/live smoke.
- Status: flag in this session. Deterministic command routing is complete: `/invoke refresh` and `invoke refresh` resolve through `.codex/commands/invoke.md`, the invoke adapter snapshot includes `refresh`, and dry-run runtime handoff generation lists `REFRESH-REPORT.md` plus `refresh-report.json` as expected command-owned artifacts. Model-backed `codex-exec` smoke launched but the nested runtime blocked before reading workspace files because `bubblewrap` was unavailable inside the inner Codex launcher.

### INV-REFRESH-005: Apply-Approved Path

- Goal: support approved mutations after proposal review.
- Dependencies: INV-REFRESH-004.
- Write scope: mode contract, adapter instructions, validation fixtures.
- Done criteria:
  - default is proposal-only;
  - apply mode requires explicit approval and declared scope;
  - validation command list is recorded;
  - changed files are listed in the report.
- Validation: local safe fixture over temporary artifacts.

### INV-REFRESH-006: Observability And Promotion

- Goal: record refresh-specific telemetry and prepare promotion evidence.
- Dependencies: INV-REFRESH-005.
- Write scope: observability template docs if needed, validation report, registry/promotion notes.
- Done criteria:
  - source signal counts, delta counts, mutation mode, and no-op/block reasons are observable;
  - promotion notes distinguish invoke gaps from target-artifact gaps.
- Validation: observed invocation closeout.

## Initial Fixture Scenario

Use a benchmark-style fixture because it captures the core lesson:

- source output: task-session completed materialization setup proof;
- target artifacts: work-pack and task file still say score smoke is ready;
- correct refresh:
  - mark materialization complete;
  - keep score smoke blocked;
  - add blocker for real candidate and worker profile;
  - label dry-run output as setup proof only.

## Acceptance Criteria

- `invoke refresh` never turns setup proof into completion proof.
- Every mutation or proposal maps to at least one `RefreshSignal`.
- Missing evidence blocks, rather than guessing.
- No-op refresh is a first-class valid result.
- The next route is updated only when supported by artifact state.

## Recommended Next Route

Run `task-session` on `INV-REFRESH-004` after deterministic fixture validation remains green. Command routing should stay deferred until the contract, template, and fixtures are stable.

## Refresh From Interrogation And Distill

- Interrogation artifact: [INVOKE-REFRESH-INTERROGATION.md](INVOKE-REFRESH-INTERROGATION.md)
- Distill artifact: [INVOKE-REFRESH-DISTILL.md](INVOKE-REFRESH-DISTILL.md)
- Context pack: [INVOKE-REFRESH-CONTEXT-PACK.md](INVOKE-REFRESH-CONTEXT-PACK.md)

Plan adjustment:

- INV-REFRESH-001 through INV-REFRESH-003 are now implemented as documentation and deterministic validation surface.
- INV-REFRESH-004 remains the next mutation-capable routing step.
- INV-REFRESH-005 apply-approved behavior remains deferred until routing exists and approval semantics are validated.
