#!/usr/bin/env bash
# Install Craft + Goal into a target project — self-contained, no Arcanum needed.
#
# Usage:
#   ./install.sh <target-project-dir> [--skills-dir <rel-path>] [--no-validate]
#
# Defaults:
#   skills dir is auto-detected: .claude/skills if a .claude/ exists, else
#   .agents/skills if a .agents/ exists, else .claude/skills is created.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS="$HERE/tools"

TARGET="${1:-}"
SKILLS_DIR=""
VALIDATE=1
shift || true
while [ $# -gt 0 ]; do
  case "$1" in
    --skills-dir) SKILLS_DIR="$2"; shift 2;;
    --no-validate) VALIDATE=0; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "usage: ./install.sh <target-project-dir> [--skills-dir <rel-path>] [--no-validate]" >&2
  exit 2
fi
if [ ! -d "$TARGET" ]; then
  echo "error: target project dir does not exist: $TARGET" >&2
  exit 1
fi
if [ ! -d "$TOOLS/craft" ] || [ ! -d "$TOOLS/goal" ]; then
  echo "error: bundled tools/ not found next to install.sh" >&2
  exit 1
fi

# auto-detect skills dir if not given
if [ -z "$SKILLS_DIR" ]; then
  if [ -d "$TARGET/.claude" ]; then SKILLS_DIR=".claude/skills"
  elif [ -d "$TARGET/.agents" ]; then SKILLS_DIR=".agents/skills"
  else SKILLS_DIR=".claude/skills"; fi
fi

DEST="$TARGET/$SKILLS_DIR"
echo "Installing Craft + Goal into: $DEST"
mkdir -p "$DEST"
rm -rf "$DEST/craft" "$DEST/goal"
cp -r "$TOOLS/craft" "$DEST/craft"
cp -r "$TOOLS/goal"  "$DEST/goal"
echo "  - craft  -> $SKILLS_DIR/craft  (model-operated, no deps)"
echo "  - goal   -> $SKILLS_DIR/goal   (python3 stdlib runtime)"

# python + optional jsonschema
if command -v python3 >/dev/null 2>&1; then
  echo "  - python3: $(python3 --version 2>&1)"
  if ! python3 -c "import jsonschema" >/dev/null 2>&1; then
    echo
    echo "Goal's validation suite needs the 'jsonschema' package (the only extra dependency)."
    printf "Install it now with pip? [y/N] "
    read -r ans || ans=""
    case "$ans" in
      y|Y) python3 -m pip install jsonschema || echo "  (pip install failed — install manually: pip install jsonschema)";;
      *) echo "  Skipped. Run 'pip install jsonschema' later to enable validation.";;
    esac
  fi
else
  echo "  - WARNING: python3 not found. Craft still works (model-operated); Goal's runtime/validation need Python 3."
fi

# validate
if [ "$VALIDATE" -eq 1 ] && command -v python3 >/dev/null 2>&1 && python3 -c "import jsonschema" >/dev/null 2>&1; then
  echo
  echo "Validating Goal install..."
  if python3 "$DEST/goal/validation/run-fixtures.py"; then
    echo "Goal validation: PASS"
  else
    echo "Goal validation: FAILED (see output above)" >&2
  fi
fi

echo
echo "Done. Open your AI agent in the project and say: \"Start a Craft project here.\""
