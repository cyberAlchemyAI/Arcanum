# Invoke Design Mode

## Identity

- Spell: `invoke`
- Mode: `design`
- Status: deterministic W1 v2, W2 v2, and W3 v3 bundle/admission chain implemented for Define v3 inputs

## Purpose

Human readers should begin with the [Design overview](./design/README.md).
Agents and operators should follow the unified
[Design authoring guide](./design-authoring-guide.md), which gives the complete
W1-to-W3 CLI path and links the detailed stage guides below.

Design mode is intended to convert approved Define outputs into a governed
architecture/design bundle. The implemented W1 slice first closes the complete
Design input set inside one owner-approved discovery boundary and projects the
one legal scope manifest and fixed-point selection result. W2 then applies that
closed denominator in one `DESIGN-SOURCE.json`, projects a candidate, validates
the exact installed coherence policy independently, and publishes the atomic
candidate boundary. W3 binds that candidate to independently passing Distill
evidence, derives the deterministic fifteen-file Design bundle, independently
replays it, and admits only `artifact_authored`.

Design mode is non-mutating: it does not silently edit upstream spec, glossary, or Necronomicon context. Upstream corrections become patch requests, blocker decisions, or explicit gap-ledger entries.

## Implementation Coverage

- W1 is implemented by the canonical boundary-approval, input-closure,
  closure-receipt, and production-receipt schemas plus the closure validator,
  scope projector, and atomic input-bundle compiler.
- W1 publishes exactly four payloads plus
  `DESIGN-INPUT-PRODUCTION-RECEIPT.json`; a governed block publishes only the
  separate attempt receipt and leaves the success directory absent.
- W2 is implemented by the public profile, source, candidate artifact,
  coherence-policy, coherence-receipt, and candidate-production-receipt
  contracts plus the deterministic projector, independent validator, and
  atomic compiler.
- W2 publishes exactly `DESIGN.json`, `DESIGN-COHERENCE-RECEIPT.json`, and
  `DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json`. A governed failure publishes only
  the separate attempt receipt and leaves the success directory absent.
- W3 is implemented by the bundle-closure v2, block-attempt v2, v3 stage,
  projection, and independent admission contracts plus the pure projector,
  atomic compiler, replay validator, shared stage-contract validator, and
  Design-specific capability-resolver branch.
- W3 publishes exactly fourteen ordered payloads plus
  `INVOKE-DESIGN-STAGE-RECEIPT.json`. The admission receipt is written outside
  the bundle after clean replay. Design v1/v2 stage receipts and admission v1
  are historical only; they cannot establish a new PASS.
- The authoritative public W2 baseline is the exact installed
  `invoke.generic-design-baseline.v1` profile in
  `development/whole-invoke-repair-plan/design-process/DESIGN-PROFILE.json`.
  It fixes the typed-fact denominator, minimum core facts, six view IDs, and
  legal fact kinds per view. Historical templates are readable guidance only;
  they do not override this machine contract.
- Dedicated candidate family scaffolds for `architecture`, `research`, `ux-plan`, `spell`, and `sigil` are available as design companions.
- Runtime execution, registry release, and canonical template promotion remain gated by validation evidence and explicit approval.

## Activation Gate

Normal design mode requires:

- a real Define v3 stage receipt plus current drift-free Define admission v1,
- one machine-valid `DesignInputBoundaryApproval` binding the target,
  visibility, observation epoch, roots, required classes, discovery rules, and
  permitted exact exclusions,
- one digest-current `DESIGN-INPUT-CLOSURE.json`,
- explicit design-stage constraints,
- source contracts or approved discovery mode,
- a closed `DesignScopeManifest` bound to exact target and source selectors,
- lifecycle owner approval for L1 design work,
- template/profile selection evidence.

Discovery-mode W1 is allowed only with the same exact boundary approval. It may
produce input evidence and selection evidence but routes only to input review;
it cannot activate W2/W3 normal Design production.

W2 activates only from one exact normal W1 PASS bundle whose production
receipt routes to `design-authoring`. Discovery W1 evidence, copied W1 payloads,
an authored selection label, or an historical Design cannot activate W2.

W3 activates only from one exact passing W2 candidate receipt and a
schema-valid `DESIGN-BUNDLE-CLOSURE.json` that exact-binds the candidate,
installed process/profile/policy, fixed output contract, and Distill request,
event log, execution receipt, and independent validation result. Distill
`flag` or `block` routes to Design remediation and cannot publish a bundle.

## Required Sigils

| Sigil | Role In Mode | Required Mode |
| --- | --- | --- |
| `context-builder` | Build bounded design context from define outputs, constraints, and existing artifacts. | lean or standard |
| `structured-interview-kits` | Clarify missing design inputs one question at a time and capture approvals. | gap-check or equivalent one-question interview mode |
| `inventory` | Resolve architecture profile/templates and record selection evidence. | lookup, ingest, validate |

## Optional Sigils

| Sigil | Use When | Notes |
| --- | --- | --- |
| `architecture-pattern-inventory` | Existing patterns, reusable architectures, or design alternatives need lookup. | Supplies evidence; does not override design gates. |
| `decision-gate` | A blocker-level design decision cannot be resolved from available evidence. | Route only consequential unresolved choices. |
| `distill` | A draft design needs unit-size validation, split pressure analysis, or gap discovery before plan handoff. | Run a design-unit check and record `pass`, `flag`, or `block` unless design blocks before material exists. |
| `spellcraft` | Approved design output targets spell authoring or spell revision. | Invoke emits handoff context; Spellcraft owns spell lifecycle mutation, validation, install/adaptation, observation, and reflection. |
| `sigil-development` | Approved design output targets sigil authoring or sigil revision. | Invoke emits handoff context; Sigil Development owns sigil lifecycle mutation, validation, observability, reflection, and promotion readiness. |

## Inputs

Normal design inputs:

- exact boundary approval path,
- exact Define v3 stage and Define admission v1 receipt paths,
- canonical whole-file input catalog using `file:<repo-relative-path>`,
- typed scope signals with one `source_input_id` each,
- explicit conditional resolutions and conflicts,
- exact greenfield determination or one producer-backed predecessor Design,
- define context summary,
- template selection evidence,
- define decision and gap ledger,
- design constraints,
- source contracts,
- exact target footprint, declared field classes, exclusions, and author
  identity for `DesignScopeManifest`,
- optional existing implementation-layering seed or gap.

Discovery-mode inputs:

- user goal and scope hints,
- exact discovery-mode boundary approval,
- source evidence boundary,
- known constraints,
- required output depth.

Optional companion inputs:

- research question and source scope,
- user goals, workflow scope, and target actors,
- existing interfaces,
- target artifact type (`spell`, `sigil`, or neutral),
- Necronomicon concept sources for glossary consistency checks.

## Template And Profile Selection

| Selection | Use When | Required Output |
| --- | --- | --- |
| `invoke.generic-design-baseline.v1` | Normal W2 design from one exact normal W1 PASS bundle. | one typed fact registry and six ID-based view projections in `DESIGN-SOURCE.json`. |
| `architecture` family | Design needs source contracts, dependency/interface rules, decision log, risks, and design transport notes. | architecture plan artifact. |
| `research` family | Evidence is absent, contradictory, or insufficient for an architecture decision. | research brief with claim status and unresolved gaps. |
| `ux-plan` family | A natural person reads, decides, acts, recovers, navigates, or performs assistive operation through a new or changed rendered semantic contract. | UX plan and handoff boundaries. Backend files, APIs, receipts, or style-only changes do not select UX by themselves. |
| `spell` family | Target artifact is a spell. | spellcraft handoff context only. |
| `sigil` family | Target artifact is a sigil. | sigil-development handoff context only. |

The six required design views are:

1. Context view.
2. High-level structure view.
3. Low-level components view.
4. Workflow process view.
5. Decision flow view.
6. Dependency interface view.

## Design Selection Protocol

W1 begins from one canonical machine source and runs this fixed chain:

```text
boundary approval -> DESIGN-INPUT-CLOSURE.json
  -> DESIGN-INPUT-CLOSURE-RECEIPT.json
  -> DESIGN-SCOPE-MANIFEST.json
  -> DESIGN-DENOMINATOR-RECEIPT.json
  -> DESIGN-SELECTION-RESULT.json
  -> DESIGN-INPUT-PRODUCTION-RECEIPT.json
```

Run it with:

```text
tools/arcanum invoke design produce input-bundle \
  --closure DESIGN-INPUT-CLOSURE.json \
  --repo-root ROOT \
  --output ABSENT_DIRECTORY
```

Exit `0` is W1 PASS, exit `1` is a governed BLOCK with a schema-valid attempt
receipt, and exit `2` is malformed invocation or unavailable contracts where a
valid attempt receipt cannot be issued. See
[design-input-authoring-guide.md](design-input-authoring-guide.md).

W2 then runs this fixed candidate chain:

```text
DESIGN-INPUT-PRODUCTION-RECEIPT.json + exact W1 payloads
  + DESIGN-PROFILE.json + DESIGN-SOURCE.json
  -> staged DESIGN.json
  -> DESIGN-COHERENCE-RECEIPT.json
  -> DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json
```

Run it with:

```text
tools/arcanum invoke design produce candidate \
  --source DESIGN-SOURCE.json \
  --repo-root ROOT \
  --output ABSENT_DIRECTORY
```

Exit `0` publishes exactly the three named W2 files in one atomic directory
replacement. Exit `1` removes staging, leaves the success directory absent,
and writes one schema-valid attempt receipt. Exit `2` is malformed invocation
or an unavailable contract boundary where no valid receipt can be issued. See
[design-source-authoring-guide.md](design-source-authoring-guide.md).

W3 then runs this fixed bundle chain:

```text
DESIGN-BUNDLE-CLOSURE.json v2 + passing W2 v2 candidate + passing Distill evidence
  -> fourteen deterministic/copy-exact payloads
  -> INVOKE-DESIGN-STAGE-RECEIPT.json (v3)
  -> independent clean replay
  -> DESIGN-BUNDLE-ADMISSION-RECEIPT.json (outside the bundle)
  -> capability artifact_authored
```

Run production and admission with:

```text
tools/arcanum invoke design produce final-bundle \
  --closure DESIGN-BUNDLE-CLOSURE.json \
  --repo-root ROOT \
  --output ABSENT_DIRECTORY

tools/arcanum invoke design admit admission \
  --bundle BUNDLE_DIR \
  --repo-root ROOT \
  --output ABSENT_RECEIPT
```

See [design-bundle-authoring-guide.md](design-bundle-authoring-guide.md) and
the [W3 executable example](examples/design-bundle-v1/README.md).

The six views remain mandatory navigation, but they are not a completeness
proof. W1 selection uses three frozen public contracts:

1. the Design author closes `DesignScopeManifest`, including every declared
   field class, exact selectors and digests, evidence-backed exclusions, an
   empty `unknowns` set, and an author identity distinct from the detector;
2. `invoke-design-scope-extractor` inspects only those exact selectors and
   emits `DesignDenominatorReceipt`; it cannot select companions or validate
   its own receipt;
3. `invoke-design-selection-validator` unions authored concerns with extracted
   signals, binds every signal to one primary concern, resolves all ownership
   roles, assigns one of four dispositions, and emits
   `DesignSelectionResult`;
4. selection repeats once from the same immutable manifest and denominator.
   Any changed concern, owner, disposition, output, diagnostic, or digest
   blocks with `CHANGED_PASS_TWO`; there is no implicit third pass.

W2 adds the installed profile, canonical Design source, deterministic candidate
projection, independent coherence policy/receipt, and failure-capable candidate
production receipt. The source applies every W1 catalog item—including exact
excluded and conditionally excluded items—through one typed application pair;
projects all thirteen W1 signal classes without field loss; declares facts once;
and indexes only fact IDs into the six views. The validator, not the author or
projector, owns the coherence verdict.

The four dispositions are `required`, `recommended`,
`not-applicable-with-rationale`, and `block`. Only `required` selects an output.
N/A requires detector-negative evidence selectors. Missing input, unknown
scope, stale/self-issued receipt, unbound signal, unresolved owner, illegal
selection, or a changed second pass blocks.

Evidence states are separate:

- `authored-complete` means the Design and planned witness contracts exist;
- `design-validator-pass` means exact manifest, denominator, ownership,
  selection, and fixed-point checks passed;
- `plan-evidence-pending|pass|fail` belongs to Plan receipts and is never a
  `DesignSelectionResult` value.

An `authored-complete` Design may route only to a remediation Plan whose
declared purpose is to materialize the missing Design validator or fixtures.
Normal implementation planning requires `design-validator-pass`, begins at
`plan-evidence-pending`, and validates its own runnable witnesses.

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- | --- |
| 1 | `context-builder` | approved define outputs, constraints, existing artifacts | bounded design context | mandatory design inputs are identified | block on contradictory scope or missing core goal |
| 2 | `structured-interview-kits` | bounded design context | approved design intent and missing-input decisions | one-question cadence and explicit approvals captured | block on unresolved blocker ambiguity |
| 3 | `inventory` | approved design intent and local template inventory | architecture profile/template selection record | eligibility evidence is explicit and tie cases request user choice | flag when candidate template is usable but not promoted |
| 4 | optional `architecture-pattern-inventory` | design intent, source contracts, pattern question | pattern evidence and alternatives | evidence is cited and alternatives are bounded | flag when pattern evidence is unavailable but local design can proceed |
| 5 | optional `research` companion | evidence gap or contradiction | research brief and claim status | research question and source scope are present | block when evidence gap affects required design decision |
| 6 | Design scope extractor | closed `DesignScopeManifest` and repository root | current `DesignDenominatorReceipt` | every selector is in-root, readable, digest-matched, and independently detected | block with exact missing/stale/self-issued/unbound diagnostic |
| 7 | Design selection validator | manifest, denominator, authored concerns, predicate config, planned witness contracts | two-pass `DesignSelectionResult` | total binding, exact owners, legal dispositions/outputs, and fixed point pass | block without partial pass; preserve `authored-complete` |
| 8 | optional `ux-plan` companion | validator-selected `ux-plan`, actor, and changed semantic surface | UX plan and handoff boundaries | natural-person plus changed-semantic-contract predicate is true | block when selected UX inputs are incomplete; do not select from keywords |
| 9 | W2 Design candidate producer | exact normal W1 PASS bundle, installed public profile/policy/process, canonical `DESIGN-SOURCE.json` | atomic `DESIGN.json`, independent coherence receipt, and candidate production receipt | total application denominator, typed registry, six-view projection, selection closure, glossary consistency, Plan-evidence separation, and exact output inventory pass | publish no success directory; issue one governed attempt receipt when possible |
| 10 | optional `decision-gate` | unresolved consequential design blocker | decision record and next route | blocker resolved or explicitly deferred | keep blocker in gap ledger with recommended next action |
| 11 | W3 Design bundle producer and admission validator | passing W2 candidate receipt, bundle closure, and independently passing Distill evidence | atomic fifteen-file Design bundle plus external replay-admission receipt | exact input rehash, deterministic projection, v2 receipt closure, and byte-equal clean replay pass | publish no bundle on governed producer failure; leave submitted bundle unchanged on admission failure |

## Mode Gates

- Normal design blocks without approved define outputs unless discovery mode is explicitly approved.
- Normal W1 blocks unless the Define receipt, its installed producer identity,
  its exact output inventory, and the target through its source all validate.
- Every discovered regular file must be included exactly once or covered by one
  approved exact exclusion. Symlinks, traversal, absolute paths, duplicate
  normalized paths, empty rules, and implicit exclusion globs block.
- A passing `DESIGN-INPUT-PRODUCTION-RECEIPT.json` proves only approved-boundary
  closure, deterministic projection, denominator compatibility, and fixed-point
  selection. It is not a Design stage receipt.
- W2 requires the exact installed public profile, process, and coherence policy
  and a normal W1 PASS bundle located at the receipt-bound paths. Repackaged or
  discovery-mode W1 evidence blocks.
- The application denominator covers every catalog input, exact conditional
  resolution, constraint, invariant, prior decision, resolved conflict, scope
  signal, selection concern, selected output, planned witness, and Design kind.
  Excluded inputs require exact upstream exclusion evidence and zero fact IDs.
- All thirteen W1 signal arrays must project field-for-field into one fact of
  the profile-mapped kind. Every fact edge resolves; a workflow operator must
  be an `actor` or `component`; view membership is ID-only and profile-legal.
- Evolution admits exactly one real predecessor whose complete live bundle,
  `DESIGN.json`, v3 stage receipt, installed producer, target, digest, and
  ordered inventory validate. v1, synthetic, ambiguous, or mismatched
  predecessors remain blocked without implicit selection.
- W2 PASS publishes only the candidate, coherence receipt, and candidate
  production receipt. It grants no final Design stage PASS, Plan entry,
  capability admission, acceptance, execution, publication, or deployment.
- Source contracts are required unless discovery mode is approved.
- Template/profile selection must include eligibility evidence and explicit user choice on tie cases.
- The design output must include the six required design views or block.
- `DesignScopeManifest` must be schema-valid, digest-current, selector-closed,
  authored independently from the detector, and have no unknowns.
- A normal Plan handoff requires both the current producer-backed v3 Design
  stage receipt and its independent v2 replay-admission receipt. W2 candidate
  PASS remains insufficient.
- Every concern must name accountable, contributing, artifact, and validator
  owners and use exactly one of the four dispositions.
- Only `required` concerns may appear in `selected_outputs`; false N/A,
  selected recommendations, or unresolved owners block.
- Planned fixtures and validator contracts remain Design artifacts. They never
  count as executed Plan evidence.
- Glossary consistency must be checked against define glossary terms; conflicts are recorded and routed instead of silently promoted.
- Design mode may emit an implementation-layering seed or record a layering gap; full layering artifacts remain required only for `plan`, `full`, and `validate`.
- Design mode must not create work-pack tasks, execution-pack waves, or mutation-ready implementation steps.
- Candidate templates, glossary terms, registry entries, and Necronomicon concepts are never promoted automatically.
- Design-stage transport appends stage reports and complements matching Necronomicon sections only when they already exist.
- Spell and sigil lifecycle work routes to `spellcraft` or `sigil-development`; design only prepares handoff context.
- Design mode must record a Dispatch Spec technique trace that names the techniques used to justify profile/template selection, companion evidence, owner boundaries, and next route.
- Design mode must run a design-unit Distill check unless it blocks before design material exists; the result must identify the coherent unit, split pressure, and any gaps that affect plan readiness.
- A `flag` or `block` Distill result routes to `define`, design follow-up, or deferred follow-up; it must not silently advance to `plan`.

## Handoff Artifacts

The implemented W3 handoff contains:

- the canonical `DESIGN-SOURCE.json` path and digest;
- the exact W1 production receipt, closure, manifest, denominator, and selection
  bindings;
- the installed profile, process, and policy bindings;
- the atomic `DESIGN.json`, `DESIGN-COHERENCE-RECEIPT.json`, and
  `DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json` paths;
- the candidate result, blockers if any, and exact W2 evidence ceiling;
- the complete ordered fifteen-file bundle, v3 stage receipt, and independent
  admission receipt;
- the next route: `plan`, `spellcraft`, `sigil-development`, or `deferred`,
  derived from selected companion ownership and unresolved gaps.

Historical Design source and receipt families remain validate-only. W3
admission does not establish Plan evidence or Plan admission.

## Observability

When `.arcanum/observability/` exists, record:

- spell name and mode,
- phases attempted,
- sigils invoked,
- selected profile/templates,
- six-view coverage status,
- Design selection receipt path, evidence state, selected output IDs, and
  blocking diagnostics,
- glossary consistency status,
- gates passed, flagged, or blocked,
- artifact paths produced,
- transport status,
- unresolved gaps and blocker decisions,
- next route recommendation.

## Mode Output Contract

Return:

```markdown
## Outcome Brief

<Two to five plain-language sentences explaining what Design tried to establish,
what it established or why it stopped, and why that matters.>

- Objective: <what Design was trying to accomplish>
- Result: <what is now designed, flagged, or blocked>
- Why it matters: <practical consequence for the operator or next owner>

## Boundary and Next Decision

- Changed: <design artifacts, evidence, or state changed>
- Unchanged: <implementation, authority, promotion, publication, deployment, or other explicit boundaries>
- Open questions: <remaining uncertainty or none>
- User decision: <exact decision needed or none>
- Next action: <next bounded action and owner>

## Technical Details

## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block
- Mode contract: spells/invoke/design.md
- Outputs: <DESIGN.json path>, <DESIGN-COHERENCE-RECEIPT.json path>, <DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json path>
- Design views: context | high-level structure | low-level components | workflow process | decision flow | dependency interface
- Design selection receipt: <DesignSelectionResult path | blocked reason>
- Design evidence state: design-candidate-pass | block
- Evidence ceiling: W2 candidate coherence and atomic output closure only
- Plan evidence: plan-evidence-pending
- Template/profile selection: <selected profile and companion templates>
- Dispatch techniques: <technique ids and rationale>
- Distill validation: pass | flag | block | not applicable; <rationale>
- Implementation layering: <seed path | gap recorded | n/a>
- Work-pack: n/a
- Decisions: <summary>
- Unresolved gaps: <summary>
- Next route: design-bundle-production | repair-w1-input | repair-installed-contract | repair-design-source
```

## Evidence Capability Contract

The canonical W2 source must carry exact upstream/profile bindings, total typed
applications, one fact registry, six view projections, selected outputs and
companions, glossary application, planned witnesses, gaps, layering,
`template_selection`, `dispatch_trace`, Distill contract, transport policy,
`next_route`, and `authority_effect`. The independent coherence verdict and
candidate production receipt—not an authored handoff label—control W2 PASS.
