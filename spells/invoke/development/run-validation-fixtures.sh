#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
INVOKE_DIR="$ROOT_DIR/arcanum/spells/invoke"
DEFINE_CONTRACT="$INVOKE_DIR/define.md"
DESIGN_CONTRACT="$INVOKE_DIR/design.md"
PLAN_CONTRACT="$INVOKE_DIR/plan.md"
FIXTURE_DIR="$INVOKE_DIR/development/fixtures"
TEMPLATE_TASKS="$INVOKE_DIR/development/TEMPLATE-VALIDATION-TASKS.md"
EXPERIMENT_REGIMES="$INVOKE_DIR/development/EXPERIMENT-REGIMES.md"
EXAMPLE_PROMPTS_DIR="$INVOKE_DIR/development/example-prompts"
EXAMPLE_OUTPUTS_DIR="$INVOKE_DIR/development/example-outputs"
PROMPT_SELECTOR="$INVOKE_DIR/development/select-template-example-prompt.sh"
CODEX_EXAMPLE_RUNNER="$INVOKE_DIR/development/run-template-example-with-codex.sh"
EXPERIMENT_CODEX_RUNNER="$ROOT_DIR/arcanum/arcana/experiment-harness/scripts/run-with-codex.sh"
RUNS_DIR="$INVOKE_DIR/development/runs"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_REPORT="$RUNS_DIR/$RUN_ID.md"

failures=0
events=()
passed_fixtures=()
failed_checks=()
output_artifacts=()
quality_bar_status="pass"
anti_pattern_hits=()
workflow_gaps=()

mkdir -p "$RUNS_DIR"

record() {
	local message="$1"
	events+=("$message")
	printf '%s\n' "$message"
}

json_array() {
	if [[ "$#" -eq 0 ]]; then
		printf '[]\n'
		return 0
	fi
	printf '%s\n' "$@" | jq -Rsc 'split("\n")[:-1]'
}

json_objects() {
	if [[ "$#" -eq 0 ]]; then
		printf '[]\n'
		return 0
	fi
	printf '%s\n' "$@" | jq -sc '.'
}

add_quality_gap() {
	local category="$1"
	local severity="$2"
	local summary="$3"
	local evidence="$4"
	workflow_gaps+=("$(
		jq -cn \
			--arg category "$category" \
			--arg severity "$severity" \
			--arg summary "$summary" \
			--arg evidence "$evidence" \
			'{
				category: $category,
				severity: $severity,
				summary: $summary,
				evidence: $evidence
			}'
	)")
	if [[ "$severity" == "severe" || "$severity" == "high" ]]; then
		quality_bar_status="fail"
	elif [[ "$quality_bar_status" == "pass" ]]; then
		quality_bar_status="partial"
	fi
}

add_anti_pattern_hit() {
	local summary="$1"
	anti_pattern_hits+=("$summary")
}

require_file() {
	local path="$1"
	if [[ ! -f "$path" ]]; then
		record "FAIL: missing file $path"
		failed_checks+=("missing file $path")
		failures=$((failures + 1))
	fi
}

require_pattern() {
	local path="$1"
	local pattern="$2"
	local label="$3"
	if ! rg -q -- "$pattern" "$path"; then
		record "FAIL: $label missing pattern: $pattern"
		failed_checks+=("$label missing pattern: $pattern")
		failures=$((failures + 1))
	fi
}

write_report() {
	local verdict="$1"
	local anti_json
	local gaps_json
	if [[ "$verdict" == "block" ]]; then
		quality_bar_status="fail"
	fi
	anti_json="$(json_array "${anti_pattern_hits[@]}")"
	gaps_json="$(json_objects "${workflow_gaps[@]}")"
	{
		printf '# Invoke Validation Fixture Run\n\n'
		printf -- '- Run ID: `%s`\n' "$RUN_ID"
		printf -- '- Verdict: `%s`\n' "$verdict"
		printf -- '- Validation: %s\n' "$verdict"
		printf -- '- Quality Bar: `%s`\n' "$quality_bar_status"
		printf -- '- Anti-Pattern hits: `%s`\n' "${#anti_pattern_hits[@]}"
		printf -- '- Runner: `arcanum/spells/invoke/development/run-validation-fixtures.sh`\n'
		printf -- '- Fixture directory: `arcanum/spells/invoke/development/fixtures/`\n'
		printf -- '- Define contract: `arcanum/spells/invoke/define.md`\n'
		printf -- '- Design contract: `arcanum/spells/invoke/design.md`\n\n'
		printf -- '- Plan contract: `arcanum/spells/invoke/plan.md`\n\n'
		printf -- '- Experiment regimes: `arcanum/spells/invoke/development/EXPERIMENT-REGIMES.md`\n\n'
		printf -- '- Template task matrix: `arcanum/spells/invoke/development/TEMPLATE-VALIDATION-TASKS.md`\n\n'
		printf -- '- Example prompts: `arcanum/spells/invoke/development/example-prompts/`\n\n'
		printf -- '- Example outputs: `arcanum/spells/invoke/development/example-outputs/`\n\n'
		printf -- '- Prompt selector: `arcanum/spells/invoke/development/select-template-example-prompt.sh`\n\n'
		printf -- '- Codex example runner: `arcanum/spells/invoke/development/run-template-example-with-codex.sh`\n\n'

		printf '## Passed Fixtures\n\n'
		if [[ "${#passed_fixtures[@]}" -eq 0 ]]; then
			printf '- none\n'
		else
			local fixture
			for fixture in "${passed_fixtures[@]}"; do
				printf -- '- `%s`\n' "$fixture"
			done
		fi
		printf '\n'

		printf '## Failed Checks\n\n'
		if [[ "${#failed_checks[@]}" -eq 0 ]]; then
			printf -- '- none\n'
		else
			local check
			for check in "${failed_checks[@]}"; do
				printf -- '- %s\n' "$check"
			done
		fi
		printf '\n'

		printf '## Output Artifacts\n\n'
		if [[ "${#output_artifacts[@]}" -eq 0 ]]; then
			printf -- '- none\n'
		else
			local artifact
			for artifact in "${output_artifacts[@]}"; do
				printf -- '- `%s`\n' "$artifact"
			done
		fi
		printf '\n'

		printf '## Runner Output\n\n'
		printf '```text\n'
		local event
		for event in "${events[@]}"; do
			printf '%s\n' "$event"
		done
		printf '```\n'
		printf '\n## Machine Summary\n\n'
		printf 'QUALITY_BAR_STATUS=%s\n' "$quality_bar_status"
		printf 'ANTI_PATTERN_HITS_JSON=%s\n' "$anti_json"
		printf 'WORKFLOW_GAPS_JSON=%s\n' "$gaps_json"
	} > "$RUN_REPORT"
}

run_template_task_matrix() {
	local matrix="$1"
	local template
	local complexity
	local id
	local templates=(
		'module-formulae'
		'implementation-layering'
		'work-pack'
		'generic'
		'research'
		'architecture'
		'implementation-plan'
		'spell'
		'sigil'
		'ux-plan'
	)
	local complexities=('low' 'medium' 'complex')

	require_file "$matrix"
	require_pattern "$matrix" '## Template Task Matrix' 'template task matrix heading'

	for template in "${templates[@]}"; do
		for complexity in "${complexities[@]}"; do
			id="$template-$complexity"
			require_pattern "$matrix" "$id" "template task $id"
			require_file "$EXAMPLE_PROMPTS_DIR/$id.md"
			require_pattern "$EXAMPLE_PROMPTS_DIR/$id.md" '## Codex Prompt' "example prompt $id codex prompt"
			require_pattern "$EXAMPLE_PROMPTS_DIR/$id.md" 'Expected Capture Path' "example prompt $id capture path"
		done
	done

	if [[ "$failures" -eq 0 ]]; then
		passed_fixtures+=('TEMPLATE-TASK-MATRIX')
		output_artifacts+=("${matrix#$ROOT_DIR/}")
		output_artifacts+=("${EXAMPLE_PROMPTS_DIR#$ROOT_DIR/}/")
		record 'PASS: TEMPLATE-TASK-MATRIX'
	fi
}

run_prompt_selector_checks() {
	require_file "$PROMPT_SELECTOR"
	require_file "$CODEX_EXAMPLE_RUNNER"
	require_file "$EXPERIMENT_CODEX_RUNNER"
	require_file "$ROOT_DIR/.codex/commands/arcanum-sigil-invoke-example-runner.md"
	require_file "$ROOT_DIR/.codex/commands/invoke-example-next.md"
	require_file "$ROOT_DIR/.codex/commands/invoke-example-run.md"
	require_file "$ROOT_DIR/.arcanum/runtimes/codex/commands/arcanum-sigil-invoke-example-runner.md"

	local exact
	local pair
	local next
	exact="$("$PROMPT_SELECTOR" sigil-medium)"
	pair="$("$PROMPT_SELECTOR" sigil medium)"
	next="$("$PROMPT_SELECTOR" next)"

	if [[ "$exact" != *'TASK_ID=sigil-medium'* ]] || [[ "$exact" != *'PROMPT=arcanum/spells/invoke/development/example-prompts/sigil-medium.md'* && "$exact" != *'PROMPT=spells/invoke/development/example-prompts/sigil-medium.md'* ]]; then
		record 'FAIL: prompt selector exact task lookup failed'
		failed_checks+=('prompt selector exact task lookup failed')
		failures=$((failures + 1))
	fi

	if [[ "$pair" != *'TASK_ID=sigil-medium'* ]]; then
		record 'FAIL: prompt selector template complexity lookup failed'
		failed_checks+=('prompt selector template complexity lookup failed')
		failures=$((failures + 1))
	fi

	if [[ "$next" != *'TASK_ID='* ]] || [[ "$next" != *'PROMPT='* ]] || [[ "$next" != *'OUTPUT='* ]]; then
		record 'FAIL: prompt selector next lookup failed'
		failed_checks+=('prompt selector next lookup failed')
		failures=$((failures + 1))
	fi

	require_pattern "$ROOT_DIR/.codex/commands/arcanum-sigil-invoke-example-runner.md" 'arcanum-sigil-invoke-example-runner' 'codex invoke example runner bridge'
	require_pattern "$ROOT_DIR/.codex/commands/invoke-example-next.md" 'run-template-example-with-codex.sh next' 'codex invoke example next command'
	require_pattern "$ROOT_DIR/.codex/commands/invoke-example-run.md" 'run-template-example-with-codex.sh <selection>' 'codex invoke example run command'
	require_pattern "$ROOT_DIR/.arcanum/runtimes/codex/commands/arcanum-sigil-invoke-example-runner.md" 'select-template-example-prompt.sh' 'codex invoke example runner adapter'
	require_pattern "$CODEX_EXAMPLE_RUNNER" 'experiment-harness/scripts/run-with-codex.sh' 'invoke codex example runner delegates to experiment harness'
	require_pattern "$EXPERIMENT_CODEX_RUNNER" 'codex.*exec' 'codex example runner uses codex exec'
	require_pattern "$EXPERIMENT_CODEX_RUNNER" '--output-last-message' 'codex example runner captures last message'
	require_pattern "$EXPERIMENT_CODEX_RUNNER" '--all' 'codex example runner explicit batch mode'

	if [[ "$failures" -eq 0 ]]; then
		passed_fixtures+=('PROMPT-SELECTOR')
		output_artifacts+=("${PROMPT_SELECTOR#$ROOT_DIR/}")
		output_artifacts+=("${CODEX_EXAMPLE_RUNNER#$ROOT_DIR/}")
		output_artifacts+=('.codex/commands/arcanum-sigil-invoke-example-runner.md')
		output_artifacts+=('.codex/commands/invoke-example-next.md')
		output_artifacts+=('.codex/commands/invoke-example-run.md')
		record 'PASS: PROMPT-SELECTOR'
	fi
}

run_example_output_checks() {
	local output
	local count=0

	if [[ ! -d "$EXAMPLE_OUTPUTS_DIR" ]]; then
		record 'PASS: EXAMPLE-OUTPUTS (none present)'
		passed_fixtures+=('EXAMPLE-OUTPUTS')
		return 0
	fi

	while IFS= read -r output; do
		count=$((count + 1))
		output_name="$(basename "$output")"
		require_file "$output"
		if rg -q -- '^Saved the .*output to ' "$output"; then
			record "FAIL: $output_name is a save-summary, not an Invoke Result body"
			failed_checks+=("$output_name is a save-summary")
			add_anti_pattern_hit "$output_name is a save-summary instead of an Invoke Result body"
			add_quality_gap "output-contract" "severe" "$output_name is not a real artifact body" "${output#$ROOT_DIR/}"
			failures=$((failures + 1))
		fi
		require_pattern "$output" '## Invoke Result|## Invoke Validation Fixture Result' "$output_name output heading"
		require_pattern "$output" 'Mode:' "$output_name output mode"
		require_pattern "$output" 'Phase status:' "$output_name output phase status"
		if [[ "$output_name" == architecture-*.output.md ]]; then
			require_pattern "$output" '## Architecture Plan' "$output_name architecture artifact"
			require_pattern "$output" '## Source Contracts' "$output_name source contracts"
			require_pattern "$output" '## View 1: Context View' "$output_name context view"
			require_pattern "$output" '## View 2: High-Level Structure View' "$output_name high-level view"
			require_pattern "$output" '## View 3: Low-Level Components View' "$output_name low-level view"
			require_pattern "$output" '## View 4: Workflow Process View' "$output_name workflow view"
			require_pattern "$output" '## View 5: Decision Flow View' "$output_name decision view"
			require_pattern "$output" '## View 6: Dependency Interface View' "$output_name dependency view"
			require_pattern "$output" '## Dependency And Interface Rules' "$output_name dependency rules"
			require_pattern "$output" '## Decision Log' "$output_name decision log"
			require_pattern "$output" '## Risks' "$output_name risks"
			require_pattern "$output" '## Downstream Planning Notes' "$output_name downstream notes"
			require_pattern "$output" '## Design Transport Notes' "$output_name design transport notes"
			require_pattern "$output" '## Gate Result' "$output_name gate result"
		fi
		output_artifacts+=("${output#$ROOT_DIR/}")
	done < <(find "$EXAMPLE_OUTPUTS_DIR" -maxdepth 1 -type f -name '*.output.md' | sort)

	if [[ "$failures" -eq 0 ]]; then
		passed_fixtures+=('EXAMPLE-OUTPUTS')
		record "PASS: EXAMPLE-OUTPUTS ($count checked)"
	fi
}

run_fixture() {
	local fixture="$1"
	local expected="$2"
	local status_pattern="$3"
	local output_status_pattern="$4"
	local mode_contract_path="$5"
	local mode_contract_output="$6"
	local contract_pattern="$7"
	local label="$8"

	require_file "$fixture"
	require_file "$expected"
	require_pattern "$fixture" "$status_pattern" "$label fixture expected status"
	require_pattern "$expected" '## Invoke Validation Fixture Result' "$label expected output heading"
	require_pattern "$expected" "$output_status_pattern" "$label expected output status"
	require_pattern "$expected" 'User request:' "$label expected user request"
	require_pattern "$expected" "$mode_contract_output" "$label expected mode contract"
	require_pattern "$expected" 'Next route:' "$label expected next route"
	require_pattern "$mode_contract_path" "$contract_pattern" "$label contract gate"

	if [[ "$failures" -eq 0 ]]; then
		passed_fixtures+=("$label")
		output_artifacts+=("${expected#$ROOT_DIR/}")
		record "PASS: $label"
	fi
}

run_integration_fixture() {
	local fixture="$1"
	local define_expected="$2"
	local design_expected="$3"
	local spec="$4"
	local glossary="$5"
	local transport="$6"
	local architecture="$7"
	local glossary_consistency="$8"
	local design_transport="$9"
	local label="${10}"
	local spec_name
	local glossary_name
	local transport_name
	local architecture_name
	local glossary_consistency_name
	local design_transport_name
	spec_name="$(basename "$spec")"
	glossary_name="$(basename "$glossary")"
	transport_name="$(basename "$transport")"
	architecture_name="$(basename "$architecture")"
	glossary_consistency_name="$(basename "$glossary_consistency")"
	design_transport_name="$(basename "$design_transport")"

	require_file "$fixture"
	require_file "$define_expected"
	require_file "$design_expected"
	require_file "$spec"
	require_file "$glossary"
	require_file "$transport"
	require_file "$architecture"
	require_file "$glossary_consistency"
	require_file "$design_transport"

	require_pattern "$fixture" 'End-to-end define-to-design handoff' "$label fixture scenario"
	require_pattern "$fixture" "$spec_name" "$label fixture spec reference"
	require_pattern "$fixture" "$glossary_name" "$label fixture glossary reference"
	require_pattern "$fixture" "$transport_name" "$label fixture transport reference"
	require_pattern "$fixture" "$architecture_name" "$label fixture architecture reference"
	require_pattern "$fixture" "$glossary_consistency_name" "$label fixture glossary consistency reference"
	require_pattern "$fixture" "$design_transport_name" "$label fixture design transport reference"

	require_pattern "$define_expected" 'Mode: define' "$label define mode"
	require_pattern "$define_expected" 'Phase status: pass' "$label define status"
	require_pattern "$define_expected" "$spec_name" "$label define output spec"
	require_pattern "$define_expected" "$glossary_name" "$label define output glossary"
	require_pattern "$define_expected" "$transport_name" "$label define output transport"
	require_pattern "$define_expected" 'Next route: design' "$label define next route"

	require_pattern "$design_expected" 'Mode: design' "$label design mode"
	require_pattern "$design_expected" 'Phase status: pass' "$label design status"
	require_pattern "$design_expected" "$architecture_name" "$label design output architecture"
	require_pattern "$design_expected" "$glossary_consistency_name" "$label design output glossary consistency"
	require_pattern "$design_expected" "$design_transport_name" "$label design output transport"
	require_pattern "$design_expected" 'Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface' "$label design six views"
	require_pattern "$design_expected" 'Glossary consistency: pass' "$label design glossary consistency"
	require_pattern "$design_expected" 'Next route: plan' "$label design next route"

	require_pattern "$spec" 'Mars rover maintenance log' "$label spec term maintenance log"
	require_pattern "$spec" 'daily inspection note' "$label spec term inspection note"
	require_pattern "$spec" 'component status' "$label spec term component status"
	require_pattern "$spec" 'operator decision' "$label spec term operator decision"
	require_pattern "$spec" 'unresolved repair question' "$label spec term repair question"

	require_pattern "$glossary" 'Mars rover maintenance log' "$label glossary term maintenance log"
	require_pattern "$glossary" 'daily inspection note' "$label glossary term inspection note"
	require_pattern "$glossary" 'component status' "$label glossary term component status"
	require_pattern "$glossary" 'operator decision' "$label glossary term operator decision"
	require_pattern "$glossary" 'unresolved repair question' "$label glossary term repair question"

	require_pattern "$transport" 'Definitions Transported' "$label transport definitions"
	require_pattern "$transport" 'component status' "$label transport term component status"
	require_pattern "$architecture" '## Context View' "$label architecture context view"
	require_pattern "$architecture" '## High-Level Structure View' "$label architecture high-level view"
	require_pattern "$architecture" '## Low-Level Components View' "$label architecture low-level view"
	require_pattern "$architecture" '## Workflow Process View' "$label architecture workflow view"
	require_pattern "$architecture" '## Decision Flow View' "$label architecture decision view"
	require_pattern "$architecture" '## Dependency Interface View' "$label architecture dependency view"
	require_pattern "$architecture" 'Mars rover maintenance log' "$label architecture glossary term maintenance log"
	require_pattern "$architecture" 'daily inspection note' "$label architecture glossary term inspection note"
	require_pattern "$architecture" 'component status' "$label architecture glossary term component status"
	require_pattern "$architecture" 'operator decision' "$label architecture glossary term operator decision"
	require_pattern "$architecture" 'unresolved repair question' "$label architecture glossary term repair question"
	require_pattern "$glossary_consistency" '## Verdict' "$label glossary consistency verdict heading"
	require_pattern "$glossary_consistency" 'pass' "$label glossary consistency pass"
	require_pattern "$design_transport" 'Design Context Transported' "$label design transport context"
	require_pattern "$DEFINE_CONTRACT" 'Define-stage transport appends stage reports' "$label define transport gate"
	require_pattern "$DESIGN_CONTRACT" 'approved define outputs' "$label design consumes define outputs"

	if [[ "$failures" -eq 0 ]]; then
		passed_fixtures+=("$label")
		output_artifacts+=("${define_expected#$ROOT_DIR/}")
		output_artifacts+=("${design_expected#$ROOT_DIR/}")
		output_artifacts+=("${architecture#$ROOT_DIR/}")
		output_artifacts+=("${glossary_consistency#$ROOT_DIR/}")
		output_artifacts+=("${design_transport#$ROOT_DIR/}")
		record "PASS: $label"
	fi
}

run_quality_antipattern_fixture() {
	local fixture="$1"
	local expected="$2"
	local label="$3"

	require_file "$fixture"
	require_file "$expected"

	require_pattern "$fixture" 'Quality Bar pass output' "$label quality pass scenario"
	require_pattern "$fixture" 'Quality Bar partial output' "$label quality partial scenario"
	require_pattern "$fixture" 'Quality Bar fail output' "$label quality fail scenario"
	require_pattern "$fixture" 'Anti-Pattern flag hit' "$label anti-pattern flag scenario"
	require_pattern "$fixture" 'Anti-Pattern block hit' "$label anti-pattern block scenario"
	require_pattern "$expected" 'QUALITY_BAR_STATUS=pass' "$label expected quality pass"
	require_pattern "$expected" 'QUALITY_BAR_STATUS=partial' "$label expected quality partial"
	require_pattern "$expected" 'QUALITY_BAR_STATUS=fail' "$label expected quality fail"
	require_pattern "$expected" 'ANTI_PATTERN_HITS_JSON=' "$label expected anti-pattern json"
	require_pattern "$expected" 'WORKFLOW_GAPS_JSON=' "$label expected workflow gaps json"
	require_pattern "$expected" 'reflection_trigger' "$label expected telemetry trigger"

	require_pattern "$DEFINE_CONTRACT" 'block on missing core goal or contradictory scope' "$label define quality missing goal"
	require_pattern "$DEFINE_CONTRACT" 'Candidate glossary promotion is never automatic' "$label define anti-pattern glossary promotion"
	require_pattern "$DESIGN_CONTRACT" 'Normal design blocks without approved define outputs unless discovery mode is explicitly approved' "$label design anti-pattern source approval"
	require_pattern "$DESIGN_CONTRACT" 'Design mode must not create work-pack tasks' "$label design anti-pattern deferred plan behavior"
	require_pattern "$DESIGN_CONTRACT" 'Spell and sigil lifecycle work routes to `spellcraft` or `sigil-development`' "$label design anti-pattern downstream mutation"

	if [[ "$failures" -eq 0 ]]; then
		passed_fixtures+=("$label")
		output_artifacts+=("${expected#$ROOT_DIR/}")
		record "PASS: $label"
	fi
}

run_plan_split_fixture() {
	local fixture="$1"
	local expected="$2"
	local label="$3"

	require_file "$fixture"
	require_file "$expected"

	require_pattern "$fixture" 'Phase status: `pass`' "$label fixture expected status"
	require_pattern "$fixture" 'Per-layer planning: L0, L1, L2, L3' "$label fixture per-layer expected"
	require_pattern "$expected" '## Invoke Validation Fixture Result' "$label expected output heading"
	require_pattern "$expected" 'Phase status: pass' "$label expected output status"
	require_pattern "$expected" 'User request:' "$label expected user request"
	require_pattern "$expected" 'Mode contract: arcanum/spells/invoke/plan.md' "$label expected mode contract"
	require_pattern "$expected" 'Work-pack: .*split' "$label expected split work-pack"
	require_pattern "$expected" 'Complexity: medium|Complexity: high' "$label expected complexity"
	require_pattern "$expected" 'Per-layer planning: L0, L1, L2, L3' "$label expected per-layer planning"
	require_pattern "$expected" 'Implementation detail: task specs complete' "$label expected implementation detail status"
	require_pattern "$expected" 'Smallest working units: complete' "$label expected SWU status"
	require_pattern "$expected" 'Execution-pack|execution-pack' "$label expected execution-pack handoff"
	require_pattern "$expected" '## Per-Layer Planning Slices' "$label per-layer slice heading"
	require_pattern "$expected" '## Implementation Detail Specs' "$label implementation detail specs heading"
	require_pattern "$expected" '## Smallest Working Units' "$label SWU heading"
	require_pattern "$expected" '\| L0 \|' "$label L0 slice"
	require_pattern "$expected" '\| L1 \|' "$label L1 slice"
	require_pattern "$expected" '\| L2 \|' "$label L2 slice"
	require_pattern "$expected" '\| L3 \|' "$label L3 slice"
	require_pattern "$expected" 'Validation Evidence' "$label validation evidence column"
	require_pattern "$expected" 'Promotion Criteria' "$label promotion criteria column"
	require_pattern "$expected" 'Inputs \| Outputs \| Implementation Notes \| Edge Cases \| Validation Evidence' "$label implementation detail columns"
	require_pattern "$expected" 'Classify item category first, then apply urgency triage' "$label algorithm detail example"
	require_pattern "$expected" 'SWU ID \| Parent Task \| Goal \| Write Scope \| Acceptance Evidence \| Verification Command' "$label SWU board columns"
	require_pattern "$expected" 'SWU-MHS-001' "$label first SWU id"
	require_pattern "$expected" 'TASK-L1-review' "$label SWU parent task"
	require_pattern "$expected" 'run category classification fixture' "$label SWU verification command"
	require_pattern "$expected" 'Next route: task-session' "$label expected next route"
	require_pattern "$PLAN_CONTRACT" 'Medium and high complexity plans must include explicit per-layer planning slices' "$label contract per-layer gate"
	require_pattern "$PLAN_CONTRACT" 'Medium/high complexity plans must include implementation-detail specs for execution tasks' "$label contract implementation detail gate"
	require_pattern "$PLAN_CONTRACT" 'Medium/high complexity plans must include SWU decomposition for non-exempt execution tasks' "$label contract SWU gate"
	require_pattern "$PLAN_CONTRACT" 'Each SWU maps to exactly one parent task' "$label contract SWU parent gate"
	require_pattern "$PLAN_CONTRACT" 'Algorithmic or domain-logic tasks must include algorithm steps or pseudocode' "$label contract algorithm detail gate"
	require_pattern "$PLAN_CONTRACT" 'Layer promotion must cite evidence from the previous layer' "$label contract promotion evidence"

	if [[ "$failures" -eq 0 ]]; then
		passed_fixtures+=("$label")
		output_artifacts+=("${expected#$ROOT_DIR/}")
		record "PASS: $label"
	fi
}

run_plan_integration_fixture() {
	local fixture="$1"
	local define_expected="$2"
	local design_expected="$3"
	local plan_expected="$4"
	local spec="$5"
	local glossary="$6"
	local architecture="$7"
	local implementation_plan="$8"
	local layering="$9"
	local work_pack="${10}"
	local plan_transport="${11}"
	local label="${12}"
	local implementation_plan_name
	local layering_name
	local work_pack_name
	local plan_transport_name
	implementation_plan_name="$(basename "$implementation_plan")"
	layering_name="$(basename "$layering")"
	work_pack_name="$(basename "$work_pack")"
	plan_transport_name="$(basename "$plan_transport")"

	require_file "$fixture"
	require_file "$define_expected"
	require_file "$design_expected"
	require_file "$plan_expected"
	require_file "$spec"
	require_file "$glossary"
	require_file "$architecture"
	require_file "$implementation_plan"
	require_file "$layering"
	require_file "$work_pack"
	require_file "$plan_transport"

	require_pattern "$fixture" 'define-to-design-to-plan handoff' "$label fixture scenario"
	require_pattern "$fixture" "$implementation_plan_name" "$label fixture implementation plan reference"
	require_pattern "$fixture" "$layering_name" "$label fixture layering reference"
	require_pattern "$fixture" "$work_pack_name" "$label fixture work-pack reference"
	require_pattern "$fixture" "$plan_transport_name" "$label fixture plan transport reference"

	require_pattern "$define_expected" 'Mode: define' "$label define mode"
	require_pattern "$define_expected" 'Next route: design' "$label define next route"
	require_pattern "$design_expected" 'Mode: design' "$label design mode"
	require_pattern "$design_expected" 'Next route: plan' "$label design next route"

	require_pattern "$plan_expected" 'Mode: plan' "$label plan mode"
	require_pattern "$plan_expected" 'Phase status: pass' "$label plan status"
	require_pattern "$plan_expected" "$implementation_plan_name" "$label plan output implementation plan"
	require_pattern "$plan_expected" "$layering_name" "$label plan output layering"
	require_pattern "$plan_expected" "$work_pack_name" "$label plan output work-pack"
	require_pattern "$plan_expected" "$plan_transport_name" "$label plan output transport"
	require_pattern "$plan_expected" 'Implementation layering: .*global L0-L3 decision boundaries' "$label plan global layering"
	require_pattern "$plan_expected" 'Per-layer planning: compact' "$label plan compact layer mapping"
	require_pattern "$plan_expected" 'Validation strategy:' "$label plan validation strategy"
	require_pattern "$plan_expected" 'preserve define glossary terms' "$label plan authority boundary"
	require_pattern "$plan_expected" 'Next route: task-session' "$label plan next route"

	require_pattern "$implementation_plan" '## Source Design References' "$label implementation plan source refs"
	require_pattern "$implementation_plan" 'INV-INTEGRATION-DEFINE-DESIGN-001.architecture.md' "$label implementation plan architecture ref"
	require_pattern "$implementation_plan" 'daily inspection note' "$label implementation plan glossary term"
	require_pattern "$implementation_plan" '## Validation Strategy' "$label implementation plan validation"
	require_pattern "$implementation_plan" '## Implementation Detail Specs' "$label implementation detail specs"
	require_pattern "$implementation_plan" 'Implementation Notes' "$label implementation detail notes column"
	require_pattern "$layering" '\| L0 \(POC\) \|' "$label layering L0"
	require_pattern "$layering" '\| L1 \|' "$label layering L1"
	require_pattern "$layering" '\| L2 \|' "$label layering L2"
	require_pattern "$layering" '\| L3 \|' "$label layering L3"
	require_pattern "$work_pack" 'Compact Layer Mapping' "$label work-pack compact mapping"
	require_pattern "$work_pack" 'outputMode \| single-file' "$label work-pack single-file"
	require_pattern "$plan_transport" 'Plan Context Transported' "$label plan transport context"
	require_pattern "$plan_transport" 'No source code or upstream design mutation occurred' "$label plan non-mutating"
	require_pattern "$PLAN_CONTRACT" 'Plan mode must not execute tasks' "$label contract no execution"

	if [[ "$failures" -eq 0 ]]; then
		passed_fixtures+=("$label")
		output_artifacts+=("${plan_expected#$ROOT_DIR/}")
		output_artifacts+=("${implementation_plan#$ROOT_DIR/}")
		output_artifacts+=("${layering#$ROOT_DIR/}")
		output_artifacts+=("${work_pack#$ROOT_DIR/}")
		output_artifacts+=("${plan_transport#$ROOT_DIR/}")
		record "PASS: $label"
	fi
}

require_file "$DEFINE_CONTRACT"
require_file "$DESIGN_CONTRACT"
require_file "$PLAN_CONTRACT"
require_file "$TEMPLATE_TASKS"
require_file "$EXPERIMENT_REGIMES"
require_pattern "$DEFINE_CONTRACT" 'Status: implemented \(L0 contract, candidate template-family scaffold coverage\)' 'define contract status'
require_pattern "$DEFINE_CONTRACT" 'block on missing core goal or contradictory scope' 'define missing-goal block'
require_pattern "$DEFINE_CONTRACT" 'flag when no eligible template exists and candidate creation is unapproved' 'define candidate-template flag'
require_pattern "$DEFINE_CONTRACT" 'Candidate glossary promotion is never automatic' 'define glossary promotion gate'
require_pattern "$DEFINE_CONTRACT" 'Define-stage transport appends stage reports' 'define transport coverage'
require_pattern "$DESIGN_CONTRACT" 'Status: implemented \(L1 contract, validation examples pending\)' 'design contract status'
require_pattern "$DESIGN_CONTRACT" 'Context view' 'design six-view coverage'
require_pattern "$DESIGN_CONTRACT" 'Glossary consistency' 'design glossary coverage'
require_pattern "$DESIGN_CONTRACT" 'Design-stage transport' 'design transport coverage'
require_pattern "$PLAN_CONTRACT" 'Status: implemented \(L2 contract, per-layer planning evidence pending\)' 'plan contract status'
require_pattern "$PLAN_CONTRACT" 'Plan blocks without approved design outputs and source design refs' 'plan missing design block'
require_pattern "$PLAN_CONTRACT" 'Low complexity plans must include compact layer mapping' 'plan low compact mapping'
require_pattern "$PLAN_CONTRACT" 'Medium/high complexity plans must include explicit L0-L3 per-layer planning slices' 'plan medium high per-layer gate'
require_pattern "$PLAN_CONTRACT" 'Medium/high complexity plans must include implementation-detail specs for execution tasks' 'plan medium high implementation detail gate'
require_pattern "$PLAN_CONTRACT" 'Task descriptions that only say to implement a bundle' 'plan vague task gate'
require_pattern "$PLAN_CONTRACT" 'Plan-stage transport appends stage reports' 'plan transport coverage'

run_template_task_matrix "$TEMPLATE_TASKS"
run_prompt_selector_checks
run_example_output_checks

run_fixture \
	"$FIXTURE_DIR/INV-DEFINE-PASS-001.md" \
	"$FIXTURE_DIR/INV-DEFINE-PASS-001.expected.md" \
	'Phase status: `pass`' \
	'Phase status: pass' \
	"$DEFINE_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/define.md' \
	'Module Formulae' \
	'INV-DEFINE-PASS-001'

run_fixture \
	"$FIXTURE_DIR/INV-DEFINE-BLOCK-001.md" \
	"$FIXTURE_DIR/INV-DEFINE-BLOCK-001.expected.md" \
	'Phase status: `block`' \
	'Phase status: block' \
	"$DEFINE_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/define.md' \
	'block on missing core goal or contradictory scope' \
	'INV-DEFINE-BLOCK-001'

run_fixture \
	"$FIXTURE_DIR/INV-DEFINE-FLAG-001.md" \
	"$FIXTURE_DIR/INV-DEFINE-FLAG-001.expected.md" \
	'Phase status: `flag`' \
	'Phase status: flag' \
	"$DEFINE_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/define.md' \
	'flag when no eligible template exists and candidate creation is unapproved' \
	'INV-DEFINE-FLAG-001'

run_fixture \
	"$FIXTURE_DIR/INV-DEFINE-GLOSSARY-001.md" \
	"$FIXTURE_DIR/INV-DEFINE-GLOSSARY-001.expected.md" \
	'Phase status: `pass`' \
	'Phase status: pass' \
	"$DEFINE_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/define.md' \
	'Candidate glossary promotion is never automatic' \
	'INV-DEFINE-GLOSSARY-001'

run_fixture \
	"$FIXTURE_DIR/INV-DESIGN-PASS-001.md" \
	"$FIXTURE_DIR/INV-DESIGN-PASS-001.expected.md" \
	'Phase status: `pass`' \
	'Phase status: pass' \
	"$DESIGN_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/design.md' \
	'Module Formulae architecture profile' \
	'INV-DESIGN-PASS-001'

run_fixture \
	"$FIXTURE_DIR/INV-DESIGN-BLOCK-001.md" \
	"$FIXTURE_DIR/INV-DESIGN-BLOCK-001.expected.md" \
	'Phase status: `block`' \
	'Phase status: block' \
	"$DESIGN_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/design.md' \
	'Normal design blocks without approved define outputs unless discovery mode is explicitly approved' \
	'INV-DESIGN-BLOCK-001'

run_fixture \
	"$FIXTURE_DIR/INV-DESIGN-FLAG-001.md" \
	"$FIXTURE_DIR/INV-DESIGN-FLAG-001.expected.md" \
	'Phase status: `flag`' \
	'Phase status: flag' \
	"$DESIGN_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/design.md' \
	'`research` family' \
	'INV-DESIGN-FLAG-001'

run_fixture \
	"$FIXTURE_DIR/INV-DESIGN-HANDOFF-001.md" \
	"$FIXTURE_DIR/INV-DESIGN-HANDOFF-001.expected.md" \
	'Phase status: `pass`' \
	'Phase status: pass' \
	"$DESIGN_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/design.md' \
	'Spell and sigil lifecycle work routes to `spellcraft` or `sigil-development`' \
	'INV-DESIGN-HANDOFF-001'

run_fixture \
	"$FIXTURE_DIR/INV-PLAN-PASS-001.md" \
	"$FIXTURE_DIR/INV-PLAN-PASS-001.expected.md" \
	'Phase status: `pass`' \
	'Phase status: pass' \
	"$PLAN_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/plan.md' \
	'Low complexity plans must include compact layer mapping' \
	'INV-PLAN-PASS-001'

run_plan_split_fixture \
	"$FIXTURE_DIR/INV-PLAN-SPLIT-001.md" \
	"$FIXTURE_DIR/INV-PLAN-SPLIT-001.expected.md" \
	'INV-PLAN-SPLIT-001'

run_fixture \
	"$FIXTURE_DIR/INV-PLAN-BLOCK-001.md" \
	"$FIXTURE_DIR/INV-PLAN-BLOCK-001.expected.md" \
	'Phase status: `block`' \
	'Phase status: block' \
	"$PLAN_CONTRACT" \
	'Mode contract: arcanum/spells/invoke/plan.md' \
	'Plan blocks without approved design outputs and source design refs' \
	'INV-PLAN-BLOCK-001'

run_integration_fixture \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.define.expected.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.design.expected.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.spec.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.glossary.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.define-transport.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.architecture.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.glossary-consistency.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.design-transport.md" \
	'INV-INTEGRATION-DEFINE-DESIGN-001'

run_plan_integration_fixture \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.define.expected.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.design.expected.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.plan.expected.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.spec.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.glossary.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-001.architecture.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.implementation-plan.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.implementation-layering.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.work-pack.md" \
	"$FIXTURE_DIR/INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.plan-transport.md" \
	'INV-INTEGRATION-DEFINE-DESIGN-PLAN-001'

run_quality_antipattern_fixture \
	"$FIXTURE_DIR/INV-QUALITY-ANTI-PATTERN-001.md" \
	"$FIXTURE_DIR/INV-QUALITY-ANTI-PATTERN-001.expected.md" \
	'INV-QUALITY-ANTI-PATTERN-001'

if [[ "$failures" -gt 0 ]]; then
	record "RESULT: block ($failures failure(s))"
	write_report "block"
	printf 'REPORT: %s\n' "$RUN_REPORT"
	exit 1
fi

record 'RESULT: pass'
write_report "pass"
printf 'REPORT: %s\n' "$RUN_REPORT"
