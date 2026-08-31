// FastExecutionEntryRequest
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session/fast-execution-entry-request/1-0-0")
	close({
		schema_version!: "1.0.0"
		execution_policy!: {}
		execution_entry!: {}
		execution_binding!: {}
		selected_unit!: close({
			work_pack_id!: strings.MinRunes( 1)
			swu_id!:       strings.MinRunes( 1)
		})
		authority_effect!: "none"
	})
}
