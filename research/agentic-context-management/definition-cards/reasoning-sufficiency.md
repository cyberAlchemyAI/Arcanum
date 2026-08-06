# Definition Card: Reasoning Sufficiency

Status: `local-research-only`

## Source Meaning

The assembled context contains all premises and bridge evidence needed for the
reasoning task, not merely a document judged relevant to the query.

Source kind: `primary-source`

Evidence: paper §3.3

## Structural Shape

```text
extract -> retrieve -> assemble -> reason
   |          |          |
   + each stage may cap answer quality
```

## Operator Reading

Ask whether the evidence closes the claim, not whether a search result looks
similar.

## Use Carefully

- Build multi-premise fixtures with explicit gold evidence sets.
- Distinguish missing bridge evidence from model reasoning failure.
- Record irrelevant context because distraction can also lower sufficiency.

## Misuse Warning

- The paper's inequality is conceptual. It does not define a directly measurable
  scalar called `reasoning sufficiency`.

## Promotion Boundary

`local-only`
