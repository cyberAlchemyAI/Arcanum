# Design Transport: Runtime Artifact Reproduction

## Transport Summary

This report carries the invoke design result for the tiny runtime artifact reproduction fixture. The design proves that command-owned artifacts can be produced under the fixture target directory while runtime-owned artifacts remain under runtime runner control.

## Target Artifact

- Name: runtime artifact reproduction
- Type: fixture capability
- Owner/cycle: framework/runtime development fixture
- Invoke mode: design
- Observed capability: invoke

## Produced Artifacts

| Artifact | Status | Purpose |
| --- | --- | --- |
| framework/runtime/development/fixtures/invoke-design-artifacts/target/development/INVOKE-DESIGN.md | produced | Invoke result, source contracts, decisions, and observability closeout. |
| framework/runtime/development/fixtures/invoke-design-artifacts/target/development/ARCHITECTURE-BUNDLE.md | produced | Six-view design bundle for the fixture capability. |
| framework/runtime/development/fixtures/invoke-design-artifacts/target/development/GLOSSARY-CONSISTENCY.md | produced | Vocabulary consistency check for the fixture design. |
| framework/runtime/development/fixtures/invoke-design-artifacts/target/development/DESIGN-TRANSPORT.md | produced | This transport report. |

## Source Design Refs

| Ref ID | Path | Use |
| --- | --- | --- |
| SD-001 | framework/runtime/development/fixtures/invoke-design-artifacts/RUNTIME-HANDOFF.md | Fixture objective, write scope, expected artifacts, and validation commands. |
| SD-002 | framework/runtime/development/fixtures/invoke-design-artifacts/expected-artifacts.txt | Exact expected command-owned artifact paths. |
| SD-003 | spells/invoke/design.md | Design-mode gates and output contract. |
| SD-004 | .codex/commands/invoke.md | Root invoke contract and observer envelope requirements. |

## Design Decisions To Preserve

| Decision ID | Decision | Preserve Because |
| --- | --- | --- |
| D-001 | Runtime-owned artifacts are not written directly by command execution. | The runtime runner owns status, result, events, adapter profile, and compatibility output copying. |
| D-002 | Command-owned artifacts are limited to the declared target development directory. | This keeps fixture validation deterministic and respects the handoff write boundary. |
| D-003 | Validation remains path-existence based. | The current fixture objective is artifact reproduction, not schema-level design validation. |

## Validation Handoff

The current fixture validation should check:

```bash
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/INVOKE-DESIGN.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/ARCHITECTURE-BUNDLE.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/GLOSSARY-CONSISTENCY.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/DESIGN-TRANSPORT.md
```

## Gap Ownership

| Gap | Owner | Status |
| --- | --- | --- |
| None for command-owned artifact reproduction. | n/a | closed |
| Future semantic validation, if desired. | runtime fixture development cycle | deferred |

## Next Route

Deferred. Route back to runtime fixture development only if the runner fails to preserve command-owned artifacts or if validation expands beyond existence checks.
