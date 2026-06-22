---
module: inventory-attachment-hook
version: draft
status: refinement-draft
updatedAt: 2026-06-21
docType: runtime-integration-design
---

# Runtime Integration Design: Inventory Attachment Hook

This design turns the runtime model into implementation-ready boundaries without
implementing hook scripts in this refine run.

## Design Target

Make Inventory Attachment Hook work for chat-invoked managed Arcanum skills and
spells across Codex, Claude Code, and generic runtimes.

## Non-Goals

- Do not design VS Code, Cursor, editor panel, or command-palette UX.
- Do not promote Inventory candidate evidence into canonical definitions,
  ontology, constitutions, axioms, disciplines, sigils, or spells.
- Do not hand-edit generated runtime mirrors as authority.
- Do not require every skill to attach Inventory evidence.

## Shared Runtime Interface

### Input

```yaml
invocation:
  capability:
    id: string
    kind: skill | sigil | spell
    source_ref: string
  request:
    summary: string
  execution:
    status: completed | partial | blocked | failed
    outputs: []
    files_changed: []
    validation: []
  inventoryAttachment:
    enabled: false
```

### Output

```yaml
closeout:
  primary_status: completed | partial | blocked | failed
  observability:
    status: recorded | deduped | skipped | failed | unavailable
    envelope_ref: string | null
  inventoryAttachment:
    policy_status: absent | disabled | enabled | required
    result: not_attempted | attached | skipped | deduped | warned | blocked | failed
    selected_output_count: number
    rejected_output_count: number
    artifacts: []
  residue: []
```

### No-Native-Hook Fallback Receipt

Runtimes without native hook APIs must emit this receipt instead of relying on
agent memory:

```yaml
fallbackReceipt:
  receipt_kind: native-hook | native-receipt | deterministic-wrapper | manual-fallback
  hook_enforcement: native | wrapper | fallback | unavailable
  capability:
    id: string
    kind: skill | sigil | spell
    source_ref: string
  invocation_id: string
  primary_result_preserved: true
  primary_status: completed | partial | blocked | failed
  artifacts: []
  validation: []
  observability:
    status: recorded | deduped | skipped | failed | unavailable
    reason: string | null
  inventoryAttachment:
    status: not_attempted | attached | skipped | deduped | warned | blocked | failed
    reason: string | null
  blockers: []
  residue: []
  handoff_note: string
```

This receipt is a valid design fallback, but it is `flag` proof unless backed by
a deterministic wrapper or native runtime event.

## Insertion Point

Inventory Attachment runs after primary telemetry handling and before final
closeout:

```text
primary capability result
  -> observed invocation envelope
  -> telemetry append or explicit skip
  -> inventoryAttachment evaluation
  -> Inventory candidate handoff
  -> closeout receipt
```

This order is mandatory because Inventory Attachment depends on the observed
envelope and must not hide telemetry failure.

## Codex Design

### Current State

- `.agents/skills/` is the native Codex skill discovery surface.
- `.codex/hooks/arcanum-user-prompt-submit.sh` currently recognizes
  command-shaped prompts by looking in `.codex/commands/`.
- `.codex/hooks/arcanum-stop.sh` closes pending envelopes and calls the observer
  path when a pending envelope exists.

### Required Design Move

Add a skill-aware observation bridge for explicit chat skill tokens:

```text
UserPromptSubmit
  -> detect first token `$<skill-name>`
  -> resolve `.agents/skills/<skill-name>/SKILL.md`
  -> read generated package metadata or canonical source frontmatter
  -> open pending envelope with `capability.kind`
  -> use the same PostToolUse and Stop closeout mechanics for skill runs
```

### Codex Validation

Future implementation should validate:

```bash
jq empty .codex/hooks.json
bash -n .codex/hooks/arcanum-user-prompt-submit.sh
bash -n .codex/hooks/arcanum-post-tool-use.sh
bash -n .codex/hooks/arcanum-stop.sh
```

Add a fixture where prompt `$inventory test attach` opens an envelope from
`.agents/skills/inventory/SKILL.md` without requiring a `.codex/commands`
adapter.

Codex runtime acceptance remains `flag` until that fixture proves explicit
`$skill-name` chat invocation produces deterministic closeout evidence on its
own.

## Claude Code Design

### Current State

- `.claude/skills/` mirrors generated native skill packages.
- `.claude/agents/arcanum-stage-worker.md` defines a bounded stage worker
  receipt with status, artifacts, validation, observer status, blockers, and
  handoff note.
- Bootstrap generation maps Codex-oriented tool names into Claude equivalents.

### Required Design Move

Claude Code should project the shared contract through native skill receipts,
not Codex Stop hooks:

```text
chat/native skill request
  -> generated Claude skill package
  -> parent agent or arcanum-stage-worker runs bounded stage
  -> receipt names primary status, artifacts, validation, blockers, residue
  -> observer/attachment adapter builds the shared closeout envelope
```

### Claude Validation

Future implementation should validate:

```bash
test -f .claude/skills/observed-invocation-loop/README.md
test -f .claude/agents/arcanum-stage-worker.md
rg -n "status, artifacts, validation, observer status" .claude/agents/arcanum-stage-worker.md
```

The receipt is valid when it can be transformed into the shared runtime
interface without requiring Codex-specific hook fields.

Claude lane acceptance gates:

| Gate | Required Evidence |
| --- | --- |
| native skill surface | `.claude/skills/<capability>/` regenerated from canonical source |
| bounded worker receipt | `.claude/agents/arcanum-stage-worker.md` receipt fields are satisfied |
| no nested model CLI | receipt states native skill/subagent execution, not `claude` or `codex exec` |
| observer status | recorded, skipped, failed, or unavailable reason is explicit |
| attachment status | not_attempted, attached, skipped, deduped, warned, blocked, or failed |

Claude implementation remains `flag` until native receipt or wrapper evidence
proves closeout rather than prose-only reporting.

## Generic Runtime Design

### Current State

`.arcanum/runtime/config.json` enables `native-skill`, `codex-skill`,
`claude-skill`, `local-skill`, and `dry-run` adapters.

### Required Design Move

Generic runtimes should implement a deterministic wrapper contract:

```text
resolve capability
  -> execute or hand off native prompt
  -> collect declared receipt fields
  -> build observed envelope
  -> call observer append authority when available
  -> evaluate Inventory Attachment
  -> write closeout receipt
```

If the runtime cannot append telemetry, it must return `observability.status:
unavailable` or `skipped` with a reason. It may still preserve the primary result
unless strict mode or required attachment says otherwise.

### Generic Validation

Future implementation should validate:

```bash
jq empty .arcanum/runtime/config.json
tools/arcanum --resolve inventory
```

Add a dry-run fixture that resolves a skill, emits a mock primary receipt, and
produces a closeout envelope without executing a model-backed CLI.

Generic implementation remains `flag` until the no-native-hook fallback receipt
schema is exercised by a fixture.

## Inventory Attachment Evaluation

Evaluation is host-neutral:

1. If policy is absent, return `not_attempted`.
2. If `enabled: false`, return `skipped`.
3. Validate `authority: candidate-read-model`.
4. Reject unsafe, private-to-public, transient, or source-less outputs.
5. Compute one idempotency key per selected output.
6. Hand selected outputs to Inventory in `ingest`, `backfill`, or `sync` mode.
7. Record `attached`, `skipped`, `deduped`, `warned`, `blocked`, or `failed`.

## Recursion Guard

Skip attachment when:

- capability id is `inventory` and the source kind is an attachment operation;
- the output is under `.arcanum/inventory/` and produced by the same attachment;
- the output is a hook operation, failure, or dedupe row;
- the envelope already has `inventoryAttachmentResult`.

Rows written by the attachment operation must carry an equivalent of
`observe: false`.

## Generated Mirror Strategy

Implementation should patch canonical sources first:

1. Inventory attachment policy and handoff contract.
2. Sigil Development and Spellcraft authoring guidance.
3. Observability and Observed Invocation Loop runtime semantics.
4. Templates and fixtures.
5. Bootstrap/runtime generation.
6. Generated mirrors.

Generated `.agents/skills/` and `.claude/skills/` packages are validation output,
not source authority.

## First Implementation Route

Recommended next route:

`task-session` on a bounded implementation unit:

```text
SWU-IAH-RUNTIME-001:
  Add skill-aware observation bridge design anchors and fixtures for explicit
  chat `$skill` invocation.

SWU-IAH-RUNTIME-002:
  Add generic no-native-hook fallback receipt schema and fixtures, then map the
  same receipt into Claude Code native stage-worker closeout.
```

Suggested write scope:

- canonical observability/OIL docs;
- hook or wrapper fixture scripts after contract approval;
- targeted generated mirrors only through bootstrap regeneration;
- no editor UI files.

## Design Verdict

`flag`: the design is ready for the next route, but implementation cannot claim
chat-skill attachment readiness until the direct `$skill-name` observation bridge
exists and passes a fixture.
