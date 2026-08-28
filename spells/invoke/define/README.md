# Define

Projects often begin using important words before anyone has checked what each
one refers to, where it applies, or whether the repository already defines it.
One team may use *account* for a person while another uses it for a billing
relationship. A feature may introduce a new name for something the repository
already defines, or quietly use an established definition beyond the area where
it applies.

Define resolves these problems before Design begins. It decides which concepts
and terms the project will use, what each one refers to, who owns the existing
definition, where it applies, and how it relates to the rest of the system. For
each concept, Define either reuses an existing definition, creates a narrower
specialization, or proposes a new definition limited to the project's scope.

## Why Define comes before Design

Design turns project intent into structures, responsibilities, interfaces, and
interactions. Those decisions become unstable when their basic terms are
unclear. A design for an *account*, for example, may be internally consistent
and still be wrong if the surrounding system uses *account* for a different
thing.

Define establishes a common starting point. It does not try to design the
system. It gives later work a checked set of definitions so that people and
tools can refer to the same things, preserve existing ownership, and notice
conflicts before they become embedded in architecture or code.

## What Define examines

Define starts with the feature or project goal, then looks for the material
that could constrain how its terms are used:

- definitions and aliases already present in the repository;
- relevant designs and architecture documents;
- the recorded owner and permitted scope of an existing definition;
- relationships between the requested concepts and existing concepts;
- registries that list those concepts; and
- systems, documents, or tools that consume them.

This search matters because a definition is more than a sentence. Its owner,
scope, relationships, and consumers determine whether the project can reuse it
safely or needs a more specific candidate.

## Three possible decisions

Define makes one of three decisions for every concept the project needs:

| Decision | What it means |
| --- | --- |
| **Reuse** | An existing definition already describes the required concept. The project refers to it without copying or changing it. |
| **Specialize** | An existing definition is correct, but the project needs a narrower version for a clearly limited scope. The broader definition remains unchanged. |
| **Define new** | No suitable definition exists. The project proposes a new candidate within its own scope. |

Creating something new is not the default. Reusing a suitable definition keeps
different parts of the system aligned. Specialization is appropriate only when
the project can state exactly how its use is narrower.

## From project goal to checked definitions

The process can be retold as one short sequence:

```text
Project goal
    ↓
Find related definitions, designs, owners, registries, and consumers
    ↓
Choose reuse, specialize, or define new for each required concept
    ↓
Create one structured candidate definition set
    ↓
Generate readable views from that set
    ↓
Check the candidate again against the current repository
```

The final check is independent of the authoring step. This makes changes in the
repository visible instead of assuming that evidence collected earlier is still
current.

## What Define produces

The principal output is one candidate definition set with two human-readable
views:

| File | Purpose |
| --- | --- |
| `DEFINITIONS.json` | The complete structured candidate used by tools and later workflows. |
| `DEFINITIONS.md` | The same definitions presented for detailed human reading. |
| `GLOSSARY.md` | A shorter reference for people working on the project. |

`DEFINITIONS.json` is the source for the generated views. The Markdown files do
not carry separate rules that can drift away from it. Supporting records also
identify the project material that was examined and show whether the candidate
could be reproduced consistently.

## A small example

Imagine a team defining terms for a returns feature:

- The repository already defines **customer** exactly as the feature needs it,
  so the feature reuses that definition.
- The repository defines a general **case**, while a **return case** has the
  same foundation but is limited to returned goods and their required steps.
  The feature specializes the existing definition without changing it.
- The feature needs **inspection window**, a period unique to this returns
  process, and no suitable definition exists. It proposes a new definition
  limited to the feature.

The result is not three new definitions. It is one reuse, one specialization,
and one new candidate, each with a reason and a visible boundary.

## When Define must check again

A previously checked candidate may no longer be current when:

- an existing definition, alias, owner, or permitted scope changes;
- a related concept or relationship is added, removed, or modified;
- a registry starts or stops listing a concept;
- a system, document, or tool starts or stops consuming it;
- the required structure of the definition files changes; or
- a generated Markdown view no longer matches `DEFINITIONS.json`.

These cases are called **definition drift** because they may change what a term
refers to, how the project may use it, or who depends on it. A changed file does
not always mean the definition changed, but uncertainty must be checked rather
than guessed away.

## What Define does not approve

A completed Define candidate does not automatically:

- make a definition canonical;
- replace or modify an existing definition;
- transfer ownership;
- approve a design or architecture;
- authorize implementation; or
- publish or deploy anything.

Define prepares checked candidate material for the next responsible process.
Any later adoption, promotion, design, or implementation keeps its own decision
and approval boundary.

## Continue from here

- To inspect the machine workflow without creating files, run
  `tools/arcanum invoke define describe` from the repository root.
- To run Define as an agent or operator, follow the
  [Define authoring guide](../define-authoring-guide.md).
- To inspect the formal mode rules and evidence requirements, read the
  [Define contract](../define.md).
