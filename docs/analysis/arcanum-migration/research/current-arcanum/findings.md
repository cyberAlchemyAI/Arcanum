# Findings — Current Arcanum

> Status: corrected parent synthesis. The original 2026-08-28 Research dispatch did not reach its canonical skeptic stage, but dispatch `2026-08-28-current-arcanum-detailed-review` subsequently challenged this document with three independent attackers and a separate skeptic. The original Research lifecycle remains historically incomplete; the corrections below incorporate only the later review's verified dispositions and do not recast that dispatch as successfully completed.

## Objective

Describe the Arcanum that exists today: its materially relevant parts, the artifacts they produce, their ownership and relationships, the behavior that has actually been evidenced, the main present-day operability and complexity problems, and the remaining unknowns. The governing rule is `claim <= proof`.

This inquiry excludes future architecture, migration design, target requirements, and proposals to add or remove capabilities.

## Results

Arcanum currently exists as a large, repository-scoped capability system with several distinct authorities and runtimes. Its strongest evidence is structural and contract-level. Some bounded flows have historical receipts, but the repository does not support a claim that all declared components form one continuously exercised end-to-end runtime.

### What exists

An independent enumeration of the present working tree found 7,817 non-`.git` files across 29 top-level scopes, including 45 canonical `arcana/*/SKILL.md` packages, five formula packages, eleven transmutations, seventeen spells, and the Orchestrate runtime. This is a snapshot of a dirty working tree, not a stable historical baseline (`research.md:15-65`).

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

The practical complexity is not established by file count alone. The evidence does establish overlapping representations, plural write authorities, different lifecycle artifacts, and proof classes that must be distinguished. Their aggregate operational cost is not measured. See `research.md:68-106`.

### How the parts connect

The clearest current relationships are owner-preserving handoffs rather than unrestricted cross-component mutation:

1. Invoke authors or refreshes a work pack and exposes readiness-relevant inputs.
2. Readiness capabilities assess whether declared prerequisites are satisfied, but do not acquire mutation authority.
3. Task Session independently admits live mutation and owns the bounded execution interval.
4. Task Session evidence may be returned to an owning capability through explicit hooks or receipts.
5. Continuation Router or Goal may project what should happen next, but projection is not the same as executing another owner's mutation.
6. Dispatch Spec validates the shape of a multi-agent route; Orchestrate owns native registration, execution evidence, handoff checks, and closeout.
7. Registries and generated projections make capabilities discoverable to humans or hosts, but are representations of canonical owners rather than equivalent authorities.

Craft write-back is intentionally mediated: a caller or user presents the proposed change to Craft, which retains authority over its own state. Manual mediation is witnessed, but its time, recurrence, error rate, and aggregate burden are unmeasured. It remains a governance boundary unless a separate failure is demonstrated (`research.md:185,267,277,300-301`).

### What actually works

| Claim | Exact evidence level | Verdict |
|---|---|---|
| Material repository surfaces can be enumerated independently of the current map | Independent recomputation of the present tree and package counts | Supported for the observed working-tree snapshot |
| The current map validator reconciles declared nodes, relations, coverage entries, and structural flags | Source inspection plus deterministic validator behavior | Supported as internal reconciliation only |
| Dispatch registration can create append-only governance proof before spawn | Executable observation in this inquiry | Supported for this dispatch |
| A mismatched explorer-to-synthesis topology is rejected | Executable observation: the current handoff was blocked | Supported |
| Task Session has an implemented bounded execution core with stored fixture evidence | Implementation inspection and stored fixtures; no fixture suite executed in this inquiry | Supported as implementation/fixture evidence; current execution and omitted whole-run closeout or owner hooks remain unverified (`research.md:182-184,241-246`) |
| Task Session → Invoke Refresh → Continuation has worked as a bounded chain | Stored historical receipts for `SWU-TSGR-001` | Supported only for that historical witness |
| Readiness layers preserve distinct authority | Contracts and implementation boundaries | Supported structurally; not a universal runtime witness |
| Goal performs live owner dispatch and applies cross-owner updates | No live end-to-end witness found; packaged runtime is read-only or synthetic in material paths | Not supported |
| Repository-wide observability captures the principal flows | Configuration exists, but central signal/reflection state and hooks were not found | Not supported |
| Fixtures prove system-wide integration | Fixtures are bounded witnesses | Rejected |

### Main problems in the current Arcanum

The following are present-system findings, not migration proposals.

1. **The analysis map proves reconciliation, not discovery.** The schema accepts caller-supplied discovery roots and methods, and the validator compares only the document's own declared sets. It does not enumerate the repository. The included example can declare a single root and still report `structurally_complete: true`. There is also no canonical executable map at the validator's default `mapping/current-system-map.json` path. Consequently, the current analysis cannot support repository-universe coverage from this validator alone (`research.md:17-19,86-90,125-131`).

2. **Canonical and generated capability instructions drift.** Research topology differs between the canonical owner and the generated `.agents` projection used to register the historical dispatch. Task Session and Invoke projections also exposed older versions than their canonical packages. This is more than cosmetic: the preserved handoff proves that the registered topology disagreed with the canonical Research owner and was blocked. The immutable evidence does not establish which component authored that registered projection (`research.md:172-176,187-198,264-266`).

3. **Task Session's main runner stops before required owner synchronization.** The runner explicitly omits whole-run closeout, owner hooks, continuation routing, and observation integration. The bounded execution core is implemented and fixture-backed while the larger declared lifecycle remains incomplete. Runs using that runner and requiring those transitions reach a structurally blocked path; prevalence across real use is unknown (`research.md:174,182-184,194,264,274`).

4. **Goal's packaged runtime is narrower than its advertised composition.** The inspected loop is materially read-only or synthetic and no live cross-owner dispatch/apply witness was found. This is an implementation limitation, not evidence that every use of Goal fails (`research.md:174,186,195,265,275`).

5. **The 2026-08-28 Research dispatch remained open after a truthful partial-fan-out close attempt.** Three explorers completed, the required downstream handoff blocked, a close input reported the three actually spawned agents, and no paired close row was appended. Those artifacts prove the attempted count and non-acceptance, but they do not preserve the registrar diagnostic or prove its exact cause. Later registrar remediation distinguishes planned, launched, and unlaunched agents and accepts bounded partial-count close records; therefore this is a date-bound historical lifecycle failure, not a claim about current registrar behavior. Evidence: the handoff and close input cited below, the absent historical ledger row, and current `arcana/subagent-strategy/scripts/append-dispatch.cjs:296-316,555-564` with `arcana/subagent-strategy/development/test-append-dispatch.cjs:515-526`.

6. **Representation plurality creates unresolved source-selection questions; aggregate diagnosis cost is unmeasured.** Canonical packages, registries, generated host projections, development copies, fixtures, and historical artifacts may disagree. Registry omissions and version drift are demonstrated, and the historical Research handoff supplies one bounded consequence. Frequency, diagnosis time, and other operational effects must be established case by case (`research.md:21,73-84,176,188,198,251-256,266,278-279,285-295`).

7. **Evidence labels are too coarse in the existing analysis.** Stored receipts, fixtures, code presence, and current-run observations are sometimes grouped as “observed.” That collapses materially different proof classes and makes broad behavior claims easier to overstate (`research.md:178-189,200-210,222-247`).

8. **The inspected observability surface is insufficient to measure prevalence or severity.** The repository declares observability concepts, but no complete repository-local telemetry surface was found that would answer how often the identified failure modes occur, how much operator effort they consume, or which flows dominate real use (`research.md:81,188-189,196,239-256,285,327-334`).

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
- Whether a future canonical Research run reproduces the corrected synthesis; the original registered dispatch did not reach its skeptic stage, while the later detailed review independently challenged this document.

## Context

The research began from the existing `docs/analysis/arcanum-migration/` material and a validated `research-initial-definitions.md`. Three explorer roles inspected repository/artifact coverage, runtime flows, and operability/problem claims. Their raw returns are preserved in `research.md`.

The historical dispatch registered a topology that disagreed with the canonical Research owner. After exploration, canonical validation blocked the downstream handoff, and no downstream agents were spawned. A subsequent close input accurately reported the three spawned explorers, but no paired close row was appended. The preserved artifacts prove the mismatch, block, attempted count, and non-acceptance; they do not preserve the registrar diagnostic or establish the precise authoring provenance of the registered projection. Later registrar remediation is current comparator evidence, not evidence available to the original inquiry.

Evidence in this document is classified as follows; these classes are not interchangeable:

- **Contract or documentation:** declared responsibility, procedure, or boundary; does not prove implementation.
- **Implementation inspection:** behavior present in source; does not prove successful execution.
- **Fixture or test evidence:** a bounded test witness, distinguished from live integration.
- **Historical execution receipt:** preserved evidence that a named bounded run occurred; not proof of current or universal behavior.
- **Current executable observation:** behavior directly exercised during the original inquiry, limited to the registered dispatch, validation, and blocked handoff events actually preserved.
- **Independent recomputation:** enumeration or comparison recomputed from the then-current dirty tree; a point-in-time result rather than a stable baseline.
- **Not found, contradictory, partial, or unknown:** epistemic statuses, not positive evidence classes.
- **Formal proof:** none claimed.

## Research-question coverage

`Administrative state` records whether this synthesis has explicitly processed the registered question. It does not imply evidential closure. `Evidential state` records whether the available evidence supports a bounded answer, only a partial answer, or leaves the question unresolved.

| RQ id | Administrative state | Evidential state | Answer to the registered question | Addressable evidence | Contrary evidence / material uncertainty | Boundary |
|---|---|---|---|---|---|---|
| RQ-00 | reviewed | partial | Principal families, artifacts, owner-preserving relations, bounded behavior, supported problems, and unknowns are described; semantic completeness for all Arcanum is not established. | All three returns (`research.md:10-340`) and this corrected synthesis | No exhaustive semantic audit or current-use denominator | Present repository system only |
| RQ-01 | reviewed | supported at family level | Material explanatory parts include canonical capabilities, runtimes, registries, projections, owner state, governance controls, knowledge/evidence surfaces, and development residue. | Enumeration and family inventory (`research.md:15-106`) | Dirty-tree snapshot; not every file semantically classified | Material families, not every instance |
| RQ-02 | reviewed | partial | Responsibility and authority are identified for principal owners including Craft, Invoke, readiness, Task Session, Decision Gate, Dispatch Spec, Orchestrate, Goal, registries, observability, Research, and Review. | Owner contracts and flow matrix (`research.md:68-84,172-189`) | No complete per-component/per-artifact authority matrix | Principal inspected owners |
| RQ-03 | reviewed | supported | The existing validator reconciles declared input only; it does not discover or compare against the repository universe. | Schema, example, validator, and recomputation (`research.md:17-19,86-90`) | No independent discovery audit in the mapping package | Current mapping protocol |
| RQ-04 | reviewed | partial | Twelve artifact families cover principal formats, producers, consumers, authority, persistence, projection, validation, and residue patterns. | Artifact-family matrix (`research.md:68-84`) | Instance-level lifecycle classification is incomplete | Family level |
| RQ-05 | reviewed | partial | Strong lifecycle and source-of-truth evidence exists for Craft state, Work Packs, Task Session/Invoke receipts, dispatch events/residue, observability, and sessions; many historical artifacts lack reconciled retention or downstream-consumer evidence. | `research.md:68-84,128-131` | Full lifecycle and retention remain unknown for many artifacts | Principal artifact families |
| RQ-06 | reviewed | partial | Explicit derivation and overlap exist among canonical packages, registries, host projections, human/machine views, and historical copies; registry/package and selected generated/canonical drift is demonstrated. | `research.md:20-21,73-84,93-106,176,188` | Full semantic parity across all projections was not tested | Inspected representations |
| RQ-07 | reviewed | partial | Necessary governance/ownership cost and generated/compatibility cost can be distinguished from demonstrated drift and unresolved duplication. Aggregate operational burden and whether each duplication is accidental remain unmeasured. | `research.md:68-106,267,277,285-295` | Artifact variety alone proves no unnecessary complexity | Qualitative classification only |
| RQ-08 | reviewed | partial | Principal relations are owner-preserving handoffs carrying work packs, readiness decisions, mutation admission, receipts, continuation routes, dispatch actions, and explicit authority boundaries. | Flow matrix (`research.md:172-189`) | Not every repository relation is mapped | Named principal relations |
| RQ-09 | reviewed | partial | One Task Session → Invoke Refresh → Continuation chain is historically witnessed; other principal compositions are supported by contract, implementation, fixtures, or partial observations rather than current end-to-end execution. | `research.md:172-189,207-212` | Main Task Session runner omits owner hooks; Goal is synthetic/read-only | Inspected flows only |
| RQ-10 | reviewed | supported for principal flows | Invoke authors; readiness assesses; Task Session admits and executes bounded mutation; Decision Gate resolves consequential choices; owners apply their own state; Dispatch Spec validates shape; Orchestrate coordinates native fan-out and causal evidence. | `research.md:172-189` | Some composed paths remain unwitnessed | Principal inspected authorities |
| RQ-11 | reviewed | partial | Craft, Task Session, Decision Gate, Invoke/Refresh, Dispatch Spec, Orchestrate, Continuation, Goal, readiness, registries/projections, observability, and Experiment Harness connect through multiple owner-preserving flows, not one universal runtime. | `research.md:172-189` | No universal end-to-end execution witness | Named system relation set |
| RQ-12 | reviewed | partial | Claim-level support is now separated into contract/documentation, implementation, fixture/test, historical receipt, current executable observation, and recomputation, with explicit scope limits. | Evidence taxonomy above and claim locators throughout this document | No formal proof; some artifact families remain only partially classified | Material claims in this synthesis |
| RQ-13 | reviewed | supported for this synthesis | Claims are explicitly distinguished as documented, implemented, fixture/test-backed, historically executed, currently observed, partial, not found, contradictory, or unknown. | Evidence taxonomy and `research.md:178-189,222-247` | The older main analysis still uses a broader “observed” class | This corrected synthesis |
| RQ-14 | reviewed | unresolved | Canonical owners govern responsibility and protected state; schemas govern accepted shape; runtime evidence governs claims about an observed run. No universal precedence rule was found for same-concern disagreement among contracts, projections, implementation, fixtures, and runtime evidence. | `research.md:20,172-198,214-220` | Same-concern precedence remains unspecified | Inspected owners and evidence |
| RQ-15 | reviewed | partial | The existing analysis generalizes by grouping fixtures and historical runs as “observed” and contains broad claims backed by stale hashes; no supported system-wide generalization from the bounded `SWU-TSGR-001` chain was found in this findings document. | `research.md:173,200-210,222-247` | A complete audit of every existing-analysis claim was outside the explorer returns | Existing analysis claims inspected |
| RQ-16 | reviewed | partial | Supported conditions include the map's discovery overclaim, Task Session's structurally incomplete owner synchronization, Goal's narrower implementation, selected projection drift with one historical blocked handoff, and insufficient telemetry. | `research.md:264-285` plus the preserved historical handoff | Recurrence and deployed impact are mostly unknown | Bounded problem set |
| RQ-17 | reviewed | partial | Generated Research drift has one demonstrated historical handoff consequence; broken links have local comprehension impact; registry omissions and most projection differences have no established operational impact. | `research.md:266,274-281,306-315` | Diagnosis time and aggregate burden are unmeasured | Case-by-case consequences |
| RQ-18 | reviewed | unresolved at aggregate level | Structural scope is bounded per problem, and the historical handoff/close sequence has a demonstrated local consequence; repository-wide recurrence, severity, user reach, recovery time, and comparative impact are not established. | `research.md:274-285,306-334` | No representative operational telemetry corpus | No prevalence extrapolation |
| RQ-19 | reviewed | supported for classified problems | Map limitations and broken links are local; Task Session closeout, Goal composition, Craft mediation, projection drift, and the historical Research lifecycle arise across handoffs or authority boundaries. | `research.md:274-281,306-315` | Classification could change with new runtime evidence | Inspected problems |
| RQ-20 | reviewed | partial | Manual gates, caller-mediated Craft decisions, `local-fallback`, separate owner receipts, staged deltas, compatibility projections, and regeneration metadata are evidenced. Their effectiveness is demonstrated only for bounded artifacts; time, recurrence, error rate, and aggregate cost are unmeasured. | `research.md:267,277,300-303,306-315` | No cost profile or failed-handoff denominator | Bounded coordination patterns |
| RQ-21 | reviewed | supported for inspected gaps | Task Session and Goal gaps are incomplete implementation; projection differences are representational drift; Craft mediation is a deliberate authority boundary; registry omission has unresolved status; unobserved integrations remain unverified. | `research.md:264-281,306-315` | Not every repository gap was classified | Inspected gaps only |
| RQ-22 | reviewed | unresolved | Missing telemetry, unknown active-surface precedence, uncertain projection parity, absent use denominator, incomplete artifact lifecycles, and undiscovered surfaces limit a trustworthy whole-system explanation. | Unresolved list above and `research.md:283-334` | Absence from inspected surfaces is not global absence | Repository-local inquiry |
| RQ-23 | reviewed | supported | The smallest evidenced protocol correction is to state that the map validator proves internal reconciliation only and that repository coverage requires independent discovery evidence with an explicit denominator. | Schema, validator, example, and `research.md:17-19,86-90,125-131` | A discovery implementation is outside this research stage | Analysis protocol only |

## Candidate claim matrix

These verdicts remain historical candidates rather than proof that the original Research dispatch completed. The later detailed review independently checked their contract vocabulary. `KILL` is used only for the Research contract's permitted `no-witness` condition; each negative row names its zeroing fact.

| Candidate | Owner / precedent | Witnessed? | Sound? | Verdict | Use-mode |
|---|---|---:|---:|---|---|
| The current map validator proves coverage of the relevant repository universe | Current analysis mapping package | No | No | KILL | `no-witness`: validator performs no repository discovery |
| Arcanum operates as one linear end-to-end runtime | No single owner found | No | No | KILL | `no-witness`: only plural owner-preserving flows were evidenced |
| Artifact authority is plural and owner-specific | Artifact constitution and capability owners | Yes | Yes | GO | Already deployed |
| A bounded Task Session → Invoke Refresh → Continuation chain has existed | Task Session / Invoke / Continuation receipts | Yes | Yes, within its bound | GO | Already deployed, bounded historical witness |
| Task Session's main runner performs whole-run owner synchronization | Task Session | No; the inspected runner explicitly stops with owner hooks unimplemented | No | KILL | `no-witness`: current implementation supplies a zeroing counterfact |
| Goal's packaged runtime performs live cross-owner dispatch and apply | Goal | No | No | KILL | `no-witness`: inspected runtime is synthetic/read-only in material paths |
| Every registry or projection difference is operationally harmful | Registry and projection owners | No | No | KILL | `no-witness`: several differences have unknown downstream impact |
| Craft's caller-mediated write-back is inherently a defect | Craft | No; mediation is contractually owner-preserving and no independent failure was witnessed | No | KILL | `no-witness`: no demonstrated defect or excessive burden |
| The 2026-08-28 Research dispatch obtained an accepted close row after its truthful three-agent partial-fan-out close input | Subagent Strategy / Orchestrate governance | No; the historical ledger contains no paired close row | No | KILL | `no-witness`: absent accepted close row; exact registrar cause remains unproved |

## Evidence anchors

- Map coverage limitation: `docs/analysis/arcanum-migration/contracts/current-system-map.schema.json:85-119`, `docs/analysis/arcanum-migration/scripts/validate_mapping.py:97-180`, and `docs/analysis/arcanum-migration/contracts/current-system-map.example.json:9-25,60-63`.
- Existing overclaim: `docs/analysis/arcanum-migration/analysis.md:131-133`.
- Artifact authority: `framework/ARTIFACT-CONSTITUTION.md:3-43,60-73`, `arcana/craft/SKILL.md:56-71`, `spells/invoke/plan.md:184-223`, and `runtime/orchestrate/SKILL.md:240-251`.
- Invoke/readiness/Task Session chain: `spells/invoke/README.md:150-193`, `spells/work-pack-readiness-audit/README.md:56-87,101-197`, `spells/implementation-readiness/README.md:47-120`, and `arcana/task-session/SKILL.md:286-326`.
- Task Session runner boundary: `arcana/task-session/scripts/task-session-governance-runner.py:2-7,2870-2881`.
- Goal runtime boundary: `spells/goal/README.md:82-108` and `spells/goal/runtime/goal_loop.py:2-7,235-249,286-334,445-464`.
- Dispatch and Orchestrate authority: `formulae/dispatch-spec/SKILL.md:137-145` and `runtime/orchestrate/SKILL.md:79-84,102-192`.
- Craft mediation: `arcana/craft/SKILL.md:129-150,312-317` and `arcana/craft/ARCHITECTURE.md:241-260`.
- Repository and artifact enumeration return: `docs/analysis/arcanum-migration/research/current-arcanum/research.md:10-159`.
- Runtime-flow and evidence-class return: `docs/analysis/arcanum-migration/research/current-arcanum/research.md:165-258`.
- Operability, consequence, and workaround return: `docs/analysis/arcanum-migration/research/current-arcanum/research.md:260-340`.
- Current dispatch handoff evidence: `.arcanum/runtime/subagents-strategy/2026-08-28-current-arcanum-research.explorers-to-synthesis.handoff.json`.
- Historical close input: `.arcanum/runtime/subagents-strategy/2026-08-28-current-arcanum-research.close.tmp.json`; the paired close row is absent from `.arcanum/observability/subagents-strategy/subagents-dispatch.yaml`.

## Limitations and evidence boundary

This synthesis is based on the original dirty repository snapshot, source and contract inspection, stored fixtures and receipts, independent enumeration, and preserved historical research-dispatch artifacts. It does not prove historical completeness, production frequency, performance, user impact, or the absence of execution evidence outside the repository. The original canonical Research synthesizer/skeptic/writer sequence did not execute. A later owner-conformant detailed review independently challenged this document and supplied the verified corrections above; that later review does not retroactively complete the original dispatch or turn later remediation into original evidence.

**One-line answer:** Arcanum today is a broad, owner-partitioned capability and artifact system with real bounded execution witnesses, but its representations drift, several advertised compositions stop short of live integration, its current map cannot prove repository coverage, and important operational prevalence and end-to-end behavior remain unknown.
