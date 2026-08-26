# Arcanum Composition Analysis

Agents are making software production cheaper and superficially easier. A person can now produce considerably more code with the help of agents than would previously have been practical.

As the amount of work that can be produced increases, it becomes more important to keep track of what was done, assess the quality of the result and understand what needs to be done next.

The goal of Arcanum is to help a person produce more and better work without turning that increase in capacity into information overload. We approach this by keeping track of the work that has been done and connecting the evidence it produces, as well as what remains open, next steps and blockers, so the user can understand the current state of the work without keeping all of it in mind.

## Practical example

Suppose a user wants to add a new authentication flow to a product. That goal can be broken into smaller pieces of work, like implementing the endpoint and testing the result.

One piece may finish and provide evidence that part of the goal is complete. Another may reveal a blocker because the authentication library no longer supports the SDK.

Arcanum keeps track of these results and where they came from, preserving their provenance as the broader state of the work changes.

The objective is to keep states explicit, so the user can see what is complete, what remains open and what needs attention next.

## How Arcanum works

At a high level, Arcanum keeps the broader context of the work separate from the execution of specific parts of it, while keeping their relationship explicit. A specific piece of work can depend on other work and contribute to a broader objective, and the system needs to preserve those relationships as the work evolves.

The three main components are Task Session, which governs what is executed; Decision Gate, which makes consequential decisions explicit; and Craft, which keeps track of the state of the work.

Task Session governs the execution of a piece of work, keeping its scope, completion criteria, and validation explicit.

Decision Gate handles decisions that can materially change the course of the work, keeping the available options and the selected direction explicit before dependent work continues.

Craft maintains the broader state of the work as it evolves, so that decisions, blockers, and evidence remain explicit and can inform what should happen next.

## Craft ledger

The Craft ledger is the project-local record of the current state of the work. It keeps track of the work as it progresses, including blockers and decisions. One of its goals is to keep what remains open visible to the user.

One of the most important concepts in Craft is evidence. It is the basis used to verify outcomes and to justify conclusions and decisions. Evidence can come from observations or tests performed during the work.

At the current stage, Craft keeps track of information such as:

| Item | What it represents |
| --- | --- |
| **Context** | A part of the project whose state is being tracked. |
| **Artifact** | Something produced or used during the work. |
| **Blocker** | Something preventing work from progressing. |
| **Decision** | A choice that affects the direction of the work. |
| **Gap** | Something known to still be missing or unresolved. |
| **Evidence** | What supports a conclusion about the work. |
| **Next move** | What should happen next. |

## Task Session

A Task Session is the execution of one bounded piece of work. It keeps the task's objective, scope, expected result, completion criteria, and validation tied together while the work is being performed.

Execution can reveal missing dependencies, new blockers, or choices that change what should happen next. A Task Session should not silently absorb those changes. If the work can be completed within its scope, the session executes it and validates the result. If it cannot, the unresolved issue remains explicit instead of being guessed away.

A Task Session keeps explicit:

- **Scope** — what work is being executed.
- **Completion criteria** — what needs to be true for the work to be considered complete.
- **Validation** — how the result will be checked.
- **Outcome** — what happened during execution and what evidence it produced.

The result of a Task Session is therefore not only an artifact or code change. It also produces evidence about what was actually executed and validated. That result can then update the broader state kept by Craft.

## Decision Gate

Some choices can materially change the direction of the work and should not be hidden inside execution. Decision Gate makes those choices explicit before dependent work continues.

When more than one viable path remains, it keeps the relevant alternatives and their consequences visible so that the direction of the work can be chosen explicitly rather than assumed by the agent.

A Decision Gate keeps explicit:

- **Decision** — what needs to be decided.
- **Options** — the viable paths being considered.
- **Trade-offs** — the relevant differences between those paths.
- **Selected direction** — the option chosen for the work to follow.

Not every implementation choice needs a Decision Gate. Local or easily reversible choices can remain inside execution. The gate is intended for decisions whose answer materially changes what should happen next.
