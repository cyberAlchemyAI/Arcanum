#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
artifact_dir="$(cd "$script_dir/.." && pwd)"
exec "$artifact_dir/../../arcana/experiment-harness/scripts/loop-harness.sh" "$artifact_dir" "$@"
