---
module: runtime-artifact-reproduction
version: current
status: draft
updatedAt: 2026-05-25
docType: architecture-bundle
---

# Architecture Bundle: Runtime Artifact Reproduction

## Design Intent

Runtime artifact reproduction is a tiny fixture capability that proves a runtime-backed invoke command can create command-owned design artifacts in addition to runtime-owned result files. The design keeps the capability file-based, deterministic, and bounded to the declared fixture target directory.

## Inputs

- framework/runtime/development/fixtures/invoke-design-artifacts/RUNTIME-HANDOFF.md
- framework/runtime/development/fixtures/invoke-design-artifacts/expected-artifacts.txt
- .codex/commands/invoke.md
- spells/invoke/design.md

## Required View Set

### 1. Context View

```mermaid
graph TD
    Runner[Runtime runner] --> Codex[Codex adapter]
    Codex --> Invoke[Invoke design command]
    Invoke --> TargetDir[Fixture target directory]
    Runner --> RuntimeArtifacts[Runtime-owned artifacts]
```

The runtime runner owns status, event, result, and compatibility-copy outputs. The invoke command owns only the design artifacts under `framework/runtime/development/fixtures/invoke-design-artifacts/target/development/`.

### 2. High-Level Structure View

```mermaid
graph TD
    Request[Handoff request] --> Contract[Invoke design contract]
    Contract --> Bundle[Architecture bundle]
    Contract --> Glossary[Glossary consistency report]
    Contract --> Transport[Design transport report]
    Contract --> Result[Invoke design summary]
```

The fixture has no service runtime, registry entry, or persistent state. Its structure is the authored artifact set plus the existing validation fixture that checks file existence.

### 3. Low-Level Components View

```mermaid
graph TD
    SourceContracts[Source contract reader] --> BoundaryRules[Boundary rule set]
    BoundaryRules --> ArtifactWriter[Command artifact writer]
    ArtifactWriter --> FileSet[Four markdown artifacts]
    FileSet --> Validator[Existence validator]
```

| Component | Responsibility | Boundary |
| --- | --- | --- |
| Source contract reader | Interpret the handoff fixture and expected artifact list. | Read-only access to fixture source files. |
| Boundary rule set | Preserve runtime-owned versus command-owned artifact ownership. | No direct writes to runtime result/status/event files. |
| Command artifact writer | Create the expected design artifact files. | Writes only under the declared target development directory. |
| Existence validator | Confirm the expected command-owned files exist. | Uses shell checks; does not mutate artifacts. |

### 4. Workflow Process View

```mermaid
graph TD
    S1[Read runtime handoff] --> S2[Read invoke command contract]
    S2 --> S3[Resolve design mode]
    S3 --> S4[Load design contract and templates]
    S4 --> S5[Author command-owned artifacts]
    S5 --> S6[Validate expected artifact paths]
    S6 --> S7[Return invoke result and observability closeout]
```

Failure behavior is intentionally simple: if any expected command-owned artifact cannot be created inside the target directory, the fixture should fail validation and route back to the runtime/invoke integration surface.

### 5. Decision Flow View

```mermaid
graph TD
    D1[User request] --> D2{Mode explicit?}
    D2 -->|design| D3[Use invoke design mode]
    D2 -->|other or absent| D4[Block or clarify]
    D3 --> D5{Write path allowed?}
    D5 -->|yes| D6[Create command-owned artifacts]
    D5 -->|no| D7[Block before mutation]
    D6 --> D8{Expected files exist?}
    D8 -->|yes| D9[Pass]
    D8 -->|no| D10[Fail validation]
```

| Decision ID | Decision | Options Considered | Reason |
| --- | --- | --- | --- |
| D-001 | Use design mode. | define, design, plan, full, validate | The request explicitly asks to design and names design-stage artifacts. |
| D-002 | Treat the handoff as discovery-mode design approval. | block for missing define outputs, proceed with discovery-mode fixture design | The fixture request is deliberately small and supplies source contracts through the handoff and expected artifact list. |
| D-003 | Keep validation at file-existence level. | content schema validation, existence checks | The fixture objective is reproduction of command-owned artifacts, not semantic promotion of a full capability. |

### 6. Dependency Interface View

```mermaid
graph TD
    InvokeDesign[Invoke design artifacts] --> FixtureHandoff[RUNTIME-HANDOFF.md]
    InvokeDesign --> ExpectedList[expected-artifacts.txt]
    InvokeDesign --> DesignContract[spells/invoke/design.md]
    RuntimeRunner[Runtime runner] --> ResultFiles[RUN/STATUS/RESULT/events]
    InvokeDesign -. no direct writes .-> ResultFiles
```

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Handoff fixture | Runtime fixture source | Invoke design run | Declares objective, write scope, expected artifacts, and validation checks. |
| Command-owned artifact set | Invoke design run | Runtime fixture validation | Must include exactly the requested markdown files under the target development directory. |
| Runtime-owned artifacts | Runtime runner | Runtime validation and compatibility surface | Must not be written directly by the invoke design run. |

## Assumptions

- The runtime runner will copy or write requested output and runtime result artifacts outside this command-owned design work.
- File existence is sufficient evidence for this fixture because the fixture objective is artifact reproduction.
- The target directory is intentionally local to `framework/runtime/development/fixtures/invoke-design-artifacts/target/development/`.

## Open Risks

| Risk ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| R-ARCH-1 | Future validation may require content assertions beyond file existence. | medium | Keep section headers and invoke result fields stable enough for later grep-based checks. |
| R-ARCH-2 | Runtime and command artifact ownership could drift. | medium | Preserve explicit "no direct runtime writes" language in INVOKE-DESIGN.md and DESIGN-TRANSPORT.md. |

## Unresolved Decisions

| Decision | Options | Current Status |
| --- | --- | --- |
| Whether to add semantic content validation for the four artifacts. | file existence only, required headings, full schema | deferred |

## Planning Notes

- Direct implementation constraints: only command-owned fixture artifacts should be authored by invoke design.
- Boundary rules: runtime `RESULT.md`, `RUN.json`, `STATUS.json`, `events.jsonl`, adapter profile files, and requested output copying are runner-owned.
- Testability implications: validation can remain a short shell check over the four expected paths.

## Handoff Targets

- Deferred follow-up if runtime validation later needs richer content checks.
- No implementation-plan or work-pack artifact is emitted by this design run.
