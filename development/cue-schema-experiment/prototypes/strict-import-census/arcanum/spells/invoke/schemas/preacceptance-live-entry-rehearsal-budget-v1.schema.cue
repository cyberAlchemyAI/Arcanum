// InvokePreacceptanceLiveEntryRehearsalBudgetV1
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/preacceptance-live-entry-rehearsal-budget/1-0-0")
	close({
		schema_version!:                             "invoke.preacceptance-live-entry-rehearsal-budget.v1"
		derivation_version!:                         "task-session.sequential-live-entry-workload.v1"
		invocation_count!:                           int & >=3 & <=7
		declared_invocation_timeout_seconds!:        int & >=3 & <=4200
		failure_stop_after!:                         "readiness" | "selection" | "fast-entry" | "context" | "admission"
		failure_stop_invocation_timeout_seconds!:    int & >=2 & <=3600
		exact_input_ref_occurrence_count!:           int & >=1 & <=16384
		unique_input_ref_count!:                     int & >=1 & <=16384
		unique_input_size_bytes!:                    int & >=1 & <=2147483648
		exact_output_path_count!:                    int & >=3 & <=1024
		workload_overhead_seconds!:                  int & >=45 & <=590
		success_coordinator_timeout_seconds!:        int & >=1 & <=3600
		failure_stop_coordinator_timeout_seconds!:   int & >=1 & <=3600
		terminalization_invocation_count!:           3
		terminalization_invocation_timeout_seconds!: 60
		stage_timeout_seconds!:                      int & >=1 & <=3600
		hard_maximum_seconds!:                       3600
		budget_digest!:                              =~"^[a-f0-9]{64}$"
	})
}
