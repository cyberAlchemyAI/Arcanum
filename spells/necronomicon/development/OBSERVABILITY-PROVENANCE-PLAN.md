# Observability Provenance Plan

## Purpose

Plan the work needed to support the general observability rule:

```text
observed capability != subject artifact
```

This plan covers the shared observability envelope, invoke call behavior, and the Necronomicon plan output that should consume the new provenance fields.

## Target Outcome

Any sigil or spell can report both:

- the capability that ran, and
- the subject artifact or lifecycle that the run produced, reviewed, maintained, or transformed.

This prevents reflection from assigning every gap to the observed capability when the real follow-up belongs to the subject artifact.

## Phase 0 - Baseline And Compatibility

**Goal:** preserve current telemetry while introducing the provenance concept safely.

**Work:**

- Treat existing envelopes without subject metadata as valid.
- Define `subject` and `gap_ownership` as optional fields first.
- Preserve legacy top-level `sigil` and current `capability` fields.
- Document that missing `subject` means "subject unknown or same as observed capability."

**Acceptance Evidence:**

- Existing invocation envelopes still pass validation.
- Existing ledgers do not need migration before new events can be appended.
- Reflection continues to work on old rows.

## Phase 1 - Shared Observability Envelope

**Goal:** add target artifact provenance to the general envelope contract.

**Files:**

- `framework/observability/templates/invocation-envelope.json`
- `framework/observability/SIGIL-OBSERVABILITY-HOOK.md`
- `framework/observability/REPOSITORY-PACKAGE.md`

**Envelope Additions:**

```json
{
  "capability": {
    "id": "invoke",
    "kind": "spell",
    "tier": "spell",
    "mode": "define"
  },
  "subject": {
    "id": "necronomicon",
    "kind": "spell",
    "lifecycle": "development",
    "artifact_paths": [
      "spells/necronomicon/development/DEFINE.md"
    ],
    "owner": "necronomicon development cycle"
  },
  "gap_ownership": {
    "capability_gaps": [],
    "subject_gaps": [
      {
        "severity": "medium",
        "summary": "State schemas are not finalized.",
        "owner": "necronomicon development cycle"
      }
    ]
  }
}
```

**Rules:**

- `capability` answers "what ran?"
- `subject` answers "what was acted on?"
- `gap_ownership.capability_gaps` are defects or improvements for the observed capability.
- `gap_ownership.subject_gaps` are follow-ups for the authored/reviewed/maintained subject.
- `gap_ownership` is the canonical routing split for unresolved gaps.
- `observer.workflow_gaps` remains normalized reflection evidence and may reference `ownership: capability | subject` when known, but reflection must not double count the same gap just because it appears in both places.

**Acceptance Evidence:**

- Template includes `subject` and `gap_ownership`.
- Hook docs explain observed capability vs subject artifact split.
- Repository package docs describe how subject-aware events are stored and reflected.

## Phase 2 - Observer Script Support

**Goal:** make the local observability scripts preserve and summarize provenance fields.

**Files:**

- `framework/observability/scripts/observe-invocation.sh`
- `framework/observability/scripts/reflect-invocation-signals.sh`
- optional fixtures or pilot script under `framework/observability/scripts/`

**Work:**

- Allow optional `subject` object in envelope validation.
- Allow optional `gap_ownership` object in envelope validation.
- Preserve both fields in central ledger events, rebuildable `by-capability` indexes, and rebuildable `by-sigil` indexes.
- Preserve subject-aware counters or summaries in `reflection-state.json` when the state file exists.
- Update reflection analysis to count:
  - capability gaps,
  - subject gaps,
  - subject IDs,
  - subject lifecycles.
- Keep hook operation ledgers unchanged.

**Acceptance Evidence:**

- Old envelope without `subject` records successfully.
- New envelope with `subject` records successfully.
- Central ledger, `by-capability`, and `by-sigil` rows retain enough subject metadata for lookup.
- Reflection state includes subject-aware counters or explicitly records that subject state is not tracked yet.
- Reflection report shows subject metadata when present.
- No hook-operation rows are mistaken for capability telemetry.

## Phase 3 - Invoke Adoption

**Goal:** make `invoke` emit target artifact provenance for every lifecycle authoring run.

**Files:**

- `spells/invoke/README.md`
- `spells/invoke/define.md`
- `spells/invoke/design.md`
- `spells/invoke/plan.md`
- relevant invoke fixtures under `spells/invoke/development/fixtures/`

**Work:**

- Keep the Target Artifact Provenance rule in the root invoke contract.
- Add mode-level requirements:
  - define outputs name target artifact and lifecycle owner,
  - design outputs preserve subject from define and add design artifact paths,
  - plan outputs preserve subject from design and add plan/work-pack paths.
- Update invoke output contract to split unresolved gaps:
  - invoke gaps,
  - subject artifact gaps.
- Update `spells/invoke/plan.md` mode output contract to include `Target artifact` and `Unresolved gaps: <invoke gaps; subject artifact gaps>` so plan-mode output matches the root invoke provenance contract.
- Update example fixtures to include subject metadata.

**Acceptance Evidence:**

- Invoke define/design/plan examples include target artifact fields.
- Invoke transport reports include subject artifact and gap ownership.
- Invoke plan-mode output names the target artifact and separates invoke gaps from subject artifact gaps.
- Invoke reflection no longer forces subject gaps to look like invoke defects.

## Phase 3B - Adapter Rule Seed

**Goal:** seed the generated adapter rule without requiring every command to adopt subject metadata before the Necronomicon pilot.

### Command Adapter Rule

Every generated command adapter should include a small provenance closeout rule:

```text
If this command acted on another artifact, record subject.id, subject.kind,
subject.lifecycle or owner, subject.artifact_paths, and split unresolved gaps
into capability_gaps and subject_gaps.
```

This should be injected by runtime installation and bootstrap after the shared observability envelope supports the fields.

### Acceptance Evidence

- Newly generated command adapters mention subject provenance in observed closeout.
- Existing command adapters are not bulk-mutated until at least one Necronomicon pilot event proves the shared envelope and scripts work.

## Phase 4 - Necronomicon Plan Output

**Goal:** run or prepare `invoke plan` for Necronomicon using the new provenance model.

**Input Artifacts:**

- `spells/necronomicon/development/DEFINE.md`
- `spells/necronomicon/development/DESIGN.md`
- `spells/necronomicon/development/GLOSSARY.md`
- `spells/necronomicon/development/INVOKE-DEFINE-DESIGN-REFLECTION.md`
- this plan

**Plan Outputs:**

- `spells/necronomicon/development/IMPLEMENTATION-PLAN.md`
- `spells/necronomicon/development/IMPLEMENTATION-LAYERING.md` update or companion
- `spells/necronomicon/development/WORK-PACK.md`
- `spells/necronomicon/development/INVOKE-PLAN-TRANSPORT.md`

**Necronomicon-Specific Plan Scope:**

- state schema drafts,
- classifier fixture matrix,
- side-note lifecycle fixtures,
- unblocker lifecycle fixtures,
- checkpoint format,
- route decision format,
- validation checks,
- smallest implementation slices for the Inventory And Ontology Substrate Loop MVP.

**Required Provenance In Plan Transport:**

```json
{
  "capability": {
    "id": "invoke",
    "kind": "spell",
    "mode": "plan"
  },
  "subject": {
    "id": "necronomicon",
    "kind": "spell",
    "lifecycle": "development",
    "artifact_paths": [
      "spells/necronomicon/development/IMPLEMENTATION-PLAN.md",
      "spells/necronomicon/development/IMPLEMENTATION-LAYERING.md",
      "spells/necronomicon/development/WORK-PACK.md",
      "spells/necronomicon/development/INVOKE-PLAN-TRANSPORT.md"
    ]
  },
  "gap_ownership": {
    "capability_gaps": [],
    "subject_gaps": []
  }
}
```

**Acceptance Evidence:**

- Plan output clearly states observed capability is `invoke`.
- Plan output clearly states subject lifecycle is Necronomicon development.
- Plan transport includes all Necronomicon-owned plan output paths: implementation plan, implementation layering, work-pack, and plan transport report.
- Subject gaps are assigned to Necronomicon plan/implementation work.
- Invoke gaps, if any, are assigned to invoke development.

## Phase 5 - Necronomicon Runtime Consumption

**Goal:** let Necronomicon use subject-aware telemetry during resume, checkpoint, maintenance, and reflection.

**Work:**

- During resume, summarize telemetry where subject is `necronomicon`.
- During maintain, distinguish:
  - route/capability problems,
  - Necronomicon subject gaps,
  - downstream capability gaps.
- During checkpoint, preserve subject-aware gap ownership.
- During reflection, avoid treating all routed-command gaps as Necronomicon defects.

**Acceptance Evidence:**

- A Necronomicon checkpoint can say "invoke produced this artifact, but Necronomicon owns these schema gaps."
- A maintenance report can say "observed capability gap belongs to invoke" separately from "subject gap belongs to Necronomicon."

## Phase 5B - Other Command Adoption

**Goal:** apply the same provenance split to every command that can act on a subject artifact different from itself.

Not every command needs rich subject metadata. Commands that only validate their own setup or answer about their own state can omit `subject`. Commands that author, critique, maintain, install, observe, inventory, or govern another thing should record it.

### High-Risk Boundary Commands

| Command/Capability | Boundary Issue | Required Subject |
| --- | --- | --- |
| `interrogation` | Critiques another plan, design, or development pack. | Reviewed artifact or pack. |
| `invoke` | Authors define/design/plan artifacts for another module, spell, sigil, or feature. | Authored target artifact. |
| `spellcraft` | Creates or revises a spell, but spellcraft is not the target spell. | Target spell. |
| `sigil-development` | Creates, revises, observes, or reflects on a sigil. | Target sigil. |
| `sigil-maintenance-loop` | Aggregates telemetry and proposes changes for selected sigils/spells. | Maintained capability or capability set. |
| `workflow-reflect` | Reflects on accumulated telemetry for a capability. | Reflected capability, plus optional subject artifact when present. |
| `signal-observer` | Observes a capability run and may describe gaps in the run output. | Observed run subject when known. |
| `observed-invocation-loop` | Wraps and observes arbitrary capabilities. | Wrapped capability and subject artifact. |
| `inventory` | Ingests or queries sources but does not own source truth. | Source set or inventory entry being acted on. |
| `discovery-to-inventory` | Converts discovery into inventory/glossary entries. | Discovered project/feature and produced entries. |
| `ontology-harness` | Maps and validates ontology candidates for another domain/system. | Ontology branch, premise set, bridge, or target domain/system. |
| `ontology-vault` | Promotes/demotes confidence, premises, conventions, and bridge claims. | Governed claim, premise, branch, or bridge edge. |
| `architecture-pattern-inventory` | Builds a reusable architecture package from a repository. | Target repository/package. |
| `definitions-governance` | Maintains canonical definitions and drift checks. | Governed term set or definition pack. |
| `skill-transcriptor` | Converts a skill/prompt/workflow into an Arcanum sigil package. | Source skill/workflow and target sigil. |
| `skill-decomposer` | Extracts a reusable sigil from a larger workflow. | Source workflow and extracted sigil candidate. |
| `residuality-spec` | Hardens a target spec through stressor/residue analysis. | Target spec. |
| `implementation-readiness` | Reviews whether a feature/work-pack is ready for execution. | Target plan/work-pack/feature. |
| `task-session` | Executes a bounded task against code/docs. | Target task and affected artifact paths. |
| `experiment-harness` | Runs experiments over a target sigil/spell/template. | Experiment target artifact. |
| `invoke-example-runner` | Runs invoke validation prompts and saves outputs. | Invoke template/example being validated. |

### Lower-Risk Or Usually Same-Subject Commands

| Command/Capability | Default |
| --- | --- |
| `observability-setup` | Subject is usually the repository observability package. |
| `sigil-runtime-installer` | Subject is the installed capability command surface. |
| `arcanum-bootstrap` | Subject is the target repository runtime installation. |
| `context-builder` | Subject is the context pack target task. |
| `feature-glossary` | Subject is the feature/workflow glossary. |
| `scope-interview` | Subject is the interviewed project/feature scope. |
| `decision-gate` | Subject is the decision record or blocked artifact. |
| `structured-interview-kits` | Subject is the active interview target. |
| `implementation-layering` | Subject is the target feature/capability implementation model. |

### Acceptance Evidence

- High-risk commands have at least one fixture or example with `subject`.
- Lower-risk commands can omit subject only when observed capability and subject are the same or unknown.

## Phase 6 - Migration And Backfill

**Goal:** make existing telemetry readable under the new model without risky rewrites.

**Work:**

- Do not rewrite historical ledgers by default.
- Add optional interpretation rule:
  - if `subject` missing and output paths point under a known artifact, infer subject only in reports,
  - mark inferred subject as `inferred`, not canonical.
- Optionally create a one-time backfill report for recent Necronomicon invoke runs.

**Acceptance Evidence:**

- Existing reflections still work.
- New reports can mention inferred subject provenance without changing old rows.

## Phase 7 - Validation Matrix

**Goal:** prove the model across more than invoke.

**Fixture Cases:**

| Observed Capability | Subject Artifact | Expected Gap Ownership |
| --- | --- | --- |
| `invoke` | `necronomicon` define/design/plan | Subject schema gaps belong to Necronomicon; output contract gaps belong to invoke. |
| `interrogation` | target spell design | Critique findings belong to target spell; interrogation gaps belong to interrogation. |
| `inventory` | repository knowledge entry | Source coverage gaps belong to inventory operation; factual authority remains with source/project. |
| `ontology-vault` | premise/confidence claim | Promotion gaps belong to ontology governance; domain contradictions belong to subject domain. |
| `spellcraft` | newly authored spell | Authoring gaps belong to spellcraft only when templates/process fail; content gaps belong to new spell. |

**Acceptance Evidence:**

- Fixture envelopes validate.
- Reflection report splits observed capability and subject artifact.
- Maintenance recommendations route to the correct owner.

## Recommended Sequence

1. Implement Phase 1 docs and template changes.
2. Implement Phase 2 script preservation.
3. Update invoke contracts and fixtures in Phase 3.
4. Seed the generated command-adapter closeout rule in Phase 3B.
5. Run `invoke plan` for Necronomicon in Phase 4.
6. Add Necronomicon runtime consumption in Phase 5.
7. Broaden command adoption after the Necronomicon pilot in Phase 5B.
8. Backfill or infer old telemetry only after new events work.
9. Add cross-capability validation fixtures.

## Current Decision

The next practical step is Phase 1: update the shared observability envelope docs and template so `subject` and `gap_ownership` are first-class optional fields.
