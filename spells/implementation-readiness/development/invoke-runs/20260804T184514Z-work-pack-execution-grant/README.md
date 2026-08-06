# Work-Pack Execution Grant

This Invoke development package repairs the plan-to-execution boundary so one
direct instruction to run or finish a Work Pack is enough to use the internal
tools and capability routes that the pack already requires.

The repair removes per-hop authorization ceremony. It does **not** remove
scope, owner, validation, or stop gates.

## Start here

1. [SPEC.md](SPEC.md) defines the behavior and decision classes.
2. [architecture-bundle.md](architecture-bundle.md) assigns the outer loop to
   `implementation-readiness` and preserves capability ownership.
3. [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) describes the implementation.
4. [WORK-PACK.md](WORK-PACK.md) contains eight ordered Smallest Working Units.
5. [execution-pack.md](execution-pack.md) shows the implementation waves.
6. [INVOKE-RESULT.md](INVOKE-RESULT.md) is the governed authoring receipt.
7. [PACKAGE-VALIDATION.md](PACKAGE-VALIDATION.md) records final deterministic checks.
8. [OBSERVABILITY-RESULT.md](OBSERVABILITY-RESULT.md) locates the Invoke and Distill signals.
9. [prototype-execution/COMPLETION-AUDIT.md](prototype-execution/COMPLETION-AUDIT.md)
   proves the implemented candidate-local prototype requirement by requirement.

## Result in one sentence

`run this Work Pack` binds the current plan and permits its declared,
repository-local tool/capability hops; the system asks again only when the work
encounters a real decision or crosses the declared risk/scope boundary.

## Current prototype status

All eight SWUs are implemented and validated locally. Declared internal routes,
including one typed repairable same-route retry, proceed without per-hop
authorization prompts. The chain is complete with
`authorization_prompt_count=0` and generated Codex/Claude parity.

## Evidence ceiling

This is candidate-local deterministic prototype evidence. It does not prove or
authorize promotion, publication, deployment, release, production readiness,
or lifecycle synchronization. Those deferred records remain assigned through
`HN-DCABCAB6B742`.
