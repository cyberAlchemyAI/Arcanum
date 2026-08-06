# TASK-PEP-INTEGRATION: Cross-capability proof and packaging

## SWU-PEP-006

Primary behavior: prove and package the full execution-entry route.

### Required canaries

1. plan-once path: one semantic audit, explicit selection, material production, live admission, zero expected pre-execution Refresh;
2. unmet unauthorized path: fast block before Context Builder with exact route;
3. authorized legacy/drift path: one owner hop, joined receipt, recheck, one context entry;
4. stale/expanded target path: block before mutation;
5. ambiguity path: block without score-based selection;
6. replay path: second dispatch rejected;
7. existing strict-profile and continuation fixtures unchanged.

### Packaging

After canonical validation, selectively regenerate the affected Codex and Claude packages using the repository sync tool. Compare canonical/generated digests and scan public outputs for forbidden private identifiers.

### Acceptance

- all acceptance-critical canaries and regressions pass;
- `git diff --check` passes on the scoped surfaces;
- generated parity passes;
- no private consuming-project strings appear;
- implementation receipt distinguishes local validation from promotion/release evidence.

### Validation

```bash
bash arcanum/arcana/task-session/development/pre-execution-prerequisite-fast-path/run-validation-fixtures.sh
bash arcanum/arcana/continuation-router/development/run-validation-fixtures.sh
python3 arcanum/spells/work-pack-readiness-audit/development/test_plan_once_end_to_end.py
python3 arcanum/arcana/task-session/development/test_plan_once_admission.py
python3 arcanum/arcana/task-session/development/test_plan_once_governance.py
git -C arcanum diff --check -- arcana/task-session arcana/continuation-router spells/invoke spells/implementation-readiness spells/work-pack-readiness-audit
```
