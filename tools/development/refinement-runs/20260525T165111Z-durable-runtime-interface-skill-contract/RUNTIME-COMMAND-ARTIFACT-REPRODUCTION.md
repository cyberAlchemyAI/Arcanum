# Runtime Command Artifact Reproduction

## Purpose

Define the missing repair between command transport compatibility and real Arcanum command reproduction.

`SWU-RUNTIME-004` proved that `tools/arcanum --exec` can delegate through the durable runtime runner, write runtime evidence, preserve `--output`, and report command summary fields. It did not prove that a command such as `invoke design` can write its normal target-owned artifacts in the same way a Codex UI or IDE chat run would.

This artifact defines `SWU-RUNTIME-004.5`.

## Problem

The current runtime handoff is too narrow for artifact-producing commands.

The `SWU-RUNTIME-004` smoke used:

```bash
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-output-swu004-final.md invoke "define runtime smoke"
```

That proved runtime transport, but the command output reported:

```text
Outputs: none written; runtime runner owns requested output and runtime artifacts
```

This is correct for the smoke request, but insufficient for real invoke use. If a user runs:

```bash
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output <result> invoke "design ..."
```

the expected behavior is:

- runtime artifacts are written under `.arcanum/runtime/runs/<id>/`,
- compatibility output is copied to the requested `--output`,
- command-owned artifacts are written to the target development directory,
- `STATUS.json.output_paths` or runtime result references include command-owned artifacts,
- the command output contract matches a normal UI/IDE chat run.

## Ownership Model

Runtime-owned artifacts:

- `RUN.json`
- `STATUS.json`
- `events.jsonl`
- `RESULT.md`
- `HANDOFF.md`
- `artifacts/adapter-profile.json`
- adapter state

Command-owned artifacts:

- invoke define/design/plan outputs,
- refine stage outputs,
- task-session reports,
- target-local development package files.

The adapter must not write runtime-owned artifacts directly. The adapter may write command-owned artifacts when the handoff explicitly grants write scope.

## Required Handoff Additions

Generated runtime handoffs for `tools/arcanum --exec` must include:

- selected command,
- command file,
- request,
- requested compatibility output,
- target artifact directory when supplied or inferred,
- allowed command artifact write scope,
- expected command-owned artifacts when known,
- validation commands for command-owned artifacts,
- instruction that runtime-owned artifacts remain runner-owned,
- instruction that command-owned artifacts may be written only inside the declared target scope.

## New SWU

```text
SWU-RUNTIME-004.5
```

Parent task:

```text
TASK-RUNTIME-003 Migrate Arcanum Exec Compatibility Path
```

Dependencies:

```text
SWU-RUNTIME-004
```

Write scope:

- `tools/arcanum`
- `tools/arcanum-runtime-run`
- `framework/runtime/development/fixtures/invoke-design-artifacts/`
- runtime development evidence and task-session report

Done criteria:

- feature-flag `tools/arcanum --exec` can run an artifact-producing invoke fixture,
- generated runtime handoff declares target artifact write scope,
- Codex adapter prompt preserves runtime ownership while allowing target artifact creation,
- expected command-owned artifacts are created in the target development directory,
- requested `--output` still receives runtime `RESULT.md`,
- runtime `STATUS.json` records the requested output and command-owned artifact paths or result references,
- validation distinguishes runtime transport pass from command artifact reproduction pass.

## Fixture Shape

Recommended fixture directory:

```text
framework/runtime/development/fixtures/invoke-design-artifacts/
  RUNTIME-HANDOFF.md
  expected-artifacts.txt
  target/
    development/
```

Recommended smoke command:

```bash
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec \
  --output /tmp/arcanum-runtime-invoke-design-output.md \
  invoke "design a tiny fixture capability named runtime artifact reproduction under framework/runtime/development/fixtures/invoke-design-artifacts/target/development; write INVOKE-DESIGN.md, ARCHITECTURE-BUNDLE.md, GLOSSARY-CONSISTENCY.md, and DESIGN-TRANSPORT.md; do not edit runtime-owned artifacts directly"
```

Expected command-owned artifacts:

```text
framework/runtime/development/fixtures/invoke-design-artifacts/target/development/INVOKE-DESIGN.md
framework/runtime/development/fixtures/invoke-design-artifacts/target/development/ARCHITECTURE-BUNDLE.md
framework/runtime/development/fixtures/invoke-design-artifacts/target/development/GLOSSARY-CONSISTENCY.md
framework/runtime/development/fixtures/invoke-design-artifacts/target/development/DESIGN-TRANSPORT.md
```

The exact prompt may be refined during implementation, but validation must assert real files, not only final response prose.

## Validation

Minimum checks:

```bash
bash -n tools/arcanum tools/arcanum-runtime-run
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-design-output.md invoke "<artifact-producing invoke design fixture request>"
test -f /tmp/arcanum-runtime-invoke-design-output.md
jq empty <runtime-run>/RUN.json <runtime-run>/STATUS.json
jq -e '.status == "passed" or .status == "flagged"' <runtime-run>/STATUS.json
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/INVOKE-DESIGN.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/ARCHITECTURE-BUNDLE.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/GLOSSARY-CONSISTENCY.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/DESIGN-TRANSPORT.md
```

Review checks:

- runtime `events.jsonl` is runner-owned,
- command-owned artifacts are under declared target write scope,
- runtime result references command-owned artifacts,
- no runtime-owned artifact was edited by nested Codex outside the runner closeout path.

## Promotion Rule

`SWU-RUNTIME-004` remains passed for transport compatibility.

L2 does not promote to L3 until `SWU-RUNTIME-004.5` passes.

`SWU-RUNTIME-005` and `SWU-RUNTIME-006` remain blocked until artifact-producing command reproduction is proven.
