// InvokeCapabilityStatusRequest
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/capability-status-request/1-0-0")
	close({
		schema_version!: "invoke.capability-status.request.v1"
		mode!:           "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		artifact_receipt?: matchN(1, [#artifact_receipt, null])
		registry_receipt?: matchN(1, [#registry_receipt, null])
		material_package_receipt?: null | {}
		runtime_receipt?: matchN(1, [#runtime_receipt, null])
	})

	#artifact_receipt: close({
		receipt_id!: strings.MinRunes(1)
		axis!:       "artifact_authored"
		mode!:       "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		status!:     "pass" | "flag" | "block"
		evidence!: list.UniqueItems() & [_, ...] & [...strings.MinRunes(1)]
		producer_receipt?: {}
		producer_admission_receipt?: {}
	})

	#pass_evidence: close({
		status!:   "pass"
		evidence!: strings.MinRunes(1)
	})

	#registry_receipt: close({
		receipt_id!:               strings.MinRunes(1)
		axis!:                     "registry_released"
		mode!:                     "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		status!:                   "released"
		owner!:                    strings.MinRunes(1)
		capability_sha256!:        =~"^[a-f0-9]{64}$"
		deterministic_validation!: #pass_evidence
		live_regime!:              #pass_evidence
	})

	#runtime_receipt: close({
		receipt_id!:              strings.MinRunes(1)
		axis!:                    "mutation_runtime_ready"
		mode!:                    "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		status!:                  "ready"
		capability_sha256!:       =~"^[a-f0-9]{64}$"
		material_package_id!:     strings.MinRunes(1)
		material_package_digest!: =~"^[a-f0-9]{64}$"
		gates!: [_, ...] & [...close({
			gate!:     strings.MinRunes(1)
			status!:   "pass" | "block"
			evidence!: strings.MinRunes(1)
		})]
	})
}
