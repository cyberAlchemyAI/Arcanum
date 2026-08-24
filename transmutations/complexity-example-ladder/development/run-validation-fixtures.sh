#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HARNESS_SCRIPTS="$(cd "$SCRIPT_DIR/../../../arcana/experiment-harness/scripts" && pwd)"

"$HARNESS_SCRIPTS/validate-harness.sh" "$ARTIFACT_DIR"

while IFS= read -r regime_file; do
	regime_id="$(basename "$regime_file" .md)"
	"$HARNESS_SCRIPTS/validate-regime.sh" "$ARTIFACT_DIR" "$regime_id"
done < <(find "$SCRIPT_DIR/regimes" -maxdepth 1 -type f -name '*.md' | sort)
