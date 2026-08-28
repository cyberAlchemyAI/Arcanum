# Review — subagent prompt-identity enforcement from session 2026-08-28-1648

## Coverage

| attacker | lens | targets checked | findings raised | zero-findings defense |
|---|---|---|---:|---|
| Turing, Alan | fidelity, governance, schema compatibility, ownership, reference integrity | all 21 declared target artifacts and 6 governing/comparator artifacts | 5 | Defended registrar/readiness equivalence, strict whitespace/body validation, generated Python parity, registrar/concurrency results, briefing/projection digest checks, and target stability. |
| Hewitt, Carl | mechanics, correctness, runtime projection, operability, portability, abuse resistance | all 21 declared target artifacts and 6 governing/comparator artifacts | 4 | Failed attacks included missing-name, mismatched-prefix, empty-body, stale generated Python, mutated briefing/projection, and registrar concurrency paths; these fail closed or reproduced successfully. |

## Findings

| # | artifact and locator | evidence | severity | consequence | proposed fix |
|---|---|---|---|---|---|
| F1 | `arcana/subagent-strategy/SKILL.md:103,108-110`; `runtime/orchestrate/scripts/native_dispatch_coordinator.py:148-172,278-281,345-347,623-647`; `runtime/orchestrate/scripts/native_dispatch_driver.py:450-490`; `formulae/dispatch-spec/scripts/validate-dispatch.py:457-510,619-636`; `.arcanum/observability/subagents-strategy/subagents-dispatch.yaml:129,136-142,150` | The governing skill makes the identity sentence part of the exact confirmed `initial_prompt` and requires passing that exact prompt to the host. Registration compares only group/count/dependency topology; identity equality is conditional on a runtime `agent_name`; actions carry a briefing binding rather than the ledger's full prompt; and the driver assembles a new host message from briefing and runtime fields. Dispatch Spec validates briefing integrity but never establishes equality with the registered agent's full prompt. The predecessor direct launch demonstrably appended context after confirmation. | CRITICAL | Deterministic gates permit a host message unequal to the confirmed `initial_prompt`, directly contradicting the governing exact-prompt law. No corrupt native execution was observed. | Bind each registered agent's name and full confirmed prompt one-to-one into executable actions, require Dispatch Spec and the coordinator to prove exact equality unconditionally, and submit those exact bytes to the host; include any required runtime context before confirmation. |
| F2 | `arcana/subagent-strategy/scripts/append-dispatch.cjs:114,239-247`; `telemetry/agents/subagents-dispatch.yaml:17` | The registrar still declares schema `0.6.1` but now requires a nonempty `agent_name`, exact `You are {agent_name}.\n\n` prefix, and nonempty body. Historical `0.6.1` data contains `agent_name: null` and a nonconforming prompt. | MAJOR | The same versioned serialized shape remains readable in the grandfathered ledger but fails when newly produced or rematerialized. No runtime failure of an already-ledgered historical row was demonstrated. | Introduce a new schema version for mandatory identity admission and retain version-specific `0.6.1` validation, or preserve prior `0.6.1` admission semantics until an explicit migration boundary exists. |
| F3 | `arcana/subagent-strategy/scripts/append-dispatch.cjs:543-549`; `.arcanum/observability/subagents-strategy/subagents-dispatch.yaml:136-142`; `runtime/orchestrate/SKILL.md:185-194` | Close validation unconditionally requires `agents_spawned.total` to equal the complete registered agent count. The failed predecessor launched one agent but records `total: 4` with `explorer: 1` and `not_launched: 3`. | MAJOR | The forced planned total cannot report actual spawns and can be misread by consumers. | Separate planned, spawned, and not-launched totals; require full planned equality only for resolved closes, while error closes validate actual spawned counts plus explicit unlaunched accounting. |
| F4 | `arcana/subagent-strategy/scripts/append-dispatch.cjs:120,235`; `arcana/subagent-strategy/scripts/validate-readiness.cjs:108-113`; `arcana/subagent-strategy/development/test-append-dispatch.cjs:212-219`; `telemetry/agents/agent-pool.yaml:4,13,20-…` | `synthesizer` remains in the admitted role enum, no configured pool entry declares it, and a test expects readiness to block it. The pool calls `role_fit` a default suggestion that a dispatch may override, while readiness treats it as mandatory authorization. | MAJOR | Under the configured pool and readiness gate, no synthesizer dispatch can become ready, and operators receive contradictory rules about role overrides. | Choose one authority: if `role_fit` is admission law, update the pool contract and add a synthesizer identity or remove the role; if it is advisory, admit explicit overrides and document the rule. |
| F5 | `sessions/2026-08-28-1648-subagent-prompt-identity.md:21,56,58-59` | The session claims 39 targeted Orchestrate tests, but its touched-test inventory names three modules whose frozen reproduction yielded 34 tests. | MINOR | The recorded count of 39 is not reproducible from the session's stated module inventory. | Record the exact command and module list yielding 39, or correct the count to the reproducible 34 for the listed modules. |
| F6 | `sessions/2026-08-28-1648-subagent-prompt-identity.md:39-60`; `.agents/skills/orchestrate/generation-manifest.json` scoped worktree status | The session's Files touched list omits the manifest. Scoped Git status reports it modified, while `git diff --ignore-cr-at-eol --exit-code` is empty, establishing a line-ending-only worktree change rather than a content change. | MINOR | The touched-surface audit trail does not exactly describe the declared target and worktree state. | List the manifest as line-ending-only normalization or explicitly qualify it as a no-content worktree change. |

## Artifact verdicts

| artifact | KEEP or FIX | rationale |
|---|---|---|
| `arcana/subagent-strategy/SKILL.md` | FIX | Its exact-prompt law is not backed by end-to-end registration and execution checks. |
| `arcana/subagent-strategy/scripts/append-dispatch.cjs` | FIX | Same-version admission drift and closeout accounting defects survive. |
| `arcana/subagent-strategy/scripts/validate-readiness.cjs` | FIX | Pool `role_fit` is enforced contrary to its declared advisory semantics. |
| `arcana/subagent-strategy/development/test-append-dispatch.cjs` | FIX | It codifies a schema-live but readiness-inadmissible synthesizer role. |
| `runtime/orchestrate/scripts/native_dispatch_coordinator.py` and generated copy | FIX | They check topology and conditional identity, not exact registered agent and prompt binding. |
| `runtime/orchestrate/scripts/native_dispatch_driver.py` and generated copy | FIX | They reconstruct host text instead of emitting the confirmed prompt bytes. |
| `formulae/dispatch-spec/scripts/validate-dispatch.py` | FIX | It validates briefing integrity but not equivalence to registered agent prompt authority. |
| `runtime/orchestrate/SKILL.md` | FIX | Closeout prose inherits misleading `agents_spawned` semantics. |
| `telemetry/agents/agent-pool.yaml` | FIX | The stated advisory meaning of `role_fit` conflicts with readiness enforcement. |
| `sessions/2026-08-28-1648-subagent-prompt-identity.md` | FIX | Test provenance and touched-surface reporting require bounded corrections. |
| Remaining declared target artifacts | KEEP | No independent defect survived: strict prefix/body rejection, registrar/readiness composition, canonical/generated Python parity, fixture updates, profile/templates, concurrency behavior, and the targeted tests were coherent within their stated scope. |

## Change requests

1. Bind each registered agent's exact name and complete confirmed prompt to its executable action and host request; reject any direct or native extension or reconstruction.
2. Establish an explicit schema migration boundary for mandatory identity admission.
3. Correct partial and error close accounting so actual spawns are not reported as planned agents.
4. Reconcile synthesizer admission and the authoritative or advisory status of pool `role_fit`.
5. Record a reproducible Orchestrate test command and count in the session.
6. Correct or explicitly qualify the generation-manifest touched-file entry.

## Evidence boundary

The review checked the 21 target artifacts and 6 governing/comparator artifacts named by dispatch `2026-08-28-subagent-prompt-identity-review-v2`, plus scoped Git status and diff only for those targets. Reproductions were read-only or used temporary locations, and target hashes remained stable. F6's worktree claim was independently rechecked with scoped `git -c safe.directory=C:/Users/thiag/Arcanum status` and `git diff --ignore-cr-at-eol`; no target was modified. All unrelated dirty-worktree and long-path artifacts were excluded. The review demonstrates the predecessor direct-launch extension and the native absence of exact prompt binding; it does not claim an observed corrupt native host execution or an observed failure executing an already-ledgered historical row. No attacker transcript was persisted.
