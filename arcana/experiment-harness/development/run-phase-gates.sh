#!/usr/bin/env bash
set -euo pipefail

ARCANUM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
WORKSPACE_ROOT="$(cd "$ARCANUM_DIR/.." && pwd)"
HARNESS_DIR="$ARCANUM_DIR/arcana/experiment-harness"
INVOKE_DIR="$ARCANUM_DIR/spells/invoke"
SCRIPT_DIR="$HARNESS_DIR/scripts"
RUNS_DIR="$HARNESS_DIR/development/runs"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT="$RUNS_DIR/$RUN_ID.md"
LESSONS="$HARNESS_DIR/development/LESSONS-LEARNED.md"
LATEST="$HARNESS_DIR/development/PHASE-GATE-LATEST.md"

mkdir -p "$RUNS_DIR"

phase_results=()
phase_lessons=()

record_result() {
	local phase="$1"
	local status="$2"
	local summary="$3"
	phase_results+=("$phase|$status|$summary")
	printf '%s: %s - %s\n' "$phase" "$status" "$summary"
}

record_lesson() {
	local phase="$1"
	local lesson="$2"
	phase_lessons+=("$phase|$lesson")
}

run_phase0() {
	local tmpdir
	local baseline_artifact
	local baseline_report
	tmpdir="$(mktemp -d)"
	mkdir -p "$tmpdir/observability"
	cat > "$tmpdir/observability/config.json" <<'JSON'
{
  "version": "0.2.0",
  "storage_model": "central-ledger-reference-indexes",
  "source_of_truth": "signals/sigil-invocations.jsonl",
  "per_sigil_index_path": "by-sigil/<sigil-name>.jsonl",
  "per_capability_index_path": "by-capability/<kind>/<capability-id>.jsonl",
  "reflection_path": "reflections/",
  "thresholds": {
    "meaningful_executions": 1,
    "generated_outputs": 10,
    "related_workflow_gaps": 3,
    "severe_workflow_gaps": 1
  }
}
JSON
	cat > "$tmpdir/observability/reflection-state.json" <<'JSON'
{
  "version": "0.1.0",
  "last_reflection_at": null,
  "counters": {
    "meaningful_executions": 0,
    "generated_outputs": 0,
    "related_workflow_gaps": 0,
    "severe_workflow_gaps": 0,
    "quality_bar_failures": 0,
    "output_contract_drift_events": 0
  },
  "by_sigil": {}
}
JSON
	baseline_artifact="$tmpdir/baseline-spell"
	mkdir -p "$baseline_artifact"
	cat > "$baseline_artifact/SKILL.md" <<'EOF'
---
name: baseline-spell
---

# Baseline Spell

<quality-bar>
- return a result
</quality-bar>

<anti-patterns>
- save summary only
</anti-patterns>
EOF
	if bash -n "$SCRIPT_DIR"/*.sh \
		&& bash -n "$INVOKE_DIR"/development/*.sh \
		&& "$INVOKE_DIR/development/run-validation-fixtures.sh" >/tmp/experiment-harness-phase0-invoke.log 2>&1 \
		&& "$SCRIPT_DIR/init-harness.sh" "$baseline_artifact" --type spell >/tmp/experiment-harness-phase0-init.log 2>&1 \
		&& EXPERIMENT_OBSERVE=0 "$SCRIPT_DIR/report-harness.sh" "$baseline_artifact" >/tmp/experiment-harness-phase0-report.log 2>&1 \
		&& baseline_report="$(sed -n 's/^REPORT=//p' /tmp/experiment-harness-phase0-report.log | tail -n 1)" \
		&& EXPERIMENT_OBSERVABILITY_DIR="$tmpdir/observability" "$SCRIPT_DIR/observe-harness.sh" "$baseline_artifact" "$baseline_report" >/tmp/experiment-harness-phase0-observe.log 2>&1 \
		&& jq -e 'select(.observer.reflection_trigger == "usage-threshold" and .observer.recommendation == "reflect-now")' "$tmpdir/observability/signals/sigil-invocations.jsonl" >/tmp/experiment-harness-phase0-reflection.log 2>&1; then
		record_result "Phase 0" "pass" "baseline controls, syntax checks, profile-aware validation, observation, and threshold reflection signal ran"
		record_lesson "Phase 0" "The deterministic baseline can stay green while loop-first features are added behind separate gates."
	else
		record_result "Phase 0" "block" "baseline controls, observation, or threshold reflection signal failed"
		record_lesson "Phase 0" "Baseline failures should block later phase work because they obscure loop regressions."
	fi
	rm -rf "$tmpdir"
}

run_phase1() {
	local regime
	local failed=0
	for regime in LIVE-DEFINE-001 LIVE-DESIGN-001 LIVE-DEFINE-DESIGN-001 LIVE-OBSERVABILITY-001; do
		if ! "$SCRIPT_DIR/validate-regime.sh" "$INVOKE_DIR" "$regime" >/tmp/experiment-harness-$regime.log 2>&1; then
			failed=1
		fi
	done
	if [[ "$failed" -eq 0 ]]; then
		record_result "Phase 1" "pass" "invoke live regime files validate"
		record_lesson "Phase 1" "Explicit prompt paths and required output patterns make regimes both readable and scriptable."
	else
		record_result "Phase 1" "block" "one or more invoke live regime files failed validation"
	fi
}

write_mock_output() {
	local path="$1"
	local mode="$2"
	cat > "$path" <<EOF
## Invoke Result

- Mode: $mode
- Phase status: pass
- Spec: present
- Glossary: present
- Define transport: present
- Source Contracts: approved define output
- View 1: Context View
- View 2: High-Level Structure View
- View 3: Low-Level Components View
- View 4: Workflow Process View
- View 5: Decision Flow View
- View 6: Dependency Interface View
- Risks: recorded
- Glossary consistency: pass
- Design transport: present
- Next route: plan

## Architecture Plan

The design consumes define output and preserves approved define authority.
EOF
}

run_phase2() {
	local mockdir
	mockdir="$(mktemp -d)"
	write_mock_output "$mockdir/LIVE-DEFINE-001-attempt-001.md" "define"
	if MAX_ATTEMPTS=1 PASS_STREAK=1 AUTO_IMPROVE=0 EXPERIMENT_LOOP_MOCK_DIR="$mockdir" \
		"$SCRIPT_DIR/loop-harness.sh" "$INVOKE_DIR" LIVE-DEFINE-001 >/tmp/experiment-harness-phase2.log 2>&1; then
		record_result "Phase 2" "pass" "single-attempt loop creates a valid attempt bundle"
		record_lesson "Phase 2" "Mocked execution lets us verify bundle shape without spending live Codex calls."
	else
		record_result "Phase 2" "block" "single-attempt loop failed"
	fi
	rm -rf "$mockdir"
}

run_phase3() {
	local mockdir
	mockdir="$(mktemp -d)"
	write_mock_output "$mockdir/LIVE-DEFINE-001-attempt-001.md" "define"
	printf 'not enough\n' > "$mockdir/LIVE-DEFINE-001-attempt-002.md"
	write_mock_output "$mockdir/LIVE-DEFINE-001-attempt-003.md" "define"
	write_mock_output "$mockdir/LIVE-DEFINE-001-attempt-004.md" "define"
	if MAX_ATTEMPTS=4 PASS_STREAK=2 AUTO_IMPROVE=0 EXPERIMENT_LOOP_MOCK_DIR="$mockdir" \
		"$SCRIPT_DIR/loop-harness.sh" "$INVOKE_DIR" LIVE-DEFINE-001 >/tmp/experiment-harness-phase3.log 2>&1; then
		record_result "Phase 3" "pass" "pass streak resets after failure and succeeds after two consecutive passes"
		record_lesson "Phase 3" "Two consecutive passes catch instability that a two-total-pass rule would miss."
	else
		record_result "Phase 3" "block" "stability loop failed"
	fi
	rm -rf "$mockdir"
}

run_phase4() {
	local mockdir
	local loop_dir
	mockdir="$(mktemp -d)"
	printf 'not enough\n' > "$mockdir/LIVE-DEFINE-001-attempt-001.md"
	printf 'not enough\n' > "$mockdir/LIVE-DEFINE-001-attempt-002.md"
	MAX_ATTEMPTS=2 PASS_STREAK=2 AUTO_IMPROVE=1 EXPERIMENT_LOOP_MOCK_DIR="$mockdir" \
		"$SCRIPT_DIR/loop-harness.sh" "$INVOKE_DIR" LIVE-DEFINE-001 >/tmp/experiment-harness-phase4.log 2>&1 || true
	loop_dir="$(sed -n 's/^LOOP_DIR=//p' /tmp/experiment-harness-phase4.log | tail -n 1)"
	if [[ -n "$loop_dir" && -f "$ARCANUM_DIR/$loop_dir/attempt-001/robot-talks.md" && -f "$ARCANUM_DIR/$loop_dir/attempt-001/improvement-argument.md" ]]; then
		record_result "Phase 4" "pass" "failed attempt creates robot-talks and improvement argument artifacts"
		record_lesson "Phase 4" "Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists."
	else
		record_result "Phase 4" "block" "robot-talks improvement artifacts were not created"
	fi
	rm -rf "$mockdir"
}

run_phase5() {
	local tmpdir
	tmpdir="$(mktemp -d)"
	(
		cd "$tmpdir"
		git init -q
		git config user.email test@example.com
		git config user.name Test
		printf 'before\n' > file.txt
		git add file.txt
		git commit -q -m init
		mkdir attempt
		cat > attempt/patch.diff <<'PATCH'
diff --git a/file.txt b/file.txt
index 66a66c6..5c003b3 100644
--- a/file.txt
+++ b/file.txt
@@ -1 +1 @@
-before
+after
PATCH
		"$SCRIPT_DIR/apply-loop-improvement.sh" attempt >/tmp/experiment-harness-phase5-apply.log
		"$SCRIPT_DIR/rollback-loop-improvement.sh" attempt >/tmp/experiment-harness-phase5-rollback.log
		test "$(cat file.txt)" = "before"
	)
	if [[ "$?" -eq 0 ]]; then
		record_result "Phase 5" "pass" "patch application and rollback work in an isolated git repo"
		record_lesson "Phase 5" "Rollback should be validated in isolation before enabling broad full-artifact edits."
	else
		record_result "Phase 5" "block" "patch rollback failed"
	fi
	rm -rf "$tmpdir"
}

run_phase6() {
	local mockdir
	mockdir="$(mktemp -d)"
	write_mock_output "$mockdir/LIVE-DEFINE-DESIGN-001-attempt-001.md" "define and design"
	write_mock_output "$mockdir/LIVE-DEFINE-DESIGN-001-attempt-002.md" "define and design"
	if MAX_ATTEMPTS=2 PASS_STREAK=2 AUTO_IMPROVE=0 EXPERIMENT_LOOP_MOCK_DIR="$mockdir" \
		"$SCRIPT_DIR/loop-harness.sh" "$INVOKE_DIR" LIVE-DEFINE-DESIGN-001 >/tmp/experiment-harness-phase6.log 2>&1; then
		record_result "Phase 6" "pass" "invoke pilot loop passes with mocked live output"
		record_lesson "Phase 6" "Mocked invoke loops prove harness control flow; live promotion evidence is recorded separately in LIVE-PROMOTION-CLOSEOUT.md."
	else
		record_result "Phase 6" "block" "invoke pilot mocked loop failed"
	fi
	rm -rf "$mockdir"
}

run_phase7() {
	local tmpdir
	tmpdir="$(mktemp -d)"
	mkdir -p "$tmpdir/toy-sigil"
	cat > "$tmpdir/toy-sigil/SKILL.md" <<'EOF'
---
name: toy-sigil
---

# Toy Sigil

<quality-bar>
- return a sigil result
</quality-bar>

<anti-patterns>
- save summary only
</anti-patterns>
EOF
	if "$SCRIPT_DIR/init-harness.sh" "$tmpdir/toy-sigil" --type sigil >/tmp/experiment-harness-phase7-init.log 2>&1 \
		&& test -d "$tmpdir/toy-sigil/development/regimes" \
		&& test -f "$tmpdir/toy-sigil/development/EXPERIMENT-PROFILE.md" \
		&& test -d "$tmpdir/toy-sigil/development/experiment-loops" \
		&& test -x "$tmpdir/toy-sigil/development/run-experiment-loop.sh"; then
		record_result "Phase 7" "pass" "new harness initialization creates profile-aware loop-ready layout"
		record_lesson "Phase 7" "Loop-ready layout and profile metadata can be installed at artifact creation time without running live Codex."
	else
		record_result "Phase 7" "block" "loop-ready initialization failed"
	fi
	rm -rf "$tmpdir"
}

run_phase0
run_phase1
run_phase2
run_phase3
run_phase4
run_phase5
run_phase6
run_phase7

{
	printf '# Experiment Harness Phase Gate Run\n\n'
	printf -- '- Run ID: `%s`\n' "$RUN_ID"
	printf -- '- Runner: `arcanum/arcana/experiment-harness/development/run-phase-gates.sh`\n\n'
	printf '## Results\n\n'
	printf '| Phase | Status | Summary |\n'
	printf '| --- | --- | --- |\n'
	row=""
	for row in "${phase_results[@]}"; do
		IFS='|' read -r phase status summary <<< "$row"
		printf '| %s | `%s` | %s |\n' "$phase" "$status" "$summary"
	done
	printf '\n## Lessons Captured\n\n'
	for row in "${phase_lessons[@]}"; do
		IFS='|' read -r phase lesson <<< "$row"
		printf -- '- **%s:** %s\n' "$phase" "$lesson"
	done
} > "$REPORT"

{
	printf '# Experiment Harness Phase Gate Latest\n\n'
	printf -- '- Latest run: `%s`\n' "$RUN_ID"
	printf -- '- Runner: `arcanum/arcana/experiment-harness/development/run-phase-gates.sh`\n'
	if printf '%s\n' "${phase_results[@]}" | rg -q '\|block\|'; then
		printf -- '- Status: `block`\n'
	else
		printf -- '- Status: `pass`\n'
	fi
	printf -- '- Evidence type: deterministic controls and mocked live-loop gates\n\n'
	printf '## Results\n\n'
	printf '| Phase | Status | Summary |\n'
	printf '| --- | --- | --- |\n'
	for row in "${phase_results[@]}"; do
		IFS='|' read -r phase status summary <<< "$row"
		printf '| %s | `%s` | %s |\n' "$phase" "$status" "$summary"
	done
	printf '\n## Lessons Captured\n\n'
	for row in "${phase_lessons[@]}"; do
		IFS='|' read -r phase lesson <<< "$row"
		printf -- '- **%s:** %s\n' "$phase" "$lesson"
	done
	printf '\n## Live Promotion Evidence\n\n'
	printf 'This latest gate proves deterministic harness mechanics. Live Codex promotion loops for `invoke` also passed and were observed in `LIVE-PROMOTION-CLOSEOUT.md`.\n'
} > "$LATEST"

{
	printf '\n## Phase Gate Run %s\n\n' "$RUN_ID"
	for row in "${phase_lessons[@]}"; do
		IFS='|' read -r phase lesson <<< "$row"
		printf -- '- **%s:** %s\n' "$phase" "$lesson"
	done
} >> "$LESSONS"

printf 'REPORT=%s\n' "${REPORT#$ARCANUM_DIR/}"

if printf '%s\n' "${phase_results[@]}" | rg -q '\|block\|'; then
	exit 1
fi
