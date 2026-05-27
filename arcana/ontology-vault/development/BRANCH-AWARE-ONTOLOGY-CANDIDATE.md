# Branch-Aware Ontology Candidate

Status: exploratory, non-canonical
Date: 2026-05-25
Lifecycle owner: Ontology Vault / Sigil Development
Source handoff: `arcana/inventory/development/ONTOLOGY-BRANCH-MODEL-HANDOFF.md`

## Purpose

This document drafts a candidate general branch-aware ontology model for systems such as Arcanum, CyberAlchemy, DomainSpec, and future systems.

It is not a governed Ontology Vault convention. It is a model candidate intended to preserve the branch-context discriminator, clarify unresolved ontology choices, and provide a stronger target for later decision gates, convention updates, templates, or validation fixtures.

## Non-Goals

- Do not mutate Inventory.
- Do not mutate structured-action-schema.
- Do not promote this model into canonical ontology truth.
- Do not freeze role catalogs, edge catalogs, or branch templates.
- Do not make Arcanum-specific labels universal.
- Do not treat CyberAlchemy discovery-mode architecture as governing authority.

## Source Interpretation

Observed source claims:

- Inventory handoff frames the ontology problem as separate from Inventory refinement.
- The smallest current unit is the `branch-context discriminator`.
- Operational ontology must not become "all action or agent things."
- A system's tools belong to `system` when they realize that system's proposition.
- Operational ontology belongs to situated use, customization, execution, learning, and self-application contexts.
- Inventory prepares source-backed candidates, but Ontology Vault owns governed meaning, confidence, contradiction handling, relation promotion, and branch boundaries.

Candidate synthesis:

- The general ontology model should keep four branch discriminator values: `proposition`, `system`, `operational`, and `bridge`.
- `business` remains a common local alias for `proposition`, especially in existing Ontology Vault material.
- `operational` should be usable as a top-level discriminator value, but only when it is bound to an explicit operating context.
- Role catalogs should be governed in layers: small global core, per-system profile, per-application overlay.

## Branch-Context Discriminator

The discriminator classifies one claim, artifact, concept, relation, action, lesson, or evidence object in one modeling context.

Recommended metadata shape:

```yaml
branch_context:
  primary: proposition | system | operational | bridge
  local_alias: business | system | operational | bridge | null
  role_hint: string
  system_subject: string
  operating_context: string | null
  bridge_scope: string | null
  rationale: string
  status: hypothesis | candidate | governed
```

Decision rule:

| Branch | Classify here when the candidate answers |
| --- | --- |
| `proposition` | What meaning, promise, method, type, policy, value, problem frame, or domain claim does the system exist to satisfy? |
| `system` | What component, capability, schema, command, template, runtime, test, or mechanism realizes that proposition for the system subject? |
| `operational` | What situated application, execution, customization, run behavior, lesson, route, workflow, or self-application context is being observed? |
| `bridge` | What alignment, realization, validation, trace, constraint, contradiction, or drift connects two or more branches? |

The discriminator is context-sensitive. The same artifact can receive different classifications in different claims:

- `Spellcraft` as an Arcanum capability: `system`.
- a Spellcraft route used to customize CyberAlchemy: `operational`.
- a drift between Spellcraft behavior and Arcanum's stated method promise: `bridge`.
- the definition of what Spellcraft is meant to accomplish: `proposition` for Spellcraft itself or `system` for Arcanum, depending on modeling scope.

## Candidate Branches

### Proposition Branch

Purpose:

Govern meaning, intent, promise, problem framing, method, policy, value, and domain rules.

Common local aliases:

- `business`
- `domain`
- `meaning`
- `intent`
- `philosophy`, when a system explicitly models philosophy as its proposition layer

Starter roles:

| Role | Meaning |
| --- | --- |
| `definition` | A governed or candidate meaning boundary. |
| `concept` | A reusable idea or abstraction used by the system. |
| `type` | A class of thing the system recognizes. |
| `method` | A way of reasoning, deciding, or transforming. |
| `problem-frame` | The problem shape the system claims to address. |
| `policy` | A rule of interpretation or allowed behavior. |
| `premise` | A falsifiable or reviewable working claim. |
| `outcome` | A desired result or success condition. |
| `value-measure` | A criterion for judging whether the proposition is being served. |

Example pressure tests:

- Arcanum's glossary, method types, and problem-solving proposition.
- CyberAlchemy's symmetry pursuit, residue reduction, and candidate-before-canon principle.
- DomainSpec's domain modeling and drift-convergence claims.

### System Branch

Purpose:

Govern the machinery that realizes the proposition for a system subject.

Starter roles:

| Role | Meaning |
| --- | --- |
| `component` | A coherent part of the system. |
| `capability` | A reusable function or behavior exposed by the system. |
| `tool` | A callable or usable mechanism. |
| `sigil` | A governed reusable reasoning capability in Arcanum terms. |
| `spell` | A composed capability workflow in Arcanum terms. |
| `schema` | Structured shape for records, entries, actions, or evidence. |
| `template` | Reusable artifact shape. |
| `command-surface` | User or agent invocation interface. |
| `validation-surface` | Fixture, test, lint, review, or harness. |
| `telemetry-surface` | Signal or observability structure. |
| `runtime-adapter` | Integration that executes or routes system behavior. |

Example pressure tests:

- Arcanum tools such as Invoke, Inventory, Ontology Vault, Spellcraft, Sigil Development, observability, and Task Session.
- CyberAlchemy harness, memory plane, route ledger, and execution plane when modeled as system components.
- DomainSpec services, pipeline stages, schemas, tests, and orchestration components.

### Operational Branch

Purpose:

Govern situated use of a system in a concrete context: application, customization, execution, learning, route behavior, user workflow, maintenance, and self-application.

Candidate decision:

`operational` is a top-level discriminator value with a required context binding. It should not be a free-floating global branch. An operational claim is invalid or incomplete unless it names the system subject and the operating context.

Required fields:

```yaml
system_subject: string
operating_context: string
context_owner: system | repository | project | user | lifecycle | unknown
scope_of_validity: string
expiry_condition: string
```

Starter roles:

| Role | Meaning |
| --- | --- |
| `application-context` | A concrete domain or repo where the system is applied. |
| `execution-context` | A task/run setting with relevant constraints. |
| `route-policy` | A rule for selecting routes or capabilities in context. |
| `invocation-pattern` | A repeated sequence or mode of use. |
| `context-solution` | A reusable context-to-route or context-to-payload shortcut. |
| `operational-lesson` | Evidence-backed lesson from situated use. |
| `failure-mode` | Repeated operational risk or breakdown. |
| `maintenance-proposal` | Candidate change derived from operational evidence. |
| `evaluation-signal` | Telemetry or review evidence used to judge operation. |
| `customization` | Context-specific adaptation of a system capability. |
| `self-build-context` | A context where a system is used to improve itself. |

Example pressure tests:

- Arcanum applied to CyberAlchemy.
- Arcanum applied to DomainSpec.
- Arcanum used to build Arcanum.
- CyberAlchemy using Arcanum's routes to improve its own agentic system.
- A repeated route miss while applying Ontology Vault to a specific repository.

### Bridge Branch

Purpose:

Govern cross-branch relations, alignment claims, evidence gaps, validation, constraints, contradictions, and drift.

Bridge claims are not mere links. A bridge claim asserts or investigates a relationship between branch-specific claims and must preserve the source context on each side.

Starter roles:

| Role | Meaning |
| --- | --- |
| `traceability-link` | A sourced relation between claims or artifacts. |
| `realization-map` | How a proposition is realized by system artifacts. |
| `operationalization-map` | How a proposition or system capability is applied in a context. |
| `drift-finding` | Evidence that behavior diverges from intent or contract. |
| `test-coverage-link` | Test evidence for a branch claim. |
| `observability-link` | Signal evidence for behavior or outcome. |
| `constraint-mapping` | How one branch limits another. |
| `evidence-gap` | Missing evidence required for alignment. |
| `contradiction` | Conflict between branch claims or evidence. |

## Role-Catalog Governance

Candidate rule:

Role catalogs should be layered rather than globally closed.

| Layer | Owner | Contents | Promotion boundary |
| --- | --- | --- | --- |
| Global core | Ontology Vault convention | Branch discriminator values, minimal role expectations, confidence split, bridge evidence rules. | Requires ontology convention update and decision gate for breaking changes. |
| System profile | System lifecycle owner | System-specific aliases, branch role catalogs, local branch templates, allowed local edge hints. | Requires system owner review and evidence from the system's sources. |
| Application overlay | Repository/project/context owner | Operational roles, context solution types, local route patterns, custom constraints. | Candidate until repeated evidence and scope rules support promotion. |

Governance constraints:

- A local role can specialize a global role, but should not silently redefine it.
- A local alias can improve reader fit, but should preserve the global discriminator mapping.
- A role catalog is not promoted merely because a template uses it.
- Operational roles require scope of validity and expiry condition.
- Bridge roles require evidence from all sides they connect or must be marked as evidence gaps.

## Context Rules

Every branch-aware ontology claim should answer these context questions:

| Question | Required for |
| --- | --- |
| What is the system subject? | All branches. |
| What is the claim about: meaning, machinery, situated use, or relation? | All branches. |
| What source evidence supports the claim? | Candidate and governed claims. |
| What local alias or role catalog is being used? | Local/system/application catalogs. |
| What is the scope of validity? | Operational, bridge, confidence-bearing claims. |
| What invalidates or expires the claim? | Operational and promoted claims. |
| Does the claim affect behavior, architecture, routing, or authority? | Commitment and promotion gates. |

Context inheritance:

- Proposition claims may inherit system subject from the ontology package being modeled.
- System claims may inherit system subject, but not operational context.
- Operational claims must state or inherit an explicit operating context.
- Bridge claims must identify each side of the relation and the branch role of each side.

Ambiguity rule:

If a claim could be classified in multiple branches, choose the branch of the claim being made, not the artifact being named. Record secondary branches only as context, not as the primary owner.

## Self-Application Handling

Self-application occurs when a system is used to inspect, improve, operate, or rebuild itself.

Candidate representation:

```yaml
branch_context:
  primary: operational
  system_subject: Arcanum
  operating_context: Arcanum-self-build
  role_hint: self-build-context
  rationale: Arcanum is being used in a situated context to modify or improve Arcanum.
```

Rules:

1. The system subject and operating context must be distinct fields even when they name the same system.
2. Self-application records are operational candidates until reviewed.
3. Self-application evidence does not automatically promote proposition or system claims.
4. A self-application claim may propose a system change, but Sigil Development, Spellcraft, or the relevant lifecycle owner must approve the actual mutation.
5. Self-application cannot cite itself as authority. It must cite run evidence, source artifacts, tests, telemetry, review, or decision records.
6. Recursive bridge claims must preserve direction:
   - proposition claim -> system behavior,
   - system behavior -> operational use,
   - operational lesson -> proposed system/proposition update.

Failure mode to avoid:

```text
Arcanum used Ontology Vault to decide Ontology Vault is canonical because Ontology Vault said so.
```

Required correction:

```text
Arcanum used Ontology Vault in the Arcanum-self-build operating context to produce a candidate. Promotion requires source evidence, contradiction review, and an explicit governance gate.
```

## Bridge Rules

Bridge edge types should be ontology-owned only when they assert meaning, confidence, promotion, contradiction, or governed relation semantics.

Starter bridge edge catalog:

| Edge | Meaning | Evidence requirement |
| --- | --- | --- |
| `realized_by` | A proposition claim is implemented or served by a system artifact. | Proposition evidence plus system evidence. |
| `depends_on` | A claim or behavior requires another capability or condition. | Source for dependency and target existence. |
| `constrained_by` | One branch limits what another branch can promise or do. | Constraint source plus affected claim. |
| `observed_by` | A claim or behavior is measured by telemetry, logs, metrics, or review signals. | Observable signal definition plus collected evidence or expected collection point. |
| `tested_by` | A claim or behavior is verified by a test, fixture, review, benchmark, or validation regime. | Test identity plus coverage rationale. |
| `drifts_from` | Observed behavior diverges from proposition, contract, or expected operation. | Expected claim plus observed behavior. |
| `traced_to` | A claim links back to a source, premise, decision, or artifact. | Stable reference or selector. |
| `operationalizes` | A proposition or system capability is adapted into a situated operating context. | Source capability plus context evidence. |
| `contradicted_by` | Evidence challenges a claim. | Claim and counterevidence must both be preserved. |
| `promotes_to` | A candidate moves to a higher authority state. | Promotion gate record. |

Action-schema boundary:

- Action schemas may record branch metadata and relation hints.
- Ontology owns the meaning of promoted branch relations.
- Schema relation fields should not silently become ontology edge authority.
- A relation can begin as an action-schema observation and later become an ontology edge only through Ontology Vault review.

Bridge validation rules:

1. Alignment claims require evidence from every connected branch.
2. Drift claims must preserve both the expected claim and observed behavior.
3. Test or telemetry evidence can support alignment but does not define meaning.
4. A bridge can connect proposition-system, system-operational, proposition-operational, or all three.
5. A bridge relation with missing evidence should be recorded as `evidence-gap`, not promoted as alignment.

## Confidence And Promotion Boundaries

Use separate confidence dimensions:

| Dimension | Question |
| --- | --- |
| Evidence confidence | How strong is the source, observation, or validation support? |
| Commitment confidence | How much should the system rely on the claim for behavior, design, routing, or governance? |
| Bridge alignment confidence | How well does the relation between branches hold? |
| Scope confidence | How clearly is the claim bounded to a system, context, repo, user, task type, or time period? |

Candidate status ladder:

| Status | Meaning | Authority |
| --- | --- | --- |
| `hypothesis` | Plausible but thinly supported. | May guide exploration only. |
| `candidate` | Source-backed enough to discuss and test. | May inform design, not govern behavior. |
| `reviewed` | Checked against evidence, contradictions, and scope. | May guide local work with caveats. |
| `promoted` | Accepted by the relevant governance route. | Can govern within its scope. |
| `deprecated` | Superseded or no longer recommended. | Retained for history. |
| `contradicted` | Challenged by unresolved counterevidence. | Must not be used as authority. |

Promotion gates:

- Proposition promotion requires meaning authority, contradiction review, and owner approval.
- System promotion requires artifact evidence, tests or validation where applicable, and lifecycle owner review.
- Operational promotion requires repeated or high-quality situated evidence, scope of validity, expiry condition, and privacy/safety review when user workflow is involved.
- Bridge promotion requires evidence from each connected branch and explicit relation semantics.
- Self-application promotion requires an additional circular-authority check.

Promotion blockers:

- claim outranks its sources,
- branch owner is unclear,
- operational context is missing,
- bridge evidence is one-sided,
- contradiction is unresolved,
- local alias redefines global branch semantics,
- action-schema or Inventory record is treated as ontology authority.

## Inventory Handoff Boundaries

Inventory remains responsible for:

- source capture,
- source summaries,
- extracted claims,
- selectors,
- tags,
- indexes,
- lookup surfaces,
- candidate cards,
- handoffs to Ontology Vault, Definitions Governance, or other lifecycle owners.

Ontology Vault remains responsible for:

- branch model,
- governed meaning,
- role catalog governance,
- confidence and commitment rules,
- contradiction handling,
- branch boundary decisions,
- formal relation claims,
- promotion or demotion recommendations,
- convention changes.

Handoff shape from Inventory to Ontology:

```yaml
handoff:
  source_inventory_entry: string
  raw_sources:
    - string
  extracted_claims:
    - claim: string
      selector: string
      branch_hint: proposition | system | operational | bridge | unknown
      role_hint: string
      confidence_hint: low | medium | high | unknown
  contradictions:
    - string
  unresolved_questions:
    - string
  requested_ontology_action: map | premise-review | convention-update | validate | promote-confidence
  non_authority_notice: Inventory supplied evidence and candidates, not governed ontology truth.
```

Boundary rule:

Inventory may propose `branch_hint`. Ontology Vault decides `branch_context`.

## Cross-System Comparison Rules

The model should support comparison without erasing local truth.

Reusable comparison fields:

```yaml
system_subject: string
branch_context.primary: proposition | system | operational | bridge
role_family: definition | component | context | relation | evidence-gap | other
local_role: string
scope_of_validity: string
evidence_confidence: low | medium | high
commitment_confidence: low | medium | high
promotion_status: hypothesis | candidate | reviewed | promoted | deprecated | contradicted
```

Rules:

- Compare systems at the branch and role-family level first.
- Use local roles as examples, not universal categories.
- Preserve system-specific aliases.
- Treat operational comparisons as context comparisons, not proof of universal behavior.
- Promote cross-system patterns only when evidence survives at least two distinct system/context cases and a governance route accepts the generalization.

## Candidate Entry Skeleton

```markdown
---
id: <system>.<stable-id>
type: <local-entry-type>
branchPrimary: proposition | system | operational | bridge
branchAlias: business | system | operational | bridge | null
roleFamily: <global-role-family>
localRole: <system-specific-role>
systemSubject: <system-name>
operatingContext: <context-or-null>
status: hypothesis | candidate | reviewed | promoted | deprecated | contradicted
evidenceConfidence: low | medium | high
commitmentConfidence: low | medium | high
bridgeAlignmentConfidence: low | medium | high | not-applicable
updatedAt: YYYY-MM-DD
---

# <Entry Title>

## Claim

## Branch Context

## Scope

## Evidence

## Confidence

## Edges

## Contradictions

## Promotion Boundary

## Maintenance
```

## Example Classifications

| Candidate | System subject | Operating context | Primary branch | Role hint | Rationale |
| --- | --- | --- | --- | --- | --- |
| Arcanum glossary | Arcanum | null | `proposition` | `definition` | Defines meaning Arcanum uses to reason. |
| Invoke spell | Arcanum | null | `system` | `spell` | Realizes Arcanum's lifecycle authoring proposition. |
| Inventory evidence-card model | Arcanum | null | `system` | `schema` | A mechanism for reusable evidence capture. |
| Inventory handoff to Ontology Vault | Arcanum | ontology development session | `bridge` | `traceability-link` | Connects evidence capture to ontology governance. |
| Arcanum applied to CyberAlchemy architecture | Arcanum | CyberAlchemy application | `operational` | `application-context` | Situated use of Arcanum for a specific system. |
| CyberAlchemy route ledger | CyberAlchemy | null | `system` | `telemetry-surface` | Part of CyberAlchemy's agentic system machinery. |
| Repeated route miss during Arcanum self-build | Arcanum | Arcanum-self-build | `operational` | `failure-mode` | Situated lesson from applying Arcanum to itself. |
| Drift between method promise and sigil behavior | Arcanum | relevant run context | `bridge` | `drift-finding` | Relates proposition expectation to system or operational behavior. |
| DomainSpec pipeline test for a domain rule | DomainSpec | null | `bridge` | `test-coverage-link` | Connects a domain/proposition rule to system validation evidence. |

## Unresolved Decisions

| Decision | Current candidate stance | Why unresolved |
| --- | --- | --- |
| Is `operational` top-level, contextual projection, or both? | Both: top-level discriminator value with mandatory context binding. | Needs validation against real Arcanum, CyberAlchemy, and DomainSpec entries. |
| Should branch role catalogs be global, per-system, or per-application? | Layered catalogs: global core, system profile, application overlay. | Governance and migration cost need decision-gate review. |
| Should `business` remain the global branch label? | Prefer `proposition` globally; preserve `business` as a common alias. | Existing Ontology Vault materials use `business`; renaming has migration cost. |
| Which edge types are ontology-owned versus action-schema-owned? | Ontology owns promoted relation semantics; schemas may record hints. | Needs structured-action-schema coordination before implementation. |
| What counts as enough operational evidence? | Repeated evidence or high-quality review, plus scope and expiry. | Thresholds likely differ by system and risk level. |
| How should user workflow models be handled? | Operational only with explicit privacy and promotion boundaries. | Privacy policy is not defined here. |
| Can bridge alignment confidence be a separate field? | Yes, candidate field. | Needs examples showing it adds value beyond evidence confidence. |
| Should research/methodology be a branch? | Treat as projection or system-specific profile for now. | CyberAlchemy suggests it may matter, but core model should stay small. |
| Where should branch templates live? | Likely `arcana/ontology-vault/templates/` after approval. | This document is not an approved template mutation. |

## Readiness Criteria For Promotion

This candidate should not become a governed ontology convention until:

1. At least one Arcanum example set is classified using the model.
2. At least one CyberAlchemy example set is classified using the model.
3. At least one DomainSpec example set is classified using the model.
4. A bridge validation pass finds whether the bridge rules are usable.
5. A decision gate resolves the `proposition` versus `business` global label question.
6. A decision gate resolves operational evidence thresholds.
7. Structured-action-schema owners confirm whether branch metadata remains optional and non-authoritative.
8. Inventory handoff shape is tested without making Inventory ontology authority.
9. Self-application examples pass the circular-authority check.

## Proposed Next Routes

| Route | Purpose |
| --- | --- |
| `ontology-vault validate` | Classify a small mixed set of Arcanum/CyberAlchemy/DomainSpec examples and report gaps. |
| `decision-gate` | Decide global branch label and operational branch governance. |
| `ontology-vault convention-update` | If approved, propose template and SKILL updates with migration impact. |
| `context-builder` | Build compact evidence packs for the example validation sets. |
| `sigil-development` | Update Ontology Vault only after candidate validation and governance decisions. |

## Invoke Result

- Mode: define
- Lifecycle owner: ontology-vault / sigil-development
- Phase status: flag
- Canonicality: exploratory, non-canonical
- Output: `arcana/ontology-vault/development/BRANCH-AWARE-ONTOLOGY-CANDIDATE.md`
- Durable session: `arcana/ontology-vault/development/DURABLE-SESSION-CONTEXT.md`
- Mutated Inventory: no
- Mutated structured-action-schema: no
- Primary blocker: operational branch governance needs validation and decision-gate review before promotion
