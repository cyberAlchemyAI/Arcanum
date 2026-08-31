#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
python3 "$repo_root/spells/invoke/development/preacceptance-closure/test_preacceptance_closure.py"
python3 "$repo_root/spells/invoke/development/preacceptance-closure/test_execution_entry_negative_cases.py"
