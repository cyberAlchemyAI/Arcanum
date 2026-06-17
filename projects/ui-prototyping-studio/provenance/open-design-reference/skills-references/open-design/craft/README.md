---
tags: [craft, ui-prototyping-studio, open-design, references]
node_type: readme
is_session: false
layer: application
nature: reference
status: active
version: 0.2.0
last_updated: 2026-05-16
---

# Craft References

## What is this?

Brand-agnostic craft knowledge — small, dense rulebooks on individual dimensions of professional UI craft (typography, color, motion, accessibility, RTL, form validation, laws of UX, anti-AI-slop). Skills opt into the references they need; the daemon injects only the requested sections into the system prompt above the active skill body.

## Business Context

In Open Design, every UI artifact sits at the intersection of three axes: artifact shape (`skills/`), brand visual language (`design-systems/`), and universal craft rules (`craft/`). `DESIGN.md` tells the agent which colors and fonts a brand uses; `craft/` tells the agent the universal rules a competent designer applies on top — e.g. ALL CAPS always needs ≥0.06em tracking, regardless of the brand.

## Why it matters

Without a per-section opt-in, every skill pays the token cost of every craft rulebook. By keeping each dimension in its own file and letting skills declare `od.craft.requires: [typography, color, …]`, prompts stay narrow, the daemon stays forward-compatible (unknown slugs are silently ignored), and rules can be promoted into the linter (`apps/daemon/src/lint-artifact.ts`) as enforcement matures.

## 📁 Navigation

- **[typography.md](typography.md)**: Typography rules (tracking, scale, hierarchy).
- **[color.md](color.md)**: Color usage, contrast, accent discipline.
- **[anti-ai-slop.md](anti-ai-slop.md)**: P0 anti-patterns auto-checked by the daemon linter.
- **[state-coverage.md](state-coverage.md)**: Required state coverage for stateful UI (empty/loading/error/success).
- **[animation-discipline.md](animation-discipline.md)**: Motion rules — durations, easings, transition discipline.
- **[accessibility-baseline.md](accessibility-baseline.md)**: Baseline a11y for interactive UI (focus, labels, keyboard).
- **[rtl-and-bidi.md](rtl-and-bidi.md)**: Right-to-left and bidirectional text/layout rules.
- **[form-validation.md](form-validation.md)**: Form validation patterns and microcopy.
- **[laws-of-ux.md](laws-of-ux.md)**: Named cognitive limits (Hick's, Fitts's, Tesler's, Goal-Gradient, Peak-End, etc.) and the composition decisions they govern.

## How a Skill Opts In

Add an `od.craft.requires` array to the skill's front-matter. Only listed sections are injected.

```yaml
od:
  craft:
    requires: [typography, color, anti-ai-slop]
```

Allowed values match file names in this directory minus the `.md` extension. Unknown values are silently ignored (forward-compatible) — a skill can list a planned slug today and start benefiting the moment a matching `craft/<slug>.md` is vendored. The cost of a missed reference is a missing paragraph in the prompt, not a broken skill.

> Note: an earlier draft used `motion` as a placeholder. The shipped equivalent is `animation-discipline`.

## Enforcement Levels

- **Auto-checked.** Rules wired into `apps/daemon/src/lint-artifact.ts` — currently the P0 list in `anti-ai-slop.md` (Tailwind-indigo accent, two-stop hero gradients, emoji-as-icons, etc.). The linter reports findings back to the UI (P0/P1 badges) and to the agent (system reminder for self-correction). Artifact persistence is not hard-blocked on P0 hits.
- **Guidance.** Everything else. The agent reads the rules, reviewers apply them, the linter doesn't check them.

A purely behavioral craft file (state-coverage, animation-discipline) is guidance unless a specific rule is later promoted into `lint-artifact.ts`.

## When to Require Each File

| File | When to require |
| --- | --- |
| `typography.md` | Any skill that emits typed content (~all skills) |
| `color.md` | Any skill that emits styled output (~all skills) |
| `anti-ai-slop.md` | Marketing pages, landing pages, decks |
| `state-coverage.md` | Any skill with stateful UI (dashboards, mobile, forms, lists) |
| `animation-discipline.md` | Any skill that ships motion |
| `accessibility-baseline.md` | Any skill that ships interactive UI |
| `rtl-and-bidi.md` | Any skill that ships localized text or layout |
| `form-validation.md` | Any skill whose primary artifact contains an interactive form |
| `laws-of-ux.md` | Any skill whose composition decisions hit named cognitive limits |

**Partial-stateful skills.** A mostly-static skill that contains an embedded form, data table, or query surface should opt in. State-coverage rules apply to the stateful component, not the whole page.

## Attribution

Craft content is adapted from the MIT-licensed [refero_skill](https://github.com/referodesign/refero_skill) project (© Refero Design), with edits to fit Open Design's house style and to link back to OD's design tokens (`var(--accent)` etc.) instead of generic Tailwind hex values.
