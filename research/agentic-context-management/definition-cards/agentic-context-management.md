# Definition Card: Agentic Context Management

Status: `local-research-only`

## Source Meaning

The full discipline of deciding what an agent holds in context, when, for how
long, and at what cost across acquisition, use, compaction, and retirement.

Source kind: `primary-source`

Evidence: paper §2

## Structural Shape

```text
context purpose
  -> architect
  -> ingest
  -> scope
  -> anticipate
  -> compact/consolidate
  -> observe and repeat
```

## Operator Reading

Treat each primitive as a question whose answer needs an owner, policy, and
receipt. Do not require a one-service-per-primitive runtime mapping.

## Use Carefully

- Use the lifecycle to find missing decisions.
- Preserve the difference between working context, durable memory, and global
  knowledge.
- Tie every scope expansion to authorization.

## Misuse Warning

- The paper proposes a category and reference implementation; it does not prove
  this decomposition exhaustive for every system.

## Promotion Boundary

`local-only`
