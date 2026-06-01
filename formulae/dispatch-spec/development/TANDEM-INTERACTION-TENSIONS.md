# Tandem Arcanum Interaction Tensions

Status: synthesis from six-agent research fanout.

## Core Tension

Arcanum and Tandem both use governance language, but they govern different things.

- Arcanum governs **capability meaning and lifecycle**: when a reusable behavior is well-scoped, validated, observable, promotable, and owned.
- Tandem governs **runtime authority and evidence**: who can act, what they can see, which tools can run, when approvals are needed, what artifacts survive, and what audit trail exists.

The integration should preserve that difference instead of flattening it.

## Complementary Approaches

1. Capability contract plus runtime enforcement

   Arcanum provides capability contracts and lifecycle boundaries. Tandem can execute a projection of those contracts with tool, workspace, memory, and approval enforcement. Evidence: Arcanum positions sigils as reusable capabilities with use/non-use, reasoning, failure, output, observation, and evolution (`README.md:31`); Tandem explicitly says prompts are not permissions and runtime controls must sit below the model (`/tmp/frumu-ai-tandem/README.md:48`).

2. Artifact governance plus artifact validation

   Arcanum requires reviewable artifacts, quality bars, observability, and promotion evidence. Tandem enforces artifact contracts, concrete paths, read/citation proof, stale-state handling, and retries. Evidence: Arcanum experiment harness validates reusable spells/sigils before promotion (`README.md:66-81`); Tandem workflow runtime rejects unsupported claims and unresolved path/citation mismatches (`/tmp/frumu-ai-tandem/docs/WORKFLOW_RUNTIME.md:29-39`).

3. Lifecycle routing plus run lifecycle

   Arcanum routes outputs to lifecycle owners such as Spellcraft, Sigil Development, Task Session, Experiment Harness, or Decision Gate. Tandem owns run/session lifecycle through engine endpoints and event streams. Evidence: Arcanum method routes next owner (`framework/CYBERALCHEMY-METHOD.md:90-94`); Tandem run lifecycle uses session/run HTTP and SSE contracts (`/tmp/frumu-ai-tandem/docs/ENGINE_COMMUNICATION.md:96-107`).

4. Repository evidence plus runtime receipts

   Arcanum observability records reusable capability signals and reflection triggers. Tandem can provide operational receipts: run IDs, approval evidence, audit rows, artifacts, and validation outcomes. Evidence: Arcanum central ledger is the source of truth for observed sigil signals (`framework/observability/README.md:33-49`); Tandem correlation fields include `correlation_id`, `session_id`, and `run_id` (`/tmp/frumu-ai-tandem/docs/ENGINE_COMMUNICATION.md:121-131`).

5. Human gates plus approval endpoints

   Arcanum can decide when a human decision is required for lifecycle or blocker ambiguity. Tandem can operationalize permission/question/approval pauses in a runtime. Evidence: Task Session blocks before mutation on gate failure (`arcana/task-session/SKILL.md:101-105`); Tandem exposes pending permission/question reply endpoints (`/tmp/frumu-ai-tandem/docs/ENGINE_COMMUNICATION.md:109-119`).

## Divergent Approaches

1. Source lifecycle vs deployment/runtime lifecycle

   Arcanum asks whether a capability should exist, be promoted, changed, observed, or retired. Tandem asks whether a concrete run/action is allowed, tenant-safe, auditable, and valid.

2. Repository-local governance vs engine-owned state

   Arcanum installs `.arcanum/` observability/runtime/necronomicon state into a target repository. Tandem owns shared runtime storage and workspace namespaces such as `.tandem/plans`, `.tandem/skill`, and engine `/skills*`. The state roots should remain separate.

3. Semantic promotion vs memory promotion

   Arcanum Inventory/Ontology promotion decides meaning and authority. Tandem memory promotion changes runtime memory visibility/status. A Tandem memory promotion must not become an Arcanum ontology or registry promotion automatically.

4. Post-run observability vs runtime enforcement

   Arcanum observer scripts validate envelopes and append central ledger rows after or around runs. Tandem runtime policy actively scopes tools, denies unoffered calls, pauses for permission, and records tool effect/audit events during execution.

5. Human approval meanings

   Arcanum approval can mean "this design/lifecycle route is valid". Tandem approval can mean "this runtime action is authorized". Both may be true or false independently.

## Overlaps Requiring Decisions

| Overlap | Decision Needed |
| --- | --- |
| Gates | Which Arcanum gates map to Tandem approvals, and which remain lifecycle-only? |
| Artifacts | Which Tandem validated artifacts count as Arcanum task completion evidence, experiment evidence, or only runtime receipts? |
| Capability registry | Does Tandem consume Arcanum registries directly, or a generated projection pack? |
| Memory/evidence | Are Tandem memory records allowed to create Arcanum inventory candidates, or only linked as runtime evidence? |
| Runtime adapter | Does Tandem become a Task Session adapter first, or a dispatch-spec compiler target first? |

## Tensions

### T1: Runtime Approval Is Not Lifecycle Promotion

Layer A: Tandem can approve or deny runtime actions, and it records operational evidence.

Layer B: Arcanum promotion requires lifecycle evidence and owner review before registry/canonical changes.

Impact: High. If blurred, a successful Tandem run could accidentally promote unvalidated sigils/spells or ontology facts.

Resolution: Tandem approvals may satisfy Arcanum runtime-execution gates, but not promotion gates. Promotion remains with Sigil Development, Spellcraft, Ontology Vault, Inventory, or other Arcanum owners.

### T2: Dispatch/Spell Shape Is Not Tandem Plan Shape

Layer A: Arcanum dispatch documents and spells describe capability references, patterns, gates, handoffs, and owner boundaries.

Layer B: Tandem workflow plans describe runtime tasks, dependencies, output contracts, agent roles, connector requirements, approval policy, and runtime projection.

Impact: High. Direct import would cause schema and authority confusion.

Resolution: Use a projection layer: Arcanum route metadata becomes Tandem plan metadata and runtime tasks only after validation.

### T3: Observability Ledgers Are Not Audit Logs

Layer A: Arcanum observability records behavior signals for reflection and capability maintenance.

Layer B: Tandem audit/tool ledgers prove runtime actions, approvals, denials, and effects.

Impact: Medium-high. Duplicating or substituting one for the other would weaken both.

Resolution: Link receipts by ID, summarize across boundary, and preserve each system's source of truth.

### T4: Local Adaptation vs Single Engine Authority

Layer A: Arcanum supports repository-local installation, local adaptations, and generated command adapters while preserving canonical source.

Layer B: Tandem centralizes runtime truth in one engine and shared state root for clients.

Impact: Medium. State drift is likely if `.arcanum/` and `.tandem/` write the same conceptual fields.

Resolution: Keep `.arcanum/` and `.tandem/` separate; define explicit import/export artifacts.

### T5: Semantic Evidence vs Operational Evidence

Layer A: Arcanum evidence supports claims about concept quality, task completion, reusable behavior, or ontology meaning.

Layer B: Tandem evidence supports claims about what happened during a run and whether runtime contracts were satisfied.

Impact: Medium. The two evidence types can strengthen each other, but neither fully replaces the other.

Resolution: Define evidence classes in the bridge: `runtime_receipt`, `task_completion_evidence`, `experiment_evidence`, `semantic_candidate`, `promotion_record`.

## Human Gate

The research supports a next decision, not implementation yet.

Recommended decision: start with a **Tandem Task Session runtime adapter design** plus a **field-level crosswalk**. Defer actual execution until the adapter can name required input, Tandem command/API shape, output receipt shape, and authority boundaries.
