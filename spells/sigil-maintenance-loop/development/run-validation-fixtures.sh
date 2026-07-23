#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPELL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ARCANUM_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
"$SCRIPT_DIR/validate-scenarios.sh"
"$ARCANUM_ROOT/arcana/experiment-harness/scripts/validate-harness.sh" "$SPELL_DIR"
