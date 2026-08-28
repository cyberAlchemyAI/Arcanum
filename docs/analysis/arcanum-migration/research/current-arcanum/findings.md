# Findings — Current Arcanum

> Status: provisional parent synthesis of the three completed explorer returns. This document is not skeptic-gated: the registered dispatch was blocked at the explorer-to-synthesis handoff because its generated Research topology disagreed with the canonical Research owner. It is therefore evidence for the current-system analysis, not proof that the original research dispatch completed successfully.

## Objective

Describe the Arcanum that exists today: its materially relevant parts, the artifacts they produce, their ownership and relationships, the behavior that has actually been evidenced, the main present-day operability and complexity problems, and the remaining unknowns. The governing rule is `claim <= proof`.

This inquiry excludes future architecture, migration design, target requirements, and proposals to add or remove capabilities.

## Results

Arcanum currently exists as a large, repository-scoped capability system with several distinct authorities and runtimes. Its strongest evidence is structural and contract-level. Some bounded flows have historical receipts, but the repository does not support a claim that all declared components form one continuously exercised end-to-end runtime.

### What exists

An independent enumeration of the present working tree found 7,817 non-`.git` files across 29 top-level scopes, including 45 canonical `arcana/*/SKILL.md` packages, five formula packages, eleven transmutations, seventeen spells, and the Orchestrate runtime. This is a snapshot of a dirty working tree, not a stable historical baseline.

For explanatory purposes, the material surface is better represented as artifact and authority families than as one flat component list:

| Family | Present responsibility | Principal authority or location |
|---|---|---|
| Canonical capability packages | Define capability contracts, procedures, boundaries, and supporting resources | `arcana/`, `formulae/`, `spells/`, `transmutations/`, `runtime/` |
| Registries and dependency catalogs | Advertise capability identity and dependency relationships | `registry/SIGILS.md`, `registry/SPELLS.md`, related catalogs |
| Generated projections and distribution bundles | Expose selected capabilities to particular agent hosts | `.agents/skills/`, `.claude/`, generated manifests/bundles |
| Invoke authoring artifacts | Describe intended work, scope, readiness, and lifecycle inputs | `spells/invoke/` work-pack artifacts |
| Craft project state | Hold project-owned intent and lifecycle state | Craft-owned project documents and ledger |
| Task Session artifacts | Bound mutation execution and produce session evidence | `arcana/task-session/`, session/run artifacts |
| Dispatch and Orchestrate control state | Validate fan-out shape, register dispatches, record runtime events and residue | `formulae/dispatch-spec/`, `runtime/orchestrate/`, `.arcanum/runtime/` |
| Decision artifacts | Record human or governed decisions without silently taking another owner's authority | Decision Gate and decision records |
| Continuation, Goal, and readiness projections | Determine whether and how work may proceed or be resumed | continuation, goal, and readiness capabilities |
| Observability and reflection artifacts | Declare or record signals, observations, and reflection state | observability configuration and related ledgers |
| Knowledge and definition artifacts | Preserve terminology, ontology, and explanatory context | framework, definitions, ontology, and documentation surfaces |
| Research, review, and session artifacts | Preserve inquiries, evidence returns, findings, reviews, and governed session closeout | `research/`, review outputs, `sessions/` |
| Fixtures, benchmarks, development, archives, and logs | Supply test witnesses, experiments, historical material, and implementation workspaces | fixture, benchmark, development, archive, and log trees |

This grouping is explanatory, not a claim that every file in the repository has been semantically classified.

### What each major part produces

Artifact production is plural and owner-specific. There is no single global artifact authority.

| Component or capability | Main artifacts or state it declares or produces | Evidence boundary |
|---|---|---|
| Craft | Project-owned definitions, lifecycle state, work-unit ledger entries, and mediated write-back | Contract and architecture documentation; no general Craft runner or automatic updater was found |
| Invoke | Work-pack authoring documents, readiness inputs, task-session launch material, and refresh/write-back proposals | Contract and stored examples; caller-mediated owner write-back remains explicit |
| Readiness capabilities | Audit or admission results for work packs and implementation/session entry | Contracted as non-mutating assessments; Task Session retains live mutation admission authority |
| Task Session | Bounded execution state, evidence, checks, receipts, and closeout-related outputs | Main runner implements the bounded execution core but explicitly omits whole-run owner hooks and continuation |
| Decision Gate | Decision requests and governed decision records | Contract-level ownership; no basis found to treat it as authority over another owner's state |
| Dispatch Spec | Temporary JSON dispatch specifications and structural validation results | Shape validation only; it does not own native execution |
| Subagent Strategy / Orchestrate | Append-only registration and close rows, handoff validation, event streams, and residue | This inquiry directly observed registration and a blocked handoff; it did not produce a complete Orchestrate causal stream |
| Continuation Router | Continuation decisions or routing artifacts derived from prior execution state | A bounded historical Task Session → Invoke Refresh → Continuation witness exists; universality is unproved |
| Goal | Goal state and loop projections | Packaged runtime is read-only or synthetic in important paths; live cross-owner dispatch/apply was not found |
| Registries | Human-readable capability inventory and lookup projections | They do not equal the physical repository universe and currently omit present packages |
| Generated skill projections | Host-specific copies or projections of capability instructions | Multiple projections drift from canonical owners in version or topology |
| Observability | Signal definitions, event/observation records, and reflection-related state | Configuration exists; a complete repository-wide telemetry loop was not found |
| Experiment Harness, fixtures, and benchmarks | Experimental scenarios, fixtures, expected outputs, and comparison evidence | They establish bounded test evidence, not production-wide integration |
| Research | Initial definitions, raw explorer returns, synthesis, skeptic review, and findings | The current run produced definitions and raw returns; canonical synthesis/skeptic completion was blocked |

The practical complexity is not merely the number of files. It comes from overlapping representations of the same capability, several write authorities, different lifecycle artifacts, and evidence types that can look similar while proving different things.

### How the parts connect

The clearest current relationships are owner-preserving handoffs rather than unrestricted cross-component mutation:

1. Invoke authors or refreshes a work pack and exposes readiness-relevant inputs.
2. Readiness capabilities assess whether declared prerequisites are satisfied, but do not acquire mutation authority.
3. Task Session independently admits live mutation and owns the bounded execution interval.
4. Task Session evidence may be returned to an owning capability through explicit hooks or receipts.
5. Continuation Router or Goal may project what should happen next, but projection is not the same as executing another owner's mutation.
6. Dispatch Spec validates the shape of a multi-agent route; Orchestrate owns native registration, execution evidence, handoff checks, and closeout.
7. Registries and generated projections make capabilities discoverable to humans or hosts, but are representations of canonical owners rather than equivalent authorities.

Craft write-back is intentionally mediated: a caller or user presents the proposed change to Craft, which retains authority over its own state. This creates operational friction, but the evidence supports treating it as a governance boundary unless a separate failure is demonstrated.

### What actually works

| Claim | Exact evidence level | Verdict |
|---|---|---|
| Material repository surfaces can be enumerated independently of the current map | Independent recomputation of the present tree and package counts | Supported for the observed working-tree snapshot |
| The current map validator reconciles declared nodes, relations, coverage entries, and structural flags | Source inspection plus deterministic validator behavior | Supported as internal reconciliation only |
| Dispatch registration can create append-only governance proof before spawn | Executable observation in this inquiry | Supported for this dispatch |
| A mismatched explorer-to-synthesis topology is rejected | Executable observation: the current handoff was blocked | Supported |
| Task Session has a functioning bounded execution core | Implementation inspection and fixtures | Supported, excluding omitted whole-run closeout and owner hooks |
| Task Session → Invoke Refresh → Continuation has worked as a bounded chain | Stored historical receipts for `SWU-TSGR-001` | Supported only for that historical witness |
| Readiness layers preserve distinct authority | Contracts and implementation boundaries | Supported structurally; not a universal runtime witness |
| Goal performs live owner dispatch and applies cross-owner updates | No live end-to-end witness found; packaged runtime is read-only or synthetic in material paths | Not supported |
| Repository-wide observability captures the principal flows | Configuration exists, but central signal/reflection state and hooks were not found | Not supported |
| Fixtures prove system-wide integration | Fixtures are bounded witnesses | Rejected |

### Main problems in the current Arcanum

The following are present-system findings, not migration proposals.

1. **The analysis map proves reconciliation, not discovery.** The schema accepts caller-supplied discovery roots and methods, and the validator compares only the document's own declared sets. It does not enumerate the repository. The included example can declare a single root and still report `structurally_complete: true`. There is also no canonical executable map at the validator's default `mapping/current-system-map.json` path. Consequently, the current analysis cannot support repository-universe coverage from this validator alone.

2. **Canonical and generated capability instructions drift.** Research topology differs between the canonical owner and the active generated `.agents` projection. Task Session and Invoke projections also expose older versions than their canonical packages. This is more than cosmetic: in this inquiry, the registered generated topology declared a combined downstream arrangement that the canonical Research handoff rejected.

3. **Task Session's main runner stops before required owner synchronization.** The runner explicitly omits whole-run closeout, owner hooks, continuation routing, and observation integration. The bounded execution core can work while the larger declared lifecycle remains incomplete. The consequence is high for runs that require those transitions; prevalence across real use is unknown.

4. **Goal's packaged runtime is narrower than its advertised composition.** The inspected loop is materially read-only or synthetic and no live cross-owner dispatch/apply witness was found. This is an implementation limitation. It is not evidence that every use of Goal fails.

5. **Blocked partial fan-out cannot currently be closed truthfully through the observed close registrar.** After three explorers completed and the required handoff blocked the downstream phases, the registrar rejected a close record with the truthful spawned count of three because the registered strategy declared six total agents. The append-only ledger therefore remains open even though all actually spawned agents are closed. This is a directly observed governance/operability problem in the present dispatch lifecycle.

6. **Representation plurality increases diagnosis cost.** Canonical packages, registries, generated host projections, development copies, fixtures, and historical artifacts may disagree without an immediately visible authority marker. Registry omissions and version drift are demonstrated; their operational effect must be established case by case.

7. **Evidence labels are too coarse in the existing analysis.** Stored receipts, fixtures, code presence, and current-run observations are sometimes grouped as “observed.” That collapses materially different proof classes and makes broad behavior claims easier to overstate.

8. **Observability is not sufficient to measure prevalence or severity.** The repository declares observability concepts, but no complete telemetry surface was found that would answer how often the identified failure modes occur, how much operator effort they consume, or which flows dominate real use.

Lower-confidence inconsistencies include Invoke's absence from the current Spell Registry and broken renamed links in one historical session. Their existence is evidenced, but their current operational consequence is unknown.

### What remains unresolved

- Whether undiscovered repository surfaces materially change the component model above.
- Which capabilities and projections are exercised in normal operation, and with what frequency.
- How often Task Session runs require the owner hooks and continuation steps omitted by its main runner.
- Whether Goal has live execution paths outside the inspected packaged runtime.
- Whether registry omissions cause failed lookup or are tolerated by other discovery mechanisms.
- Whether generated-projection drift is systematically detected before execution.
- The full producer/consumer lifecycle, retention policy, and authoritative copy for every artifact family.
- Repository-wide failure rates, operator effort, recovery time, and the comparative severity of the identified problems.
- Whether central observability state exists outside the inspected repository surfaces.
- A skeptic-gated synthesis of these findings; the registered research dispatch did not reach that stage.

## Context

The research began from the existing `docs/analysis/arcanum-migration/` material and a validated `research-initial-definitions.md`. Three explorer roles inspected repository/artifact coverage, runtime flows, and operability/problem claims. Their raw returns are preserved in `research.md`.

The registered dispatch used the generated Research projection active for the host. After exploration, canonical Research validation found that the registered route shape did not provide the required separate synthesizer, skeptic, and writer stages. The handoff was correctly blocked. No downstream agents were spawned. A subsequent close attempt accurately reported the three spawned explorers but was rejected because the registrar expected the six agents declared in the registered strategy. These events are part of the current-system evidence, not merely process commentary.

Evidence in this document is classified as follows:

- **Documentary assertion:** contracts, READMEs, source text, stored receipts, and pre-existing records.
- **Executable observation:** behavior directly exercised during this inquiry, such as dispatch registration, validation, and handoff blocking.
- **Independent recomputation:** repository enumeration and comparisons recomputed from the current tree.
- **Formal proof:** none claimed.

## Research-question coverage

| RQ id | Status | Answer | Addressable evidence | Contrary evidence / material uncertainty | Boundary |
|---|---|---|---|---|---|
| RQ00 | unresolved | The principal present-system families, relationships, bounded behavior, and problems are described, but the whole-system claim is not closed. | Three explorer returns; present-tree recomputation | No canonical skeptic stage; semantic exhaustiveness is unproved | Present system only |
| RQ01 | answered | The material surface spans canonical packages, registries, projections, runtimes, governance state, knowledge, and evidence/development surfaces. | 7,817-file enumeration; package counts | Snapshot includes a dirty tree | Material families, not every file |
| RQ02 | unresolved | Responsibilities and authorities are identifiable at family and principal-capability level. | Owner contracts and artifact constitution | A complete per-component/per-artifact authority matrix was not produced | Principal parts only |
| RQ03 | answered | The map validator checks internal reconciliation of declared content, not repository-universe discovery. | Schema and validator inspection; minimal example | No separate discovery audit exists in the package | Current validator |
| RQ04 | unresolved | Major artifact families and representative outputs are inventoried. | Artifact-family inventory and owner contracts | Not every materially relevant component has an exhaustive producer/output row | Family-level inventory |
| RQ05 | unresolved | Several producer/consumer relationships are established, especially Invoke, readiness, Task Session, dispatch, and continuation. | Contracts, implementation, stored receipts | Full lifecycle and retention are unknown for many artifacts | Principal flows |
| RQ06 | unresolved | Authority is plural: Craft, work-pack owners, Task Session, Orchestrate, and others retain distinct state ownership. | Artifact constitution and capability contracts | Ambiguous or duplicate authority may remain outside inspected families | Owner-level findings |
| RQ07 | unresolved | Multiple formats and projections impose visible coordination and diagnosis cost. | Projection drift, registry gaps, artifact-family count | Frequency and operator burden are not measured | Demonstrated complexity, unmeasured prevalence |
| RQ08 | answered | Principal relationships are owner-preserving handoffs rather than a single shared mutation plane. | Invoke/readiness/Task Session/Orchestrate contracts and implementations | Does not establish all repository relations | Named principal relations |
| RQ09 | unresolved | Inputs, outputs, and transitions are known for the main inspected flows. | Contracts, runners, receipts | Several owner-hook and lifecycle transitions lack live evidence | Main flows only |
| RQ10 | answered | Readiness assesses; Task Session admits and executes mutation; Dispatch Spec validates shape; Orchestrate owns native fan-out governance. | Owner contracts and runtime inspection | Some composed paths remain unwitnessed | Inspected authorities |
| RQ11 | unresolved | Bounded composition exists, but no universal end-to-end Arcanum execution path is evidenced. | `SWU-TSGR-001` receipts; current dispatch events | Stored witness is bounded; current dispatch blocked before synthesis | No generalization from one run |
| RQ12 | answered | Each major claim above is labeled by documentary assertion, executable observation, or independent recomputation. | Evidence table and context classification | No formal proof and no canonical skeptic approval | Claims in this synthesis |
| RQ13 | answered | Contract, implementation, fixture, historical receipt, and current execution are kept distinct. | Flow and works tables | Some older analysis text still uses broader “observed” language | This findings document |
| RQ14 | unresolved | At least one bounded cross-owner chain is evidenced historically. | Task Session → Invoke Refresh → Continuation receipts | No basis for system-wide reliability or current reproducibility | Single bounded witness |
| RQ15 | unresolved | Several capabilities have contract or fixture evidence without successful live integration evidence. | Goal, observability, Task Session closeout findings | Additional external or uninspected execution evidence may exist | Repository evidence inspected |
| RQ16 | answered | Principal present problems are coverage overclaim, projection drift, incomplete lifecycle runners, narrow Goal runtime, partial-fan-out close failure, and weak telemetry. | Source inspection and current-run observations | Ranking by prevalence is not possible | Bounded problem set |
| RQ17 | answered | Each problem is classified as implementation limitation, governance failure, representation drift, analysis limitation, or unknown consequence. | Problem descriptions and evidence distinctions | Some classifications could change with runtime evidence | Current evidence |
| RQ18 | unresolved | Consequence is demonstrated for the current topology/closeout failure and structurally plausible for other issues. | Blocked handoff and rejected close; runner omissions | System-wide frequency, severity, and user impact are unmeasured | No prevalence extrapolation |
| RQ19 | answered | Craft mediation and readiness authority separation are deliberate boundaries unless independent failure is shown. | Craft, readiness, and Task Session contracts | Boundaries may still create operational cost | Defect claim rejected without proof |
| RQ20 | unresolved | Some complexity is justified by ownership; duplicated projections and evidence ambiguity add unsupported cost. | Authority contracts and drift findings | Net value and operator effort are not measured | Qualitative only |
| RQ21 | answered | Missing behavior is separated into incomplete implementation, unverified behavior, drift, deliberate boundary, and unknown. | Findings taxonomy | Not every repository gap has been classified | Inspected gaps |
| RQ22 | unresolved | Major unknowns are listed explicitly. | Unknowns section and explorer returns | Absence from inspected surfaces is not proof of global absence | Repository-local inquiry |
| RQ23 | answered | The minimum correction is to state that the current validator proves internal reconciliation only; repository coverage requires independent discovery evidence. | Schema, validator, example, missing canonical map | A specific discovery implementation is outside this stage | Analysis protocol only |

## Candidate claim matrix

These are provisional parent verdicts. They did not pass the registered Research skeptic gate.

| Candidate | Owner / precedent | Witnessed? | Sound? | Verdict | Use-mode |
|---|---|---:|---:|---|---|
| The current map validator proves coverage of the relevant repository universe | Current analysis mapping package | No | No | KILL | Typed negative: no witness |
| Arcanum operates as one linear end-to-end runtime | No single owner found | No | No | KILL | Typed negative: no witness |
| Artifact authority is plural and owner-specific | Artifact constitution and capability owners | Yes | Yes | GO | Already deployed |
| A bounded Task Session → Invoke Refresh → Continuation chain has existed | Task Session / Invoke / Continuation receipts | Yes | Yes, within its bound | GO | Already deployed, bounded historical witness |
| Task Session's main runner performs whole-run owner synchronization | Task Session | No; source states the omission | No | KILL | Typed negative: contradicted implementation claim |
| Goal's packaged runtime performs live cross-owner dispatch and apply | Goal | No | No | KILL | Typed negative: no witness |
| Every registry or projection difference is operationally harmful | Registry and projection owners | No | No | KILL | Typed negative: no witness |
| Craft's caller-mediated write-back is inherently a defect | Craft | No | No | KILL | Typed negative: authority boundary |
| The observed dispatch lifecycle can truthfully close a fan-out blocked before all declared stages spawn | Subagent Strategy / Orchestrate governance | No; the close was rejected | No | KILL | Typed negative: executable counterexample |

## Evidence anchors

- Map coverage limitation: `docs/analysis/arcanum-migration/contracts/current-system-map.schema.json:85-119`, `docs/analysis/arcanum-migration/scripts/validate_mapping.py:97-180`, and `docs/analysis/arcanum-migration/contracts/current-system-map.example.json:9-25,60-63`.
- Existing overclaim: `docs/analysis/arcanum-migration/analysis.md:131-133`.
- Artifact authority: `framework/ARTIFACT-CONSTITUTION.md:3-43,60-73`, `arcana/craft/SKILL.md:56-71`, `spells/invoke/plan.md:184-223`, and `runtime/orchestrate/SKILL.md:240-251`.
- Invoke/readiness/Task Session chain: `spells/invoke/README.md:150-193`, `spells/work-pack-readiness-audit/README.md:56-87,101-197`, `spells/implementation-readiness/README.md:47-120`, and `arcana/task-session/SKILL.md:286-326`.
- Task Session runner boundary: `arcana/task-session/scripts/task-session-governance-runner.py:2-7,2870-2881`.
- Goal runtime boundary: `spells/goal/README.md:82-108` and `spells/goal/runtime/goal_loop.py:2-7,235-249,286-334,445-464`.
- Dispatch and Orchestrate authority: `formulae/dispatch-spec/SKILL.md:137-145` and `runtime/orchestrate/SKILL.md:79-84,102-192`.
- Craft mediation: `arcana/craft/SKILL.md:129-150,312-317` and `arcana/craft/ARCHITECTURE.md:241-260`.
- Raw evidence returns: `docs/analysis/arcanum-migration/research/current-arcanum/research.md`.
- Current dispatch handoff evidence: `.arcanum/runtime/subagents-strategy/2026-08-28-current-arcanum-research.explorers-to-synthesis.handoff.json`.

## Limitations and evidence boundary

This synthesis is based on the current repository tree, source and contract inspection, stored fixtures and receipts, independent enumeration, and the directly observed research-dispatch lifecycle. It does not prove historical completeness, production frequency, performance, user impact, or the absence of execution evidence outside the repository. The current working tree was dirty. The canonical Research synthesizer/skeptic/writer sequence did not execute, so these findings remain provisional until independently challenged.

**One-line answer:** Arcanum today is a broad, owner-partitioned capability and artifact system with real bounded execution witnesses, but its representations drift, several advertised compositions stop short of live integration, its current map cannot prove repository coverage, and important operational prevalence and end-to-end behavior remain unknown.
