#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPELL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ARCANUM_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
"$ARCANUM_ROOT/arcana/experiment-harness/scripts/loop-harness.sh" "$SPELL_DIR" "$@"
