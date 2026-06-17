# Refine Seed Proposal: Craft Feature Readiness Indexes

## Target

- Target package: `arcana/craft`
- Target update: additive execution-readiness indexes for Craft ledgers and human views.
- Run folder: `arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes/`
- Run ID: `20260614T200439Z-craft-feature-readiness-indexes`

## Operator Intent

Refine new Craft updates from the readiness reflection evidence, then Invoke design and plan artifacts for those updates before lifecycle execution.

## Source Context

- Current Craft canonical contract: `arcana/craft/SKILL.md`
- Current Craft package entrypoint: `arcana/craft/README.md`
- Current ledger schema: `arcana/craft/templates/ledger.schema.yml`
- Current examples: `arcana/craft/examples/product-launch-ledger.yml`, `arcana/craft/examples/platform-governance-ledger.yml`
- Reflection source: parent-repository feature-readiness reflection, sanitized here as public-safe workflow evidence.
- Evidence pattern: plans and ledgers can say "next move" while the executable boundary depends on a work-pack, ready SWU, approval scope, execution mode, product worktree, and blocked mutation scope.

## Public Boundary

This packet is stored in the public `arcanum` submodule, so private workspace names, product findings, and local-only paths are intentionally not copied here. The public-safe pattern is:

- a plan may be ready for one execution mode while blocked for another;
- approval records are part of readiness, not narrative side notes;
- product mutation and publication gates must remain separate from local/static or documentation-only work;
- Craft should index those distinctions when an existing ledger already points to an Invoke work-pack.

## Refined Unit

The smallest coherent update is **Craft execution-readiness indexing**:

- extend the optional ledger index contract with handles for the current executable target;
- let `state all` and exported human views expose those handles when present;
- preserve Craft as a ledger and route-memory owner, not as an executor;
- keep all fields additive so existing ledgers remain valid.

## Proposed Field Family

Use an optional `execution_readiness` index family, plus optional row fields where they fit existing rows:

- `current_execution_target`
- `work_pack_gate_status`
- `ready_swu_ids`
- `approval_record`
- `execution_mode`
- `product_worktree`
- `blocked_mutation_scope`
- `blocked_publication_scope`
- `owner_route`

## Non-Goals

- Do not make Craft execute SWUs or task sessions.
- Do not rewrite Invoke or Refine contracts in this Craft update.
- Do not make `CRAFT.md` the source of truth.
- Do not require readiness indexes for ledgers with no work-pack or execution plan.
- Do not publish private evidence into the public `arcanum` submodule.

## Done Criteria

- Design artifact describes all six Invoke design views.
- Plan artifact includes L0-L3 implementation layering.
- Work-pack is split into task and wave files because the update touches multiple public surfaces.
- Each non-exempt task has SWUs with write scope, acceptance evidence, and validation.
- Future execution route is explicit: `sigil-development` or maintainer-approved `task-session`, one selected SWU at a time.

## Preset And Research Decision

- Preset: `standard`
- Research mode: `no-research`
- Reason: local Craft, Invoke, Refine, and reflection evidence is sufficient; no external research is needed for this additive contract update.

## Selected Overlays

- `baseline_sequence`: the update needs the ordinary Refine-to-Invoke sequence.
- `memory_residue_for_context_recovery`: prior Craft promotion and readiness reflections are material.
- `protected_context_for_external_or_sensitive_evidence`: some evidence is private and must be abstracted before entering public Craft development artifacts.

## Runtime Permission State

Runtime-backed Refine stages and delegated subagents were not dispatched from this packet. The current output is an authored, non-executed refinement and Invoke design/plan bundle.
