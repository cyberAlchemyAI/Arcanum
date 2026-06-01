# Arcanum And Tandem Research Subagent Strategy

Status: draft research route.

## Scope

Primary comparison pair:

- Whole Arcanum repository at `/home/vrondelli/projects/domainspec-core/arcanum`.
- `frumu-ai/tandem` from `https://github.com/frumu-ai/tandem`, inspected from a fresh shallow clone at `/tmp/frumu-ai-tandem` on 2026-05-28.

Arcanum evidence should include the framework, registries, sigils, spells, Formulae packages, observability, experiment harness, runtime adapters, and development artifacts. `dispatch-spec` is only one candidate interaction surface.

Tandem evidence should include the engine runtime, workflow runtime, plan compiler, memory, tools, governance, clients, contracts, and enterprise/readiness material.

## Central Question

How could Arcanum as a governed capability/lifecycle framework and Tandem as a governed AI runtime interact, and where are their approaches complementary, overlapping, divergent, or mutually constraining?

## Assumptions To Challenge

1. Arcanum is not only `dispatch-spec`; it is a method, lifecycle, capability registry, observability model, experiment harness, and composed spell system.
2. Tandem is not only an agent app; it is a runtime authority layer for state, tools, approvals, memory, artifacts, and audit evidence.
3. Arcanum may provide method, vocabulary, lifecycle, and reusable capability governance that Tandem could host, execute, audit, or import.
4. Tandem may provide runtime enforcement, approval gates, artifact contracts, tenant-aware memory, and operational evidence that Arcanum currently models more as method and repository-local governance.
5. The strongest integration may be a narrow bridge between Arcanum capabilities/spells and Tandem workflow/runtime primitives, not a merger of the two systems.
6. Divergences should be preserved when they protect different authority boundaries.

## Chosen Decomposition

Use six parallel research agents, decomposed by concern rather than repository path. Each agent must inspect both repositories and cite evidence from both sides.

Rejected alternative:

- A `dispatch-spec`-centered comparison. That was too narrow: it treats one Arcanum Formulae package as the whole system and misses Arcanum's lifecycle, registry, observability, experiment, spell, and runtime-adapter surfaces.

Second rejected alternative:

- A file-tree tour of both repositories. It would be broad but weak; the useful result needs cross-system tensions and interaction options.

## Agent Roles

| Agent | Concern | Central Question | Explicit Exclusions | Evidence Targets |
| --- | --- | --- | --- | --- |
| A1 System Identity And Authority | What each project fundamentally owns | Is Arcanum a capability/lifecycle governance layer while Tandem is a runtime authority layer, or is there deeper overlap? | Do not reduce Arcanum to prompts. Do not reduce Tandem to UI or chat. | Arcanum `README.md`, `framework/CYBERALCHEMY-METHOD.md`, `registry/SIGILS.md`, `registry/SPELLS.md`; Tandem `README.md`, `PRINCIPLES.md`, `ARCHITECTURE.md` |
| A2 Capability And Workflow Model | Sigils/spells vs workflows/plans/runs | How do Arcanum sigils, spells, packs, and task sessions compare to Tandem workflows, plan packages, agent teams, and runtime runs? | Do not assume naming equivalence means semantic equivalence. | Arcanum `arcana/`, `spells/`, `formulae/dispatch-spec/`, `arcana/task-session/`; Tandem `docs/WORKFLOW_RUNTIME.md`, `crates/tandem-plan-compiler/`, `crates/tandem-workflows/`, `crates/tandem-agent-teams/` |
| A3 Runtime And Enforcement | Execution, tools, approvals, permissions | Where does each system enforce behavior: skill contract, repository convention, command adapter, runtime policy, approval gate, or audit trail? | Do not propose execution integration before authority boundaries are explicit. | Arcanum `tools/`, `spells/arcanum-bootstrap/`, `arcana/sigil-runtime-installer/`, observability docs; Tandem `crates/tandem-core/`, `crates/tandem-server/`, `crates/tandem-tools/`, `docs/AI_RUNTIME_INFRASTRUCTURE.md` |
| A4 Memory, Evidence, And Observability | Durable context and learning loops | How do Arcanum inventory/ontology/observability/experiment evidence compare to Tandem runtime-owned memory, context runs, logs, and artifact validation? | Do not promote candidate memory terms or blur audit evidence with canonical knowledge. | Arcanum `arcana/inventory/`, `arcana/ontology-vault/`, `framework/observability/`, `arcana/experiment-harness/`; Tandem `crates/tandem-memory/`, `crates/tandem-observability/`, `docs/LOGGING_SCHEMA.md`, `docs/WORKFLOW_RUNTIME.md` |
| A5 Governance, Compliance, And Lifecycle | Promotion, review, compliance, lifecycle | How do Arcanum's lifecycle and promotion guardrails compare with Tandem's tenant/security/compliance posture? | Do not treat enterprise compliance as the same thing as capability lifecycle governance. | Arcanum `framework/SIGIL-DEVELOPMENT-WORKFLOW.md`, `framework/QUALITY-BAR.md`, registries; Tandem `docs/ENTERPRISE_READINESS.md`, `docs/EU_AI_ACT_COMPLIANCE.md`, `docs/compliance/`, `crates/tandem-governance-engine/` |
| A6 Integration Architecture | Bridge options and anti-options | What are the smallest credible interaction shapes between Arcanum and Tandem, and which should be explicitly avoided? | Do not write adapter code. Do not select one path before comparing failure modes. | Findings from A1-A5; Arcanum `formulae/dispatch-spec/`, `arcana/task-session/runtime-adapters/`, `spells/arcanum-bootstrap/`; Tandem `docs/ENGINE_PROTOCOL_MATRIX.md`, `docs/ENGINE_COMMUNICATION.md`, `contracts/http.md` |

## Required Agent Report Format

Each agent returns:

1. Key findings: 3-5 bullets, each with concrete file or doc evidence from both repositories.
2. Complementary approaches: what Arcanum and Tandem could strengthen in each other.
3. Divergent approaches: what should remain separate or unresolved.
4. Interaction candidates: handoff, adapter, import/export, runtime host, evidence bridge, workflow bridge, or audit path.
5. Anti-candidates: integrations that seem tempting but would confuse ownership or authority.
6. Risks and blockers: licensing, trust boundary, schema mismatch, lifecycle mismatch, authority confusion, missing evidence.
7. Questions for synthesis: what the parent synthesis must decide.

## Synthesis Questions

The synthesis should answer:

1. Is Tandem best treated as an execution host for Arcanum, a peer governed runtime, an external comparator, a future runtime adapter, or a deployment substrate?
2. Which Arcanum artifacts could map to Tandem primitives: sigil, spell, work-pack, dispatch document, context pack, experiment run, observability signal, inventory entry, ontology finding?
3. Which Tandem primitives could map to Arcanum concepts: workflow plan bundle, runtime projection, artifact contract, approval gate, memory record, tool ledger event, audit record, agent team?
4. Where does authority live if an Arcanum spell runs inside Tandem?
5. What should be the first proof artifact: concept crosswalk, toy workflow, runtime adapter spike, artifact-contract bridge, memory/evidence bridge, or governance decision record?
6. Which integration paths should be explicitly rejected for now?

## Expected Outputs

| Output | Purpose |
| --- | --- |
| `TANDEM-ARCANUM-CROSSWALK.md` | Evidence-backed concept map across whole Arcanum and Tandem. |
| `TANDEM-INTERACTION-TENSIONS.md` | Synthesis of complementary, overlapping, and divergent approaches. |
| `TANDEM-INTEGRATION-OPTIONS.md` | Ranked options with gates, proof artifacts, and rejected paths. |
| `tandem-research.dispatch.json` | Dispatch-shaped route for this whole-system research strategy. |

## Preliminary Hypothesis

The strongest likely complement is:

```text
Arcanum defines governed capability methods, lifecycle artifacts, reusable sigils/spells, context packs, validation practices, and reflection loops.
Tandem hosts governed runtime execution with scoped tools, approvals, memory, artifact contracts, tenant boundaries, and audit evidence.
The bridge is not one object; it may be a layered adapter between Arcanum capability/spell contracts and Tandem workflow/runtime projections.
```

The likely divergence is:

```text
Arcanum treats durable knowledge, method vocabulary, promotion, and lifecycle ownership as repository-governed authoring concerns.
Tandem treats authority, state, memory, tools, approvals, and evidence as runtime-owned operational concerns.
```

That divergence is productive. It suggests the first research output should be a whole-system crosswalk plus a small proof recommendation, not a merged architecture.
