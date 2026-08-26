# Evidence-Grounded Diagrams

Evidence-Grounded Diagrams is a Transmutation sigil for creating, reviewing,
and revising structural diagrams without letting their visual grammar claim
more than the available evidence supports.

## Problem It Solves

Nodes, arrows, order, loops, enclosure, grouping, and emphasis all communicate
claims. A diagram can therefore look clear while inventing sequence,
dependency, ownership, causality, completeness, or certainty.

This sigil converts a bounded evidence corpus into an auditable semantic model,
selects the representation from the supported relation, checks the rendered
result, and preserves every delivered diagram as a tagged and versioned bundle.

## Use When

- creating architecture, process, state, sequence, dependency, hierarchy,
  timeline, causal, containment, or typed-relation diagrams;
- deciding whether prose or a table is more faithful than a diagram;
- reviewing a diagram for unsupported visual claims;
- revising a reviewed diagram without losing its prior version;
- preparing a diagram for an official document or governed artifact.

## Do Not Use When

- the primary representation is a quantitative chart or statistical plot;
- the task is cartographic or geospatial;
- the user wants decorative illustration rather than structural explanation;
- no evidence corpus exists and unsupported relations cannot be marked honestly.

## Inputs

The sigil needs one reader question, intended resolution, permitted evidence
with stable locators, publication intent, desired source/renderer when known,
and an output root. Review and revise also need an exact artifact revision;
revise requires explicit correction authorization.

## Outputs

A successful emitted diagram is a versioned bundle:

```text
<output-root>/<diagram-id>/<revision>/
  diagram.request.yml
  diagram.<source>
  diagram.<render>              # when available
  diagram.model.yml
  diagram.meta.yml
  textual-equivalent.md
  validation.receipt.yml
```

The bundle keeps the immutable normalized request and permitted evidence set,
editable source, render when available, semantic claims,
evidence references, caption, rationale, tags, revision lineage, textual
equivalent, member digests, and validation receipt together.

A read-only review does not alter or silently extend that bundle. It produces a
separate review receipt bound to the exact inspected member digests, or to a
disclosed normalization and digest when the supplied target is inline source.

The machine contracts live under `schemas/`; `references/schema-guide.md`
defines what each contract and field family means, which values are identities
or states, and which receipts carry authority. Templates under `templates/`
are valid starting instances, not alternative contracts.

## Lifecycle

```text
working -> draft -> validated -> published
                         \-> rejected
any revision -> superseded by a preserved newer revision
published -> separately promoted when governance permits
```

Internal scratch may remain ephemeral. A diagram becomes emitted when it is
delivered to a user or inserted into another artifact; persistence must complete
before that handoff. Saving, publishing, and promotion are separate decisions.

## Why This Is a Transmutation

The capability applies bounded judgment to an evidence corpus and transforms it
into a faithful representation. It uses deterministic schemas and validators,
but its primary act is evidence-constrained synthesis rather than a fixed rule
check or recursive orchestration.

## Canonical and Runtime Surfaces

This folder is the canonical source. `.agents/skills/`, `.claude/skills/`, and
personal Codex skill folders are generated runtime surfaces and must not be
edited as owners.

Before using the packaged scripts in a fresh runtime, run:

```text
python scripts/preflight_runtime.py
python -m pip install -r requirements.txt  # only when preflight blocks
```

The selective Arcanum sync command additionally requires Bash, Git, and
`rsync`; those are installer prerequisites, not Python package dependencies.

Generate or update one runtime package with:

```text
tools/sync-generated-skill-package.sh --target <repo> --sigil evidence-grounded-diagrams --apply
```

The experiment harness and independent promotion gates have passed. Current
lifecycle evidence is recorded in `development/VALIDATION.md`; registry,
download, and runtime surfaces remain generated derivatives after promotion.
