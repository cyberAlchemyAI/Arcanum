# Command Surface Evidence

## Summary

- Change: Added a repository-local Arcanum command surface.
- Command: `tools/arcanum`
- Date: 2026-05-18
- Status: implemented

## Purpose

The host chat UI does not dynamically load repository `.codex/commands` into its slash-command menu. The local command surface gives Arcanum a real executable entrypoint that accepts slash-like commands such as `/invoke`, resolves the generated adapter, and can run the Codex CLI with OIL telemetry.

## Verification Commands

```bash
bash -n tools/arcanum
tools/arcanum --resolve /invoke
tools/arcanum --resolve interrogation
tools/arcanum /invoke define a new sigil
tools/arcanum --list
arcana/experiment-harness/scripts/find-codex.sh
```

## Expected Behavior

| Command | Expected Result |
| --- | --- |
| `tools/arcanum --resolve /invoke` | Resolves to `.arcanum/runtimes/codex/commands/arcanum-spell-invoke.md`. |
| `tools/arcanum --resolve interrogation` | Resolves to `.arcanum/runtimes/codex/commands/arcanum-sigil-interrogation.md`. |
| `tools/arcanum /invoke define a new sigil` | Prints the runtime prompt that follows the `invoke` adapter. |
| `tools/arcanum --exec invoke ...` | Runs Codex CLI, writes output, and appends OIL telemetry. |

## Results

| Check | Result |
| --- | --- |
| shell syntax | pass |
| `/invoke` resolution | pass |
| `interrogation` resolution | pass |
| prompt generation | pass |
| command listing includes `invoke` | pass |
| command listing includes `interrogation` | pass |
| Codex CLI discovery | pass |

Codex CLI was found at:

```text
/home/vrondelli/.vscode-server/extensions/openai.chatgpt-26.513.21555-linux-x64/bin/linux-x86_64/codex
```

Nested `--exec` was not run during this verification to avoid launching a second model session from inside the active Codex session.

## Acceptance

Pass when the command resolves bare aliases and slash-like aliases without relying on the host chat slash menu.
