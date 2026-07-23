---
name: decision-gate
description: "Use when: resolving blocker-level multi-option decisions before planning, implementation, document mutation, or other consequential changes continue."
argument-hint: "<target-scope> [--profile generic|pilot|release|custom] [--output <path>]"
tier: arcana
domain: decision-governance
version: 0.3.0
origin: generalized from recurring pre-mutation decision governance practice
allowed-tools: Read, Write, Glob, Grep, AskQuestions
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
3. Before asking a preference question, represent every candidate with a stable
   option ID, option kind (`action`, `defer`, or `stop`), owner-supplied
   structural status and evidence, reversibility, hazard class, rejection
   reasons, and owning gate when one applies.
4. Run `scripts/prefilter-options.py` with the canonical request and receipt
   schemas. Decision Gate consumes structural verdicts from the caller or
   owning validator; it does not manufacture application-specific validity.
5. Route the admissible cardinality exactly:
   - zero: return structural `BLOCK` with rejected options and reasons; ask no
     preference question,
   - one: return `direct` with the sole option and its owner gate; do not
     manufacture consent or execute the route,
   - two or more: continue through Decision Gate with only those admissible
     options.
6. Treat destructive, authority, promotion, publication, and spend hazards,
   plus every irreversible candidate, as inadmissible unless a named owner gate
   is present. The prefilter does not satisfy or bypass that gate.
7. Persist the option-admissibility receipt with its request digest. Duplicate
   option IDs, malformed evidence/status combinations, and invalid schema block
   before human presentation.
8. Enumerate unresolved decisions with two or more admissible options.
9. Classify each decision:
   - blocker: must be resolved before consequential mutation,
   - deferrable: can be recorded and revisited later,
   - assumption: can proceed if clearly labeled.
10. For each blocker decision, prepare concrete options with concise trade-offs:
   - option name,
   - benefit,
   - cost or risk,
   - when to choose it,
   - downstream impact.
11. Ask the user each blocker decision:
   - prefer an ask-questions interface when available,
   - otherwise use plain conversation with numbered options,
   - always present a standing "Explain / more context" choice alongside the real
     options (see <context-option>); it is never one of the decision answers.
12. Continue until all blocker decisions are resolved or the user explicitly defers/stops.
13. If any blocker decision remains unresolved, return `BLOCK` and do not proceed with consequential mutation.
14. Persist the decision record with:
   - decision question,
   - considered options,
   - selected option,
   - rationale,
   - source of decision,
   - timestamp,
   - remaining blockers,
   - deferred decisions or assumptions.
15. Return a decision-gate summary with `PASS` or `BLOCK`, resolved decisions, remaining blockers, the option-admissibility receipt, and the decision artifact path.
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
When this sigil returns `BLOCK`, consequential mutation must not proceed until
the blocker decisions are resolved or a typed, matching, current, unconsumed
non-protected override is consumed by `scripts/consume-override.py`. Ambient
assent and free-form approval are not overrides. Destructive, authority,
promotion, publication, and spend hazards always remain with their owning gate;
the generic override consumer cannot admit them.
</authority-rule>

<override-consumption>
An override is a durable one-use artifact conforming to
`schemas/override.schema.json`. The live consumption request binds one run,
target, normalized scope, and hazard class through
`schemas/override-consumption-request.schema.json`.

Before relying on an override:

1. Run `scripts/consume-override.py` with the override artifact, live request,
   and canonical schemas.
2. Require exact target, scope, and hazard equality; valid issuance/expiry
   timestamps; and `consumed_by=null`.
3. For a non-protected override, the consumer acquires an exclusive lock,
   re-reads the current artifact, persists the consuming run, and emits a
   schema-valid consumption receipt.
4. On every rejection, preserve the override bytes. A replay retains the first
   consumer and returns `block`.
5. For a protected hazard, return `owner_route_required=true` and route to the
   owning gate. A free-form `owner_gate_receipt` path is not producer-owned
   typed evidence and cannot make the generic override valid.

The consumption receipt authorizes only the exact decision override it names.
It is not reusable authority and does not satisfy another lifecycle,
publication, promotion, destructive-action, or spend gate.
</override-consumption>

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
- prefilter structurally inadmissible and unsafe-unowned candidates before
  asking the user,
- route zero/one/two-plus admissible candidates to block/direct/gate exactly,
- preserve defer and stop as legitimate typed options,
- never treat a direct route as consent, execution, or owner-gate satisfaction,
- require exact target/scope/hazard/time bindings before consuming an override,
- persist one-use consumption before returning an admitted override receipt,
- preserve the first consumer on replay and leave rejected override bytes
  unchanged,
- route every protected hazard to its owning gate,
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
- presenting structurally inadmissible options to the user,
- invoking Decision Gate when zero or one admissible option remains,
- treating owner-supplied structural status as permission to bypass a protected
  owner gate,
- treating ambient assent, a path string, or an untyped approval note as an
  override,
- accepting stale, mismatched, already consumed, or scope-expanding override
  evidence,
- admitting a protected hazard through the generic override consumer,
- returning override success before `consumed_by` is durably persisted,
- silently dropping defer or stop from the candidate set,
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
- Admissibility receipt: <path>
- Admissible routing: block | direct | gate
- Override receipt: <path or none>
- Override verdict: consumed | block | not-requested
- Decision artifact: <path>
- Deferred decisions: <summary or none>
- Assumptions recorded: <summary or none>
- Validation: <checks performed>
- Next step: <proceed | ask remaining decision | stop>
```
</output-contract>
