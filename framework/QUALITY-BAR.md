# Quality Bar

The Quality Bar defines what must be true for a sigil execution to count as successful.

It is not a general wish list. It is the minimum standard that lets another agent or human reviewer decide whether the sigil did its job. A good Quality Bar turns the sigil's intent into observable completion criteria.

## Problem It Solves

Without a Quality Bar, a sigil can appear complete because it produced output, even when the output is vague, unsafe, unreviewable, or mismatched to the task.

The Quality Bar prevents that by naming the conditions that separate acceptable execution from merely plausible execution.

## What A Quality Bar Should Do

- define success in terms of observable evidence,
- match the sigil's tier and logic type,
- identify the minimum acceptable result,
- make review possible without rereading the agent's hidden reasoning,
- prevent low-effort or over-scoped outputs from passing.

## Tier-Specific Shape

Formulae Quality Bars should emphasize determinism, exactness, input handling, repeatability, and machine-checkable output.

Transmutations Quality Bars should emphasize faithful synthesis, source grounding, handling of ambiguity, reviewable structure, and clear separation between evidence and inference.

Arcana Quality Bars should emphasize role clarity, phase discipline, evidence preservation, decision gates, synthesis quality, and responsible continuation or stop conditions.

## Authoring Pattern

Write each criterion as a check the reviewer can apply:

```text
A successful execution must <observable result or constraint>.
```

Prefer concrete checks:

- The output names all required inputs and marks missing inputs explicitly.
- Each finding includes an evidence reference or is labeled as an inference.
- The final result follows the declared output contract.

Avoid vague checks:

- The output should be good.
- The agent should understand the context.
- The result should be useful.

## Minimum Contents

Every sigil Quality Bar should answer:

- What must be present in the result?
- What evidence or structure makes the result reviewable?
- What constraints must the agent preserve while executing?
- What failure mode would make the result unacceptable?
- What level of completeness is enough for this sigil's tier?

For governed work that can cross an owner or effect boundary, the Quality Bar must
also name the terminal outcome contract. Component PASS receipts are insufficient:
success requires a schema-valid terminal receipt whose exact boundary, effects,
postimages, authority ceiling, and successor state satisfy the frozen predicate.

Preacceptance checks collect every reachable blocker and preserve the first nonzero.
Effectful execution fails fast. A task is bounded only when it is the smallest
complete vertical slice that traverses all required consumers and can reach that
terminal predicate.

## Example Criteria

For a Formulae sigil:

- A successful execution must return the same result for the same input state.
- A successful execution must report invalid inputs instead of repairing them silently.
- A successful execution must use the declared output schema.

For a Transmutation sigil:

- A successful execution must identify source material used for synthesis.
- A successful execution must separate direct evidence, inference, and open decisions.
- A successful execution must produce the declared artifact without adding unrelated scope.

For an Arcana sigil:

- A successful execution must preserve phase outputs and decision history.
- A successful execution must distinguish findings from synthesized tensions.
- A successful execution must stop at the human gate before recommending action that changes the system.

## Common Mistakes

- Writing quality criteria as aspirations rather than checks.
- Duplicating the process steps instead of defining success conditions.
- Making the Quality Bar so broad that every execution fails.
- Making the Quality Bar so soft that any output passes.
- Forgetting tier differences and applying the same criteria to every sigil.

## Relationship To Anti-Patterns

The Quality Bar says what good execution must include. [Anti-Patterns](ANTI-PATTERNS.md) say what misuse or degraded execution must avoid.

Together, they create the operating boundary for the sigil: one side defines success, the other defines failure modes.
