# Architecture Pattern Library

Purpose: provide composable implementation patterns so agents and reviewers can load the minimum context needed for a task.

## Source Evidence

This package is derived from observed repository evidence:

- source structure,
- module boundaries,
- dependency direction,
- tests,
- runtime interfaces,
- existing docs,
- repeated implementation motifs.

## Context Packs

Use one or more packs instead of loading the full architecture package.

| Pack | Use When | Include Concept Cards | Include Relationship Cards |
| ---- | -------- | --------------------- | -------------------------- |
| `{pack-id}` | `{task type}` | `{concept cards}` | `{relationship cards}` |

## Concept Pattern Cards

| Concept | Layer | Pattern Contract | Evidence | Detail Card |
| ------- | ----- | ---------------- | -------- | ----------- |
| `{concept}` | `{layer}` | `{contract}` | `{path or observation}` | `{link}` |

## Relationship Pattern Cards

| Relationship | From -> To | Contract | Evidence | Detail Card |
| ------------ | ---------- | -------- | -------- | ----------- |
| `{relationship}` | `{source} -> {target}` | `{contract}` | `{path or observation}` | `{link}` |

## Implementation Slice Recipe

For any task, build context in this order:

1. Select concept cards relevant to the task.
2. Select relationship cards connecting those concepts.
3. Read dependency rules for affected layers.
4. Derive implementation and test obligations from selected cards.
5. Verify that the resulting change preserves the observed architecture or explicitly updates this package.

## Coverage Checklist

- [ ] Layers documented.
- [ ] Dependency rules documented.
- [ ] Concept cards created for recurring patterns.
- [ ] Relationship cards created for recurring interactions.
- [ ] Testing alignment documented.
- [ ] Observability alignment documented.
- [ ] Gaps and unknowns recorded.
