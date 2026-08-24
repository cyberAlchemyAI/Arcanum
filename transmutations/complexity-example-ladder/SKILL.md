---
name: complexity-example-ladder
description: "Use when: an explanation or comparison needs aligned low-, medium-, and complex examples without changing evidence, option semantics, or decision authority."
argument-hint: "<subject-or-decision> [--mode explanatory|comparative]"
tier: transmutations
domain: explanation-calibration
version: 0.1.0
origin: extracted from a user correction requiring complexity-calibrated examples during Decision Gate explanation
allowed-tools: Read, Glob, Grep
---

# Sigil: Complexity Example Ladder

<objective>
Turn one evidence-bounded explanation or comparison into aligned low-, medium-,
and complex examples that increase structural complexity without changing the
underlying concept, options, recommendation, or authority state.
</objective>

<logic-type>
Transmutation: bounded example synthesis and complexity calibration.
</logic-type>

<trigger>
Use this sigil when:

- the user asks to explain, illustrate, or provide examples,
- a caller contract requires complexity-calibrated examples,
- multiple options need comparable examples before a human choice,
- interacting identity, state, dependency, boundary, or failure conditions make
  an abstract distinction hard to evaluate.

Do not invoke it for unrelated factual or mechanical answers merely to add prose.
For Decision Gate, invoke only after the user selects "Explain / more context" or
otherwise signals uncertainty.
</trigger>

<inputs>
Resolve, when available:

- the subject, question, or decision being explained,
- authoritative source evidence and its claim ceiling,
- the invariant concept or distinction that must stay fixed across all rungs,
- every admissible action option when the mode is comparative,
- defer and stop choices when their continuation effects matter,
- constraints, assumptions, and authority boundaries,
- caller and trigger kind,
- audience baseline and optional complexity axes.

If the source cannot support a rung and a safe hypothetical cannot be labeled,
return `BLOCK` rather than fabricate the example.
</inputs>

<complexity-model>
- `low`: one primary concept or action; local context; no material dependency;
  reversible or consequence-light behavior.
- `medium`: multiple interacting concepts or options; at least one dependency,
  state change, boundary, or downstream consequence.
- `complex`: several actors, layers, states, or dependencies plus an exception,
  uncertainty, failure path, authority boundary, or dependent decision.

These are structural differences, not word-count, jargon, or detail targets.
</complexity-model>

<process>
1. Determine mode:
   - `explanatory` for one concept or mechanism,
   - `comparative` for two or more admissible options.
2. Separate source evidence, caller-provided constraints, and agent inference.
   Label every invented scenario detail as hypothetical.
3. Extract one invariant concept, distinction, or comparison that must remain
   stable across all three rungs.
4. Choose the smallest useful structural complexity axes from interacting
   concepts, dependencies, state, boundaries, consequences, exceptions, and
   uncertainty.
5. Build the low example. Keep it local and remove nonessential dependencies.
6. Build the medium example by preserving the low invariant and adding at least
   one interaction, dependency, state change, boundary, or consequence.
7. Build the complex example by preserving the same invariant and adding a
   cross-boundary interaction, exception, ambiguity, failure path, authority
   consequence, or dependent decision.
8. State explicitly what each rung adds over the previous rung.
9. In comparative mode:
   - reuse the same scenario for every admissible action option within a rung,
   - give every option equivalent explanatory depth,
   - show defer and stop only as unchanged or terminated continuation states,
   - do not change option wording, recommendation, or admissibility.
10. For each rung, state what it demonstrates and what it does not prove.
11. Validate that all three rungs exist, the invariant is preserved, option
    coverage is even, unsupported claims are zero, and decision effect is none.
12. Return the ladder. If called by a decision workflow, return control without
    selecting, recording, admitting, executing, or authorizing an option.
</process>

<observability>
A meaningful execution is an attempted or completed three-rung ladder.

When repository observability is available, record the standard sigil signal plus:

- trigger kind and caller,
- explanatory or comparative mode,
- required and produced rungs,
- complexity axes,
- invariant-preservation result,
- required options and per-rung coverage,
- hypothetical count,
- unsupported-claim count,
- unequal-option-coverage flag,
- decision effect,
- user correction signal.

Default reflection triggers are 5 meaningful executions, 10 generated outputs,
3 related gaps, or 1 severe gap. Severe gaps include unlabelled fabrication,
examples treated as consent or selection, material option bias, and private/public
or authority-boundary leakage.
</observability>

<quality-bar>
A successful execution must:

- produce low, medium, and complex rungs,
- increase structural complexity at every rung,
- preserve one stable concept or comparison invariant,
- distinguish evidence from labelled hypothetical details,
- use one shared scenario per rung in comparative mode,
- cover every admissible action option evenly,
- keep defer and stop as continuation states rather than invented product behavior,
- state what each example demonstrates and does not prove,
- report any unsupported claim instead of hiding it,
- preserve the caller's recommendation, admissibility, gate, and authority state,
- keep public templates and experiment fixtures product-neutral,
- return `decision effect: none` whenever a decision is involved.
</quality-bar>

<anti-patterns>
Avoid:

- increasing length without increasing structural complexity,
- changing the core subject or invariant between rungs,
- equating jargon with complexity,
- introducing unsupported domain facts,
- presenting a hypothetical as source evidence,
- giving a recommended option richer or more favorable examples,
- using unrelated scenarios that prevent controlled comparison,
- silently omitting a rung or admissible action option,
- turning an example into a recommendation, choice, consent, or owner approval,
- treating the ladder as application-specific validity or admissibility proof,
- expanding into implementation, mutation, promotion, publication, or execution,
- copying caller-private material into public sigil examples or fixtures.
</anti-patterns>

<output-contract>
Return:

```markdown
## Complexity Example Ladder Result

- Status: pass | block
- Subject: <subject or decision>
- Mode: explanatory | comparative
- Complexity basis: <structural axes>
- Evidence: <sources or supplied context>
- Assumptions: <labelled hypotheticals or none>

### Low
- Scenario: <shared low scenario>
- Example: <concept behavior or every option under the scenario>
- Demonstrates: <what becomes visible>
- Limits: <what this does not prove>

### Medium
- Added complexity: <structural addition>
- Scenario: <shared medium scenario>
- Example: <concept behavior or every option under the scenario>
- Demonstrates: <what becomes visible>
- Limits: <what this does not prove>

### Complex
- Added complexity: <structural addition>
- Scenario: <shared complex scenario>
- Example: <concept behavior or every option under the scenario>
- Demonstrates: <what becomes visible>
- Limits: <what this does not prove>

### Coverage
- Rungs produced: <n>/3
- Options covered: <IDs or not applicable>
- Unsupported claims: <count and details>
- Decision effect: none | not applicable
- Next step: <return to caller | supply missing evidence>
```
</output-contract>
