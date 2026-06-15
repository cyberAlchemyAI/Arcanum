---
to: Arcanum user-guide maintainers
from: User / Translate / Guide development surface
re: "Core idea and applications of guided user translation"
date: 2026-06-10
audit-against: "development/user-guide/packages/{user-ledger,translate,guide}/ + role-bound handoff pattern"
status: guide entrypoint - concept and application handoff
---

# User / Translate / Guide

User / Translate / Guide is a candidate Arcanum pattern for helping a person
understand something unfamiliar without flattening either side of the encounter.

The core idea is simple: **Guide orchestrates the explanation, Translate builds
honest bridges between domains, and User keeps protected evidence about what
helped this person understand.** Those three responsibilities stay separate so
the system can adapt without hidden profiling, translate without distorting the
target domain, and guide without becoming an unbounded all-purpose tutor.

---

## The one-sentence thesis

Guide should not merely explain a target; it should route the explanation through
the user's known anchors, Translate's mapping limits, and active evidence of
understanding, then leave behind a receipt that can improve the next guide run.

---

## 1. The three-part model

| Part | Owns | Does not own |
| --- | --- | --- |
| `user-ledger` | Protected local handles: domain anchors, vocabulary preferences, concept states, mastery evidence, residues, and receipt proposals. | Hidden profiling, canonical truth, translation logic, or Guide orchestration. |
| `translate` | Meaning maps between vocabularies, domains, and concept frames, including where the bridge breaks. | User memory, full Guide routing, canonical glossary promotion, or unbounded research. |
| `guide` | The route: frame the request, inspect context, choose whether research/x-ray/Translate is needed, sequence the explanation, ask for active evidence, and emit a receipt. | User memory internals, translation internals, canonical definitions, or unlimited dispatch. |

This separation is the load-bearing move. If Guide owns everything, it becomes
opaque. If Translate ignores User, it explains with the wrong anchors. If User
stores every interaction as truth, adaptation becomes surveillance instead of
learning support.

---

## 2. The user-facing promise

The pattern is for moments where a person says some version of:

- "Explain this architecture in terms I already understand."
- "Translate this scientific idea into software-engineering intuition."
- "Help me understand this workflow from my business context."
- "Show me where this analogy works and where it breaks."
- "Guide me through this repo, plan, paper, design, or feature until I can use it."

The answer should not be a generic summary. It should be a guided bridge:

1. Identify the target and what the user wants to do with it.
2. Find or ask for the user's useful anchors.
3. Translate unfamiliar concepts through those anchors.
4. Preserve target-domain truth and mapping limits.
5. Check understanding with an active prompt, not passive completion.
6. Propose what the User ledger may remember, without silently writing identity.

---

## 3. What "translation" means here

Translation is not word substitution. It is a structured bridge between meaning
systems.

| Translation object | Example |
| --- | --- |
| Term map | "boundary" in architecture maps partly to "contract line" in business operations. |
| Bridge map | A deployment pipeline can be explained like a staged manufacturing process. |
| Primitive alignment | "Dependency" may mean import relation, work sequencing, or conceptual reliance depending on domain. |
| Mapping limit | A sales funnel analogy may explain flow, but not type safety or failure isolation. |
| Target-domain definition | The explanation must still preserve what the target actually means in its own domain. |

Translate should make bridges useful and make their limits visible. The limit is
part of the explanation, not a footnote.

---

## 4. Applications

| Application | How the pattern helps |
| --- | --- |
| Repository onboarding | Guide inspects a repo surface, Translate maps unfamiliar architecture terms into the user's known domains, and User records clarified concepts. |
| Product discovery | Guide explains a product workflow through stakeholder language while preserving technical constraints and open decisions. |
| Research comprehension | Guide routes papers, standards, or references through Translate so the user gets usable analogies without losing source precision. |
| Cross-functional collaboration | Engineers, designers, sales, operations, and domain experts can receive the same target explanation through different anchors. |
| MVP planning | Guide turns a broad idea into understandable layers, Translate bridges business and technical vocabulary, and User keeps residues for the next refinement. |
| Learning loop | Active evidence prompts distinguish "the explanation seemed clear" from "the user can now transfer or teach back the concept." |
| Handoff and continuity | Guide receipts and User ledger proposals let a future session resume from evidence rather than restarting the explanation. |
| Accessibility of complex systems | X-ray-style structure plus Translate bridges can make dense architectures, processes, or plans navigable to non-specialists. |

This is especially useful anywhere the failure mode is not lack of information,
but mismatch between the target's native vocabulary and the user's current frame.

---

## 5. Example route

```text
User asks:
  "Guide me through this architecture using examples from logistics operations."

Guide:
  frames the target and goal
  inspects the architecture context
  decides whether x-ray, research, or inventory is needed
  calls Translate for architecture -> logistics bridges

Translate:
  maps terms and primitives
  names where the logistics analogy breaks
  returns a translation receipt

Guide:
  sequences the explanation
  includes mapping limits at the right moments
  asks an active evidence prompt
  proposes a User ledger update

User ledger:
  stores only approved/protected handles and evidence
  marks concepts clarified or mastered only when evidence supports it
```

The end state is not "the assistant explained it." The end state is a bounded
receipt: what was explained, which bridge was used, what limits were named, what
evidence was requested, and what may improve the next guide run.

---

## 6. Current local artifacts

| Artifact | Role |
| --- | --- |
| `ARCANUM-DEVELOPMENT-USAGE-GUIDE.md` | Main guide for turning an idea into a governed Arcanum development route. |
| `arcanum-development-loop.html` | Visual explanation of the broader Arcanum development loop. |
| `guide-user-translate-overview.html` | Visual overview of the User / Translate / Guide relationship. |
| `packages/user-ledger/` | Candidate sigil package for protected user learning/profile handles. |
| `packages/translate/` | Candidate sigil package for meaning bridges and mapping limits. |
| `packages/guide/` | Candidate spell/orchestrator package for guided explanation routes. |
| `fixtures/whisper-idea-to-mvp/` | Example fixture for guiding an idea toward MVP development. |
| `refinement-runs/` | Evidence from refine-driven guide development passes. |
| `task-sessions/` | Bounded execution records for guide-related work. |
| `session-handoffs/` | Continuation context for future sessions. |

These artifacts are development evidence. They do not by themselves promote a
sigil, install a command, mutate registries, or create durable user profile state.

---

## 7. Boundary rules

1. **Guide routes; it does not absorb.** Guide may call Translate, x-ray,
   dispatch-spec, inventory, or task-session, but it should not duplicate their
   responsibilities internally.
2. **Translate preserves target truth.** A bridge is only useful if the target
   domain survives the analogy.
3. **User memory is proposed, protected, and evidence-backed.** Passive exposure
   is not mastery, and local preferences are not canonical definitions.
4. **Applications stay bounded.** A guide route should name its target, budget,
   evidence expectations, and residue.
5. **Candidate packages remain candidate packages.** Promotion belongs to the
   relevant sigil or spell lifecycle.

---

## 8. Known risks and open questions

- **Guide can become too broad.** The pattern fails if Guide becomes a catch-all
  tutor instead of an orchestrator.
- **Analogies can overclaim.** Translate must surface mapping limits early enough
  that the user does not inherit a false model.
- **User-ledger boundaries need care.** Adaptation should help explanation, not
  become hidden diagnosis or identity capture.
- **Application fixtures are still narrow.** More examples are needed across repo
  onboarding, research comprehension, product planning, and cross-functional work.
- **Promotion status must stay visible.** The packages can look complete while
  still being unpromoted development artifacts.

---

## Three sharpest next questions

1. Which application should prove the pattern first: repo onboarding, research
   comprehension, product planning, or cross-functional translation?
2. What is the smallest fixture that can show Guide calling Translate while User
   only receives an evidence-backed update proposal?
3. Which package needs the next lifecycle step: `user-ledger`, `translate`, or
   `guide`?
