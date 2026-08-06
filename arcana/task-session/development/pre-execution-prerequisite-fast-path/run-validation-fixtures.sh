#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARCANUM_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
REPO_ROOT="$(cd "$ARCANUM_ROOT/.." && pwd)"

cd "$REPO_ROOT"

python3 arcanum/arcana/task-session/development/pre-execution-prerequisite-fast-path/validate-fixtures.py --group schema
python3 arcanum/arcana/task-session/development/pre-execution-prerequisite-fast-path/test_classifier.py
python3 arcanum/arcana/task-session/development/pre-execution-prerequisite-fast-path/test_integration.py
python3 arcanum/arcana/task-session/development/pre-execution-prerequisite-fast-path/test_owner_resume.py
bash arcanum/arcana/continuation-router/development/run-validation-fixtures.sh
python3 arcanum/spells/work-pack-readiness-audit/development/test_plan_once_end_to_end.py
python3 arcanum/arcana/task-session/development/test_plan_once_admission.py
python3 arcanum/arcana/task-session/development/test_plan_once_governance.py
python3 arcanum/spells/implementation-readiness/scripts/validate_execution_contracts.py
python3 arcanum/spells/implementation-readiness/development/validate-outer-loop.py

echo "PRE_EXECUTION_PREREQUISITE_FAST_PATH=pass"
