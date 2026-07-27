# Invoke Template Example Runbook

This runbook explains how to run every task in [TEMPLATE-VALIDATION-TASKS.md](TEMPLATE-VALIDATION-TASKS.md) through `invoke`.

## Current Reality

`arcanum-spell-invoke` is a Codex command adapter, not a shell executable. That means the shell runner can generate prompts and validate saved outputs, but the actual invocation happens in Codex by using the command adapter.

## Generate Prompts

Run:

```bash
arcanum/spells/invoke/development/generate-template-example-prompts.sh
```

This creates one prompt per task under:

```text
arcanum/spells/invoke/development/example-prompts/
```

Each prompt contains:

- task ID,
- template target,
- complexity,
- realistic user request,
- expected invoke use,
- output capture path.

## Run One Example In Codex

Short Codex commands:

```text
invoke-example-next
invoke-example-run sigil-medium
invoke-example-run sigil medium
```

Automated native skill/subagent execution is preferred. The Codex CLI runner remains available only as an explicit legacy adapter test:

```bash
arcanum/spells/invoke/development/run-template-example-with-codex.sh sigil-medium
arcanum/spells/invoke/development/run-template-example-with-codex.sh sigil medium
arcanum/spells/invoke/development/run-template-example-with-codex.sh next
```

The legacy runner calls `codex exec`, writes the last Codex message to `example-outputs/<task-id>.output.md`, and stores command logs under `example-runs/`. If Codex exits with an error, the runner prints the log path and does not create the output file.

If `codex` is not on `PATH`, the runner tries common VS Code extension install paths. You can also set `CODEX_BIN` explicitly:

```bash
CODEX_BIN=/absolute/path/to/codex \
  arcanum/spells/invoke/development/run-template-example-with-codex.sh next
```

Preferred command:

```text
arcanum-sigil-invoke-example-runner <task-id | template complexity | next>
```

Examples:

```text
arcanum-sigil-invoke-example-runner sigil-medium
arcanum-sigil-invoke-example-runner sigil medium
arcanum-sigil-invoke-example-runner next
```

Manual fallback:

1. Open a prompt from `example-prompts/`.
2. Send its **Codex Prompt** section to Codex.
3. Codex should read `.codex/commands/arcanum-spell-invoke.md`.
4. Codex should apply the canonical `invoke` contract.
5. Save the result to the prompt's `example-outputs/<task-id>.output.md` path.

## Run All Examples

Run the prompts one by one in Codex, or explicitly use batch mode:

```bash
arcanum/spells/invoke/development/run-template-example-with-codex.sh --all
```

Batch mode can take time because it starts one non-interactive Codex run per prompt.

The current shell suite validates:

- that every template has low, medium, and complex task coverage,
- that core define/design fixtures pass,
- that the define-to-design integration fixture produces inspectable artifacts.

The next hardening step is to add an output validator for:

```text
arcanum/spells/invoke/development/example-outputs/
```

That validator should compare each saved output against the expected mode, template target, complexity, and `Invoke Result` shape.

## Prompt Selection Utility

To select a prompt without running it:

```bash
arcanum/spells/invoke/development/select-template-example-prompt.sh sigil-medium
arcanum/spells/invoke/development/select-template-example-prompt.sh sigil medium
arcanum/spells/invoke/development/select-template-example-prompt.sh next
```

## Rerun Existing Output

By default the CLI runner skips examples that already have output files. To overwrite one:

```bash
RERUN=1 arcanum/spells/invoke/development/run-template-example-with-codex.sh sigil-medium
```

## Why This Is Split

The template task matrix is coverage planning.

The generated prompts are invocation inputs.

The saved example outputs are evidence of what users actually receive.

The validation runner is the repeatable proof that the coverage and saved outputs remain intact.
