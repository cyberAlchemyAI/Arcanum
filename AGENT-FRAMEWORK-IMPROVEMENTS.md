# Agent Framework Improvements — Memo

External memo proposing targeted improvements to Arcanum's multi-agent and lifecycle machinery, mapped from a sibling project (`domainspec`) that has been operationalizing multi-agent dispatch under a single schema. Written as a candid review, not a sales pitch.

## What I'm Proposing

Arcanum already has most of the moving parts I would otherwise propose — `robot-talks`, `spellcraft`, `signal-observer`, `workflow-reflect`, `experiment-harness`, and the `sigil-development` lifecycle. What it does **not** have is a unified **dispatch spec** that names the fan-out shape, role-order invariants, and per-agent budgets at the time a multi-agent run is launched. Today this knowledge is implicit inside individual Arcana sigils (e.g. Robot-Talks's Phase 1 strategy step, Spellcraft's `design` mode). Making it explicit — as a small portable schema referenced by Spellcraft and Robot-Talks — would close three observable gaps without adding a new tier.

Below: what Arcanum already does well, then 3 concrete proposals that fit, then 2 ideas from the source material I would **not** import.

## Arcanum Today (My Read)

The repo is well factored. Specifically:

- **Three-tier ontology** by epistemic nature: `formulae/` (deterministic), `transmutations/` (bounded synthesis), `arcana/` (sovereign orchestration). The placement rules in [`formulae/README.md`](formulae/README.md), [`transmutations/README.md`](transmutations/README.md), and [`arcana/README.md`](arcana/README.md) are clear and self-policing.
- **Composition is a separate layer**: [`spells/`](spells/) compose sigils by reference, governed by [`arcana/spellcraft/`](arcana/spellcraft/). Spells don't copy sigil internals.
- **Multi-agent investigation** is owned by [`arcana/robot-talks/`](arcana/robot-talks/) — 4 phases, mandatory human gate, scope-by-concern decomposition, evidence-as-data rule.
- **Observability is portable**: [`framework/observability/REPOSITORY-PACKAGE.md`](framework/observability/REPOSITORY-PACKAGE.md), the [`SIGIL-OBSERVABILITY-HOOK.md`](framework/observability/SIGIL-OBSERVABILITY-HOOK.md), [`arcana/signal-observer/`](arcana/signal-observer/), and [`arcana/workflow-reflect/`](arcana/workflow-reflect/) form a closed telemetry → reflection loop. The [`spells/observed-invocation-loop/`](spells/observed-invocation-loop/) wires this around managed invocations.
- **Lifecycle governance**: [`arcana/sigil-development/`](arcana/sigil-development/) and [`framework/SIGIL-DEVELOPMENT-WORKFLOW.md`](framework/SIGIL-DEVELOPMENT-WORKFLOW.md) cover authoring → observation → reflection → iteration. [`arcana/experiment-harness/`](arcana/experiment-harness/) gives spells a real-runtime validation loop.

So the gap is not "missing concepts" — it is "implicit contracts that should be made explicit and reusable".

## Concrete Improvement Opportunities

### 1. Promote Robot-Talks's "Step 2 — Orchestrator proposes strategy" into a reusable Dispatch Spec

**Where it lives today.** [`arcana/robot-talks/SKILL.md`](arcana/robot-talks/SKILL.md) Phase 1 Step 2 has the agent state agent roles plus "one alternative decomposition considered and why it was rejected", then humans approve. Spellcraft's `design` mode in [`arcana/spellcraft/SKILL.md`](arcana/spellcraft/SKILL.md) does the same job in prose for spells.

**The gap.** The strategy is rewritten from scratch each time and lives only in the session transcript. There is no machine-readable artifact a `signal-observer` can later attribute findings against, no schema a validator can lint, and no way to recognize that "this run was a flat-fanout with 3 investigators" from telemetry alone.

**Proposal.** Add a small `dispatch-spec` Formulae sigil under `formulae/dispatch-spec/` whose only job is to validate a YAML/JSON document with fields like:

```yaml
dispatch_id: <ulid>
mode: investigation | composition | sequential
shape: single | flat-fanout | triangulation | adversarial-audit | parent-synthesis
layers:
  - role: investigate | evaluate | synthesize
    n: <int>
    parallel: true | false
    sigils: [<sigil-id>, ...]
loop_cap: <int <= 5>
stop_conditions: [...]
```

Robot-Talks Phase 1 and Spellcraft `design` then emit and reference a `dispatch-spec` instance. This is a Formulae sigil (deterministic validation), and it slots cleanly under the existing tier rules in [`formulae/README.md`](formulae/README.md).

**Before/after.** Today, Robot-Talks's "alternative decomposition considered" lives as prose in the session file under `claude/current_conversations/...`. After, it lives as `shape_considered: triangulation` and `shape_chosen: flat-fanout` in the spec — and [`arcana/signal-observer/`](arcana/signal-observer/) can finally aggregate "how often does the orchestrator pick triangulation vs flat-fanout, and which one produces more actionable tensions?"

### 2. Add role-order and synthesizer-identity invariants to Spellcraft `validate`

**Where it lives today.** [`arcana/spellcraft/SKILL.md`](arcana/spellcraft/SKILL.md) `validate` mode checks that referenced sigils exist and aliases resolve uniquely. Robot-Talks already enforces a phase order (Setup → Exploration → Synthesis → Gate) in prose.

**The gap.** Nothing currently prevents a spell from declaring a `synthesize` phase that runs **before** `investigate`, or a synthesizer that is itself a sub-orchestrator (recursion without a budget). In a small registry this is fine; once spells compose spells, it becomes a real failure mode.

**Proposal.** Three rules in `spellcraft validate`:

1. `investigate` phases must precede `evaluate` and `synthesize`.
2. `synthesize` phases must be performed by the parent orchestrator, not a delegated sub-agent (analogous to "synthesize MUST use `model: parent`" in the source material — Arcanum's neutral phrasing is "synthesis stays with the spell, not its composed sigils").
3. A spell that composes other spells must declare a `recursion_budget: { depth, breadth }` and `spellcraft validate` blocks if depth > 2 without an explicit user override.

This fits Spellcraft's existing `validate` mode and the [`framework/ANTI-PATTERNS.md`](framework/ANTI-PATTERNS.md) house style.

### 3. Bind the Observed Invocation Loop to a `dispatch_id`, not just a sigil name

**Where it lives today.** [`spells/observed-invocation-loop/`](spells/observed-invocation-loop/), with [`framework/observability/SIGIL-OBSERVABILITY-HOOK.md`](framework/observability/SIGIL-OBSERVABILITY-HOOK.md) appending JSON per invocation, and [`arcana/workflow-reflect/`](arcana/workflow-reflect/) reading those signals.

**The gap.** Today each sigil invocation is observed independently. When Robot-Talks fires 4 investigators in parallel, telemetry sees 4 unrelated signal rows. Workflow-Reflect cannot ask "did this fan-out as a whole succeed?" — only "did agent #3 follow its output contract?".

**Proposal.** Add two optional fields to the telemetry schema in [`framework/observability/REPOSITORY-PACKAGE.md`](framework/observability/REPOSITORY-PACKAGE.md): `dispatch_id` (links siblings in a fan-out) and `parent_dispatch_id` (links a nested spell to its caller). The hook in [`framework/observability/SIGIL-OBSERVABILITY-HOOK.md`](framework/observability/SIGIL-OBSERVABILITY-HOOK.md) accepts both as environment variables. [`arcana/signal-observer/`](arcana/signal-observer/) groups signals by `dispatch_id` before deriving behavior signals. This is a strict addition — older signals without the field still parse.

**Why this matters.** Until siblings are linked, `workflow-reflect` cannot detect things like "in 7 of the last 10 Robot-Talks runs, investigator #2 produced the most evidence but synthesis never cited it" — the kind of pattern that justifies a sigil revision.

## What I Would NOT Import

Two pieces of the source material do not fit Arcanum and I would explicitly leave them out.

- **Hard-coded heuristic-row taxonomy** (`single-lookup`, `triangulation`, `parent-synthesis`, `meta-dispatch`, `adversarial-audit`). In the source project they were defaults the strategist picks when the user does not specify. Arcanum's culture is "concept files explain placement, sigils carry the rules" — a fixed taxonomy contradicts that. The `shape:` field in proposal 1 should be an open string with a recommended starter set, not an enum.
- **Discovery-promotion gate** (the source project's "Step 7": promote findings into a knowledge vault, with separate `vault/discovery/` and `docs/features/<feature>/discovery/` paths). Arcanum already has [`arcana/inventory/`](arcana/inventory/) and [`arcana/ontology-vault/`](arcana/ontology-vault/) for compiled knowledge; trying to import the source project's vault-path convention would force Arcanum into a folder layout it has consciously declined. Robot-Talks's existing handoff to `claude/current_conversations/` plus the inventory sigil is the right Arcanum-shaped equivalent.

I would also be cautious about the source project's 9-item validator checklist as-is. The principle (a structured validator) is good and fits Arcanum's existing `validate` modes; the specific list is tuned to the source project's vault and should not be ported verbatim.

## Suggested Next Step — One Small Experiment

Pick **proposal 3** as the smallest testable change:

1. Add `dispatch_id` and `parent_dispatch_id` as optional fields to the telemetry hook in [`framework/observability/SIGIL-OBSERVABILITY-HOOK.md`](framework/observability/SIGIL-OBSERVABILITY-HOOK.md).
2. Modify [`arcana/robot-talks/SKILL.md`](arcana/robot-talks/SKILL.md) Phase 1 to generate a `dispatch_id` and pass it to each investigator via env.
3. Run one real Robot-Talks investigation in a consuming repository and confirm that `signal-observer` can group the four siblings.
4. Use [`arcana/experiment-harness/`](arcana/experiment-harness/) to make the run reproducible.

If grouping works and `workflow-reflect` produces a useful cross-sibling observation, proposal 1 (the dispatch-spec sigil) becomes the natural next move — proposal 1 is essentially "give that `dispatch_id` a schema-validated body". If grouping by ID does not change what `workflow-reflect` can say, the deeper proposals are not worth the weight and should be dropped.

A memo that recommends one cheap experiment with a clear kill criterion is more honest than one that recommends five mappings without one.
