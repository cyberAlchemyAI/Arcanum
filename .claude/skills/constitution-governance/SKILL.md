---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/constitution-governance/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: constitution-governance
description: "Use when: creating, splitting, selecting, composing, validating, or promoting modular constitutions that enforce artifact structure/form without overloading task context."
argument-hint: "<create|add-rule|select|compose|validate|split|promote> <target-or-task> [--constitution <path>] [--output <path>] [--dry-run]"
tier: arcana
domain: constitution-governance
version: 0.1.0
origin: created from the artifact constitution/context-load concern and generalized into an Arcanum canonical sigil
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Agent
---

# Sigil: Constitution Governance

<objective>
Create, maintain, select, compose, and validate modular constitutions so structure/form rules remain enforceable without bloating task context.
</objective>

<logic-type>
Arcana: long-lived governance of modular rule artifacts, context selection, composition precedence, validator integration, and promotion decisions.
</logic-type>

<modes>
- `create`: draft a new constitution with scope, authority, selectors, rules, validation surface, and promotion boundary.
- `add-rule`: add or propose a new rule to an existing constitution, including validator impact.
- `select`: choose constitution excerpts relevant to a task or artifact before execution.
- `compose`: produce a minimal constitution pack from selected constitutions, resolving precedence and conflicts.
- `validate`: check whether an artifact, task, or validator satisfies selected constitution rules.
- `split`: propose a decomposition when one constitution has become too broad or low-effect.
- `promote`: prepare a constitution or rule for canonical adoption after evidence and validation pass.
</modes>

<applicability>
Use this sigil when:

- a governance rule should apply across future artifacts,
- a constitution is becoming a catch-all file,
- a task needs only the constitutions that match its artifact type or structure,
- selected constitutions need composition before a task runs,
- a new constitution rule requires a validation adapter,
- a validator should be updated in response to a constitution rule,
- constitution context load is weakening rule effect.
</applicability>

<non-applicability>
Do not use this sigil when:

- a local task note is enough,
- there is no reuse or validation expectation,
- a deterministic validator already covers the rule and no governance decision remains,
- Context Builder selection alone is enough and no composition, conflict, or validator impact exists.
</non-applicability>

<inputs>
Expected inputs, if available:

- target task, artifact type, constitution path, or rule proposal,
- existing constitution files,
- validator scripts or checks,
- known artifact failures,
- desired canonicality level,
- context budget or task scope,
- evidence from prior runs or reviews.
</inputs>

<default-output>
Prefer target-local outputs:

1. `arcana/constitution-governance/development/` for sigil development artifacts,
2. `<target>/development/constitution-pack.md` for task-specific composition packs,
3. `framework/<NAME>-CONSTITUTION.md` for framework-level constitutions,
4. `tools/` updates only when the user approves or the rule is already accepted.
</default-output>

<process>
1. Resolve the target rule, constitution, task, or artifact type.
2. Classify the request:
   - new constitution,
   - rule addition,
   - selection before execution,
   - composition pack,
   - validation adapter,
   - split/debloat,
   - promotion.
3. Gather only relevant constitution sources and validation surfaces.
4. Decide whether Context Builder selection is enough:
   - enough when the task only needs focused context,
   - not enough when selected rules interact, conflict, need precedence, or require validators.
5. For constitution creation or rule addition, define:
   - scope,
   - owner,
   - authority level,
   - selection predicates,
   - rules,
   - examples and non-examples,
   - validation adapters,
   - promotion boundary,
   - retirement or split triggers.
6. For selection, return only matching constitution rules with source paths, rationale, and excluded rules.
7. For composition, produce a compact constitution pack with:
   - selected rules,
   - precedence,
   - conflicts,
   - validators to run,
   - context budget,
   - pass/flag/block semantics.
8. For validator integration, map each rule to:
   - deterministic check,
   - review-only check,
   - future check,
   - blocked check.
9. Route unresolved precedence, canonicality, or mutation scope decisions through Decision Gate.
10. Validate the result against the target artifact or constitution package.
11. Return paths changed, rules selected, validators required, blockers, and next route.
</process>

<composition-rules>
Constitutions should compose by narrowest applicable scope first:

1. task-specific constitution pack,
2. artifact-type constitution,
3. domain or capability constitution,
4. framework constitution,
5. repository-wide default.

When two rules conflict:

- preserve both rules,
- classify the conflict as blocker, deferrable, or local override,
- use Decision Gate for blocker conflicts,
- do not silently let the larger constitution override the narrower one.

Context packs should include only the rules needed for the task, plus enough source links to audit them.
</composition-rules>

<validation-model>
Each rule must declare one validation mode:

- `deterministic`: script, lint, test, schema, or static check can enforce it,
- `review`: human or model review required,
- `hybrid`: deterministic precheck plus review,
- `none-yet`: constitution records intent, but promotion is blocked until a validation route exists.

Validator changes must cite the constitution rule they enforce.
</validation-model>

<quality-bar>
A successful execution must:

- keep constitutions modular and scoped,
- avoid loading a large constitution when selected rules suffice,
- separate Context Builder selection from constitution composition,
- define rule authority, selectors, examples, and validation mode,
- identify validator updates needed by new rules,
- preserve conflicts instead of smoothing them over,
- route blocker precedence or canonicality decisions through Decision Gate,
- keep generated task packs separate from canonical constitutions,
- return a pass, flag, or block result with paths and validators.
</quality-bar>

<anti-patterns>
Avoid:

- adding every new rule to one giant constitution,
- treating context selection as enforcement,
- treating validators as authority without a constitution rule,
- promoting rules without examples and non-examples,
- loading all constitutions into every task,
- hiding conflicts by choosing the newest rule,
- adding a validator check that is broader than its constitution scope,
- making a constitution canonical because it is convenient rather than evidenced.
</anti-patterns>

<observability>
For meaningful executions, emit or prepare telemetry with:

- mode,
- constitutions inspected,
- rules selected,
- rules added,
- composition pack path,
- validator changes proposed or applied,
- conflicts found,
- decision gates required,
- pass/flag/block result,
- context budget status.
</observability>

<output-contract>
Return:

```markdown
## Constitution Governance Result

- Mode: <create | add-rule | select | compose | validate | split | promote>
- Target: <target>
- Status: pass | flag | block
- Constitutions inspected: <paths>
- Rules selected or changed: <summary>
- Composition pack: <path or none>
- Validator impact: <required | applied | none | blocked>
- Conflicts: <none or list>
- Decisions needed: <none or list>
- Validation: <checks and result>
- Next route: context-builder | decision-gate | task-session | sigil-development | deferred
```
</output-contract>
