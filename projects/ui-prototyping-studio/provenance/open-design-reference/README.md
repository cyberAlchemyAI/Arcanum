---
tags: [ui-prototyping-studio, inventory, provenance, vendored]
node_type: readme
is_session: false
layer: application
nature: reference
status: active
version: 0.2.0
last_updated: 2026-05-16
---

# UI Prototyping Studio Inventory

## What is this?

Feature-local, reference-only snapshots of external assets (VoltAgent design-md, Open Design skills and craft references) used during the UI Prototyping Studio specification process. Each imported tree is paired with provenance metadata recording source repo, commit SHA, and retrieval date.

## Business Context

The UI Prototyping Studio feature borrows vocabulary and structure from upstream OSS projects (VoltAgent's design-md corpus, Open Design's skill/craft contracts). Rather than depending on those repos at build time, we vendor snapshots at known commits so the feature spec remains reproducible and auditable even if upstream changes or disappears.

## Why it matters

Reference-only snapshots make the provenance of every borrowed idea explicit and decouple the feature spec from upstream churn. They also create a clear update protocol (re-clone, replace, record commit, re-run link checks) so refreshes are deliberate, not accidental.

## 📁 Navigation

- **`voltagent-design-md/`**: Snapshot of VoltAgent's `design-md` corpus (70 brand folders) plus `PROVENANCE.md`.
- **`skills-references/`**: Snapshot of Open Design skills/craft contracts (`open-design/`) plus `INVENTORY.md` and `PROVENANCE.md`.

## Imported Assets

### VoltAgent design-md
- Source: https://github.com/VoltAgent/awesome-design-md, path `design-md`
- Retrieved: `2026-05-07T20:02:41Z` at commit `da068674dbe2f7073059d0c38c0ac60aa83c1660`
- Scope: full `design-md` folder with top-level folder names preserved (70 brand folders)

### Open Design skills references
- Source: https://github.com/nexu-io/open-design
- Retrieved: `2026-05-07T21:49:26Z` at commit `2bb029cb5870f73cbe1aa357b4cc3dd7190bdd15`
- Imported paths (relative to repo root):
  - `docs/skills-protocol.md`, `docs/modes.md`, `craft/*.md`
  - Folder snapshots for `skills/web-prototype/`, `skills/web-prototype-taste-editorial/`, `skills/web-prototype-taste-brutalist/`, `skills/web-prototype-taste-soft/`, `skills/critique/`, `skills/tweaks/`, `skills/wireframe-sketch/`, `skills/design-brief/`, `skills/dashboard/`, `skills/docs-page/`, `skills/mobile-app/`, `skills/saas-landing/`, `skills/live-dashboard/`, `skills/live-artifact/`
- Imported file count: 58

## Update Guidance

1. Re-clone the upstream repositories and record exact commit SHAs.
2. Replace imported snapshots in this inventory with the refreshed source files.
3. Update both provenance files and this index with new retrieval metadata.
4. Re-run markdown link checks for changed markdown files.

## Usage Boundary

Assets in this inventory are reference-only. They do not create runtime, build-time, or package dependency requirements for this feature.
