# Learning Residue — `veritasium` preset, run: `skill-anatomy`

- Date: 2026-06-23
- Preset: `veritasium` (first proof run)
- Transport: `explanatory_deep_dive`
- Objective: add `refine-skill-xray.html` to the CyberAlchemy docs as a deep-dive mini-course that
  teaches "a skill is a layered stack of nudges" and closes the loop to the method.
- Artifacts produced:
  - `arcanum/docs/skill-anatomy.html` — the surface (first-class docs page).
  - `arcanum/docs/refine-skill-xray.html` — the x-ray copied into the public site as the instrument.
  - nav link "Anatomy" added to all docs pages + a homepage explore card.

## Durable lessons (reusable)

- The existing x-ray already *is* the show-don't-tell instrument the `veritasium` preset wants. The
  surface's job was not to re-explain the x-ray but to **frame it**: name the wrong model, break it,
  hand over the instrument, walk the layers in the x-ray's own band vocabulary, then zoom out. The
  preset's misconception→turn→instrument→walk→boundary→zoom-out arc mapped cleanly onto an embed.
- The x-ray's **quote=source vs mechanism=inference** boundary is a native fit for the preset's
  "honest boundary" technique and for CyberAlchemy's **claim ≤ proof** — reuse this pairing whenever
  an x-ray is the instrument.
- The docs design system (tokens + `.topbar/.subnav/.hero/.section/.panel/.footer`) is stable and
  copy-reusable; new surfaces should inline the same `:root` tokens and chrome rather than invent.

## Observed (not yet canonical)

- "Anatomy of a Skill" worked as the title because dissecting something familiar is the Veritasium
  move; consider an `anatomy_of_X` title pattern for future explanatory surfaces — candidate, not law.

## Open / deferred

- Visual + interaction verification in a real browser (iframe height, mobile nav, tour controls) is
  not yet run — recommend a Playwright/`run` pass before treating the page as shipped.
- Not committed/pushed: changes live in the **public `arcanum`** submodule; submodule-first
  commit + push, then parent gitlink bump, is required when the operator chooses to publish.
