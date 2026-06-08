---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/ontology-vault/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: ontology-vault
description: "Use when: mapping, distilling, validating, or evolving a governed knowledge vault with roles, confidence, premises, sessions, edge rules, branch-aware ontology, and ontology conventions."
argument-hint: "<map|distill-sessions|promote-confidence|premise-review|convention-update|validate> [--path <repo-root>] [--source <path>] [--branch <business|system|bridge>] [--branches business,system] [--bridge business-system] [--output <path>] [--dry-run]"
tier: arcana
domain: ontology-governance
version: 0.1.0
origin: generalized from governed knowledge-vault maintenance patterns
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Agent
---

# Sigil: Ontology Vault

<objective>
Govern a knowledge vault by mapping ontology structure, distilling sessions, reviewing premises, promoting or demoting confidence, proposing convention changes, validating relationship rules, and preserving delegated evidence traceability.
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

<branch-aware-arguments>
Branch-aware ontology is optional. Use it when the repository has both business/domain material and system/runtime material, or when the user asks for intent-to-implementation traceability.

- `map --branch business`: map domain language, intent, rules, outcomes, premises, policies, and value claims.
- `map --branch system`: map components, services, APIs, events, jobs, data structures, tests, metrics, and runtime constraints.
- `map --branches business,system`: map both branches and classify mixed or ambiguous documents.
- `validate --bridge business-system`: validate cross-branch links, drift, tests, observability, constraints, and evidence gaps.
- `promote-confidence --branch business`: promote or demote business knowledge only when evidence and commitment gates pass.
- `promote-confidence --branch system`: promote or demote system knowledge only when implementation/runtime evidence supports it.
- `convention-update --branch business|system|bridge`: propose convention changes scoped to one branch or to bridge rules.
  </branch-aware-arguments>

<applicability>
Use this sigil when a repository has vault-like knowledge governance: sessions, discoveries, premises, constitutions, ontology conventions, confidence rules, edge types, or delegated research artifacts.
</applicability>

<inputs>
Expected inputs, if available:

- repository root,
- vault, ontology, notes, wiki, or docs folders,
- session records,
- discovery or research folders,
- premise, axiom, constitution, or convention documents,
- existing inventory entries,
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
## Step 1 - Resolve Scope And Local Vocabulary

1. Resolve the target repository, source folders, mode, and output path.
2. Detect local knowledge-governance structures before asking questions.
3. Identify local labels for roles, statuses, confidence dimensions, tags, edge types, and sessions.
4. Translate local labels into generic Arcanum concepts:
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
   - bridge ontology.
5. Preserve local label names as aliases only when reporting on the repository. Do not promote local labels into canonical Arcanum vocabulary.

## Step 2 - Map Current Ontology

6. Inventory source folders and representative documents.
7. Record observed roles, axes, statuses, tags, edge types, promotion rules, and source authority rules.
8. Identify gaps, contradictions, stale conventions, and undocumented practices.
9. Estimate the domain-knowledge inflection position:
   - low knowledge: prioritize discovery and session distillation,
   - near inflection: prioritize decision gates and focused ontology experiments,
   - high knowledge: justify promotion gates, convention changes, and heavier ontology investment.

## Step 2A - Map Branch-Aware Ontology When Needed

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

## Step 2B - Validate Branch Bridges

16. Every promoted business behavior with implementation impact should have at least one bridge edge or an explicit evidence gap.
17. Every promoted system artifact claim should identify whether it realizes, observes, tests, constrains, or merely supports a business claim.
18. Drift edges must preserve both the business expectation and the observed system behavior.
19. Bridge claims that assert alignment must cite evidence from both branches.
20. System claims must not silently redefine business meaning; business claims must not pretend implementation exists without bridge evidence.

## Step 3 - Distill Sessions And Delegated Evidence

21. Treat sessions as evidence records, not authority.
22. Extract durable claims, decisions, contradictions, open questions, and promoted candidates.
23. Preserve context and goal for each distillation.
24. When delegated research exists, keep raw delegated research separate from synthesis findings.
25. Require synthesis findings to cite delegated research before making load-bearing claims.
26. Surface contradictions between raw evidence outputs instead of resolving them silently.

## Step 4 - Review Premises And Confidence

27. For each premise or working bet, identify evidence, counterevidence, current use, falsification criteria, and confidence state.
28. Separate evidence confidence from commitment confidence.
29. Recommend one action: promote, keep, revise, demote, split, merge, retire, or escalate to decision gate.
30. Block promotion when evidence links are missing, contradictions remain unresolved, or the claim would outrank its sources.
31. For branch-aware promotion, keep business confidence and system confidence separate until bridge evidence supports alignment.

## Step 5 - Propose Convention Changes

32. For schema or ontology changes, record current rule, proposed rule, rationale, migration impact, affected files, and rollback path.
33. Ask one blocker-level governance decision at a time.
34. Do not mutate conventions unless the user explicitly approves the change.
35. For branch-aware convention changes, state whether the rule affects business, system, bridge, or cross-branch validation.

## Step 6 - Validate And Report

36. Validate links, role consistency, confidence gates, delegated-evidence traceability, source authority rules, branch ownership, bridge edges, drift findings, test links, and observability links.
37. Return a concise report with outputs, blockers, promotion decisions, convention changes, and next action.
    </process>

<branch-role-catalogs>
Use these as starter catalogs, not a universal taxonomy.

Business roles can include: actor, capability, business rule, policy, premise, outcome, workflow, domain event, decision, constraint, value measure.

System roles can include: component, service, module, endpoint, event, schema, table, queue, job, configuration, metric, test, deployment unit.

Bridge roles can include: traceability link, realization map, drift finding, test coverage link, observability link, constraint mapping, evidence gap.
</branch-role-catalogs>

<quality-bar>
A successful execution must:

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
  </quality-bar>

<anti-patterns>
Avoid:

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
  </anti-patterns>

<observability>
When `.arcanum/observability/` exists, emit post-run signals for:

- mode,
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
- Branch: business | system | bridge | mixed | none
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
