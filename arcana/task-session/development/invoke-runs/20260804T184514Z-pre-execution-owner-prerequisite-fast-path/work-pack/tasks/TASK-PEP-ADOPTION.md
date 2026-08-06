# TASK-PEP-ADOPTION: Plan and entrypoint consistency

## SWU-PEP-005

Primary behavior: make the authored next route agree with prerequisite state.

### Inputs

- passing Task Session/Router prerequisite receipts;
- existing Work Pack Readiness Audit `selected-unit-at-task-session` implementation and canary;
- Invoke Plan and work-pack template contracts;
- Implementation Readiness composition.

### Ordered rules

1. Add execution-entry output requirements to Invoke Plan and the work-pack template.
2. Prefer plan-once for new work whose material is intentionally selected/produced at runtime.
3. When a genuine prerequisite remains, name it as the immediate route; do not claim Task Session is immediate.
4. Make Implementation Readiness carry exact authorization only when the current direct user request or durable approval binds the declared route and scope.
5. Keep bare unauthorized Task Session fail-closed and fast.
6. Preserve legacy full-frontier behavior.

### Decision boundary

This SWU may recommend but must not silently make plan-once the global default or convert generic execution intent into ambient apply authority. Those changes require explicit lifecycle-owner evidence.

### Validation

```bash
python3 arcanum/spells/work-pack-readiness-audit/development/test_plan_once_end_to_end.py
arcanum/spells/invoke/development/run-validation-fixtures.sh
```
