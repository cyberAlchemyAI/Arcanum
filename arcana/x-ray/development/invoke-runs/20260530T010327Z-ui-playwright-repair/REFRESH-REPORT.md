# Invoke Refresh Report: x-ray UI Repair

## Target

`arcana/x-ray/development/example-outputs/XRAY-COMPONENT-001.html`

## Refresh Signal

The existing generated HTML was structurally valid but visually broken in a browser. Playwright screenshots showed overlapping layers and fragile spacing caused by absolute positioning and a hard-coded evidence offset.

## Applied Changes

- Replaced the absolute overlay stack with a normal grid of lane panels.
- Changed unchecked layer behavior from faded overlays to `display: none`, making the controls act like real layer selectors.
- Removed the fixed `590px` evidence margin so evidence follows the layer stack in document flow.
- Added responsive sizing and mobile-specific readable summaries for diagram-heavy lanes while keeping desktop SVGs.
- Added stable box sizing, heading rhythm, control sizing, and evidence card spacing.

## Evidence

- Before desktop: `output/playwright/xray-component-001-before-desktop.png`
- Before mobile: `output/playwright/xray-component-001-before-mobile.png`
- After desktop: `output/playwright/xray-component-001-after-desktop.png`
- After mobile: `output/playwright/xray-component-001-after-mobile.png`

## Validator Impact

Required validators still pass after refresh:

```bash
python3 arcana/x-ray/scripts/validate-xray-example.py --lanes arcana/x-ray/development/example-outputs/XRAY-COMPONENT-001.lanes.json --html arcana/x-ray/development/example-outputs/XRAY-COMPONENT-001.html
python3 arcana/x-ray/scripts/validate-xray-library.py
tools/validate-artifact-constitution.sh
```

## Follow-Up Candidate

Add a visual QA gate for x-ray generated examples. The current structural validator cannot detect overlapping layers, hard-coded spacers, or mobile legibility failure.

