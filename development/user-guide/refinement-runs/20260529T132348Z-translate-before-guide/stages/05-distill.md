# Stage 05: Distill

Status: `pass`

## Selected Coherent Unit

`Translate` as a separate sigil candidate.

## Why This Is Smaller Than Guide

Guide has many possible jobs:

- explain architecture,
- research missing context,
- dispatch subagents,
- sequence sections,
- adapt to user state,
- validate understanding,
- produce a walkthrough.

Translate has one core job:

```text
map meaning between vocabularies/domains while preserving target truth
```

## Minimal Translate Contract

Input:

- target concept or artifact,
- source domain,
- target domain,
- user vocabulary preferences,
- requested style,
- optional glossary/context handles.

Output:

- translated explanation,
- term map,
- analogy/metaphor map,
- mapping limits,
- target-domain definition,
- receipt of what was attempted.

## Recomposition

Translate recomposes into Guide as a callable step:

```text
Guide route
  -> inspect / research / decompose
  -> call Translate for vocabulary bridge
  -> call User ledger for preferences and receipts
  -> synthesize guided explanation
```
