# Tandem Arcanum Crosswalk

Status: research synthesis from `arcanum-tandem-research-20260528`.

## Executive Finding

Arcanum and Tandem are complementary but sit at different authority layers.

Arcanum is a governed capability and lifecycle framework: it defines reusable sigils, composed spells, lifecycle routes, validation evidence, observability, and promotion guardrails. Tandem is a governed runtime: it owns sessions, runs, scoped tools, tenant context, approvals, artifacts, validation state, memory, and audit records.

The useful bridge is not "sigil equals Tandem step" or "spell equals Tandem workflow". The bridge should translate between Arcanum capability/lifecycle contracts and Tandem runtime/workflow projections while preserving separate authority.

## Source Anchors

| System | Anchor | Evidence |
| --- | --- | --- |
| Arcanum | Identity | `README.md:3-7` defines Arcanum as reusable agent capabilities through governed synthesis with method, lifecycle, quality bar, observability, and capability structure. |
| Arcanum | Capability model | `README.md:95-135` splits Formulae, Transmutations, Arcana, and spells; spells compose sigils without copying internals. |
| Arcanum | Lifecycle ownership | `README.md:137-149` routes define/design/plan, sigil lifecycle, spell lifecycle, implementation layering, and bounded execution to different owners. |
| Arcanum | Registry authority | `README.md:151-159`, `registry/SIGILS.md:87-101`, and `registry/SPELLS.md:29-39` require governed promotion before reusable listing. |
| Arcanum | Runtime adapters | `arcana/task-session/runtime-adapters/README.md:1-42` says adapters delegate execution without making the runtime the Arcanum contract. |
| Tandem | Identity | `/tmp/frumu-ai-tandem/README.md:27-40` defines Tandem as the runtime authority layer below the model. |
| Tandem | Engine shape | `/tmp/frumu-ai-tandem/ARCHITECTURE.md:1-31` defines an engine-owned workflow runtime with core/server/runtime/tools/memory/workflows crates. |
| Tandem | Runtime enforcement | `/tmp/frumu-ai-tandem/README.md:52-60` and `/tmp/frumu-ai-tandem/docs/ENGINE_COMMUNICATION.md:47-59` define governed execution, approvals, artifacts, audit trails, and session/run endpoints. |
| Tandem | Workflow contract | `/tmp/frumu-ai-tandem/docs/WORKFLOW_RUNTIME.md:27-65` defines artifact contracts, stale-state elimination, concrete paths, and self-healing workflow attempts. |
| Tandem | Plan portability | `/tmp/frumu-ai-tandem/docs/WORKFLOW_RUNTIME.md:85-113` defines `plan_package_bundle` as the portable workflow plan unit. |

## Concept Map

| Arcanum Concept | Tandem Nearest Neighbor | Fit | Translation Rule |
| --- | --- | --- | --- |
| Sigil | Skill, workflow step, routine, tool-capability entry | Partial | Treat sigil as a governed capability contract, not a Tandem step. Tandem may reference it by id and project it into runtime work. |
| Spell | Workflow plan, plan package, routine bundle | Partial | Treat spell as a composition contract over sigils. Tandem workflow may execute a projection, but Spellcraft keeps lifecycle authority. |
| Dispatch document | Workflow graph / plan preview input | Strong candidate | Use as route metadata or preview input. Do not assume dispatch JSON is a Tandem plan bundle. |
| Task Session | Runtime run / workflow execution | Strong candidate | Best first adapter boundary: strict handoff in, Tandem run evidence out, Task Session reviews completion. |
| Context pack | Runtime context projection / prompt input refs | Strong candidate | Arcanum context-builder supplies covered obligations; Tandem can enforce concrete paths and read evidence. |
| Work-pack / SWU | Plan task / workflow task | Partial | Work-pack tasks can become Tandem task objectives, but Arcanum keeps dependencies, done criteria, and sync obligations. |
| Experiment Harness | Workflow validation / eval run | Strong candidate | Tandem can host runs and provide attempt-level validation, but Arcanum owns promotion evidence interpretation. |
| Observability signal | Tool ledger / audit event / structured log | Partial | Link by IDs and summary receipts. Do not mirror all Tandem runtime state into Arcanum. |
| Inventory evidence-card | Memory item / knowledge item draft | Partial | Tandem memory validation can attach proof, but Arcanum evidence-card remains non-authority unless promoted. |
| Ontology Vault finding | Knowledge governance / memory promotion | Weak-partial | Keep separate; Tandem memory promotion is not Arcanum ontology promotion. |
| Promotion guardrail | Approval / policy / runtime validation | Partial | Arcanum promotion is lifecycle authority. Tandem approval is runtime authorization. Both may be required. |
| Human gate | Approval/question endpoint | Strong candidate | Map Arcanum decision gates to Tandem approvals only for runtime actions; preserve Arcanum decision record. |

## Complementary Surface

Arcanum can provide Tandem:

- reusable capability contracts with trigger conditions, non-use cases, quality bars, anti-patterns, and output contracts;
- spell composition semantics: shared state, gates, handoffs, failure policy, and observability;
- lifecycle decisions about whether a capability should exist, change, be promoted, or retire;
- research and synthesis methods for creating strong workflow/capability definitions.

Tandem can provide Arcanum:

- runtime-owned enforcement for tool visibility, write scope, tenant context, approvals, and protected actions;
- concrete run receipts: `session_id`, `run_id`, event stream, artifacts, validation results, approvals, and audit records;
- artifact-contract enforcement: concrete paths, citation/read verification, stale-state repair, and retry-aware validation;
- deployment substrate: local/headless/hosted/customer-infrastructure runtime surfaces.

## Divergence To Preserve

| Divergence | Why Preserve It |
| --- | --- |
| Arcanum lifecycle authority vs Tandem runtime authority | A runtime approval proves a run was allowed; it does not prove a sigil should be promoted. |
| Repository-local `.arcanum/` state vs engine/workspace `.tandem/` state | They have different ownership, retention, and drift risks. Use explicit handoff files or receipt links. |
| Arcanum semantic evidence vs Tandem operational evidence | Arcanum asks whether a capability remains meaningful and reusable; Tandem asks what happened and whether it was allowed/valid. |
| Markdown capability contracts vs typed runtime schemas | The bridge needs a typed projection rather than pretending the formats are interchangeable. |
| Agent role collaboration vs agent-team runtime coordination | Arcanum subagents are role-bound under a parent sigil; Tandem agent teams are runtime coordination primitives. |

## Bridge Candidate

The best initial bridge is a **Tandem Task Session runtime adapter spec** backed by a small **dispatch/work-pack crosswalk**.

Minimum input:

- selected Arcanum task/SWU or dispatch step,
- context-builder handoff pack with strict coverage,
- capability refs and owner boundaries,
- write scope and validation surface,
- gate mapping and fallback exploration policy.

Minimum Tandem output:

- `session_id`, `run_id`, and event stream reference,
- tool/write/approval policy applied,
- artifacts and concrete paths read/written,
- validation state and failures,
- approval receipts or questions,
- audit/tool ledger references,
- final status and retry/repair history.
