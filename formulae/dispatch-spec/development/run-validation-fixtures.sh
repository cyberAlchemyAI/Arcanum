#!/usr/bin/env bash
set -euo pipefail

root="/home/vrondelli/projects/domainspec-core/arcanum"
validator="$root/formulae/dispatch-spec/scripts/validate-dispatch.py"
fixtures="$root/formulae/dispatch-spec/development/fixtures"

overall="pass"

run_case() {
	local expected="$1"
	local path="$2"
	local output
	output="$("$validator" "$path" 2>&1 || true)"
	printf '%s\n' "$output"
	local actual
	actual="$(printf '%s\n' "$output" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
	if [[ "$actual" != "$expected" ]]; then
		printf 'BLOCK: expected %s but got %s for %s\n' "$expected" "${actual:-missing}" "$path"
		overall="block"
	fi
}

run_case pass "$fixtures/pass-refine-dispatch.json"
run_case block "$fixtures/block-missing-validation-evidence.json"
run_case flag "$fixtures/flag-unused-technique.json"
run_case pass "$fixtures/pass-route-menu-overlay.json"
run_case block "$fixtures/block-dialectic-missing-roles.json"
run_case block "$fixtures/block-tournament-missing-convergence.json"
run_case block "$fixtures/block-xray-missing-handle.json"
run_case block "$fixtures/block-toy-game-missing-evidence.json"
run_case pass "$fixtures/pass-memory-protected-overlay.json"
run_case block "$fixtures/block-subagent-strategy-missing-roles.json"
run_case pass "$fixtures/pass-subagent-lifecycle-closeout.json"
run_case block "$fixtures/block-subagent-lifecycle-open-agent.json"
run_case pass "$fixtures/pass-boundary-evidence.json"
run_case flag "$fixtures/flag-boundary-technique-no-schema.json"
run_case block "$fixtures/block-boundary-unknown-step.json"
run_case block "$fixtures/block-promotion-split-violation.json"
run_case pass "$fixtures/pass-native-stage-receipts.json"
run_case block "$fixtures/block-command-interface-active-proof.json"
run_case pass "$root/arcana/refine/templates/refine-dispatch.json"

printf 'DISPATCH_SPEC_VALIDATION=%s\n' "$overall"
printf 'VALIDATION=%s\n' "$overall"

[[ "$overall" == "pass" ]]
