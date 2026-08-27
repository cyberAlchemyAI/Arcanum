#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ARCANUM_ROOT="$(cd "$ARTIFACT_DIR/../.." && pwd)"
EXPERIMENT_REPO_ROOT="${EXPERIMENT_REPO_ROOT:-$ARCANUM_ROOT}" \
  "$ARTIFACT_DIR/../experiment-harness/scripts/validate-harness.sh" "$ARTIFACT_DIR"
node "$SCRIPT_DIR/test-append-dispatch.cjs"
