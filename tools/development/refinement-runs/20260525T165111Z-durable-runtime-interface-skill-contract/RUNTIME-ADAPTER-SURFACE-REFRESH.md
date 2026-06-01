# Runtime Adapter Surface Refresh

## Decision

Keep `tools/arcanum` as the single user-facing execution tool, but do not make Codex the implicit runtime model.

The command surface must expose runtime selection through a stable adapter boundary:

```bash
tools/arcanum --exec --adapter <adapter-id> --output <output> <command> <request>
```

When `--adapter` is omitted, `tools/arcanum` may default to `codex-exec` for current Codex UI parity. That default is convenience only. It is not the architecture.

## Adapter Contract

Every runtime adapter must provide:

- stable `adapter_id`,
- runtime profile path,
- supported command kinds,
- input translation rule,
- output capture rule,
- state and isolation policy,
- status classifier,
- validation grade mapping,
- blocked reason vocabulary,
- evidence files written under the optional runtime envelope.

Codex is one adapter:

```text
codex-exec
```

Other adapters should be addable without changing refine, task-session, or command-specific invoke/interrogation/distill contracts.

## Single Tool, Multiple Runtimes

`tools/arcanum` owns:

- command resolution,
- adapter selection,
- adapter profile resolution,
- generic handoff construction,
- output path ownership,
- optional runtime envelope evidence,
- observed invocation closeout.

The selected adapter owns:

- runtime-specific translation,
- runtime-specific process/API invocation,
- runtime-specific state preparation,
- runtime-specific classification of raw outcomes.

The command owns:

- command-specific artifacts,
- command-specific target development outputs,
- normal requested response content.

## Required Command Surface

Minimum v1 surface:

```bash
tools/arcanum --resolve <command>
tools/arcanum --exec --output <path> <command> <request>
tools/arcanum --exec --adapter <adapter-id> --output <path> <command> <request>
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter <adapter-id>
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter <adapter-id>
```

`--list-adapters` and `--resolve-adapter` may start as static table output. Dynamic plugin discovery is deferred.

`--get-default-adapter` and `--set-default-adapter` read and update installed `.arcanum/runtime/config.json`. They should not edit generated command files.

Adapter ids for v1:

- `dry-run`
- `codex-exec`

Future adapter examples:

- `shell-exec`
- `local-agent`
- `remote-agent`
- `noop-contract`

## Adapter Profile Layout

Profiles should remain easy to inspect and cheap to validate:

```text
framework/runtime/adapters/<adapter-id>.md
framework/runtime/adapters/<adapter-id>.json
```

The Markdown file explains behavior. The JSON file, if present, is the machine-checkable summary copied into runtime envelope evidence as:

```text
artifacts/adapter-profile.json
```

If the JSON file is not present in v1, `tools/arcanum` may generate the profile snapshot from a static shell table, but the selected adapter properties must still be recorded.

## Validation Impact

`SWU-RUNTIME-008` must prove single-tool execution with at least two adapters:

```bash
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter dry-run
tools/arcanum --resolve-adapter codex-exec
tools/arcanum --exec --adapter dry-run --output /tmp/arcanum-dry-run-output.md invoke "define runtime smoke"
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-codex-output.md invoke "define runtime smoke"
```

The `dry-run` check proves the generic adapter path without Codex. The `codex-exec` check proves Codex can be selected as an adapter without owning the runtime model.

## Reflection Trigger

Trigger another design refresh if:

- `tools/arcanum --exec` cannot select a non-Codex adapter,
- adapter selection requires command-specific code in refine or task-session,
- adapter profile evidence is missing from envelope-backed runs,
- `codex-exec` behavior is hardcoded as the generic execution behavior,
- adding a new runtime requires changing command contracts instead of adding an adapter profile and adapter dispatch branch.
