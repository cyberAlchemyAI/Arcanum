#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$script_dir/validate-option-admissibility.py"
python3 "$script_dir/validate-override-consumption.py"
