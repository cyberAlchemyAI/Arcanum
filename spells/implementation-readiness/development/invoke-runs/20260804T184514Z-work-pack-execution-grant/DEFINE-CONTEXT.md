# Define Context

## Intent

When a user says to run, finish, or continue a Work Pack until a real blocker,
the system should execute the pack's declared internal tool and capability
routes without asking for a new route authorization at each hop.

## Observed failure pattern

A plan can declare an owner prerequisite and still advertise Task Session as
its next route. Task Session then performs expensive context and admission work
before reporting that the owner prerequisite must run. Continuation Router can
identify the correct owner but refuses to dispatch because no exact
`--authorize-route` tuple was repeated by the user.

That sequence confuses three different things:

- user intent to execute a bounded Work Pack;
- deterministic use of internal tools and capability owners;
- consequential authorization for effects outside the Work Pack.

Only the third requires another decision.

## Existing evidence adopted

- Work Pack Readiness Audit already implements the opt-in
  `selected-unit-at-task-session` profile.
- Its end-to-end fixture proves one semantic audit, explicit selected-unit
  binding, live material admission, and zero pre-execution Refresh calls.
- Task Session already validates exact writes, target baselines, validation
  contracts, owner boundaries, and single-use mutation admission.
- Continuation Router already ranks owner routes, prevents cycles, invokes one
  owner, and joins its receipt.
- `task-session-until-blocker` already owns a finite outer serial loop across
  fresh Task Sessions.

The missing behavior is therefore adoption and orchestration, not a new
mutation authority system.

## Scope

- Upgrade `implementation-readiness` into the plan-to-execution outer loop.
- Make new Invoke Plans emit one unambiguous execution-entry projection.
- Treat a direct Work Pack execution instruction as sufficient for declared,
  in-scope, repository-local capability and tool usage.
- Let Continuation Router consume that execution binding without per-hop route
  approval.
- Let Task Session reject or route a missing prerequisite before full context
  construction.
- Preserve current stop boundaries and legacy ad hoc continuation behavior.

## Non-goals

- No ambient permission to edit arbitrary repository paths.
- No automatic authority, promotion, publication, deployment, credentials,
  network integration, spending, destructive cleanup, or irreversible effect.
- No weakening of live path, digest, validation, owner, or receipt checks.
- No recursive Task Session and no multi-SWU Task Session receipt.
- No private consuming-project content in this public package.

## Definition verdict

Pass. The target is a single bounded behavior: one execution intent should
carry internal plan-declared routing until the work reaches a real blocker.

