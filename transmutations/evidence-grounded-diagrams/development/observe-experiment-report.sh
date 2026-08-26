#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
artifact_dir="$(cd "$script_dir/.." && pwd)"
exec "$artifact_dir/../../arcana/experiment-harness/scripts/observe-harness.sh" "$artifact_dir" "$@"
