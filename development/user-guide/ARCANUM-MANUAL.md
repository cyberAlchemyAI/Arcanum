---
to: anyone trying to understand and use Arcanum
from: the Arcanum manual research strategy (x-ray → inventory → distill → whisper → validate)
re: "What Arcanum is, what its processes are, and how each kind of user can leverage it"
date: 2026-06-16
audit-against: "README.md + framework/ + registry/ + disciplines/ + spells/ + arcana/ + development/user-guide/"
status: manual — source-backed, validated against ARCANUM-MANUAL.validation.md
---

# The Arcanum Manual

A guide to what Arcanum is, how it works, and how to put it to use. Every claim here is
backed by a file in this repository; the companion
[ARCANUM-MANUAL.validation.md](ARCANUM-MANUAL.validation.md) maps claims to their sources.

This manual is modeled on the existing [User / Translate / Guide user-guide](README.md): it
explains one layer at a time, surfaces the load-bearing ideas, and routes you to the right
capability instead of trying to be everything at once.

---

## The one-sentence thesis

**Arcanum is a framework for creating reusable agent capabilities through governed synthesis** —
it turns vague intent into artifacts that humans and agents can understand, reuse, validate, and
improve, by keeping the objective, the output, the discovery, the tension, and the lifecycle owner
visible the whole way through. *(Source: [README.md](../../README.md))*

The center of Arcanum is the [CyberAlchemy Method](../../framework/CYBERALCHEMY-METHOD.md): a way
of working that refuses to let work start before its intent is clear, refuses to close before
discovery is done, and always leaves a reviewable artifact behind.

---

## Part 1 — What Arcanum is

### The problem it solves

Most agent work evaporates: a clever prompt produces a one-off answer, and the reasoning, the
trade-offs, and the lessons vanish. Arcanum's bet is that capability should *compound*. Instead of
re-deriving the same workflow each time, you build a **capability** once — with a contract, a
quality bar, failure modes, and observability — and reuse it. *(Source:
[README.md](../../README.md), [framework/CYBERALCHEMY-METHOD.md](../../framework/CYBERALCHEMY-METHOD.md))*

### The three building blocks

Arcanum has exactly three kinds of reusable thing. Keeping them distinct is the load-bearing move.

| Block | What it is | What it does **not** do | Source |
| --- | --- | --- | --- |
| **Sigil** | One reusable agent capability (a folder with `README.md` + `SKILL.md`). | It is not a workflow; it solves one bounded problem. | [registry/SIGILS.md](../../registry/SIGILS.md), [arcana/README.md](../../arcana/README.md) |
| **Spell** | A composed workflow that *references* several sigils and defines their phases, shared state, gates, and observability. | It does not copy sigil internals — it orchestrates them. | [registry/SPELLS.md](../../registry/SPELLS.md), [spells/README.md](../../spells/README.md) |
| **Discipline** | A cross-capability operating practice (e.g. planning, schema, observability) that shapes many capabilities without being one. | It is not a registry entry and holds no promotion authority. | [disciplines/README.md](../../disciplines/README.md), [disciplines/DISCIPLINES.md](../../disciplines/DISCIPLINES.md) |

Today the repository ships **34 sigil packages** under [arcana/](../../arcana/), plus **4** under
[transmutations/](../../transmutations/) and **2** under [formulae/](../../formulae/); **14 spells**
under [spells/](../../spells/); and a discipline catalog of ~21 practices in
[disciplines/DISCIPLINES.md](../../disciplines/DISCIPLINES.md).

### The three capability tiers

Sigils are organized not by *function* but by the *kind of reasoning* they perform. *(Source:
[README.md](../../README.md), [framework/QUALITY-BAR.md](../../framework/QUALITY-BAR.md),
[framework/ANTI-PATTERNS.md](../../framework/ANTI-PATTERNS.md))*

- **Formulae** — deterministic, rule-based, repeatable. Same input → same output; invalid input is
  *reported*, not silently repaired. (e.g. `observability-setup`.)
- **Transmutations** — bounded cognitive synthesis. Probabilistic interpretation with source
  grounding and clearly separated evidence vs. inference. (e.g. `context-builder`,
  `feature-glossary`.)
- **Arcana** — autonomous orchestration. Recursive inquiry, decision gates, multi-agent
  governance, stop conditions. (e.g. `craft`, `refine`, `dispatch-spec`, `task-session`.)

The tier sets the quality bar and the anti-patterns: a Formula is judged on determinism, an Arcana
on role clarity and responsible continuation.

---

## Part 2 — What its processes are

Arcanum has four processes worth knowing. They nest: the **method** governs a single run, the
**lifecycle** governs a capability's life, the **observe→reflect loop** governs its improvement, and
**governance** keeps authority from collapsing.

### Process A — The CyberAlchemy Method (one run)

Every Arcanum run keeps five anchors visible. *(Source:
[framework/CYBERALCHEMY-METHOD.md](../../framework/CYBERALCHEMY-METHOD.md),
[README.md](../../README.md))*

1. **Objective** — what are we trying to solve?
2. **Output artifact** — what should exist when this is done?
3. **Discovery** — what must we learn before it can responsibly close?
4. **Tension** — what could make it brittle, oversized, misleading, or unsafe?
5. **Route** — who or what owns the next step?

The method runs as a recursive loop: **Orient** (name the seed, bound context, state the target) →
**Discover** (evidence, gaps, alternative frames) → **Shape** (choose route, draft, stress with
tension, revise) → **Stabilize** (make navigable, record trace, route ownership) → **Evolve**
(reflect so the next run is better).

Its governing principles read like house rules: *intent before machinery, discovery feeds
synthesis, artifact over vibes, ergonomics is governance, lifecycle ownership matters, reflection
closes the loop.* *(Source: [framework/CYBERALCHEMY-METHOD.md](../../framework/CYBERALCHEMY-METHOD.md))*

### Process B — The capability lifecycle (one sigil's life)

A sigil is not created in one pass. It moves through a **12-stage workflow**: candidate capture →
tier classification → intent design (`README.md`) → behavior contract (`SKILL.md`) → quality &
failure design → templates → observability design → review & validation → trial execution →
**promotion** → observe & reflect → maintenance. Promotion is *evidence-gated*, not a vibe: the
folder must be complete, the quality bar and anti-patterns specific, links valid, and a realistic
trial must not expose blocking ambiguity. *(Source:
[framework/SIGIL-DEVELOPMENT-WORKFLOW.md](../../framework/SIGIL-DEVELOPMENT-WORKFLOW.md),
[arcana/sigil-development/SKILL.md](../../arcana/sigil-development/SKILL.md))* Spells follow the
analogous lifecycle under [spellcraft](../../arcana/spellcraft/).

### Process C — The observe → reflect → iterate loop (improvement)

Arcanum treats observability as infrastructure, not optional logging. After a run, exactly one JSON
signal is appended to a central ledger ([.arcanum/observability/](../../.arcanum/observability/));
counters accumulate; when a **reflection trigger** fires (manual request, 5 meaningful executions,
10 generated outputs, 3 related workflow gaps, or 1 severe gap) the capability is routed to
reflection. The loop is owned by three sigils in sequence:
[signal-observer](../../arcana/signal-observer/) (append telemetry, never mutate) →
[workflow-reflect](../../arcana/workflow-reflect/) (analyze, propose — never mutate) →
[sigil-development](../../arcana/sigil-development/) (decide and apply). *(Source:
[framework/observability/README.md](../../framework/observability/README.md),
[framework/observability/SIGIL-OBSERVABILITY-HOOK.md](../../framework/observability/SIGIL-OBSERVABILITY-HOOK.md),
[framework/SIGIL-DEVELOPMENT-WORKFLOW.md](../../framework/SIGIL-DEVELOPMENT-WORKFLOW.md))*

### Process D — Governance & boundaries (authority)

Authority is distributed by lifecycle role, and roles do not reach outside their lane. `invoke`
owns define/design/plan/handoff; `sigil-development` owns sigil lifecycle and promotion;
`spellcraft` owns spell lifecycle; `task-session` owns bounded execution; `signal-observer` is
append-only and non-blocking; `workflow-reflect` proposes but never mutates; `decision-gate`
resolves blocker-level choices. Every created file is an artifact with an owner and a retention
class (source / durable-evidence / generated / local-runtime) under the
[Artifact Constitution](../../framework/ARTIFACT-CONSTITUTION.md). Crucially, **execution evidence
never silently promotes canonical knowledge** — promotion belongs to the owning capability.
*(Source: [CLAUDE.md](../../CLAUDE.md),
[arcana/constitution-governance/SKILL.md](../../arcana/constitution-governance/SKILL.md),
[framework/ARTIFACT-CONSTITUTION.md](../../framework/ARTIFACT-CONSTITUTION.md))*

---

## Part 3 — How each kind of user can leverage it

Arcanum is wide, so the most useful question is not "what can it do?" but "what do *I* need right
now?" The table routes seven reader personas to their entry points. Personas marked *(inferred)* are
grounded in registry "use-when" conditions and the user-guide thesis rather than a single explicit
roster. *(Source: [development/user-guide/README.md](README.md),
[development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.md](ARCANUM-DEVELOPMENT-USAGE-GUIDE.md),
[README.md](../../README.md), [FRIEND-INSTALL-TUTORIAL.md](../../FRIEND-INSTALL-TUTORIAL.md))*

### Newcomer / learner — *"What is this and where do I start?"*
Read the [README Start-Here](../../README.md), then this manual, then the interactive
[user-guide HTML](arcanum-development-loop.html). To try it on a repo, follow
[FRIEND-INSTALL-TUTORIAL.md](../../FRIEND-INSTALL-TUTORIAL.md).

### Capability consumer / invoker — *"Help me shape an idea into real work."*
This is the most common path. Use [refine](../../arcana/refine/) to turn a vague target into a
seed/design/plan; [invoke](../../spells/invoke/) to author durable define/design/plan artifacts;
[decision-gate](../../arcana/decision-gate/) when a blocking choice appears;
[x-ray](../../arcana/x-ray/) to see hidden structure; and [task-session](../../arcana/task-session/)
to execute one bounded task with validation.

### Capability author — *"I want to build a new reusable capability."*
Start at [sigil-development](../../arcana/sigil-development/) (for one sigil) or
[spellcraft](../../arcana/spellcraft/) (for a composed workflow). Prove it with
[experiment-harness](../../arcana/experiment-harness/). If you already have a tangled skill, use
[skill-decomposer](../../arcana/skill-decomposer/) or
[skill-transcriptor](../../arcana/skill-transcriptor/) to extract and convert it.

### Repository maintainer / installer — *"Get Arcanum running here."*
Use the [arcanum-bootstrap](../../spells/arcanum-bootstrap/) spell and
[sigil-runtime-installer](../../arcana/sigil-runtime-installer/) to expose capabilities through your
host runtime (Claude Code, Codex, Copilot), and [observability-setup](../../formulae/observability-setup/)
for the telemetry skeleton. Walkthrough: [FRIEND-INSTALL-TUTORIAL.md](../../FRIEND-INSTALL-TUTORIAL.md).

### Reviewer / validator *(inferred)* — *"Is this output safe to trust?"*
Audit against [QUALITY-BAR.md](../../framework/QUALITY-BAR.md) and
[ANTI-PATTERNS.md](../../framework/ANTI-PATTERNS.md); demand evidence via
[experiment-harness](../../arcana/experiment-harness/) and the
[Validation Experiment Protocol](../../framework/VALIDATION-EXPERIMENT-PROTOCOL.md); read run signals
through [signal-observer](../../arcana/signal-observer/).

### Researcher / evidence hunter *(partly inferred)* — *"Organize discovery and claims."*
Route research with [dispatch-spec](../../.claude/skills/dispatch-spec/SKILL.md), compile knowledge
with [inventory](../../arcana/inventory/), govern sessions/premises/confidence with
[ontology-vault](../../arcana/ontology-vault/), scope with
[scope-interview](../../arcana/scope-interview/), surface cross-layer tensions with
[robot-talks](../../arcana/robot-talks/), and drive a paper end-to-end with the
[publication-research-pipeline](../../spells/publication-research-pipeline/).

### Cross-functional collaborator *(inferred)* — *"Same system, different lenses."*
Use [guide-architecture](../../spells/guide-architecture/) and the
[User / Translate / Guide](README.md) pattern to bridge vocabularies without flattening any domain,
and [decision-gate](../../arcana/decision-gate/) so each role's contribution is visible.

---

## Part 4 — A closer look at the tools you asked about

This part zooms in on four things newcomers most often ask about, grounded in how people
actually drive Arcanum (pipelines + delegation). *(Sources verified in
[research/manual-question-types/](research/manual-question-types/): witnessed user prompts +
capability contracts; adjudicated by a research dispatch.)*

### Use the tools the way you already work

If your instinct is "set up a space, route a plan, then turn it into something readable," Arcanum
already matches that shape — you don't adopt a new workflow, you name the one you have. A common
real pipeline is **`craft` → `dispatch-spec` → `whisper`**: open a Craft ledger to hold context and
decisions, author a validated route, then synthesize the result into an explainer. Two habits make
this work: **couple *do* with *explain*** — every pipeline ends in an artifact a human can read —
and **delegate execution** by spawning subagents for bounded stages rather than running everything
inline.

### How `refine` helps (and how it differs from `invoke` and `task-session`)

`refine` is for when the idea is still broad. It runs a fixed **ten-stage** discovery/design loop —
context baseline → invoke-define → interrogation review → research decision → distill →
invoke-design → design review → distill-repair → invoke-plan → final synthesis — and presets tune
the *depth*, not the stages. It makes discovery **mandatory before design**, and it does **not
auto-execute**: it shows you a Run Strategy Proposal and waits for permission. The switch-rule:
reach for **`refine`** when the target is still vague; **`invoke`** when you already have approval
and want durable define/design/plan artifacts; **`task-session`** only once a bounded unit of work
exists. *(Source: [arcana/refine/SKILL.md](../../arcana/refine/SKILL.md))*

### Constructing a `dispatch-spec` to execute actions

A dispatch-spec is the *shape* of a route, not the run itself — **it validates structure and does
not execute**. The required fields are `dispatch_id, intent, mode, steps, gates, observability`.
Each step carries `step_id, name, capability_ref, pattern, inputs[], outputs[]`, where `pattern` is
one of the catalogued kinds (`route | sequential | fanout | dialectic | tournament | distill | xray
| decision | validation | toy_game | synthesis | handoff`). Parallel steps need a `join_policy`; a
`validation` step needs an `evidence_artifact`; techniques are cited from the catalog only when
actually used; and **gates** (`policy | quality | promotion_guardrail | validation | human_approval`)
prevent unsafe continuation. You **author** a route by writing this document, and **validate** it
(the `validate-dispatch` script) before running. One seam worth holding: the Run Strategy Proposal
`refine` shows you is *not yet* a validated dispatch-spec — `refine` may recommend a route, but the
dispatch-spec is the explicit shape you validate before anything runs. *(Source:
[.claude/skills/dispatch-spec/SKILL.md](../../.claude/skills/dispatch-spec/SKILL.md) +
[formulae/dispatch-spec/dispatch.schema.yml](../../formulae/dispatch-spec/dispatch.schema.yml))*

### What `constitution-governance` is, and why it matters

A constitution is a **modular, scoped ruleset** that governs the *structure and form* of artifacts.
Constitutions compose **narrowest-scope-first** (task → artifact-type → domain → framework → repo),
and each rule declares a **validation mode** — `deterministic`, `review`, `hybrid`, or `none-yet`.
The point is that it is a **selector**, not a 200-rule catch-all: you load only the rules that apply
to the artifact in front of you. Why it matters, without circularity: it lets you **validate an
artifact without context bloat** and **promote work only once its rules are met** — so authority and
quality stay legible instead of living in someone's head. (Operationally: when you have an artifact,
`constitution-governance` is also how you *select and compose* which constitution binds it.)
*(Source: [arcana/constitution-governance/SKILL.md](../../arcana/constitution-governance/SKILL.md))*

## A worked path (the shortest real loop)

The existing user-guide demonstrates the canonical loop end-to-end. *(Source:
[development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.md](ARCANUM-DEVELOPMENT-USAGE-GUIDE.md))*

1. **Start with a rich idea** — no polish required.
2. **Refine** it into a seed, then **invoke** define → design → plan as durable artifacts.
3. **Route blockers** through `decision-gate`, `dispatch-spec`, or `x-ray` instead of guessing.
4. **Execute one `task-session`** at a time, only when scope and validation are clear.
5. **Record evidence and residue** — what passed, what failed, what's still open — and let the
   observe→reflect loop improve the capabilities you used.

This manual itself was produced that way: a validated `dispatch-spec` route ran `x-ray` →
`inventory` → `distill` → `whisper` → validation, with the route and residue tracked in a
[Craft ledger](../../CRAFT.md).

---

## Glossary (local, source-linked)

- **Sigil** — one reusable agent capability. *([registry/SIGILS.md](../../registry/SIGILS.md))*
- **Spell** — a workflow composing multiple sigils. *([registry/SPELLS.md](../../registry/SPELLS.md))*
- **Discipline** — a cross-capability practice with no promotion authority. *([disciplines/README.md](../../disciplines/README.md))*
- **Tier** — Formulae / Transmutations / Arcana, by kind of reasoning. *([README.md](../../README.md))*
- **CyberAlchemy Method** — the governed-synthesis working method. *([framework/CYBERALCHEMY-METHOD.md](../../framework/CYBERALCHEMY-METHOD.md))*
- **Quality Bar / Anti-Patterns** — observable success criteria / misuse boundaries. *([framework/QUALITY-BAR.md](../../framework/QUALITY-BAR.md), [framework/ANTI-PATTERNS.md](../../framework/ANTI-PATTERNS.md))*
- **Promotion** — the evidence-gated step that makes a capability library-ready. *([framework/SIGIL-DEVELOPMENT-WORKFLOW.md](../../framework/SIGIL-DEVELOPMENT-WORKFLOW.md))*
- **Reflection trigger** — the usage threshold that routes a capability to improvement. *([framework/observability/README.md](../../framework/observability/README.md))*

---

## Questions this manual now answers

Grounded in real usage (a research dispatch mined the question-types people actually bring to
Arcanum). **Answered** are witnessed; the **can also answer** set is contract-backed but not yet a
question anyone asked here — labelled so the manual never overclaims.

**Answered:**
- How do I compose a multi-capability pipeline like `craft → dispatch-spec → whisper`?
- How do I distill a large body of knowledge into an explainer?
- How do I inspect/expose the framework surface to work from it? (`x-ray`)
- How do I execute work by spawning subagents instead of running inline?
- How do I validate or design a dispatch route before running it?
- How do I build a research strategy that mines my own prompts?
- How do I use the tools the way I already work, and how does `refine` help?
- What is `constitution-governance` and why does it matter?

**Can also answer (contract-backed, not yet asked here):**
- `refine` vs `invoke` vs `task-session` — when each? · How do I see what happened in a run I
  dispatched, and make it reflect/improve? (`signal-observer` → `workflow-reflect`) · Which
  constitution applies to *this* artifact, and how do I compose one? · When does a pipeline graduate
  into a reusable spell? · How do I install Arcanum in another repo?

## Where to go next

- The working philosophy: [framework/CYBERALCHEMY-METHOD.md](../../framework/CYBERALCHEMY-METHOD.md)
- Pick one capability: [registry/SIGILS.md](../../registry/SIGILS.md)
- Pick a workflow: [registry/SPELLS.md](../../registry/SPELLS.md)
- Install it: [FRIEND-INSTALL-TUTORIAL.md](../../FRIEND-INSTALL-TUTORIAL.md)
- See the visual surface: [arcanum-surface-xray.html](arcanum-surface-xray.html)

*This manual is documentation. It explains the sigils, spells, definitions, and registries of
Arcanum; it does not hold authority over them and promotes nothing.*
