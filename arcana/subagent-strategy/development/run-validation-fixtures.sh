#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
"$ARTIFACT_DIR/../experiment-harness/scripts/validate-harness.sh" "$ARTIFACT_DIR"
