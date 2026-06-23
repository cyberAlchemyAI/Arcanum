# Install Craft + Goal in your own project

This package is **self-contained**. You do **not** need to install Arcanum to use
Craft and Goal. You only need to drop two folders into your project and (optionally)
install one small Python package.

> **Verified:** copied into a bare project with nothing else, `goal`'s runtime runs
> on the Python 3 standard library alone, and its validation suite prints
> `goal-fixtures-pass`. See "What it actually needs" below.

---

## What's in the box (`tools/`)

```
tools/
  craft/     # the logbook skill — pure model-operated, NO code dependencies
  goal/      # the autopilot skill — Python 3 runtime + JSON schemas + validation
```

- **`tools/craft/`** — `SKILL.md`, `README.md`, `ARCHITECTURE.md`, `templates/`,
  `examples/`. Your AI agent operates it by reading `SKILL.md`. It writes plain
  `.craft/ledger.yml` + `CRAFT.md` files in *your* project. Nothing to compile.
- **`tools/goal/`** — `SKILL.md` + `README.md` (the operating contract),
  `runtime/goal_loop.py`, `schemas/*.json`, and `validation/`.

---

## What it actually needs (the honest dependency list)

| To do this | You need |
| --- | --- |
| Use Craft (the logbook) | **Nothing.** It's model-operated; the agent reads/writes files. |
| Use the Goal loop with your agent | **Nothing** beyond your AI agent (Claude Code / Codex / etc.). |
| Run the Goal Python runtime skeleton (`goal_loop.py`) | **Python 3** (standard library only — no pip installs). |
| Run Goal's validation fixtures (`run-fixtures.py`) | **`jsonschema`** → `pip install jsonschema`. This is the *only* third-party import in the whole package. |

Goal *mentions* other capabilities (decision-gate, task-session, …) in its README.
Those are **optional governance owners it routes to if present** — not install
requirements. With nothing but Craft + Goal, the loop still runs and simply
**fail-closed stops** at any step that would need one. You lose nothing required;
you only defer richer governance.

---

## Install — one command

From inside this package folder:

```bash
# install into the current project (auto-detects .claude/skills or .agents/skills)
./install.sh /path/to/your/project

# or choose the skills dir explicitly:
./install.sh /path/to/your/project --skills-dir .agents/skills
```

The script copies `tools/craft` and `tools/goal` into your project's skills
directory, checks Python, offers to `pip install jsonschema`, and runs Goal's
validation to confirm the install works.

## Install — manual (if you prefer)

```bash
# pick ONE skills dir for your agent:
#   Claude Code -> .claude/skills      Codex/others -> .agents/skills
DEST=/path/to/your/project/.claude/skills
mkdir -p "$DEST"
cp -r tools/craft "$DEST/craft"
cp -r tools/goal  "$DEST/goal"

# optional: enable Goal's validation suite
pip install jsonschema
python3 "$DEST/goal/validation/run-fixtures.py"   # expect: goal-fixtures-pass
```

---

## Confirm it works

```bash
# 1. Goal runtime is importable and stdlib-only:
python3 .claude/skills/goal/runtime/goal_loop.py --help

# 2. Goal validation passes (needs jsonschema):
python3 .claude/skills/goal/validation/run-fixtures.py
#   -> goal-fixtures-pass
```

Then open your agent and say: **"Start a Craft project here."** You're running.

---

## Notes

- These `tools/` are a **snapshot copy** of Craft (`arcana/craft`) and Goal
  (`spells/goal`, native runtime surface). They are pinned with this package so it
  installs without the Arcanum repo. To track upstream changes, re-export from the
  source repo or use `arcanum-bootstrap`.
- `goal_loop.py` is a **read-only skeleton**: it classifies risk and emits results;
  it never mutates your files. All mutation stays behind your agent + approval.
- Updating later: re-run `./install.sh` — it overwrites the two skill folders and
  leaves your project's own `.craft/` ledger untouched.
