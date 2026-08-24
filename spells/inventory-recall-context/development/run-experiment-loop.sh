#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
artifact_root="$(cd -- "$script_dir/.." && pwd)"
arcanum_root="$(cd -- "$artifact_root/../.." && pwd)"
"$arcanum_root/arcana/experiment-harness/scripts/loop-harness.sh" "$artifact_root" "$@"
