# Plan: From Design To Buildable Work

Plan answers a practical question: **what exactly must be built, in what
order, and how will we know each part works?**

It starts from an admitted Design. The author writes one JSON file containing
the objectives, delivery slices, implementation layers, waves, tasks, Smallest
Working Units, implementation details, tests, gates, blockers, gaps, later
execution routes, and closeout evidence.

The compiler turns that JSON into a Work Pack and smaller task and wave pages.
Those pages make the work easier to read; they are not separate plans. If a
generated page is wrong, correct the JSON and compile again.

Plan also checks what later tools will need. For example, a mutation-capable
plan runs the real readiness audit twice without executing implementation; a
task routed through Task Session produces a Task Session projection; delegated
or bounded-context work produces one checked context projection per unit; and
multi-owner, delegated, protected, or reusable routes produce checked dispatch
input. When a tool does not apply, the bundle says why instead of silently
skipping it.

Finally, admission compiles the source again and compares every generated
byte. A passing admission means the plan can be reproduced from its source. It
does **not** mean that anyone approved or started implementation.

For exact fields and commands, use the [Plan authoring guide](../plan-authoring-guide.md).
The [Plan contract](../plan.md) defines the normative behavior.
