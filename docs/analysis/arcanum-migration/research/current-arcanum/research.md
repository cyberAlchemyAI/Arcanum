# Current Arcanum — Collected Research Returns

## Objective

Preserve the three explorer returns from registered dispatch
`2026-08-28-current-arcanum-research` without promoting them to accepted
findings. The explorer-to-synthesis handoff is blocked because the registered
downstream topology conflicts with the canonical Research owner contract.

## Return: repository-artifact-cartographer

task_status=completed  
domain_gate_status=pass

### Key Findings

- The smallest repository-evidenced discovery denominator is the current physical tree excluding `.git`: **7,817 files across 29 top-level repository scopes**. It includes 45 `arcana/*/SKILL.md` packages, 5 formulae packages with `SKILL.md` or `README.md`, 11 transmutations, 17 spell packages, `runtime/orchestrate`, registries, framework contracts, generated runtime surfaces, `.arcanum` state, research, sessions, benchmarks, development material, projects, ontology, definitions, disciplines, tools, and docs. This is materially broader than the 13 minimum roots named by the analysis at `docs/analysis/arcanum-migration/analysis.md:129-133`.
- The current mapping machinery **reconciles declared entries; it does not discover the repository universe**. The schema accepts any nonempty `discovery.roots`, methods, and edge list (`current-system-map.schema.json:85-119`). The validator loads only the supplied document, checks references among its declared inventory/relation/edge sets, and derives structural completion from absence of those internal errors (`validate_mapping.py:97-180`); it contains no filesystem enumeration. The example declares only `arcana/craft`, one edge, and `structurally_complete: true` (`current-system-map.example.json:9-25,60-63`). The analysis statement that the validator checks discovery closure (`analysis.md:131-133`) is therefore stronger than the implementation.
- No canonical executable map currently exists at `docs/analysis/arcanum-migration/mapping/current-system-map.json`. The validator’s default points there (`validate_mapping.py:25-29,183-194`) and presently returns `BLOCK: missing file`. The checked example also cannot currently validate because its clean-git baseline commit is not resolvable. Consequently, there is no present machine-readable coverage result to compare with the denominator.
- Artifact authority is explicitly plural. The constitution separates versioned source, intentionally promoted durable evidence, ignored-by-default generated output, and never-versioned local runtime state (`framework/ARTIFACT-CONSTITUTION.md:3-6,10-24,26-43,60-73`). Specific owners further distinguish canonical state from projections: Craft makes `.craft/ledger.yml` authoritative and `CRAFT.md`/`index.json` derived (`arcana/craft/SKILL.md:56-71`); Invoke Plan makes `WORK-PACK.md` canonical execution state while task, wave, execution-pack, and execution-entry files are specialized companions or projections (`spells/invoke/plan.md:184-223`); Orchestrate separates causal `events.jsonl` from non-causal `residue.jsonl` (`runtime/orchestrate/SKILL.md:240-251`).
- Declared lookup and projection surfaces do not equal the physical capability universe. Physical package comparison found 12 `arcana` packages absent from `registry/SIGILS.md`, two formulae packages absent, and five spell packages absent from `registry/SPELLS.md`; examples include `arcana/research-tower/`, `arcana/verification-weaver/`, `formulae/dispatch-spec/`, and `spells/invoke/`. The registries declare themselves quick-reference/offered-composition indexes and require updates when capabilities change (`registry/SIGILS.md` table at lines 9-56 and maintenance rule under `## Maintenance Rule`; `registry/SPELLS.md:9-22,27-40`). This establishes representation divergence, not operational consequence.

### Explicit Discovery Denominator

Method: recursive physical-file enumeration of the current working tree with hidden files included, excluding `.git`; cross-checked against `git -c safe.directory=C:/Users/thiag/Arcanum ls-files`.

- Current physical files excluding `.git`: **7,817**
- Tracked-path catalog: **7,795**
- Dominant physical scopes:
  - `arcana/` 2,206
  - `spells/` 1,674
  - `research/` 826
  - `development/` 720
  - `formulae/` 539
  - `.claude/` 305
  - `projects/` 290
  - `benchmark/` 274
  - `tools/` 224
  - `transmutations/` 193
  - `docs/` 120
  - `framework/` 99
  - `runtime/` 88
  - `.agents/` 85
- Principal physical formats: 4,822 Markdown, 1,684 JSON, 288 Python, 177 shell, 119 YML, 98 TypeScript, 87 HTML, 78 ZIP, 67 PNG, 66 JSONL, 56 log, and 48 YAML files.
- Capability-package denominator:
  - 45 `arcana/*/SKILL.md`
  - 5 `formulae/*/{SKILL.md|README.md}`
  - 11 `transmutations/*/SKILL.md`
  - 17 `spells/*/README.md`
  - `runtime/orchestrate/`
  - 10 currently exposed `.agents/skills/*` packages, plus larger `.claude/skills/` and legacy `.codex/` surfaces.

Exclusions:

- `.git/**`: repository metadata, not an Arcanum-produced artifact surface.
- External consumer repositories and user-global runtime homes: outside the requested repository boundary.
- In-memory chat/tool state: not repository artifacts.
- Runtime-success claims: explicitly excluded; inspected scripts, schemas, fixtures, and present files establish only documented/implemented/fixture-backed surfaces.
- Proposed future lifecycle boundary, migration design, removals, and fixes: excluded.
- Database family: no current physical SQLite/database file was found. The constitution only classifies `*.sqlite*` as local runtime artifacts (`framework/ARTIFACT-CONSTITUTION.md:60-73`).

Limitations:

- The tree is dirty and contains current-dispatch temporary files under `.arcanum/runtime/subagents-strategy/`; counts are a present-tree observation, not a reproducible repository baseline. The analysis itself records the dirty-tree limitation at `analysis.md:135-139`.
- Git reports long-path warnings for deeply staged historical material. Recursive filesystem enumeration reported no enumeration errors, but semantic inspection of every one of 7,817 files was not attempted.
- Family-level classification does not prove every historical file has the nearby promotion rationale required by the constitution.

### Material Artifact Families

| Artifact family | Format/location | Producer → consumer | Persistence / authority | Lifecycle / validation / divergence evidence |
|---|---|---|---|---|
| Canonical capability packages | Markdown, JSON/YAML schemas, scripts, templates under `arcana/`, `formulae/`, `transmutations/`, `spells/`, `runtime/` | Capability maintainers → native agents, registries, installers, composed spells | Versioned source; owner package is canonical | Constitution classifies these as source (`framework/ARTIFACT-CONSTITUTION.md:10-24`). Package-specific validators vary. Registry coverage is incomplete relative to physical packages. |
| Registries and dependency catalogs | `registry/SIGILS.md`, `SPELLS.md`, `SIGIL-DEPENDENCIES.tsv` | Capability maintainers → lookup, bootstrap, selective installation | Persistent lookup/index surface; not the capability body | Registry maintenance rule requires synchronization. `tools/bootstrap_arcanum.sh:370-405` consumes and validates dependency metadata. Physical-vs-registry divergence is present. |
| Runtime skill projections and distribution bundles | `.agents/skills/`, `.claude/skills/`, `.codex/`, `docs/downloads/**/*.zip` | `tools/bootstrap_arcanum.sh` / sync tooling → Codex, Claude, legacy command users, download users | Tracked generated projection or compatibility artifact; canonical source remains tier package | Bootstrap records `canonical_source` and `mutation_policy: regenerate-from-canonical-source` (`tools/bootstrap_arcanum.sh:844-858,1189-1226`). `.agents/README.md:3-5` says packages are symlinks, but inspected packages are ordinary directories/files. Byte differences alone were not treated as semantic drift because generated frontmatter is expected. |
| Invoke lifecycle-authoring artifacts | Markdown/JSON: DEFINE, DESIGN, PLAN, implementation layering, `WORK-PACK.md`, task/wave files, manifests, transports, receipts under `spells/invoke/`, capability `development/invoke-runs/`, and project folders | Invoke modes → readiness, Task Session, Dispatch, Refresh, capability lifecycle owners | Mixed: authored source/current execution state plus run evidence; `WORK-PACK.md` owns current executable plan | `spells/invoke/README.md:22-26,66-101`; Plan boundaries at `spells/invoke/plan.md:184-223`. Multiple historical receipt-schema versions and deeply staged copies are present; authority is version/contract-specific rather than filename-only. |
| Craft project state | YAML ledger, Markdown view, JSON index, evidence under `.craft/` and capability examples | Authorized Craft operations → Craft readers, Goal, Task Session, project operators | `.craft/ledger.yml` source of truth; `CRAFT.md` human projection; `index.json` rebuildable projection | `arcana/craft/SKILL.md:56-89`. Supporting evidence/receipts persist under `.craft/artifacts/`. Older `development/craft/` is historical material, not runtime authority (`:33-54`). |
| Bounded execution and closeout artifacts | Context packs, semantic manifests, admission request/receipt, material packages, executor receipt, terminal receipt, closeout sync, continuity cursor under Task Session/Invoke run directories | Context Builder, Task Session, executor → validators, owner closeout routes, Continuation Router, Invoke Refresh | Mixed durable evidence, transient execution material, and owner-specific receipts; receipts are evidence rather than promotion authority | `arcana/task-session/SKILL.md:178-225,290-343,404-452`. Transients must be declared and absent before terminal reconciliation (`:293-343`). |
| Dispatch and Orchestrate control state | Dispatch JSON; schemas; run plan/state; action JSON; receipt JSON; `events.jsonl`; `residue.jsonl`; strategy registration; append-only YAML ledger under `formulae/dispatch-spec/`, `runtime/orchestrate/`, `.arcanum/runtime/`, `.arcanum/observability/subagents-strategy/` | Dispatch Spec / coordinator / host driver → Orchestrate, reducers, later-wave gates, auditors | Dispatch is route representation; runtime files are local state; append-only ledger supplies registration evidence | Orchestrate preflight and emitted state are documented at `runtime/orchestrate/SKILL.md:90-126`; causal/residue authority split at `:240-251`. `.gitignore:11-15` excludes `.arcanum/runtime/`; current dispatch JSON remains physical temporary residue. |
| Decision artifacts | Markdown decision records plus JSON request/receipt/override schemas under `docs/decisions/`, `decisions/`, root `DECISIONS.md`, and `arcana/decision-gate/` | Decision Gate/user → blocked work, callers, owning gates | Durable reusable decision record; admissibility and override receipts are narrower evidence | Default locations and contents: `arcana/decision-gate/SKILL.md:43-49,51-101`; override consumption is separately persisted and scoped (`:149-169`). |
| Continuation, Goal, and readiness control projections | Route receipts, execution-entry JSON, frontier snapshots, claims, staged deltas, audit receipts under `arcana/continuation-router/`, `spells/goal/`, readiness spells | Task Session/Goal/readiness → owner capabilities, gates, Task Session | Control evidence/projection, not protected-state authority | Continuation route receipt and separate owner receipt boundary: `arcana/continuation-router/SKILL.md:149-170,238-269`. Goal keeps staged proposals separate from direct ledger mutation (`spells/goal/README.md:89-105,129-155`). |
| Observability and reflection state | JSON config/state, append-only JSONL, Markdown reflection reports under `.arcanum/observability/` | Observability Setup, Signal Observer, hooks → Workflow Reflect, maintainers | Generated, repository-local evidence; preserved by default but not source authority | Package contract: `formulae/observability-setup/SKILL.md:35-83`. Constitution classifies indexes, signals, reflection state, runs, and reports as generated (`framework/ARTIFACT-CONSTITUTION.md:38-58,75-89`). |
| Knowledge, ontology, and definitions | Raw inputs, generated Markdown pages, JSON indexes, tags/logs, definition documents/indexes, ontology receipts | Inventory / Ontology Vault / Definitions Governance → lookup, context builders, downstream documents | Mixed immutable raw source, canonical definitions, and derived indexes | Inventory layout and producer/consumer model: `arcana/inventory/SKILL.md:14-35,37-56,103-140`; it explicitly treats `index.json` as primary machine view and validates projection conformance (`:129-176`). |
| Research, review, and session records | `research-initial-definitions.md`, dispatch JSON/JSONL, `research.md`, `findings.md`, `review.md`, session Markdown under `research/`, `docs/analysis/**/research/`, `sessions/` | Research/review/session owners → synthesis, later investigations, human readers | Persistent evidence/context; not automatically active policy | Research output split and citation retention: `arcana/research/SKILL.md:108-133`. Review persists only confirmed `review.md`, not attacker transcripts (`arcana/review/SKILL.md:37-41`). Sessions carry a 60-day `expires` field but have no automatic review (`arcana/close-session/SKILL.md:38-59,143-157`). |
| Fixtures, benchmarks, development runs, archives, and logs | Markdown, JSON, JSONL, logs, PNG, ZIP under `**/development/`, `benchmark/`, `docs/downloads/`, fixtures/tests | Harnesses, validators, build/export tooling → tests, review, distribution, historical inspection | Mixed curated durable evidence, reproducible generated output, historical working material, and packaged projection | Constitution distinguishes curated fixtures/reports from ignored generated runs and benchmark outputs (`framework/ARTIFACT-CONSTITUTION.md:26-58`). The tracked tree includes 78 ZIP and 56 log files; per-file promotion rationale was not reconciled. |

### Gaps or Inconsistencies

- The analysis mandates producer × write-location × artifact-family × consumer enumeration (`analysis.md:131-133`), but neither schema nor validator has a repository-derived denominator against which completeness can be tested.
- The schema’s discovered-edge shape records producer, write location, family, consumer, and status only (`current-system-map.schema.json:122-154`). It cannot directly encode persistence, retention, source-of-truth/projection class, mutation behavior, validator, or derivation/drift relation. Some can be buried in prose elsewhere, but are not typed artifact properties.
- The example’s single-root discovery and `structurally_complete: true` demonstrate that the schema permits a declared subset to self-close (`current-system-map.example.json:9-25,60-63`), even though the analysis requires substantially broader roots.
- The canonical map is absent, so the analysis open items are not carried in the promised typed `open_items` collection (`analysis.md:211-225`).
- Registry coverage differs from package-folder coverage:
  - unregistered Arcana: `audit-alignment`, `code-tag-audit`, `intent-route-resolver`, `invoke-example-runner`, `observability-derivation`, `research-evidence-harness`, `research-tower`, `sync-user-stories`, `test-derivation`, `verification-weaver`, `workbench-poll`, `workbench-up`;
  - unregistered formulae: `anti-bias-vector-composition`, `dispatch-spec`;
  - unregistered spells: `guide-architecture`, `inventory-recall-context`, `invoke`, `publication-research-pipeline`, `task-session-until-blocker`.
- `.agents/README.md:5` describes skill folders as symlinks; the inspected filesystem exposes ordinary directories/files. The current documentation and physical representation therefore differ.
- The artifact constitution calls development runs, observability records, benchmark artifacts/logs, and similar material generated/ignored-by-default (`framework/ARTIFACT-CONSTITUTION.md:38-58`), while the tracked catalog contains examples from those locations. This establishes a need for per-item promotion-evidence reconciliation, not a conclusion that tracking is invalid.
- Session nodes declare expiration but the workflow says there is no automatic review (`arcana/close-session/SKILL.md:52,156-157`); actual retention action is not established.

### Local Tensions

- Canonical capability ownership versus several tracked host-specific projections.
- Registry-as-quick-reference versus materially present but unregistered package folders.
- Constitution-level artifact classes versus producer-specific, path-dependent lifecycle rules.
- Source preservation versus large checked-in historical/staged run trees.
- Human and machine projections that intentionally duplicate data versus incomplete proof of projection freshness.
- Append-only evidence requirements versus local-runtime paths intentionally excluded from version control.
- A narrative claim of discovery closure versus a validator whose observable logic is declaration reconciliation.

These are representational or ownership tensions only; no severity or runtime consequence is inferred.

### Questions for Synthesis

- Should the synthesis use the physical-tree denominator, the tracked-path denominator, or both as separate coverage universes given the dirty working tree?
- Which of the 19 physically present but unregistered capability/spell packages are intentionally outside registry scope, and where is that authority recorded?
- Which tracked development, benchmark, log, and ZIP artifacts have adjacent promotion rationale, and which remain lifecycle-unknown?
- Are generated host packages expected to be complete mirrors, selected installations, or overlays? Current repository evidence supports all three mechanisms in different places.
- What authority governs retention after a session’s `expires` date, given the explicit absence of automatic review?
- Should artifact edges remain relation-level prose, or must synthesis distinguish family discovery from individual artifact-instance coverage?

### RQ Coverage

| RQ | Status | Evidence-bounded result |
|---|---|---|
| RQ-01 | supported | Denominator identifies canonical packages, runtime, registries, projections, state stores, governance, research/session evidence, benchmarks, development residue, and hidden runtime surfaces needed to explain the repository. |
| RQ-02 | supported at family level | Owner contracts establish differentiated authority for Craft, Invoke, Dispatch, Orchestrate, Task Session, Decision Gate, registries/installers, observability, research, review, and sessions. Per-file historical ownership remains incomplete. |
| RQ-03 | supported | Current validator reconciles declared map contents and baseline locators; it does not independently enumerate repository roots or artifacts. |
| RQ-04 | supported at artifact-family level | Twelve material artifact families are enumerated above with formats, locations, producers, consumers, mutations/projections, validators, and residue. Exhaustive instance-level classification of 7,817 files is not claimed. |
| RQ-05 | partial | Strong authority/persistence evidence exists for Craft, Work Pack, runtime events/residue, source/generated/local classes, decisions, observability, and sessions. Many historical artifacts lack reconciled retention and downstream-consumer evidence. |
| RQ-06 | partial | Explicit projections and duplications are established; registry/package and `.agents` documentation/filesystem divergence are established. Full semantic drift across generated projections was not tested. |
| RQ-07 | partial | Repository contracts support necessary source/governance cost, generated/projection cost, compatibility surfaces, and unresolved duplication/drift categories. Artifact variety alone was not converted into a complexity judgment. |
| RQ-23 | supported | The smallest warranted correction is textual: revise `analysis.md:133` from “The validator checks both claims” to state that the validator checks **internal reconciliation of declared roots, edges, relations, baseline, and blocking items only; repository-universe discovery remains externally evidenced and unverified**. This accurately states present coverage without prescribing architecture or implementation. |

evidence:

- Validated initial-definitions baseline SHA-256: `9de54771bb6bbb012279b5c44fab115f59585faf1027586eaf43abf4b8a49f77`.
- Exact repository locators and line selectors are embedded above.
- Read-only validator observations:
  - example: unresolved clean-git baseline and evidence;
  - default map: missing `mapping/current-system-map.json`.
- Physical and tracked counts were independently enumerated; no repository file was edited.

limitations:

- Dirty, changing working tree; no reproducible full-tree baseline.
- No runtime success, operational consequence, severity, future architecture, removal, migration design, or proposed system-fix claim.
- No exhaustive semantic audit of every generated projection or historical artifact.
- No database artifact found; absence is limited to the current physical tree.

blockers:

- None for this bounded repository-artifact cartography task.
- A decision-ready global map remains unestablished because the canonical map is absent and the repository-wide denominator is not validator-bound.

residue:

- No files created or modified.
- Current-dispatch temporary JSON files already exist under `.arcanum/runtime/subagents-strategy/`; they were observed only.
- Open synthesis residue: intentionality of registry omissions, projection selection policy, historical artifact promotion rationale, and retention enforcement.

reroute:

- Return to the parent synthesizer for cross-agent reconciliation. No further repository mutation or runtime verification is authorized.

## Return: runtime-flow-verifier

task_status=completed  
domain_gate_status=pass

### Key Findings

- Arcanum’s principal behavior is a family of owner-preserving flows, not one linear runtime. Invoke authors plans/work packs; readiness owners assess selection/admission; Task Session executes one bounded unit; Decision Gate owns consequential choices; Continuation Router admits and joins one owner hop; Craft alone owns its ledger; Dispatch Spec validates routes while Orchestrate owns native scheduling and closeout. Evidence: `spells/invoke/README.md:150-193`, `arcana/task-session/SKILL.md:38-44,249-326,469-470`, `arcana/continuation-router/SKILL.md:147-170`, `formulae/dispatch-spec/SKILL.md:137-145`, `runtime/orchestrate/SKILL.md:75-84`.
- The strongest inspected cross-owner execution witness is one bounded Task Session → Invoke Refresh → Continuation Router sequence for `SWU-TSGR-001`. It preserves an approval block, later mutation admission, a passing Task Session result, an Invoke owner receipt, and a joined continuation receipt returning `SWU-TSGR-002` without executing it. Evidence: `.../task-session-review/PRE-MUTATION-REVIEW.json` (`result=BLOCK`, Decision Gate blocker); `.../task-session-apply/mutation-admission-receipt.json` (`admissionVerdict=admit`); `.../work-pack/results/SWU-TSGR-001-RESULT.json:1-61`; `.../work-pack/closeout/SWU-TSGR-001-INVOKE-OWNER-RECEIPT.json:1-39`; `.../work-pack/closeout/SWU-TSGR-001-CONTINUATION-OWNER-RECEIPT.json:1-24`. This is repository-preserved bounded run evidence, not proof of every Task Session or production route.
- Current deterministic implementation is materially narrower than several owner contracts. Task Session’s governance runner explicitly omits whole-run closeout, owner hooks, continuation, and observation, ending with `next_action=owner-hooks-not-implemented` (`arcana/task-session/scripts/task-session-governance-runner.py:2-7,2870-2881`). Goal’s current runtime calls itself a read-only skeleton, builds synthetic receipts, and never applies Craft state (`spells/goal/runtime/goal_loop.py:2-7,235-249,286-334,445-464`), although its reusable contract describes dispatch, audit, staged delta, approval, and Craft apply (`spells/goal/README.md:82-108`).
- Readiness is explicitly non-mutating and layered. WPRA captures and rechecks an immutable frontier, simulates graph/runtime/receipt behavior without executing commands, and emits a proposal-only Invoke Refresh pack (`spells/work-pack-readiness-audit/README.md:56-87,101-197`). Implementation Readiness then manages a one-action outer loop and treats `task-ready` as entry to Task Session, not mutation authority (`spells/implementation-readiness/README.md:47-120`). Task Session alone issues the later live mutation-admission verdict (`arcana/task-session/SKILL.md:286-326`).
- Capability lookup and evidence projections are not uniformly current. Registries declare themselves catalogs (`registry/README.md:1-13,37-39`), while canonical owners retain authority. The repository-local `.agents/skills/craft` points to `../../development/craft`, whose own contract says it is superseded and must not be used as runtime authority (`development/craft/SKILL.md:14-17`); current Claude projections advertise Task Session `0.3.1` and Invoke `0.2.0`, versus canonical `0.8.3` and `0.5.0`. This proves local projection disagreement, not system-wide runtime failure.

### Flow-by-Flow Evidence Matrix

| Flow | Initiation / coordinator | Inputs → outputs and transitions | Authority / completion | Evidence status |
|---|---|---|---|---|
| Invoke Plan → readiness → Task Session | User invokes Plan; Invoke coordinates authoring; WPRA/Implementation Readiness coordinate pre-execution decisions | Intent/design → work pack, SWUs, validation contracts → immutable audit snapshot/report → selection/intent binding → `task-ready` → Task Session context and mutation admission | Invoke owns authored artifacts; readiness admits selection only; Task Session owns execution and live mutation admission. Complete only after a fresh Task Session receipt, not readiness pass. | Documentary: strong. Implementation: WPRA and outer-loop code present (`audit_work_pack.py`, `execution_loop.py`). Fixtures: present. Observed end-to-end: partial/bounded only. |
| Task Session → Decision Gate | Task Session detects two or more admissible consequential options | Task context/options → admissibility receipt → durable decision record; unresolved choice transitions session to `BLOCK` | Decision Gate owns preference resolution, not application-specific validity or target mutation. Completion requires resolved blockers or a valid narrowly scoped override. | Documentary and tooling implemented (`arcana/decision-gate/SKILL.md:51-101,139-171`). Stored SWU witness shows a real approval block. No universal caller integration established. |
| Task Session execution → Invoke Refresh closeout → Continuation join | Task Session produces terminal result; required closeout sync derives exact authorization; Continuation Router selects owner | Terminal receipt + target inventory/baselines/deltas → material package/admission → Invoke owner receipt → joined continuation receipt → next route | Task Session cannot perform Invoke mutation; Router cannot perform owner work; Invoke owns Refresh; source result remains separate. Complete when owner receipt is schema-valid and joined; next route is reported, not recursively executed. | Strong contract; partial generic implementation because main runner omits owner hooks; one strong bounded historical chain observed. |
| Craft ↔ Decision/Task outcomes | Caller identifies that external evidence affects a selected Craft scope | Native receipt/decision → caller translation → scoped Craft `decide` or other operation → ledger update/recomposition | `.craft/ledger.yml` is source of truth; `CRAFT.md` and index are projections. Craft never rewrites native owner results (`arcana/craft/SKILL.md:56-71,235-268`). | Documentary. Manual/caller-specific witnesses exist. Generic semantic write-back coordinator or adapter: not found. |
| Craft-backed Goal loop | User names goal/Craft context; Goal coordinates frontier rounds | Craft frontier → risk → dispatch route → synthetic/current owner receipt → audit → staged delta → approval token → Craft apply request | Goal owns snapshot/routes/proposals, not Craft mutation. Completion requires terminal lanes, audit acceptance, explicit approval, and Craft-owned validation (`spells/goal/README.md:58-68,82-108,144-168`). | Contract broad; implementation is read-only/synthetic. Fixture report passes bounded cases (`spells/goal/validation/results/fixture-report.md:1-36`). Live end-to-end owner dispatch/apply: not found. |
| Dispatch Spec → Orchestrate | Caller supplies dispatch; Dispatch Spec validates; Orchestrate preflights and schedules | Dispatch JSON → validation → registration/authorization/host checks → action plan → spawn/wait/terminal/join/gate events → paired strategy close | Dispatch Spec owns shape only. Orchestrate owns host-native actions and causal closeout; delegated capability owns its result; lifecycle authority remains external (`runtime/orchestrate/SKILL.md:79-84,102-137,139-192`). | Implementation and extensive fixtures present. Current research dispatch validated `pass` in this investigation, but it is `binding_mode=descriptive`, retains `authorization=requires_user_permission`, and has no Orchestrate causal event stream; therefore it is not an Orchestrate execution witness. |
| Registry → generated/native projections | Registry/build/bootstrap tooling | Canonical packages + dependency manifest → catalogs, downloads, host projections/aliases | Registry is lookup; canonical owner contract governs responsibility; generated surface should identify canonical source and regeneration ownership. | Documentary and builder implementation present. Local projection disagreements observed; downstream impact remains flow-specific. |
| Experiment Harness → Signal Observer | Developer runs harness mode; harness coordinates examples/loops; observer runs post-result | Contract/profile/prompts → attempts/output/log/report → invocation envelope → JSONL signal/reflection counters | Harness owns testing mechanics, not target semantics; observer is non-blocking and cannot change primary outcome (`arcana/experiment-harness/SKILL.md`, `<artifact-boundary>`; `arcana/signal-observer/SKILL.md`, `<authority-rule>`). | Scripts, deterministic reports, and claimed live-loop reports exist. They prove named harness cycles only. Current `.arcanum/observability/` lacks the configured central signal ledger, reflection state, and hook ledgers, so repository-wide observed coverage is unavailable. |

### Gaps or Inconsistencies

- No generic current Craft write-back coordinator or typed semantic adapter was found. This remains `not_found` in the inspected flows, not proof that no private consumer integration exists.
- Task Session’s canonical closeout contract and its main governance runner differ: the contract requires owner synchronization; the runner intentionally stops before that responsibility.
- Goal’s contract describes a broad autonomous control spine, while the shipped runtime is explicitly a non-mutating fixture/caller-payload skeleton.
- Current observability configuration names `signals/sigil-invocations.jsonl` as source of truth, but that file, `reflection-state.json`, and hook JSONL ledgers are absent. The subagent-strategy YAML ledger exists independently.
- The existing analysis’s evidence manifest is stale for current Orchestrate and Implementation Readiness bytes. It records Orchestrate contract hash `895f...`, coordinator `b30f...`, and Implementation Readiness `6cdd...` (`analysis.md:148-152`); current hashes are respectively `5cf208...`, `87bee4...`, and `1556ce...`. This limits currentness but does not refute each claim.
- No universal same-concern precedence rule was found for disagreements among canonical contracts, schemas, implementations, registries, and generated projections.

### Local Tensions

- `analysis.md:101` defines “observed” to include a fixture, run, or receipt, while the validated current baseline requires fixture/test witness and observed execution to remain separate. `analysis.md:112` similarly groups fixtures and bounded historical runs as “observed.”
- `SWU-TSGR-001-RESULT.json:13-37` reports one declared validation command blocked, followed by a passing accepted equivalent; the overall result is pass. This is explicit residue, not a clean all-declared-commands-pass witness.
- The current research dispatch is schema-valid and registered, and this agent is a live bounded host witness, but the dispatch remains descriptive and lacks Orchestrate causal events. It must not be used to claim Orchestrate execution.
- Experiment Harness reports claim live Codex loops passed, but those preserved reports were not replayed here; their scope remains the named historical cycles.

### Contrary Evidence

- The stored Task Session/Invoke/Continuation receipts counter any claim that no cross-owner closeout has ever occurred; they support exactly that bounded chain.
- Goal fixtures counter a claim that no Goal mechanics are implemented, but do not counter the narrower finding that live owner dispatch and Craft apply are absent from the current runtime.
- The current Dispatch Spec validator returned `VALIDATION=pass` for the registered research dispatch, countering a claim that it is merely unvalidated prose; it does not establish native execution.
- Canonical Craft and generated Orchestrate surfaces explicitly name their source authority, countering a claim that every projection lacks provenance. The inconsistency is local, not universal.

### Questions for Synthesis

- Should preserved receipts be labeled “bounded historical execution witness” rather than the existing analysis’s broad “observed” category?
- Should the current research fan-out be recorded as native host execution under Subagent Strategy while explicitly excluded from Orchestrate evidence?
- How should synthesis represent projection disagreements whose operational consumers are unknown?
- Does accepted-equivalent validation remain sufficient for the named SWU witness, or should its evidence state be `partial` because one declared command blocked?
- Which owner, if any, authoritatively resolves same-concern contract/projection/implementation disagreements?

### RQ Coverage

| RQ | Coverage | Evidential resolution |
|---|---|---|
| RQ-08 | answered for principal inspected relations | supported, relation-specific |
| RQ-09 | partial | supported for bounded flows; unknown for universal/current end-to-end behavior |
| RQ-10 | answered | supported mainly by contracts, with implementation and receipt witnesses where noted |
| RQ-11 | partial | named components connected; several generic integrations remain not found or unobserved |
| RQ-12 | answered for matrix claims | supported with exact evidence classes and scopes |
| RQ-13 | answered | documentary, implementation, fixture/test, stored execution, partial, contradictory, not found, and unknown kept separate |
| RQ-14 | partial | concern-specific authority is supportable; universal precedence is not found |
| RQ-15 | partial | no clear system-wide generalization from the strongest bounded flow was found, but the existing analysis collapses fixtures and runs into one “observed” class and contains broad claims backed by stale hashes |

evidence:

- Validated baseline read fully; SHA-256 `9de54771bb6bbb012279b5c44fab115f59585faf1027586eaf43abf4b8a49f77`.
- Current registered dispatch validated read-only with `VALIDATION=pass`.
- Exact contracts, implementation sources, fixtures/reports, stored run receipts, registries, projections, and observability state cited above.

limitations:

- Read-only investigation; no files changed.
- No fixture suite, live Goal loop, live Experiment Harness loop, or Orchestrate native causal run was executed.
- Stored reports and receipts were inspected, not independently replayed.
- This is a principal-flow investigation, not a repository inventory or proof of every consumer/runtime.
- Current dispatch closeout was not yet available while this agent returned.

blockers: none

residue:

- Universal source-precedence rule unresolved.
- Generic Craft write-back and Task Session main-runner owner-hook integration not found.
- Goal live end-to-end dispatch/apply and current central observability coverage remain unestablished.
- Projection-consumer impact remains unknown.

reroute: parent synthesis; preserve this return verbatim, then route the resulting findings through the declared coverage and claim-to-proof skeptic gates.

## Return: operability-problem-falsifier

### Key Findings

- The strongest demonstrated runtime gap is bounded to the deterministic Task Session runner. Its contract makes terminal closeout synchronization required for changed evidence/status/route and says missing or unjoined owner receipts make the Task Session result `BLOCK` (`arcana/task-session/SKILL.md:402-440`). The runner, however, intentionally omits whole-run closeout, owner hooks, and continuation (`arcana/task-session/scripts/task-session-governance-runner.py:2-7`) and returns `next_action: owner-hooks-not-implemented` after commit (`:2870-2881`). This is a recurring structural limitation of that runner whenever owner synchronization is required; repository-wide frequency is unknown.
- Goal’s advertised composition is ahead of its packaged runtime. Goal is registered as reusable and described as driving a Craft-backed work graph (`spells/goal/README.md:3`; `registry/SPELLS.md:22`), but `goal_loop.py` identifies itself as a read-only fixture runtime (`spells/goal/runtime/goal_loop.py:2-7`), constructs its own terminal “execution” receipt rather than invoking Task Session (`:235-249`), and never directly applies to Craft (`:286-334`). This demonstrates incomplete cross-owner execution, not a failed live deployment: no live use-rate or failed production invocation was found.
- Generated runtime projections demonstrably drift from their declared canonical sources. Current hashes differ for Research, Task Session, and Invoke; Task Session is canonical `0.8.3` versus projected `.claude` `0.3.1`, and Invoke is canonical `0.5.0` versus projected `0.2.0`. Research differs substantively: canonical requires a synthesizer, skeptic exchange, then separate writer (`arcana/research/SKILL.md:28-60`), while the active generated projection exposes a different contract (`.agents/skills/research/SKILL.md:74-117`). The current dispatch ledger assigns the pre-skeptic synthesis role to a `writer`, with feedback returning to that same group (`.arcanum/observability/subagents-strategy/subagents-dispatch.yaml:64,76-77`). This is a witnessed operating-contract ambiguity across canonical, generated, and dispatch surfaces. Effects beyond these inspected packages are unknown.
- Manual coordination across authority boundaries is witnessed, but is not by itself a defect. Craft deliberately owns only its selected ledger and requires external resolutions to return through `decide` (`arcana/craft/SKILL.md:129-150,312-317`). Craft also explicitly lacks an automated runner, public CLI, row updater, and route-exchange schema (`arcana/craft/SKILL.md:14-19`; `arcana/craft/ARCHITECTURE.md:241-260`). A historical user-invoked Decision Gate (`docs/decisions/craft-distill-receipt-route.md:1-17`) and a Goal apply receipt attributed to `local-fallback` witness the coordination burden. Its time, error rate, and recurrence are not measured.
- The migration-analysis validation path is presently blocked locally: the documented default artifact is `mapping/current-system-map.json` and the documented command uses `--require-ready` (`docs/analysis/arcanum-migration/analysis.md:119-137`), but that file is absent. The validator deterministically treats a missing input as `BLOCK` (`docs/analysis/arcanum-migration/scripts/validate_mapping.py:28-38,183-215`). This establishes an analysis-package failure, not an Arcanum runtime-wide failure.

### Problem Ledger

| Candidate | Classification | Scope / boundary | Recurrence and severity supported | Evidence / confidence |
|---|---|---|---|---|
| Task Session main runner stops before required owner synchronization | Demonstrated implementation burden / blocked completion path | Cross-boundary: Task Session → Continuation Router → Invoke Refresh or another owner | Structural on every use of this runner requiring synchronization; actual run frequency unknown. High consequence for those runs only. | Contract and current implementation; high confidence in limitation, low confidence in prevalence |
| Goal does not execute its advertised cross-owner loop | Demonstrated implementation limitation; operational failure unverified | Cross-boundary: Goal → Task Session / Decision Gate / Craft | Packaged runtime always synthetic/read-only; no evidence of live failure frequency. Potentially high consequence if treated as deployed. | Current code and registry; high confidence in limitation, unknown deployed impact |
| Canonical/generated instruction drift | Demonstrated inconsistency with operating ambiguity | Projection and host-authority boundary | Three inspected package pairs drift; current research dispatch supplies one concrete process consequence. Wider rate unknown. | Current bytes/hashes and dispatch ledger; high confidence for inspected packages |
| Craft write-back requires operator/caller mediation | Deliberate governance/ownership cost with demonstrated manual burden | Craft ↔ external owners | Two bounded historical patterns: user-invoked gate and `local-fallback` apply. No cost or error metrics. | Contracts plus historical receipts; high confidence in mediation, low confidence in aggregate cost |
| Missing current-system map | Demonstrated blocked path | Local to migration-analysis package | Current state; default validation cannot start. Severity high for claiming map readiness, irrelevant to unrelated runtime paths. | Independent file-existence check plus validator code; high confidence |
| Invoke absent from Spell Registry while present as lifecycle entry | Apparent inconsistency; deliberate classification or impact unknown | Registry/discovery boundary | One current omission. No failed resolver or user lookup was witnessed. | `registry/SPELLS.md:1-35`; `README.md:148-161`; insufficient to call a problem |
| Two renamed provenance links in lifecycle session | Demonstrated local navigation burden | One session artifact | Two links only; low severity. Targets point to a nonexistent former directory. | `sessions/2026-08-26-1400-artifact-lifecycle-repository-direction.md:27-28`; current path check |
| Prior claim that Task Session automatically updates Craft | Challenged / no longer current | Current migration prose | Earlier review finding is stale against current text. | Current analysis explicitly requires a separate caller and denies automatic update (`analysis.md:70`); not a current problem |

### Gaps or Inconsistencies

- No repository-wide operational telemetry was found: `.arcanum/observability/` contains configuration, placeholders, and the dispatch ledger, but no material run corpus. Recurrence, failure rate, duration, retry count, and operator effort therefore remain unresolved.
- The bounded historical Task Session → Invoke owner receipt proves one successful chain, but not that the current main runner performs it automatically.
- Generated projection divergence is clear, but no repository-wide freshness/parity rule establishes which differences are permitted.
- Goal’s “registered reusable” status and fixture-only runtime are in tension; whether “reusable” intentionally means contract/fixture maturity rather than deployed orchestration is not explicit in the inspected surfaces.
- Git baseline/state assertions were not independently recomputed because Git rejected this process under its safe-directory ownership check. File-content claims use directly read current bytes; the supplied baseline SHA-256 was independently confirmed.

### Local Tensions

- Fail-closed governance increases explicit preparation and owner-receipt work, but the evidence does not establish that this deliberate cost is excessive.
- A runner may validly pass its bounded transaction while still leaving the broader capability flow unfinished; treating its `pass` as end-to-end completion would overstate evidence.
- Generated projections are necessary compatibility surfaces, yet checked-in copies can expose stale semantics. Drift is demonstrated; the value or necessity of each projection is not disproved.
- Goal’s skeleton safely refuses protected mutation, but that same safety means it cannot witness the advertised autonomous composition.

### Current Workarounds or Mitigations

- Task Session owner transitions have been completed through separately produced material packages and owner receipts in bounded historical runs; effectiveness is proven only for those exact artifacts.
- Craft coordination uses explicit user/caller invocation, Decision Gate records, scoped approval tokens, and `local-fallback` application. These preserve ownership attribution but have no measured cost profile.
- Generated packages declare `canonical_source`, `generated_by`, and `mutation_policy: regenerate-from-canonical-source`, providing provenance and a regeneration path. No current freshness guarantee was established.
- Goal stages deltas and emits `craft_apply_request=true` while keeping `direct_apply_performed=false`, mitigating unauthorized mutation but not completing the cross-owner flow.
- The current analysis now explicitly distinguishes its minimum product model from the wider orientation inventory and denies ambient Task Session → Craft propagation (`analysis.md:31,70,89-99`).

### RQ Coverage

| RQ | Status | Supported answer / boundary |
|---|---|---|
| RQ-16 | answered | Bounded operational limitations are supported for Task Session owner closeout, Goal cross-owner execution, generated-contract ambiguity, and the missing mapping input. No system-wide unreliability claim is warranted. |
| RQ-17 | answered | Consequential inconsistency: generated Research contract drift affects current dispatch shape. Low local consequence: broken provenance links. Unknown/inert: Invoke registry omission. Artifact count alone establishes nothing. |
| RQ-18 | unresolved | Scope and structural recurrence are established per candidate, but incident frequency, user reach, elapsed cost, retry rate, and aggregate severity are absent. |
| RQ-19 | answered | Mapping failure and broken links are local. Task Session closeout, Goal execution, Craft mediation, and projection drift emerge across handoff or authority boundaries. |
| RQ-20 | unresolved | Manual gates, local fallback, separate owner receipts, staged deltas, compatibility projections, and regeneration metadata are evidenced; effectiveness and cost are only bounded or unmeasured. |
| RQ-21 | answered | Task Session/Goal gaps are incomplete implementation; projection drift is representational inconsistency; Craft separation is deliberate authority cost; registry omission has unresolved status; no missing cross-owner authority was automatically classified as defective. |
| RQ-22 | unresolved | Missing telemetry, unknown active-surface precedence, uncertain projection parity, no deployment/use denominator, and inability to verify current Git state limit a trustworthy system-wide problem account. |

### Questions for Synthesis

- Which named runners are actually used for current Task Session and Goal operations, and at what frequency?
- Does “registered reusable” assert deployable end-to-end behavior, or only a reusable contract and fixture surface?
- Which source governs behavior when canonical and generated skill packages differ, and which current hosts consume each projection?
- How often do Craft write-backs require operator intervention, and are there recorded unsuccessful or abandoned handoffs?
- Is Invoke intentionally excluded from the Spell Registry because it is a lifecycle front door rather than a reusable composition?
- Can any available run corpus establish recurrence, user impact, or recovery cost without generalizing historical development witnesses?

### Explicit Unknowns

- End-to-end success and failure rates for Task Session closeout, Goal dispatch, Decision Gate activation, and Craft apply.
- Number of active users/hosts exposed to stale projections.
- Whether current generated drift is temporary worktree state, accepted semantic adaptation, or unintended staleness.
- External consumers of canonical paths, aliases, schema IDs, or generated provenance.
- Actual operator time, cognitive burden, and error rate for caller-mediated coordination.
- Whether the missing mapping artifact is expected work-in-progress or an unintended omission.
- Current clean/dirty Git baseline and commit identity from this execution context.

task_status=completed

domain_gate_status=pass

evidence=Validated baseline SHA-256 `9de54771bb6bbb012279b5c44fab115f59585faf1027586eaf43abf4b8a49f77`; current contracts, runtimes, schemas/validator, registries, generated projections, dispatch ledger, historical receipts, and review artifacts inspected read-only.

limitations=No end-to-end commands were run because the task was read-only and repository workflows can emit artifacts; no production telemetry corpus or external-consumer inventory was available; Git state verification was blocked by safe-directory ownership policy.

blockers=None for the bounded RQ-16–RQ-22 investigation.

residue=System-wide prevalence and severity remain unresolved; no files were created or modified.

reroute=Return to the registered synthesis group for reconciliation with the repository-universe and cross-capability-flow explorer evidence.
