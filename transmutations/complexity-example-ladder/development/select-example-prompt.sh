#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HARNESS_SCRIPTS="$(cd "$SCRIPT_DIR/../../../arcana/experiment-harness/scripts" && pwd)"

"$HARNESS_SCRIPTS/select-prompt.sh" "$ARTIFACT_DIR" "$@"
