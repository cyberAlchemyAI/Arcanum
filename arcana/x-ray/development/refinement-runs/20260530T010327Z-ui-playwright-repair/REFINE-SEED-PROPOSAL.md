# Refine Seed Proposal: x-ray UI Repair

## Target

`arcana/x-ray/development/example-outputs/XRAY-COMPONENT-001.html`

## Problem

The generated x-ray page passed structural validation but failed browser usability. The lane sections were absolutely stacked in one panel, producing visual overlap when all layers were enabled. Evidence content was separated from the stack with a fixed `590px` margin, which made layout correctness depend on one hard-coded height. Mobile rendering also made SVG labels too small to read.

## Desired Shape

- Layers remain selectable by checkbox.
- Enabled layers render as readable, non-overlapping sections.
- Desktop preserves the SVG visual explanation.
- Mobile gets readable lane summaries instead of scaled-down, illegible diagrams.
- Evidence content follows normal document flow.

## Completion Signal

Playwright screenshots show the desktop and mobile page without overlapping layers or clipped page content, and existing x-ray validators still pass.

