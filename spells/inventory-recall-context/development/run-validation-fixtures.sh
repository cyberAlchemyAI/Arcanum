#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
artifact_root="$(cd -- "$script_dir/.." && pwd)"
arcanum_root="$(cd -- "$artifact_root/../.." && pwd)"
"$script_dir/validate-scenarios.sh"
"$arcanum_root/arcana/experiment-harness/scripts/validate-harness.sh" "$artifact_root"
