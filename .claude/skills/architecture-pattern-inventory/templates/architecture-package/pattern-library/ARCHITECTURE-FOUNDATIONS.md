# Architecture Foundations

Use this document for the stable architecture baseline: principles, layers, and evidence boundaries.

## Principles

1. Evidence-first: describe observed architecture separately from recommended architecture.
2. Selective context: keep the package navigable by linking to focused files.
3. Dependency clarity: record allowed and forbidden dependency directions.
4. Boundary ownership: identify which layer or module owns each decision.
5. Verification alignment: connect architecture rules to tests and observability.

## Layer Model

```text
+------------------------------+
| {Outer Layer}                |
+------------------------------+
| {Middle Layer}               |
+------------------------------+
| {Inner Layer}                |
+------------------------------+
```

## Layer Snapshot

| Layer | Owns | Must Not Depend On | Evidence |
| ----- | ---- | ------------------ | -------- |
| `{layer}` | `{responsibilities}` | `{forbidden dependencies}` | `{paths or observations}` |

## Observed vs Recommended

| Topic | Observed | Recommended | Status |
| ----- | -------- | ----------- | ------ |
| `{topic}` | `{current state}` | `{target state}` | `{current | gap | proposed}` |

## Next References

- Dependency constraints: `DEPENDENCY-RULES.md`
- Testing obligations: `TESTING-ALIGNMENT.md`
- Observability obligations: `OBSERVABILITY-ALIGNMENT.md`
