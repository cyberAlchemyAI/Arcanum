# Spellcraft

Spellcraft is an Arcana sigil for designing, installing, validating, observing, and revising spells.

It helps users combine existing sigils into localized workflows without copying or mutating the sigils themselves. A spell defines orchestration: phases, shared state, gates, handoffs, failure policy, local customization, and observability.

Spellcraft also manages spell aliases. A spell keeps a stable canonical ID for filenames and automation, while users can invoke it through memorable aliases such as `Repository Codex`. The name `Necronomicon` is reserved for the persistent repository harness.

Spellcraft is the lifecycle owner for spell artifacts. It may consume handoff packets produced by [Invoke](../../spells/invoke/), but Invoke does not replace spell lifecycle design, installation, validation, observation, or reflection.

## Problem It Solves

Some work is best handled by multiple sigils together. Users should not have to remember the right sequence every time, and individual sigils should not grow extra responsibilities just to support a common workflow.

Spellcraft solves this by creating explicit spell contracts that compose sigils by reference.

## Use When

- several sigils should run together in a repeatable workflow,
- a repository needs a local spell under `.arcanum/spells/`,
- a user wants to adapt a library spell to local paths and policies,
- continuing from an Invoke handoff that targets spell creation or revision,
- outputs from one sigil should become inputs to another,
- a spell needs validation, observability, or revision.

## Do Not Use When

- one sigil already handles the task,
- the composition is a one-off experiment,
- the workflow has no handoff artifacts or gates,
- the spell would copy sigil internals instead of referencing them,
- the user needs immediate execution rather than a reusable local workflow.

## Chain Position

Spellcraft sits after Invoke and before execution:

```text
invoke handoff -> spellcraft lifecycle work -> task-session for approved implementation tasks
```

Responsibilities:

- Invoke owns discovery, authoring baseline, and handoff artifacts.
- Spellcraft owns spell composition, phase/gate design, local installation/adaptation, validation, observability, reflection, and revision.
- Sigil Development owns changes to individual sigil contracts referenced by the spell.
- Task Session owns bounded execution of approved work-pack tasks or SWUs.
- Experiment Harness owns repeatable test mechanics, live Codex examples, validation reports, and telemetry emission for reusable spells.

If a referenced sigil needs to change, Spellcraft should route that work to Sigil Development instead of redefining the sigil internally.

## Codex Goal And Experiment Closure

When spell implementation or local adaptation work uses Codex native Goals, close the loop through both Task Session and Experiment Harness:

```text
spellcraft owns lifecycle work-pack
  -> task-session selects one ready task/SWU
  -> codex-goal adapter creates native /goal
  -> Codex executes the bounded runtime goal
  -> task-session reviews evidence and syncs the work-pack
  -> experiment-harness validates reusable spell behavior
  -> spellcraft consumes validation, telemetry, and reflection signals
```

Codex Goal evidence can prove that one bounded implementation or adaptation unit completed. It does not replace spell experiments. A reusable spell is not promotion-ready until experiment evidence checks realistic prompts, phase outputs, gates, handoffs, Quality Bar, Anti-Patterns, and observability.

For spell lifecycle proof, initialize the harness with the Spellcraft profile:

```bash
arcana/experiment-harness/scripts/init-harness.sh <spell-path> --type spell --profile spellcraft
```

This keeps Experiment Harness responsible for mechanics while Spellcraft remains responsible for spell lifecycle judgment.

## Default Output

Repository-local spells should live at:

```text
.arcanum/spells/<spell-name>/README.md
```

Reusable library spells live in [spells](../../spells/).

## Alias Rules

- Canonical IDs are stable and use kebab-case.
- Aliases are human-facing names that resolve to canonical IDs.
- Alias lookup is case-insensitive.
- An alias must resolve to exactly one active spell.
- Local repositories may add local aliases without changing upstream spell contracts.
- Spell run reports should record both the alias used and the canonical ID.

## Why This Is Arcana

Spellcraft coordinates workflow design, local repository adaptation, sigil compatibility checks, gate design, observability, and lifecycle maintenance across multiple sigils.
