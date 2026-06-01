# Craft Runtime Command Surface Glossary

## Purpose

Define local terms for the runtime/command-surface blocker that prevents Refine from validating Craft.

Terms remain local to `development/craft/` unless a later runtime lifecycle route promotes them.

## Terms

| Term | Definition | Status |
| --- | --- | --- |
| Command Surface | The repository-local interface used by `tools/arcanum` to list, resolve, and execute named Arcanum commands from `.codex/commands`. | validated-local |
| Bare Command Route | A direct command name such as `dispatch-spec` that resolves without an `arcanum-sigil-*` prefix. | candidate |
| Command Alias | A command file or route that forwards to an existing canonical capability without changing the capability owner. | candidate |
| Dispatch Spec Route | The command route that validates a dispatch document's schema, techniques, gates, observability, and boundary evidence. | candidate |
| Runtime Handoff Route | The command route that validates or emits a runtime handoff contract before delegated or command-backed execution. | candidate |
| Runtime Adapter | A runtime-specific execution profile such as `codex-skill`, `claude-skill`, `copilot-instructions`, `local-skill`, `dry-run`, or `codex-exec`. | existing-local |
| Stage Worker | A bounded executor for one Refine stage, returning artifact path, validation, blockers, and handoff note. | candidate |
| Stage Receipt | Structured result returned by a stage worker or blocked-gap recorder. | candidate |
| Observation Envelope | Pre/post run wrapper that preserves run identity, request, outputs, files changed, validation, blockers, and recommendation. | existing-local |
| Command Smoke | A small validation that proves command resolution and minimal command behavior without running the full lifecycle. | candidate |

## Boundary Notes

- A command alias does not own the target capability lifecycle.
- A runtime handoff route does not imply full adapter implementation.
- A passing command smoke does not promote Craft.
