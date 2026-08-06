---
name: ontology-vault
description: "Use when: selecting, mapping, distilling, validating, or evolving a governed ontology with explicit archetype routing, roles, confidence, premises, typed properties, branch-aware edges, and conventions."
argument-hint: "<map|distill-sessions|promote-confidence|premise-review|convention-update|validate> [--ontology-type <id>] [--path <repo-root>] [--source <path>] [--profile <path>] [--runtime inline|agents] [--branch <business|system|bridge>] [--branches business,system] [--bridge business-system] [--output <path>] [--dry-run]"
tier: arcana
domain: ontology-governance
version: 0.2.0
origin: generalized from governed knowledge-vault maintenance patterns
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions, Task
---

# Sigil: Ontology Vault

<objective>
Govern an ontology by first selecting the ontology archetype that matches the
user's intended job, then mapping structure, distilling sessions, reviewing
premises, evaluating typed properties, promoting or demoting confidence,
proposing convention changes, validating relationship rules, and preserving
delegated evidence traceability.
</objective>

<logic-type>
Arcana: long-lived ontology governance, evidence preservation, confidence promotion, convention change control, branch-aware traceability, and cross-document consistency.
</logic-type>

<modes>
- `map`: inspect existing docs and infer current ontology roles, axes, statuses, tags, edge rules, and gaps.
- `distill-sessions`: extract durable claims, decisions, contradictions, open questions, and promotion candidates from session records.
- `promote-confidence`: evaluate whether knowledge can be promoted, must remain in place, or should be demoted.
- `premise-review`: test working premises against evidence, contradictions, usage, and falsification criteria.
- `convention-update`: propose changes to roles, statuses, tags, axes, edge rules, or schema conventions.
- `validate`: check role consistency, source authority, links, evidence coverage, delegated-evidence traceability, and promotion rule violations.
</modes>

<ontology-type-arguments>
Ontology type is the primary routing axis. It describes the job the ontology
must do, not the authority or canonical class of any project artifact.

- `--ontology-type <id>`: explicitly select one reusable ontology archetype
  from [the ontology type catalog](catalogs/ontology-types.json).
- Without the argument, infer one type only when the user's intent clearly
  matches one catalog entry.
- When two or more types remain plausible, ask the user to select from the two
  or three strongest mutually exclusive choices. Each choice must state what
  will be modeled and the consequence of choosing it.
- A project-local type may be supplied as a runtime-profile alias. The profile
  must map it to one catalog type. Keep the local alias in the report; do not
  add it to reusable Arcanum vocabulary by proximity.

The initial catalog contains:

- `knowledge-vault`: roles, confidence, premises, sessions, evidence, and
  convention lifecycle;
- `business-domain`: domain meaning, actors, rules, policies, workflows,
  outcomes, and value;
- `system-runtime`: components, interfaces, events, data, tests, telemetry,
  deployment, and runtime constraints;
- `business-system-bridge`: realization, traceability, coverage, observation,
  constraints, evidence gaps, and drift across the two branches;
- `authority-governance`: authority kinds, source posture, owners, gates,
  reliance, non-collapse, and residue;
- `architecture-property`: architecture element types, typed properties,
  allowed relations, constraint operators, architecture profiles, observation
  projections, and explainable property findings.

Architecture-enforcement intent that asks an ontology to understand or test an
architecture's properties selects `architecture-property`. Do not silently
substitute intent-to-implementation traceability; that is
`business-system-bridge`.
</ontology-type-arguments>

<branch-aware-arguments>
Branch-aware ontology is optional. Use it when the repository has both business/domain material and system/runtime material, or when the user asks for intent-to-implementation traceability.

- `map --branch business`: map domain language, intent, rules, outcomes, premises, policies, and value claims.
- `map --branch system`: map components, services, APIs, events, jobs, data structures, tests, metrics, and runtime constraints.
- `map --branches business,system`: map both branches and classify mixed or ambiguous documents.
- `validate --bridge business-system`: validate cross-branch links, drift, tests, observability, constraints, and evidence gaps.
- `promote-confidence --branch business`: promote or demote business knowledge only when evidence and commitment gates pass.
- `promote-confidence --branch system`: promote or demote system knowledge only when implementation/runtime evidence supports it.
- `convention-update --branch business|system|bridge`: propose convention changes scoped to one branch or to bridge rules.

Ontology type and branch arguments are compatible but not interchangeable:

1. Ontology type selects the model shape and validation questions.
2. `--branch`, `--branches`, and `--bridge` select traversal or reporting scope
   within that model.
3. When no branch argument is explicit, use the catalog entry's derived branch
   defaults. `business-domain` derives `--branch business`; `system-runtime`
   and `architecture-property` derive `--branch system`; and
   `business-system-bridge` derives `--branches business,system --bridge
   business-system`.
4. An explicit compatible branch argument overrides only the derived traversal
   scope. It never changes the selected ontology type.
5. If the explicit branch excludes the selected type's required evidence—for
   example, a bridge type with only one branch—report the conflict and ask for
   one correction rather than silently rerouting.
6. Existing invocations without `--ontology-type` remain valid. Infer a type
   from clear intent and arguments; otherwise use the ambiguity policy before
   scanning broadly.
  </branch-aware-arguments>

<project-runtime-profile-arguments>
Project-local runtime profiles are optional. Use them when a repository has a
local ontology surface that instantiates a reusable ontology model and needs
repeatable map, validate, distill, confidence, drift, or projection runs before
it has a dedicated runtime.

- `--profile <path>`: load a project-local runtime profile that names local
  ontology refs, owner refs, source-spine refs, implementation/runtime refs,
  allowed runtime modes, allowed outputs, blocked outputs, owner gates, residue
  route, and observability route.
- A profile may declare `ontology_type` with one catalog ID and may declare
  `ontology_type_alias` for its project-local name. The alias does not extend
  the reusable catalog.
- `--runtime inline`: default. Run the selected Ontology Vault mode directly
  over the profile sources inside the current agent session.
- `--runtime agents`: use a governed subagent strategy as an execution backend
  only when the profile permits it and the repository has a local strategy
  owner. The subagent strategy must handle trigger checks, tension design,
  explicit human confirmation, registration, closeout, and ledger evidence.

Profile outputs are evidence artifacts, validation reports, confidence action
reports, drift reports, and optional read-model projections. They are not
promotion verdicts, source authority, spec mutations, runtime conformance
verdicts, or canonical source edits unless a separate owner route explicitly
permits that movement.
</project-runtime-profile-arguments>

<applicability>
Use this sigil when a repository has vault-like knowledge governance: sessions, discoveries, premises, constitutions, ontology conventions, confidence rules, edge types, or delegated research artifacts.
</applicability>

<inputs>
Expected inputs, if available:

- explicit ontology type or user intent from which it can be selected,
- repository root,
- vault, ontology, notes, wiki, or docs folders,
- session records,
- discovery or research folders,
- premise, axiom, constitution, or convention documents,
- existing inventory entries,
- project-local runtime profile, when using `--profile`,
- local ontology, owner, source-spine, implementation, test, telemetry, or
  projection references named by that profile,
- prior findings and audits,
- schema or frontmatter conventions,
- user-stated ontology goal.
  </inputs>

<default-output>
If the user does not provide `--output`, prefer:

1. `.arcanum/ontology-vault/<mode>-<date>.md` when `.arcanum/` exists,
2. `docs/ontology/<mode>-<date>.md` when `docs/ontology/` exists,
3. `docs/knowledge/<mode>-<date>.md` when `docs/knowledge/` exists,
4. a markdown report in chat when no safe output location exists.
   </default-output>

<process>
## Step 0 - Select The Ontology Type

1. Load `catalogs/ontology-types.json` and record all viable catalog matches
   before broad source discovery.
2. Resolve selection in this precedence order:
   - explicit `--ontology-type` catalog ID,
   - runtime profile `ontology_type` and optional project-local alias,
   - one high-confidence intent match,
   - user selection from the two or three strongest candidates.
3. Clear intent must not prompt. Record `selection_source` as `explicit`,
   `profile`, or `inferred`, the confidence, and why competing types were
   excluded.
4. Ambiguous intent must not silently pick a generic map. Present two or three
   concise, mutually exclusive choices using the catalog labels and selection
   consequences. After selection, record `selection_source: user` and preserve
   the rejected candidates as routing evidence.
5. When a profile names a project-local alias, require its reusable
   `ontology_type` base. Record the alias but do not register it in the catalog.
6. Resolve derived branch defaults from the selected type, then apply only
   compatible explicit branch arguments.

## Step 1 - Resolve Scope And Local Vocabulary

7. Resolve the target repository, source folders, mode, and output path.
8. Detect local knowledge-governance structures before asking questions.
9. When `--profile` is provided, load the project-local runtime profile before
   broad source discovery and treat its source refs as the execution boundary.
10. Identify local labels for roles, statuses, confidence dimensions, tags, edge types, and sessions.
11. Translate local labels into generic Arcanum concepts:
   - knowledge role,
   - maturity status,
   - evidence confidence,
   - commitment confidence,
   - session record,
   - delegated research,
   - synthesis findings,
   - convention change,
   - business ontology,
   - system ontology,
   - bridge ontology,
   - architecture property ontology.
12. Preserve local label names as aliases only when reporting on the repository. Do not promote local labels into canonical Arcanum vocabulary.

## Step 2 - Map Current Ontology

6. Inventory source folders and representative documents.
7. Record observed roles, axes, statuses, tags, edge types, promotion rules, and source authority rules.
8. Identify gaps, contradictions, stale conventions, and undocumented practices.
9. Estimate the domain-knowledge inflection position:
   - low knowledge: prioritize discovery and session distillation,
   - near inflection: prioritize decision gates and focused ontology experiments,
   - high knowledge: justify promotion gates, convention changes, and heavier ontology investment.

## Step 2A - Map Architecture Properties When Selected

When `ontology_type: architecture-property` is selected:

10. Map architecture element types and their inheritance or composition rules.
11. Map typed property definitions, including value domains, valid subjects,
    observation stages, owner routes, and forbidden inferences.
12. Map allowed relation definitions, endpoint types, relation properties,
    direction, cycle policy, and evidence requirements.
13. Map architecture profiles as explicit constraints over properties and
    relations. Keep portable constraints separate from language- or
    project-specific realizations.
14. Map observation projections from source, AST, compiler, module, runtime,
    test, or telemetry evidence into typed facts. Projections are evidence, not
    architecture authority.
15. Validate generic constraint operators and require findings to retain the
    subject, property or relation, expected value, observed value, originating
    profile, evidence ref, and owner route.
16. Preserve unknown or indeterminate observations as typed unsupported
    evidence. Never infer a passing value from absence or naming similarity.
17. Use bridge edges only when the requested question also concerns alignment
    between domain intent and implementation. Architecture-property selection
    alone does not imply a business-system bridge.

## Step 2B - Map Branch-Aware Ontology When Needed

When branch-aware mapping is requested or clearly useful:

10. Classify documents and claims as `business`, `system`, `bridge`, `mixed`, or `unknown`.
11. Map business ontology claims around intent, meaning, actors, rules, policies, workflows, outcomes, premises, decisions, and value measures.
12. Map system ontology claims around components, services, APIs, events, jobs, data structures, tests, metrics, deployment units, runtime behavior, and technical constraints.
13. Preserve mixed documents when they are useful, but assign branch ownership at the claim or section level.
14. Create bridge edges only when there is evidence on both sides of the branch boundary.
15. Use these starter bridge edge types:

- `realized_by`: business concept or behavior is implemented by a system artifact,
- `depends_on`: business behavior depends on a system capability,
- `constrained_by`: business rule or outcome is limited by a technical constraint,
- `observed_by`: business outcome or behavior is measured by a metric, log, event, or trace,
- `tested_by`: business claim, rule, or outcome is verified by a test,
- `drifts_from`: observed system behavior diverges from business intent,
- `traced_to`: system artifact links back to a business premise, decision, discovery, or rule.

## Step 2C - Validate Branch Bridges

16. Every promoted business behavior with implementation impact should have at least one bridge edge or an explicit evidence gap.
17. Every promoted system artifact claim should identify whether it realizes, observes, tests, constrains, or merely supports a business claim.
18. Drift edges must preserve both the business expectation and the observed system behavior.
19. Bridge claims that assert alignment must cite evidence from both branches.
20. System claims must not silently redefine business meaning; business claims must not pretend implementation exists without bridge evidence.

## Step 2D - Execute A Project-Local Runtime Profile When Provided

When `--profile` is provided:

21. Validate that the profile names at least local ontology refs, local owner
    refs, source or evidence refs, allowed runtime modes, allowed outputs,
    blocked outputs, owner gates, and residue route.
22. Treat profile refs as local aliases to generic concepts; do not add profile
    labels, statuses, or roles to canonical Arcanum vocabulary by default.
23. For `--runtime inline`, run the selected mode over the profile refs and
    record profile coverage, profile gaps, and blocked output attempts.
24. For `--runtime agents`, verify the profile permits an agent backend and
    route through the repository-local governed subagent strategy. Do not spawn
    agents directly from Ontology Vault when the local strategy requires its
    own trigger check, tension gate, human confirmation, registry append, and
    closeout.
25. Treat agent returns, dispatch findings, close rows, and ledger evidence as
    delegated evidence records. They may support synthesis or confidence
    review, but they do not decide authority.
26. Emit only allowed profile outputs. Block or escalate any attempt to emit a
    promotion verdict, source mutation, spec mutation, runtime conformance
    verdict, or generated projection that outranks its owner evidence.

## Step 3 - Distill Sessions And Delegated Evidence

27. Treat sessions as evidence records, not authority.
28. Extract durable claims, decisions, contradictions, open questions, and promoted candidates.
29. Preserve context and goal for each distillation.
30. When delegated research exists, keep raw delegated research separate from synthesis findings.
31. Require synthesis findings to cite delegated research before making load-bearing claims.
32. Surface contradictions between raw evidence outputs instead of resolving them silently.

## Step 4 - Review Premises And Confidence

33. For each premise or working bet, identify evidence, counterevidence, current use, falsification criteria, and confidence state.
34. Separate evidence confidence from commitment confidence.
35. Recommend one action: promote, keep, revise, demote, split, merge, retire, or escalate to decision gate.
36. Block promotion when evidence links are missing, contradictions remain unresolved, or the claim would outrank its sources.
37. For branch-aware promotion, keep business confidence and system confidence separate until bridge evidence supports alignment.
38. For project-local profiles, promotion recommendations must name the local
    owner route and remain non-executing unless that owner route returns an
    approval or PromotionRecord-compatible decision.

## Step 5 - Propose Convention Changes

39. For schema or ontology changes, record current rule, proposed rule, rationale, migration impact, affected files, and rollback path.
40. Ask one blocker-level governance decision at a time.
41. Do not mutate conventions unless the user explicitly approves the change.
42. For branch-aware convention changes, state whether the rule affects business, system, bridge, or cross-branch validation.
43. For project-local profile changes, separate reusable profile convention
    changes from one repository's private profile data.

## Step 6 - Validate And Report

44. Validate ontology type selection, type-specific model shape, links, role consistency, confidence gates, delegated-evidence traceability, source authority rules, branch ownership, bridge edges, drift findings, test links, and observability links.
45. When a project-local profile is used, validate profile completeness, runtime
    mode permission, blocked output attempts, owner-gate coverage, and whether
    agent backend evidence has closeout receipts.
46. Return a concise report with outputs, blockers, promotion decisions, convention changes, runtime profile state, and next action.
    </process>

<branch-role-catalogs>
Use these as starter catalogs, not a universal taxonomy.

Business roles can include: actor, capability, business rule, policy, premise, outcome, workflow, domain event, decision, constraint, value measure.

System roles can include: component, service, module, endpoint, event, schema, table, queue, job, configuration, metric, test, deployment unit.

Bridge roles can include: traceability link, realization map, drift finding, test coverage link, observability link, constraint mapping, evidence gap.
</branch-role-catalogs>

<quality-bar>
A successful execution must:

- select one cataloged ontology type before broad mapping,
- avoid prompting when explicit profile or high-confidence intent determines one type,
- ask for one selection from two or three consequence-bearing choices when intent is ambiguous,
- keep project-local type aliases mapped to a reusable type without making the alias canonical,
- route architecture-property intent to types, typed properties, relations, profiles, observation projections, and explainable findings,
- separate observed evidence, inference, synthesis, and decisions,
- preserve sessions as evidence records rather than authority,
- distinguish evidence confidence from commitment confidence,
- map local labels to generic concepts without making local labels canonical,
- keep delegated research separate from synthesis findings,
- require synthesis claims to cite raw evidence,
- surface contradictions and unresolved governance choices,
- block promotion when source authority or evidence coverage is insufficient,
- keep business confidence, system confidence, and bridge alignment evidence distinct,
- require bridge claims to cite evidence from both branches before asserting alignment,
- preserve drift as a first-class finding rather than smoothing it away,
- identify migration impact before convention changes,
- use the inflection heuristic to justify ontology investment level.
- keep project-local runtime profiles bounded to their owner routes and source
  refs,
- treat governed-agent runtime returns as delegated evidence rather than
  authority,
- block profile outputs that would mutate specs, canonical sources, runtime
  conformance, or promotion state without owner approval.
  </quality-bar>

<anti-patterns>
Avoid:

- treating every ontology request as a generic knowledge-vault map,
- defaulting architecture-property questions to business-system traceability,
- asking the user to select a type after clear intent or an explicit type/profile already resolves it,
- silently choosing among multiple plausible ontology types,
- registering project-local type aliases as reusable Arcanum ontology types,
- copying a local ontology taxonomy into Arcanum as universal vocabulary,
- treating session summaries as settled truth,
- promoting a premise because it is familiar rather than evidenced,
- collapsing evidence confidence and commitment confidence into one score,
- hiding contradictions during synthesis,
- writing convention changes without migration impact,
- using a full ontology workflow when inventory lookup is enough,
- letting synthesis findings cite themselves instead of raw evidence,
- splitting business and system ontology into disconnected worlds,
- allowing system artifacts to silently redefine business intent,
- claiming implementation alignment without bridge evidence,
- treating test coverage or telemetry as business meaning instead of bridge evidence,
- forcing branch-aware ontology on repositories that only need a simple map.
- hardcoding one project-local runtime profile into the reusable sigil contract,
- treating an agent-backed profile run as permission to bypass the local
  governed subagent strategy,
- letting a generated projection or profile report become canonical authority
  by proximity.
  </anti-patterns>

<observability>
When `.arcanum/observability/` exists, emit post-run signals for:

- mode,
- selected ontology type,
- ontology type selection source,
- selection confidence,
- ambiguity candidates,
- whether user selection was required,
- runtime profile path when provided,
- runtime mode,
- agent backend status,
- source folders scanned,
- sessions distilled,
- delegated research records found,
- synthesis findings validated,
- business documents mapped,
- system documents mapped,
- bridge edges created,
- drift findings found,
- traceability gaps found,
- test links found,
- observability links found,
- premises reviewed,
- promotions recommended,
- demotions recommended,
- convention changes proposed,
- contradictions found,
- blockers remaining,
- validation result.
  </observability>

<output-contract>
Return:

```markdown
## Ontology Vault Result

- Mode: map | distill-sessions | promote-confidence | premise-review | convention-update | validate
- Repository: <path>
- Ontology type: <catalog-id>
- Type selection source: explicit | profile | inferred | user
- Type selection confidence: high | medium | low | exact
- Ambiguity candidates: <ids or none>
- User selection required: yes | no
- Project-local type alias: <alias | none>
- Branch: business | system | bridge | mixed | none
- Runtime profile: <path | none>
- Runtime mode: inline | agents | none
- Sources reviewed: <count>
- Business documents mapped: <count>
- System documents mapped: <count>
- Bridge edges checked: <count>
- Drift findings: <count>
- Traceability gaps: <count>
- Sessions distilled: <count>
- Delegated research records: <count>
- Synthesis findings checked: <count>
- Premises reviewed: <count>
- Promotions recommended: <count>
- Demotions recommended: <count>
- Convention changes proposed: <count>
- Contradictions found: <count>
- Blockers: <count>
- Outputs: <paths or dry-run>
- Validation: pass | flag | block | not run
- Next action: <action>
```

</output-contract>
