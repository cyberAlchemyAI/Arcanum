---
module: inventory-attachment-hook
version: draft
status: refinement-draft
updatedAt: 2026-06-21
docType: architecture
---

# Architecture: Inventory Attachment Hook

This development architecture is non-authoritative until the listed canonical
sources are patched and generated mirrors are refreshed from those sources.

## Purpose

Inventory Attachment Hook lets selected sigils and spells shorten future search
by sending durable run outputs to Inventory as candidate evidence.

The architecture is explicit, opt-in, and authority-bounded. It adds a governed
handoff from observed invocation evidence to Inventory read models; it does not
create a new promotion path.

## Core Unit

`AttachedInventoryHandoff`

Responsibility: convert one meaningful attached invocation into one validated
Inventory candidate-evidence request.

## Architecture Principles

1. Attachment is explicit.
2. Inventory writes candidate read models only.
3. Observability sees the run before Inventory receives the selected outputs.
4. Source artifacts remain owned by their source capability.
5. Generated runtime mirrors are refreshed from canonical source only.
6. Promotion into definitions, ontology, constitutions, axioms, disciplines,
   sigils, or spells requires a separate owner route.
7. Failure warns by default and blocks only when attachment is declared required.

## Components

| Component | Owner | Responsibility | Writes |
| --- | --- | --- | --- |
| Attachment Policy | Inventory with Sigil Development and Spellcraft consumers | Declares whether attachment is enabled, what to include/exclude, mode, authority, and failure behavior. | canonical docs/templates first |
| Durable Output Selector | invoking sigil/spell | Names output artifacts, changed files, decisions, residues, validation reports, and source-backed claims eligible for handoff. | invocation envelope fields |
| Observed Invocation Envelope | Observed Invocation Loop and observability framework | Captures request summary, selected capability, outputs, validation, quality status, and hook metadata after primary execution. | `.arcanum/observability/` |
| Attachment Evaluator | Observed Invocation Loop | Checks policy, meaningful-run status, output presence, exclusion classes, public-boundary safety, and idempotency. | hook operation status |
| Inventory Handoff Envelope | Observed Invocation Loop to Inventory | Carries selected safe refs and metadata into Inventory mode routing. | handoff artifact or direct request |
| Inventory Request Handler | Inventory | Creates or refreshes candidate evidence-card, EvidenceSet, index, tag, and log entries. | `.arcanum/inventory/` |
| Telemetry/Hook Operation Recorder | observability framework | Records whether observation and Inventory attachment happened, skipped, deduped, warned, or blocked. | `.arcanum/observability/` |
| Generated Runtime Propagation | bootstrap/runtime generation | Carries attachment metadata into installed native packages after canonical source changes. | `.agents/skills/`, `.codex/skills/`, other generated surfaces |

## Data Flow

```text
sigil/spell primary run
  -> durable outputs and validation result
  -> observed invocation envelope
  -> primary telemetry append or skipped reason
  -> attachment policy lookup
  -> eligibility, exclusion, and idempotency checks
  -> Inventory handoff envelope
  -> Inventory ingest/backfill/sync request
  -> candidate evidence/index/log writes
  -> telemetry and hook-operation closeout
```

## Runtime Order

| Step | Actor | Gate | Outcome |
| --- | --- | --- | --- |
| 1 | primary sigil/spell | capability completes or blocks | primary result exists or closeout reports blocker |
| 2 | Observed Invocation Loop | enough evidence to assemble envelope | observed invocation envelope |
| 3 | Signal Observer | primary result can be observed | primary telemetry append or skipped reason |
| 4 | Attachment Evaluator | policy exists and `enabled: true` | attach, skip, warn, or block |
| 5 | Attachment Evaluator | output refs are durable and safe | selected output refs |
| 6 | Attachment Evaluator | idempotency key not already handled | new handoff or deduped skip |
| 7 | Inventory | requested mode is allowed | candidate evidence/index/log update |
| 8 | observability | closeout status known | telemetry and hook operation row |

## State Namespaces

| Namespace | Owner | Write Policy |
| --- | --- | --- |
| `arcanum/arcana/inventory/` | Inventory canonical source | Attachment contract and templates are patched here first. |
| `arcanum/arcana/sigil-development/` | Sigil Development canonical source | Sigil authoring guidance consumes the policy contract. |
| `arcanum/arcana/spellcraft/` | Spellcraft canonical source | Spell authoring guidance consumes the policy contract. |
| `arcanum/framework/observability/` | observability framework | Shared envelope/failure semantics and hook-operation guidance. |
| `arcanum/spells/observed-invocation-loop/` | Observed Invocation Loop | Runtime handoff sequence and generated marker requirements. |
| `.agents/skills/` | bootstrap/runtime generation | Regenerated mirror only, no hand-edited authority. |
| `.arcanum/inventory/` | Inventory read model | Candidate evidence-card, EvidenceSet, index, tag, and log writes. |
| `.arcanum/observability/` | observability package | Telemetry, hook operations, dedupe, failure rows, and rebuildable indexes. |

## Authority Split

| Authority Class | Owner |
| --- | --- |
| Lifecycle contract | Inventory for attachment policy, Sigil Development and Spellcraft for authoring guidance, Observed Invocation Loop for runtime handoff. |
| Runtime execution | Observed Invocation Loop or installed runtime hook/wrapper. |
| Evidence writes | Inventory for candidate evidence; observability for telemetry and hook operations. |
| Validation | Dispatch Spec for route shape; Inventory/observability for local artifact validation. |
| Memory/read-model visibility | Inventory generated pages and indexes. |
| Promotion | downstream governance owner through a separate route. |

## Failure Semantics

| Failure | Default Behavior | Blocking Behavior |
| --- | --- | --- |
| policy missing | skip attachment | never blocks |
| `enabled: false` | skip attachment | never blocks |
| no durable outputs | skip with residue | block only if `required: true` |
| unsafe/private output | skip output and warn | block if all required outputs are unsafe |
| idempotency duplicate | dedupe skip | never blocks |
| Inventory write fails | warn and record hook failure | block only when `onFailure: block` or `required: true` |
| observability write fails | warn per observability policy | block only in strict telemetry mode |

## Idempotency

The idempotency key should be deterministic:

```text
inventory-attachment:
  <capability-id>:
  <invocation-id-or-dispatch-id>:
  <output-ref>:
  <content-hash-or-mtime-token>
```

Idempotency is per selected output. A multi-output handoff can partially dedupe:
one output may be skipped as a duplicate while another is written as new
candidate evidence.

When content hash is unavailable, use a weaker key and mark the Inventory record
as `dedupeConfidence: weak`.

## Recursion Guard

Inventory attachment operations must not themselves become attached runs.

The evaluator skips any envelope where:

- `capability.id` is `inventory`;
- `source_kind` is `inventory-attachment-operation`;
- the output ref is under `.arcanum/inventory/` and was produced by the same
  attachment operation;
- the output ref is under `.arcanum/observability/hooks/`;
- the envelope already carries `inventoryAttachmentResult`.

Hook operation rows, failure rows, dedupe rows, and Inventory records created by
the attachment must carry `observe: false` or an equivalent non-recursive marker
when they pass through observability infrastructure.

## Privacy And Public Boundary

The Attachment Evaluator must exclude:

- secrets and credentials;
- raw full private prompts;
- transient runtime files;
- private parent-repo material when writing into public Arcanum surfaces;
- source text without a stable source ref;
- statements that imply canonical promotion.

Safe records may summarize a private run only when the output target is private
or the summary is explicitly public-boundary safe.

`publicBoundary: inherit` is resolved from the source capability, output
artifact, or repository boundary declaration before any write. If the evaluator
cannot resolve `inherit` to `public-safe` or `private-only`, it blocks writes to
public output namespaces and records residue.

## Generated Mirror Strategy

Canonical source changes come first:

1. Inventory contract;
2. Sigil Development guidance;
3. Spellcraft guidance;
4. observability/Observed Invocation Loop handoff semantics;
5. templates;
6. bootstrap/runtime regeneration.

Generated skill packages are not patched by hand except as temporary diagnostic
evidence. The final implementation should use the existing bootstrap/generator
path. When Observed Invocation Loop canonical docs change, its generated mirror
is in scope for regeneration rather than optional.

## Minimal Implementation Interfaces

### Attachment Policy

Defined by source capabilities and later copied into generated runtime metadata.

### Handoff Envelope

Produced after observed invocation envelope assembly and before Inventory write.

### Inventory Request

Consumed by Inventory in `ingest`, `backfill`, or `sync` mode.

### Hook Operation Receipt

Recorded whether attachment was attached, skipped, deduped, warned, blocked, or
failed.

## Acceptance Architecture

The architecture is ready for implementation when:

- authors can declare attachment without ambiguity;
- runtime can decide attach/skip/block from the envelope alone;
- Inventory can reject unsafe or authority-confused requests;
- observability can report attachment status without causing recursive
  observation;
- generated mirrors can be regenerated from canonical source;
- a pilot run produces lookup evidence and does not promote it.
