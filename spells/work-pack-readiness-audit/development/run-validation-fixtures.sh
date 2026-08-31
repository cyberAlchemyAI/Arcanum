#!/usr/bin/env bash
set -euo pipefail

development_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$development_root/test_work_pack_readiness.py"
python3 "$development_root/test_work_pack_readiness_v2.py"
python3 "$development_root/test_plan_once_selection.py"
python3 "$development_root/test_continuity_compatibility.py"
python3 "$development_root/test_plan_once_end_to_end.py"
