# Design: OIL Automatic Runtime Attachment

## Design Objective

Add a generator-backed attachment layer so every Arcanum-managed runtime adapter can carry the Observed Invocation Loop closeout contract automatically.

This should be implemented as an extension of `observed-invocation-loop`, using `sigil-runtime-installer` as the propagation mechanism. Codex commands should be supported as a runtime target, but they should not become the only enforcement path.

## Architecture Decision

Use a three-part attachment model:

| Part | Role | Owner |
| --- | --- | --- |
| observed closeout template | canonical generated block or link to runtime-local OIL contract | OIL |
| runtime installer integration | emits or refreshes adapter blocks for selected runtimes | `sigil-runtime-installer` |
| attachment validator | proves installed adapters include observed closeout or explicit exemption | OIL validation |

## Runtime Surfaces

| Runtime | Current Repo State | Design Treatment |
| --- | --- | --- |
| GitHub Copilot | many `.github/skills/` bridges and `.arcanum/runtimes/github-copilot/skills/` adapters exist | first implementation target |
| Codex | `.codex/` exists but no command files are installed | generate command adapter plans first, then commands when convention is confirmed |
| Claude | installer contract has path conventions, local files may be absent | planned target after GitHub Copilot/Codex proof |

## Attachment Contract

Every generated adapter must include or point to:

```text
.arcanum/runtimes/<runtime>/OBSERVED-INVOCATION.md
```

The adapter must resolve:

- `capability.id`
- `capability.kind`
- `capability.tier`
- `capability.mode`
- primary status
- output artifact or result summary
- validation status

The adapter must close with:

1. assemble invocation envelope,
2. call `framework/observability/scripts/observe-invocation.sh`,
3. optionally call `framework/observability/scripts/reflect-invocation-signals.sh`,
4. report telemetry status with the primary result.

## Generated Adapter Shape

The adapter text should remain thin. It should not copy OIL internals into every command. Use a stable marker block:

```markdown
<!-- arcanum:observed-invocation:start -->
Read `.arcanum/runtimes/<runtime>/OBSERVED-INVOCATION.md` and apply its closeout flow for capability `<id>` with kind `<kind>`.
<!-- arcanum:observed-invocation:end -->
```

The marker lets the installer refresh the block safely without rewriting unrelated adapter instructions.

## Codex Command Strategy

Codex commands are useful, but they are a runtime projection, not the canonical source.

Recommended path:

1. Keep canonical generated command files under `.arcanum/runtimes/codex/commands/`.
2. Add thin discovery bridges under `.codex/commands/`.
3. Generate one command per installed artifact:
   - `arcanum-sigil-<id>.md`
   - `arcanum-spell-<id>.md`
   - `arcanum-orchestrate.md`
4. Put the same observed invocation marker block in those command files.
5. Validate Codex command coverage using the same attachment manifest.

This gives the user "attach to every command" behavior without making Codex-specific files the only place where correctness lives.

## Attachment Manifest

The manifest should be deterministic and machine-readable enough for validation:

```markdown
# Observed Runtime Attachment Manifest

| Runtime | Command | Kind | Capability ID | Adapter Path | Bridge Path | OIL Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Status values:

- `attached`
- `planned`
- `exempt`
- `missing`
- `conflict`

## Safety Rules

- Refresh only marker blocks when they exist.
- If an adapter lacks a marker but has local differences, report `conflict` unless `--force` is explicitly requested.
- Discovery bridges stay thin and point at runtime-local canonical adapters.
- OIL failure must not hide the primary capability result unless strict mode is enabled.
- Exemptions require a reason and cannot be the default for installed sigils.

## Failure Modes

| Failure | Response |
| --- | --- |
| adapter path missing | mark `missing`; installer may create it |
| bridge path missing | mark `missing`; installer may create bridge |
| observability dir missing | flag unless strict mode requires block |
| marker block drift | refresh marker only |
| unsupported runtime convention | generate command adapter plan and mark `planned` |
| telemetry append fails | return primary result plus telemetry failure; block only in strict mode |

## Validation Design

Validation should check:

- every installed `arcanum-sigil-*` adapter is present in the manifest,
- every non-exempt adapter contains the observed marker or direct OIL contract reference,
- generated GitHub Copilot adapters still parse as valid skill markdown,
- Codex command plans name `.arcanum/runtimes/codex/commands/` and `.codex/commands/`,
- pilot invocation still appends telemetry through the deterministic observer.

## Invoke Result

- Mode: design
- Spell: invoke
- Phase status: pass
- Design status: approved for planning
- Next route: plan
