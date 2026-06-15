---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/decision-gate/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: decision-gate
description: "Use when: resolving blocker-level multi-option decisions before planning, implementation, document mutation, or other consequential changes continue."
argument-hint: "<target-scope> [--profile generic|pilot|release|custom] [--output <path>]"
tier: arcana
domain: decision-governance
version: 0.1.0
origin: generalized from recurring pre-mutation decision governance practice
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
---

# Sigil: Decision Gate

<objective>
Resolve every blocker-level multi-option decision before consequential work proceeds, and persist a reusable decision record.
</objective>

<logic-type>
Arcana: decision governance with human gatekeeping and pass/block authority.
</logic-type>

<applicability>
Use this sigil when:

- a task has multiple viable options,
- the choice affects future scope, implementation, documentation, rollout, policy, verification, cost, or risk,
- the agent cannot responsibly infer the correct option,
- downstream work should stop until the decision is explicit,
- a durable decision record is needed.
</applicability>

<inputs>
Expected inputs, if available:

- target scope or task name,
- existing request, plan, notes, requirements, architecture docs, or implementation files,
- known constraints,
- options already proposed by the user,
- preferred output path,
- decision profile, if the project has one.
</inputs>

<default-output>
If the user does not provide `--output`, write or update the decision record at the first suitable location:

1. `docs/decisions/{target-scope}.md` when a docs folder exists,
2. `decisions/{target-scope}.md` when a decisions folder exists,
3. `DECISIONS.md` at the repository root when no better location exists.
</default-output>

<process>
1. Identify the target scope and the consequential work that is blocked by unresolved decisions.
2. Gather only relevant context: user request, current plan, requirements, architecture notes, related docs, implementation files, tests, and known constraints.
3. Enumerate unresolved decisions with more than one viable option.
4. Classify each decision:
   - blocker: must be resolved before consequential mutation,
   - deferrable: can be recorded and revisited later,
   - assumption: can proceed if clearly labeled.
5. For each blocker decision, prepare concrete options with concise trade-offs:
   - option name,
   - benefit,
   - cost or risk,
   - when to choose it,
   - downstream impact.
6. Ask the user each blocker decision:
   - prefer an ask-questions interface when available,
   - otherwise use plain conversation with numbered options,
   - always present a standing "Explain / more context" choice alongside the real
     options (see <context-option>); it is never one of the decision answers.
7. Continue until all blocker decisions are resolved or the user explicitly defers/stops.
8. If any blocker decision remains unresolved, return `BLOCK` and do not proceed with consequential mutation.
9. Persist the decision record with:
   - decision question,
   - considered options,
   - selected option,
   - rationale,
   - source of decision,
   - timestamp,
   - remaining blockers,
   - deferred decisions or assumptions.
10. Return a decision-gate summary with `PASS` or `BLOCK`, resolved decisions, remaining blockers, and the decision artifact path.
</process>

<context-option>
Every blocker decision must offer a non-committal "Explain / more context" choice in
addition to its real options. Selecting it does not resolve the gate. When the user
takes it — or otherwise signals they are unsure ("let me think", "not sure", a
question instead of a choice) — expand the decision before asking again:

- restate the decision and why it blocks the consequential work,
- give the deeper rationale and the source evidence behind each option, citing files,
  prior decisions, or notes,
- spell out what each option concretely changes downstream, including reversibility,
  cost, risk, and any decision it forces or forecloses,
- surface related or dependent decisions,
- name the recommended option and why, without choosing it.

After explaining, re-present the same decision with the same real options and the
standing "Explain / more context" choice again. Loop until the user picks a real
option or explicitly defers or stops. The explain choice never counts as consent.
</context-option>

<authority-rule>
When this sigil returns `BLOCK`, consequential mutation should not proceed until the blocker decisions are resolved or the user explicitly overrides the gate.
</authority-rule>

<observability>
For reusable use, emit a post-run invocation signal using the repository-local observability package when available.

Recommended signals:

- decision count,
- blocker count,
- unresolved blocker count,
- pass/block result,
- output path,
- user override, if any,
- follow-up reflection trigger when the same decision type repeats.
</observability>

<quality-bar>
A successful execution of this sigil must:

- identify every visible blocker-level multi-option decision,
- separate blocker decisions from deferrable decisions and assumptions,
- present options with meaningful trade-offs,
- offer a non-committal explain / more-context choice on every blocker decision and expand on request before asking again,
- avoid choosing on the user's behalf when the decision is consequential,
- persist a reviewable decision record,
- return a clear `PASS` or `BLOCK` result,
- preserve enough context for future reviewers to understand why each decision was made.
</quality-bar>

<anti-patterns>
Avoid:

- asking the user to decide trivial or fully reversible details,
- bundling multiple independent decisions into one vague question,
- presenting options without trade-offs,
- forcing a choice when the user is unsure instead of offering deeper explanation,
- treating silence as consent for a blocker decision,
- proceeding with consequential mutation after a `BLOCK` result,
- hiding assumptions inside implementation or documentation,
- writing a decision record that cannot be traced back to the user choice or source context.
</anti-patterns>

<output-contract>
Return:

```markdown
## Decision Gate Result

- Target scope: <scope>
- Result: PASS | BLOCK
- Decisions resolved: <count>
- Blockers remaining: <count>
- Decision artifact: <path>
- Deferred decisions: <summary or none>
- Assumptions recorded: <summary or none>
- Validation: <checks performed>
- Next step: <proceed | ask remaining decision | stop>
```
</output-contract>