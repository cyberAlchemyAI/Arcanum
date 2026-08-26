---
name: evidence-grounded-diagrams
description: Create Mermaid structural diagrams with concise business metadata, show them for user review, and save the confirmed source under output/diagrams. Use for process flows, state transitions, sequences, dependency maps, hierarchies, containment maps, timelines, causal maps, and relationship maps.
---

# Evidence-Grounded Diagrams

Create the smallest Mermaid diagram that answers one reader question. Keep the
editable source, a PNG preview, and concise metadata; do not create governed
bundles, receipts, manifests, indexes, hashes, telemetry, or publication records.

## Workflow

1. Identify the reader question and the business process or activity involved.
2. Choose the diagram kind from the list below.
3. Read `schemas/diagram.schema.json`, then draft `diagram.mmd` and fill
   `diagram.yml` from `templates/diagram.yml` according to its field and enum
   descriptions.
4. Show the Mermaid diagram to the user when review is requested or useful.
5. Apply requested corrections.
6. Save with `scripts/save_diagram.py`.

Use `status: draft` before confirmation and `status: confirmed` when the user
has approved the content. Never imply that confirmation proves business truth.

## Storage

Save every diagram below the workspace root:

```text
output/diagrams/YYYYMMDD-short-name/
  diagram.yml
  diagram.mmd
  diagram.png
```

The directory name and metadata `id` must match. Prefix the ID with the current
date in `YYYYMMDD` form and use lowercase kebab-case for the remaining name.
The prefix must match `created_at`.

Run from any directory by passing the workspace explicitly:

```text
python <skill>/scripts/save_diagram.py <draft>/diagram.yml <draft>/diagram.mmd --workspace-root <workspace>
```

The script validates the metadata, verifies non-empty UTF-8 Mermaid source,
renders `diagram.png` with the pinned Mermaid CLI adapter, refuses an existing
destination, and saves all three files together. It requires `npx`; do not
choose a different storage root unless the user explicitly requests it.

## Metadata

Keep only:

- identity: `schema_version`, `id`, `title`, and `created_at`;
- diagram: `kind` and the canonical `diagram.mmd` and `diagram.png` names;
- business: what it represents, process name and description, applicable
  contexts, and the reader question;
- scope: material inclusions and exclusions;
- lifecycle: `draft` or `confirmed`;
- optional evidence pointers under `sources`.

Treat `schemas/diagram.schema.json` as the field reference. Its `description`,
`examples`, and enum option descriptions define how to fill each value; do not
invent additional fields.

Keep arrows, ordering, containment, and causality no stronger than the available
information. If a relation is uncertain, label that uncertainty in the Mermaid
source or explain it to the user.
