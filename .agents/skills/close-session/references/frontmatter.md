---
description: Minimal, self-contained guide for authoring frontmatter and typed Connections in session nodes.
---

# Frontmatter & Connections

This guide is the compact authoring reference for governed session Markdown.
The creating agent chooses and writes metadata and connections; hooks and tools
must not invent values or targets.

## Structural obligations

Every session node created by `close-session` must carry:

1. a YAML frontmatter block (`---` ... `---`); and
2. a `## Connections` section containing meaningful typed edges, or a one-line
   explanation when no real connection is known.

Never fabricate a connection target merely to satisfy the structural
obligation.

## Frontmatter schema

```yaml
---
tags: [topical labels only]
artifact_kind: session
layer: project | domain | capability | feature | task | others
version: 0.x.x
created_at: YYYY-MM-DDTHH:MM:SS±HH:MM
updated_at: YYYY-MM-DDTHH:MM:SS±HH:MM
expires: YYYY-MM-DD
decisions_made: true | false
contradictions_found: true | false
specs_updated: [paths or []]
promoted_candidates: [nodes or []]
expected_importance: 0-10
importance_rationale: "meaningful sentence"
---
```

### `layer`: primary contextual altitude

`layer` answers one question:

> At which contextual altitude does this artifact primarily operate?

Choose exactly one primary layer:

| `layer` | Meaning |
|---|---|
| `project` | Shapes the project as a whole: its mission, system-wide policy, or overall direction. |
| `domain` | Shapes one bounded problem or knowledge domain within the project. |
| `capability` | Shapes a reusable ability across one or more features. |
| `feature` | Shapes a user- or system-visible outcome delivered through related work. |
| `task` | Shapes one bounded unit of execution or its immediate result. |
| `others` | Fallback after none of the listed altitudes fits; explain the altitude in the document. |

Use the highest level whose decisions the document directly shapes, not every
level it may eventually affect. Broader or narrower relationships belong in
`## Connections`.

Topic, concern, and origin are different dimensions. Values such as `ontology`
and `architecture` describe subject matter and belong in tags; `external`
describes origin and is not a layer.

### Other fields

- `tags` describe subject matter only, never document role or maturity. Use
  concrete topical labels.
- `artifact_kind` is always `session` for this workflow.
- `version`, `created_at`, `updated_at`, and `expires` provide lifecycle
  metadata.
- `expires` is the calendar date 60 days after `created_at` unless repository
  policy explicitly replaces that retention rule.

### Lifecycle timestamps

For a newly created session, include both `created_at` and `updated_at`. Produce
them as RFC 3339 timestamps in the `America/Sao_Paulo` civil timezone, with the
UTC offset effective at that instant written explicitly, for example
`2026-07-27T15:26:46-03:00`.

- Set `created_at` when the artifact is first durably created and never change
  it.
- Set `updated_at` to the time of the latest durable content or applicable
  metadata revision.
- Reading, indexing, validating, or copying an unchanged artifact must not
  advance `updated_at`.

## `## Connections`: typed edges

```markdown
## Connections

| Document | Type | Description |
|----------|------|-------------|
| [other document](path) | `derives-from` | One-line explanation of the actual relationship. |
```

Every row needs a real target, a type, and a description explaining why the edge
exists. When the target is governed and the relationship has a meaningful
inverse, add the inverse row there only if that target is in scope for the same
change.

The following edge types are the starting vocabulary:

| Type (A → B) | Meaning |
|---|---|
| `resolves` | A solves the problem B states. |
| `derives-from` | A was built upon or generated from B. |
| `grounds` | A is the foundation B rests on; inverse of `derives-from`. |
| `implements` | A concretely realizes specification or constitution B. |
| `validates` | A provides evidence that supports B. |
| `promotes-from` | A ratifies or formalizes the thesis stated in B. |
| `exemplifies` | A is a concrete instance of abstract B. |
| `refines` | A adds detail or precision to B while retaining its subject. |
| `contextualizes` | A supplies useful background for B without creating a functional dependency. |
| `depends-on` | A cannot function or remain valid without B. |
| `is-part-of` | A belongs structurally to the real context represented by B. |
| `contains` | A structurally contains B; inverse of `is-part-of`. |
| `alternative-to` | A is a competing or discarded alternative to B. |
| `contradicts` | A is materially in tension with or refutes B. |
| `supersedes` | A directly succeeds B and makes it obsolete. |
| `deprecates` | A partially or informally replaces B. |
| `other` | A real relationship exists, but no listed type fits; describe the missing semantics. |

`is-part-of` and `contains` require real context targets. Do not infer either
edge only from directory structure or from files read, mentioned, or touched.

If no real connection is known, keep the section and state that explicitly
instead of creating a placeholder edge.
