# Tandem Arcanum Integration Options

Status: ranked options after whole-system research.

## Recommendation

Start with **Option 1: Task Session Runtime Adapter Spec** and support it with **Option 2: Dispatch/Plan Crosswalk**.

This is the smallest credible proof because Task Session already has an adapter boundary that preserves Arcanum authority, while Tandem already has engine/session/run and artifact-contract surfaces that can return execution evidence.

## Option 1: Tandem Task Session Runtime Adapter Spec

Rank: 1

Goal:

Define `runtime_id=tandem` as a Task Session adapter candidate. It consumes one selected Arcanum task/SWU with a strict context-builder handoff pack and returns Tandem runtime receipts.

Why first:

- Arcanum Task Session already requires selected task/SWU, strict context handoff, write scope, validation, fallback rules, result evidence, and ownership boundary (`arcana/task-session/runtime-adapters/README.md:18-42`).
- Tandem already exposes session/run endpoints, event streams, permission/question endpoints, and health checks (`/tmp/frumu-ai-tandem/docs/ENGINE_COMMUNICATION.md:47-59`, `:109-119`).

Proof artifact:

- `arcana/task-session/runtime-adapters/tandem.md` design only, no execution code yet.

Minimum input contract:

- selected task/SWU id,
- handoff Markdown path plus JSON/index path,
- strict coverage status,
- bounded write scope,
- validation command/surface,
- fallback exploration policy,
- required approvals and protected actions,
- Arcanum owner boundaries.

Minimum Tandem result evidence:

- engine URL/state root used,
- `session_id`, `run_id`, event stream attachment,
- permissions/questions asked and answers,
- artifacts read/written with concrete paths,
- validation results and failures,
- tool/audit ledger references,
- final run status and retry/repair notes.

Gate:

Block if the adapter cannot produce a receipt shape that Task Session can review without reading raw transcript prose.

## Option 2: Dispatch/Plan Crosswalk

Rank: 2

Goal:

Map Arcanum `dispatch.schema.yml` fields to Tandem plan package / workflow projection concepts.

Why useful:

- Arcanum dispatch validates route shape but does not execute (`formulae/dispatch-spec/README.md:47-59`).
- Tandem plan compiler owns mission/workflow planning, draft lifecycle, runtime projection IR, output-contract seeds, and host traits (`/tmp/frumu-ai-tandem/crates/tandem-plan-compiler/README.md:22-29`).

Proof artifact:

- `formulae/dispatch-spec/development/TANDEM-DISPATCH-PLAN-CROSSWALK.md`.

Gate:

Every field must be marked `direct`, `metadata-only`, `requires-translation`, `no-equivalent`, or `Tandem-owned`.

## Option 3: Runtime Evidence Bridge

Rank: 3

Goal:

Define how Tandem runtime receipts become Arcanum observability or task-session evidence without becoming canonical knowledge.

Why useful:

- Arcanum central observability ledger records capability signals and reflection triggers.
- Tandem has structured logs, correlation/session/run IDs, tool effect ledgers, approval receipts, artifacts, and validation outcomes.

Proof artifact:

- `framework/observability/development/TANDEM-RUNTIME-EVIDENCE-BRIDGE.md`.

Gate:

Do not duplicate full Tandem state into `.arcanum/observability/`; store summary and stable receipt references.

## Option 4: Experiment Harness Hosted In Tandem

Rank: 4

Goal:

Run Arcanum experiment-harness prompts through Tandem workflows so Tandem supplies attempt validation, retries, concrete path enforcement, and runtime logs.

Why later:

This becomes valuable after the adapter receipt shape is known. Without that, harness evidence and runtime evidence will blur.

Proof artifact:

- one toy harness profile using Tandem as execution host.

Gate:

Experiment Harness owns promotion evidence interpretation; Tandem owns run evidence only.

## Option 5: Arcanum Capability Pack For Tandem

Rank: 5

Goal:

Export selected Arcanum sigil/spell metadata into a Tandem-consumable catalog or skill pack.

Why later:

It risks catalog drift and lifecycle confusion unless the adapter/crosswalk first defines which fields remain Arcanum-owned.

Proof artifact:

- generated projection for one low-risk sigil and one spell.

Gate:

No copied sigil internals unless the projection explicitly records source version, owner, and non-authority status.

## Rejected For Now

| Path | Reason |
| --- | --- |
| Treat every sigil as a Tandem workflow step | Loses lifecycle semantics and makes capability contracts look like runtime tasks. |
| Treat every spell as a Tandem workflow plan | Spells are composition contracts; Tandem plans are runtime/compiler artifacts. |
| Auto-import Arcanum into `.tandem/skill` | Confuses install surface with lifecycle integration and risks stale copied contracts. |
| Let Tandem runtime success update Arcanum registries | Runtime success is not promotion evidence by itself. |
| Mirror Tandem audit logs into Arcanum observability | Duplicates runtime authority; use receipt links and summaries. |
| Wrap Arcanum shell commands to bypass Tandem policy | Violates Tandem's purpose as runtime authority below the model. |

## First Work-Pack Candidate

Task ID: `TANDEM-ADAPTER-DESIGN-001`

Objective:

Design a Tandem runtime adapter contract for Arcanum Task Session without implementation.

Deliverables:

- `arcana/task-session/runtime-adapters/tandem.md`
- optional `formulae/dispatch-spec/development/TANDEM-DISPATCH-PLAN-CROSSWALK.md`
- validation checklist proving no authority collapse

Done criteria:

- names input contract, transformation, handoff shape, result evidence, ownership boundary, and blocked fallback;
- cites Tandem endpoints/state/evidence surfaces;
- preserves Arcanum owner boundaries;
- marks Tandem as runtime host, not lifecycle owner;
- identifies at least one toy proof task and required receipt fields.
