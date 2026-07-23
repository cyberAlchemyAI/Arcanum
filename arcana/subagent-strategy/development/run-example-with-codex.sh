#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
"$ARTIFACT_DIR/../experiment-harness/scripts/run-with-codex.sh" "$ARTIFACT_DIR" "$@"
