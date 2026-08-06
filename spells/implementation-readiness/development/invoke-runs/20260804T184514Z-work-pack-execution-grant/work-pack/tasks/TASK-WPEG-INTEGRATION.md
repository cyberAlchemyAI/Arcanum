# TASK-WPEG-INTEGRATION — Causal proof and package parity

## Objective

Prove the repaired behavior end to end and expose it consistently through
canonical and generated runtime packages.

## SWU-WPEG-007 — Prove direct-intent execution

### Primary behavior

Run public-safe causal fixtures from one direct Work Pack execution intent to
frontier completion or the first real blocker.

### Write scope

- `arcanum/spells/implementation-readiness/development/integration/`

### Required cases

1. Plan-once selection/material/admission with zero pre-execution Refresh.
2. Real semantic drift automatically routes to Refresh and rejoins.
3. Mechanical internal owner/tool choices produce no authorization prompt.
4. Two-unit finite frontier uses two fresh Task Sessions.
5. Product choice stops.
6. Scope expansion stops.
7. Destructive/external/authority/promotion/deployment action stops.
8. Failed critical validation stops.
9. Legacy ad hoc Router path keeps its current gate.
10. Fast guard read/phase budget passes.
11. Undeclared internal route and target/write expansion block.
12. Binding replay after Work Pack/frontier change blocks.
13. Repeated owner/session fingerprint blocks without re-entry.
14. One typed repairable owner condition retries the unchanged route without a
    prompt; a second retry stops before another dispatch.

### Acceptance

- One invocation identity is bound to the Work Pack.
- `authorization_prompt_count` equals zero for declared internal routes.
- Owner and Task Session receipt chains are complete and distinct.
- No stop-case fixture reaches its protected effect.
- Existing plan-once, Router, Task Session, and chain suites pass.

### Verification

```bash
python3 arcanum/spells/implementation-readiness/development/integration/test_work_pack_execution.py
python3 arcanum/spells/work-pack-readiness-audit/development/test_plan_once_end_to_end.py
bash arcanum/arcana/continuation-router/development/run-validation-fixtures.sh
bash arcanum/arcana/task-session/development/run-validation-fixtures.sh
bash arcanum/spells/task-session-until-blocker/development/run-validation-fixtures.sh
```

### Split analysis

One end-to-end causal acceptance boundary. Unit tests alone cannot prove the
handoff chain or absence of repeated authorization prompts.

## SWU-WPEG-008 — Sync packages and observability

### Primary behavior

Generate consistent Codex/Claude packages and document/observe the new route
after canonical validation passes.

### Write scope

- generated packages for only the five changed canonical capabilities
- package-local documentation and observability fixtures

### Ordered rules

1. Sync from canonical source using the selective generated-skill tool.
2. Never edit generated skill bytes as the source of truth.
3. Validate canonical/generated parity.
4. Record entry states, automatic/stop decision counts, route hops, joins,
   fast-guard phase count, authorization prompt count, and stop reason.
5. Keep telemetry non-authoritative.

### Acceptance

- Canonical and both generated runtime packages match.
- Documentation says internal Work-Pack routes require no per-hop
  authorization.
- Ad hoc and protected-effect boundaries remain explicit.
- Full scoped validation and `git diff --check` pass.

### Verification

```bash
arcanum/tools/sync-generated-skill-package.sh --target . --spell implementation-readiness --apply
arcanum/tools/sync-generated-skill-package.sh --target . --spell invoke --apply
arcanum/tools/sync-generated-skill-package.sh --target . --sigil continuation-router --apply
arcanum/tools/sync-generated-skill-package.sh --target . --sigil task-session --apply
arcanum/tools/sync-generated-skill-package.sh --target . --spell task-session-until-blocker --apply
git diff --check -- arcanum/spells/implementation-readiness arcanum/spells/invoke arcanum/arcana/continuation-router arcanum/arcana/task-session arcanum/spells/task-session-until-blocker .agents/skills .claude/skills
```

### Split analysis

Generated parity and documentation are one post-validation packaging boundary;
they must not be mixed into behavior implementation.
