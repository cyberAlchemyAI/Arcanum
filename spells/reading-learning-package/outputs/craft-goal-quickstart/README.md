# Craft + Goal — Quickstart Learning Package

A beginner-friendly learning package that teaches **Craft** (a project's durable
memory) and the **Goal** loop (a fail-closed autopilot), how they compose into an
easy automated pipeline, and how a **controller agent** (e.g. a Hermes-class model
or an OpenClaw agent runtime) can conduct Claude Code / Codex / itself.

Composed with **Whisper** using the **`learning_distill`** preset
(Feynman / Veritasium voice — see
`../../presets/learning_distill/`).

## Read it

| File | What it is |
| --- | --- |
| **`learning-package.pdf`** | The downloadable guide — share this. (5 pp) |
| **`learning-package.html`** | Print-ready web version, same content. |
| `manuscript.md` | The source text (Markdown). |

## Install it (self-contained — no Arcanum needed)

| File | What it is |
| --- | --- |
| **`INSTALL.md`** | Focused install guide for **craft + goal only**, with the honest dependency list. |
| **`install.sh`** | One-line installer: `./install.sh /path/to/your/project`. |
| **`tools/craft/`** | Snapshot of the Craft skill (model-operated, zero deps). |
| **`tools/goal/`** | Snapshot of the Goal skill (Python 3 stdlib runtime; `jsonschema` only for validation). |

**Verified self-contained:** the bundled `tools/` were installed into a bare
project with no Arcanum present; `goal` ran on the Python 3 stdlib and its
validation printed `goal-fixtures-pass`. The only third-party import in the whole
kit is `jsonschema`, needed only to run Goal's self-check.

## How it was built (the trace)

| File | Role |
| --- | --- |
| `text-intent-substrate.yaml` | Whisper substrate: objective + the three SCU cores. |
| `composition-plan.md` | Section plan, voice rules, validation checklist. |
| `source-trace.md` | Every mechanism claim → its source skill file. |
| `validation.md` | Pass/flag gates and honesty flags. |
| `build-html.py` | Renders `manuscript.md` into the spell's HTML template. |

## Rebuild

```bash
# HTML
python3 arcanum/spells/reading-learning-package/outputs/craft-goal-quickstart/build-html.py

# Downloadable PDF
python3 ~/.claude/tools/pdfkit/pdfkit.py build \
  arcanum/spells/reading-learning-package/outputs/craft-goal-quickstart/manuscript.md \
  --out arcanum/spells/reading-learning-package/outputs/craft-goal-quickstart/learning-package.pdf \
  --title "Craft + Goal in Five Minutes" --no-cover   # --no-cover: manuscript already has its own title block

# Bundle for download
(cd arcanum/spells/reading-learning-package/outputs && \
  zip -r craft-goal-quickstart.zip craft-goal-quickstart \
  -x '*/build-html.py')
```

## Boundary

This is a **learning artifact**, not source authority. It does not promote any
Craft / Goal / OpenClaw vocabulary into canon. The linked skill files are the
authority. See `source-trace.md` for honesty flags (the controller-agent pattern
is a design you grow into, not a shipped one-click feature).
