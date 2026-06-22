---
module: inventory-attachment-hook
version: draft
status: refinement-draft
updatedAt: 2026-06-21
docType: spec
---

# Specification: Inventory Attachment Hook

This development specification is non-authoritative until the listed canonical
sources are patched and generated mirrors are refreshed from those sources.

## Scope

This specification defines the policy envelope, handoff envelope, validation
rules, idempotency behavior, and acceptance tests for Inventory Attachment Hook.

## Policy Envelope

`inventoryAttachment` is optional. Absence means no Inventory attachment.

```yaml
inventoryAttachment:
  enabled: true
  required: false
  mode: ingest
  authority: candidate-read-model
  attachWhen:
    - meaningful-run
    - durable-output-present
  include:
    - changed-files
    - output-artifacts
    - durable-decisions
    - source-backed-claims
    - residues
    - validation-reports
  exclude:
    - secrets
    - credentials
    - private-user-prompts
    - transient-runtime-files
    - canonical-promotion-claims
  onFailure: warn
  promotion_owner: downstream-owner
  publicBoundary: inherit
```

## Policy Fields

| Field | Required | Allowed Values | Default | Meaning |
| --- | --- | --- | --- | --- |
| `enabled` | yes | `true`, `false` | `false` | Enables attachment for the capability/run. |
| `required` | no | `true`, `false` | `false` | Makes attachment failure block closeout when safe outputs were expected. |
| `mode` | yes when enabled | `ingest`, `backfill`, `sync` | `ingest` | Inventory operation requested by the handoff. |
| `authority` | yes when enabled | `candidate-read-model` | `candidate-read-model` | Prevents promotion confusion. |
| `attachWhen` | no | controlled trigger list | meaningful run and durable output | Conditions for attempting handoff. |
| `include` | no | controlled include classes | empty | Output classes eligible for selection. |
| `exclude` | no | controlled exclusion classes | safety exclusions | Output classes never selected. |
| `onFailure` | no | `warn`, `block`, `skip` | `warn` | Closeout behavior when the Inventory handoff fails. |
| `promotion_owner` | no | owner id or `none` | `downstream-owner` | Owner for any later promotion decision. Mirrors the existing Inventory `promotion_owner` vocabulary. |
| `publicBoundary` | no | `inherit`, `public-safe`, `private-only` | `inherit` | Boundary rule for selected outputs. |

## AttachWhen Values

| Value | Meaning |
| --- | --- |
| `meaningful-run` | Primary capability returned a useful pass/flag result or a residue-bearing block worth indexing. |
| `durable-output-present` | At least one stable artifact, changed file, decision, residue, or validation report exists. |
| `validation-attempted` | A validation check or reviewable validation note exists. |
| `residue-present` | The run produced an unresolved gap with an owner or next route. |
| `explicit-operator-request` | The user explicitly asked to inventory the run output. |

## Include Classes

| Class | Requirement |
| --- | --- |
| `changed-files` | file paths must be durable and inside allowed write scope |
| `output-artifacts` | artifact path, owner, status, and source refs when available |
| `durable-decisions` | decision text, decision owner, rejected alternatives, and source refs |
| `source-backed-claims` | claim plus source refs or explicit inference marking |
| `residues` | unresolved gap, owner, next route, and severity |
| `validation-reports` | validation command/check, result, artifact path, and residue |

## Exclusion Classes

The evaluator must reject or redact:

- secrets;
- credentials;
- raw full private prompts;
- private material crossing into a public output namespace;
- transient runtime files;
- source-less claims;
- canonical promotion claims;
- generated mirror contents that are not backed by canonical source refs.

## Handoff Envelope

```json
{
  "schema": "inventory-attachment-handoff/v0",
  "dispatch_id": "optional-dispatch-id",
  "invocation_id": "required-stable-run-id",
  "capability": {
    "id": "capability-id",
    "kind": "sigil|spell|skill",
    "source_ref": "canonical/source/path"
  },
  "policy": {
    "enabled": true,
    "required": false,
    "mode": "ingest",
    "authority": "candidate-read-model",
    "onFailure": "warn",
    "promotion_owner": "downstream-owner",
    "publicBoundary": "inherit"
  },
  "selected_outputs": [
    {
      "class": "output-artifacts",
      "ref": "path/to/artifact.md",
      "owner": "capability-id",
      "status": "pass|flag|block|draft",
      "source_refs": ["path:line"],
      "source_ref_strength": "strong|weak|none",
      "hash": "optional-content-hash",
      "idempotency_key": "inventory-attachment:<capability>:<invocation>:<output>:<hash>",
      "dedupe_confidence": "strong|weak",
      "public_boundary": "public-safe|private-only|inherit",
      "residue": []
    }
  ],
  "validation": {
    "status": "pass|flag|block|not_checked",
    "checks": ["command or reviewable check"],
    "residue": []
  },
  "non_authority_notice": "Inventory Attachment creates candidate read models only.",
  "requested_at": "ISO-8601 timestamp"
}
```

## Attachment Attempt Decision

No handoff envelope is created when the policy is absent or `enabled: false`.
That is a normal skip, not an invalid handoff.

Envelope validation applies only after an attachment attempt starts. If an
attempted envelope carries `enabled` as false or missing, the evaluator treats it
as malformed attachment input and skips or blocks according to `required` and
`onFailure`.

## Envelope Validation

Block the handoff before Inventory write when:

- `authority` is missing or not `candidate-read-model`;
- `mode` is outside `ingest`, `backfill`, or `sync`;
- `selected_outputs` is empty and `required: true`;
- an output is unsafe or crosses a public/private boundary;
- `public_boundary: inherit` cannot be resolved before a public-surface write;
- any selected output is missing `idempotency_key`;
- `non_authority_notice` is missing;
- the handoff requests promotion.

Flag, but do not block by default, when:

- source refs are weak but artifact refs are durable;
- content hash is unavailable;
- validation status is `not_checked`;
- optional `promotion_owner` is missing.

Weak source refs must lower confidence and create residue. A material claim
requires `source_refs`; otherwise it must be marked explicitly as `inference`,
`synthesis`, or `open-question`.

## Inventory Request Mapping

| Handoff Field | Inventory Use |
| --- | --- |
| `capability.id` | tag, source system, evidence producer |
| `capability.kind` | entry type routing |
| `selected_outputs[].class` | evidence-card or EvidenceSet classification |
| `selected_outputs[].ref` | source ref or artifact handle |
| `selected_outputs[].source_refs` | material evidence refs |
| `selected_outputs[].source_ref_strength` | confidence and residue routing |
| `selected_outputs[].status` | `pass` maps to higher confidence; `flag` or `block` maps to explicit residue |
| `selected_outputs[].residue` | evidence-card residue and follow-up owner |
| `validation.status` | evidence confidence and residue |
| `selected_outputs[].idempotency_key` | dedupe key |
| `non_authority_notice` | downstream packet boundary |
| `policy.promotion_owner` | Inventory `promotion_owner` |

## Evidence-Card And EvidenceSet Mapping

Selected outputs become evidence-cards first. EvidenceSets may only group
evidence-card IDs; they must not copy source excerpts, summaries, or trace
arrays from the cards.

| Inventory Record Field | Source |
| --- | --- |
| evidence-card id | generated from capability id, output ref, and idempotency key |
| `source_refs` | `selected_outputs[].source_refs` |
| authority state | `candidate-read-model` plus `non_authority_notice` |
| captured metadata | capability id, invocation id, output class, status, hash, validation status |
| `promotion_owner` | `policy.promotion_owner` or downstream owner default |
| `trace` | dispatch id, invocation id, output ref, validation checks |
| `residue` | output residue plus validation residue |
| EvidenceSet included IDs | evidence-card IDs created or selected by the handoff |
| EvidenceSet excluded IDs | skipped/deduped/rejected card IDs, when known |
| EvidenceSet synthesis note | short non-authority summary of the grouped evidence |

## Idempotency Rules

1. Compute one idempotency key per selected output.
2. Prefer content hash over modification time.
3. If the same key already exists, skip the write and record `deduped`.
4. If a weaker key is used, write `dedupeConfidence: weak`.
5. Never dedupe across different capability owners unless the source refs and
   content hash match exactly.

## Public Boundary Resolution

`publicBoundary: inherit` resolves in this order:

1. selected output metadata;
2. source capability boundary declaration;
3. repository boundary configuration;
4. target namespace owner policy.

If resolution is still `inherit` and the destination is public, block the write.
If the destination is private, flag the unresolved boundary and record residue.

## Recursion Guard

Do not attach attachment operations.

Skip any invocation or output where:

- `source_kind` is `inventory-attachment-operation`;
- output refs are hook-operation, failure, or dedupe rows;
- output refs are Inventory records created by the same attachment operation;
- an envelope already has `inventoryAttachmentResult`;
- the candidate output would cause Inventory to inventory its own attachment
  write without a separate operator request.

## Failure Rules

| Condition | `onFailure: skip` | `onFailure: warn` | `onFailure: block` |
| --- | --- | --- | --- |
| Inventory unavailable | skip and record hook operation | warn and continue | block closeout |
| invalid handoff | skip invalid outputs | warn unless required | block |
| unsafe output | skip output | warn if requested | block if required output |
| duplicate key | dedupe skip | dedupe skip | dedupe skip |
| observability unavailable | follow observability policy | follow observability policy | block only in strict telemetry mode |

## Observability Requirements

The post-run closeout should record:

- attachment policy status: absent, disabled, enabled, required;
- attachment result: attached, skipped, deduped, warned, blocked, failed;
- Inventory request mode;
- selected output count;
- rejected output count;
- idempotency keys or dedupe summary;
- public-boundary result;
- Inventory artifacts written or skipped reason;
- residue and next route.

Hook operation rows must not trigger another observer pass.

## Observed Invocation Loop Insertion Point

The Inventory attachment phase belongs after observed invocation envelope
assembly and primary telemetry handling, before final closeout:

```text
resolve capability
  -> execute primary capability
  -> assemble observed invocation envelope
  -> append or skip primary telemetry through signal-observer
  -> evaluate inventoryAttachment policy
  -> hand selected outputs to Inventory or record skipped/deduped/warned/blocked
  -> write hook-operation/failure/dedupe row with observe false
  -> return closeout with primary result, observability status, and attachment status
```

## Canonical Edit Requirements

Implementation must update canonical sources first:

1. `arcanum/arcana/inventory/SKILL.md`;
2. optional `arcanum/arcana/inventory/README.md`;
3. `arcanum/arcana/sigil-development/SKILL.md`;
4. `arcanum/arcana/spellcraft/SKILL.md`;
5. `arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md`;
6. `arcanum/spells/observed-invocation-loop/README.md`;
7. templates under Inventory development or template roots.

Generated `.agents/skills/*` mirrors are refreshed only after canonical edits.
When `arcanum/spells/observed-invocation-loop/README.md` changes, the generated
Observed Invocation Loop mirror is part of the required regeneration scope.

## Acceptance Tests

| Test ID | Scenario | Expected Result |
| --- | --- | --- |
| IAH-001 | no `inventoryAttachment` policy | attachment skipped, primary run unaffected |
| IAH-002 | `enabled: false` | attachment skipped with optional telemetry |
| IAH-003 | enabled with one durable public-safe artifact | Inventory candidate evidence/index/log request produced |
| IAH-004 | enabled with private prompt output | output rejected before Inventory write |
| IAH-005 | duplicate idempotency key | deduped skip recorded |
| IAH-006 | Inventory write fails with `onFailure: warn` | primary closeout continues with warning and hook failure row |
| IAH-007 | Inventory write fails with `onFailure: block` | closeout blocks with exact failure |
| IAH-008 | handoff requests ontology/definition promotion | validation blocks |
| IAH-009 | generated mirror changes not regenerated from canonical source | validation flags or blocks release |
| IAH-010 | pilot attached invocation | later Inventory lookup finds evidence by capability, output ref, and residue |

## Validation Commands

After implementation, run:

```bash
rg -n "inventoryAttachment|candidate-read-model|Inventory Attachment|onFailure" arcanum/arcana arcanum/framework arcanum/spells
git diff --check -- arcanum/arcana/inventory arcanum/arcana/sigil-development arcanum/arcana/spellcraft arcanum/framework/observability arcanum/spells/observed-invocation-loop .agents/skills
```

Add fixture/schema checks for:

- controlled `attachWhen`, include, exclude, mode, and failure values;
- required `source_refs` or explicit inference/synthesis/open-question marking;
- `non_authority_notice`;
- per-output `idempotency_key`;
- public-boundary inheritance resolution;
- EvidenceSet references to evidence-card IDs only.

When generated mirrors are touched, validate with the repository bootstrap path
instead of hand-editing generated packages.

## Promotion Gate

Inventory Attachment is implementation-ready only when:

- policy and handoff templates exist;
- canonical docs define the contract;
- observed invocation handoff semantics are documented;
- generated mirrors can be refreshed;
- acceptance tests have a pilot path;
- no direct promotion authority is claimed.
