#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FRAMEWORK_ROOT="$(cd "$PACKAGE_ROOT/.." && pwd)"
POSITIVE="$SCRIPT_DIR/fixtures/positive"
first_nonzero=0
checks_run=0

run_check() {
	local label="$1"
	shift
	checks_run=$((checks_run + 1))
	"$@"
	local status=$?
	if (( status != 0 )); then
		printf 'BLOCK %s exit=%s\n' "$label" "$status" >&2
		if (( first_nonzero == 0 )); then
			first_nonzero=$status
		fi
	else
		printf 'PASS %s\n' "$label"
	fi
}

fixture_tmp="$(mktemp -d)"

run_check unit-and-negative-suite \
	env PYTHONDONTWRITEBYTECODE=1 python3 "$SCRIPT_DIR/test_governance_flow.py"

run_check positive-terminal-cli \
	env PYTHONDONTWRITEBYTECODE=1 python3 "$PACKAGE_ROOT/scripts/run_governance_flow.py" fixture \
	"$POSITIVE/terminal-boundary-source.json" \
	"$POSITIVE/terminal-boundary-executor.py" \
	"$fixture_tmp/root" \
	"$fixture_tmp/evidence" \
	--expected-human "$POSITIVE/expected-human-view.md" \
	--expected-terminal "$POSITIVE/expected-terminal-receipt.json"

privacy_pattern='(/(home|mnt)/|(^|/)ops/(development|research)/|01[a-f0-9]{6,}-[a-f0-9-]{20,}|approval[-_ ]loop|private[[:space:]]+authority[[:space:]]+spine)'
privacy_output="$(rg -n -i "$privacy_pattern" \
	"$FRAMEWORK_ROOT/GOVERNANCE-FLOW-CONTRACT.md" \
	"$FRAMEWORK_ROOT/README.md" \
	"$FRAMEWORK_ROOT/CYBERALCHEMY-METHOD.md" \
	"$FRAMEWORK_ROOT/QUALITY-BAR.md" \
	"$FRAMEWORK_ROOT/OUTCOME-BRIEF-CONTRACT.md" \
	"$PACKAGE_ROOT" 2>/dev/null)"
privacy_status=$?
if (( privacy_status == 0 )); then
	printf 'BLOCK public-privacy-scan matches:\n%s\n' "$privacy_output" >&2
	if (( first_nonzero == 0 )); then
		first_nonzero=1
	fi
elif (( privacy_status == 1 )); then
	printf 'PASS public-privacy-scan\n'
else
	printf 'BLOCK public-privacy-scan validator_exit=%s\n' "$privacy_status" >&2
	if (( first_nonzero == 0 )); then
		first_nonzero=$privacy_status
	fi
fi
checks_run=$((checks_run + 1))

printf 'governance-flow validation checks=%s positive=1 negative=21 first_nonzero=%s\n' \
	"$checks_run" "$first_nonzero"
printf 'run-local evidence retained at %s\n' "$fixture_tmp"
exit "$first_nonzero"
