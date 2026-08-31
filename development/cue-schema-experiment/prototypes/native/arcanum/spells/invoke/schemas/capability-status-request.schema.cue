// InvokeCapabilityStatusRequest
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/capability-status-request/1-0-0")
	close({
		artifact_receipt?: matchN(1, [close({
			axis!: "artifact_authored"
			evidence!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			mode!: "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
			producer_admission_receipt?: {}
			producer_receipt?: {}
			receipt_id!: strings.MinRunes(1)
			status!:     "pass" | "flag" | "block"
		}), null])
		material_package_receipt?: null | {}
		mode!: "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		registry_receipt?: matchN(1, [close({
			axis!:              "registry_released"
			capability_sha256!: =~"^[a-f0-9]{64}$"
			deterministic_validation!: close({
				evidence!: strings.MinRunes(1)
				status!:   "pass"
			})
			live_regime!: close({
				evidence!: strings.MinRunes(1)
				status!:   "pass"
			})
			mode!:       "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
			owner!:      strings.MinRunes(1)
			receipt_id!: strings.MinRunes(1)
			status!:     "released"
		}), null])
		runtime_receipt?: matchN(1, [close({
			axis!:              "mutation_runtime_ready"
			capability_sha256!: =~"^[a-f0-9]{64}$"
			gates!: [...close({
				evidence!: strings.MinRunes(1)
				gate!:     strings.MinRunes(1)
				status!:   "pass" | "block"
			})] & [_, ...]
			material_package_digest!: =~"^[a-f0-9]{64}$"
			material_package_id!:     strings.MinRunes(1)
			mode!:                    "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
			receipt_id!:              strings.MinRunes(1)
			status!:                  "ready"
		}), null])
		schema_version!: "invoke.capability-status.request.v1"
	})

	#artifact_receipt: close({
		axis!: "artifact_authored"
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		mode!: "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		producer_admission_receipt?: {}
		producer_receipt?: {}
		receipt_id!: strings.MinRunes(1)
		status!:     "pass" | "flag" | "block"
	})

	#pass_evidence: close({
		evidence!: strings.MinRunes(1)
		status!:   "pass"
	})

	#registry_receipt: close({
		axis!:              "registry_released"
		capability_sha256!: =~"^[a-f0-9]{64}$"
		deterministic_validation!: close({
			evidence!: strings.MinRunes(1)
			status!:   "pass"
		})
		live_regime!: close({
			evidence!: strings.MinRunes(1)
			status!:   "pass"
		})
		mode!:       "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		owner!:      strings.MinRunes(1)
		receipt_id!: strings.MinRunes(1)
		status!:     "released"
	})

	#runtime_receipt: close({
		axis!:              "mutation_runtime_ready"
		capability_sha256!: =~"^[a-f0-9]{64}$"
		gates!: [...close({
			evidence!: strings.MinRunes(1)
			gate!:     strings.MinRunes(1)
			status!:   "pass" | "block"
		})] & [_, ...]
		material_package_digest!: =~"^[a-f0-9]{64}$"
		material_package_id!:     strings.MinRunes(1)
		mode!:                    "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		receipt_id!:              strings.MinRunes(1)
		status!:                  "ready"
	})
}
