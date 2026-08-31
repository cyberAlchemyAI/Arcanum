// Whisper Editorial Run Receipt
//
// Shape contract for one Whisper composition run. It records independent
// evidence and computed decisions without judging editorial semantics or
// decision-policy consistency.
package prototype

import (
	"list"
	"strings"
	"time"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/spells/whisper/schemas/editorial-run-receipt.schema.json")
	matchN(9, [matchIf({
		approval_records!: null | bool | number | string | [_, ...] | {}
	}, {
		selected_approval_id?: #stableId
	}, _) & {}, matchIf({
		approval_records!: null | bool | number | string | list.MaxItems(0) | {}
	}, {
		selected_approval_id?: null
	}, _) & {}, matchIf({
		comprehension_records!: null | bool | number | string | [_, ...] | {}
	}, {
		selected_comprehension_id?: #stableId
	}, _) & {}, matchIf({
		comprehension_records!: null | bool | number | string | list.MaxItems(0) | {}
	}, {
		selected_comprehension_id?: null
	}, _) & {}, matchIf({
		evidence_axes!: null | bool | number | string | [...] | {
			editorial_language_audition!: null | bool | number | string | [...] | {
				status!: "pass" | "flag" | "block"
			}
		}
	}, {
		approval_records?: null | bool | number | string | [_, ...] | {}
		selected_approval_id?: #stableId
	}, _) & {}, matchIf({
		evidence_axes!: null | bool | number | string | [...] | {
			operator_or_reader_comprehension!: null | bool | number | string | [...] | {
				status!: "pass" | "flag" | "block"
			}
		}
	}, {
		comprehension_records?: null | bool | number | string | [_, ...] | {}
		selected_comprehension_id?: #stableId
	}, _) & {}, matchIf({
		transport_profile!: null | bool | number | string | [...] | {
			editorial_approval_required!: true
		}
	}, {
		evidence_axes?: null | bool | number | string | [...] | {
			editorial_language_audition?: matchN(0, [null | bool | number | string | [...] | {
				status!: "not_required"
			}])
		}
	}, _) & {}, matchIf({
		transport_profile!: null | bool | number | string | [...] | {
			comprehension_gate!: null | bool | number | string | [...] | {
				required!: true
			}
		}
	}, {
		evidence_axes?: null | bool | number | string | [...] | {
			operator_or_reader_comprehension?: matchN(0, [null | bool | number | string | [...] | {
				status!: "not_required"
			}])
		}
	}, _) & {}, matchIf({
		transport_profile!: null | bool | number | string | [...] | {
			post_apply_review_required!: true
		}
	}, {
		post_apply_editorial_verification?: matchN(0, [null | bool | number | string | [...] | {
			status!: "not_required"
		}])
	}, _) & {}]) & close({
		schema_version!:       "whisper.editorial_run_receipt.v0.1"
		run_id!:               #stableId
		target_id!:            #stableId
		created_at!:           #timestamp
		transport_profile!:    #transportProfile
		audience!:             #audience
		intent!:               #intent
		composition_plan_ref!: #nonEmptyString
		change_manifest_ref!:  #nonEmptyString
		artifact_manifest!:    #artifactManifest
		surface_manifest!:     #surfaceManifest
		approval_records!: list.UniqueItems() & [...#approvalRecord]
		selected_approval_id!: matchN(1, [#stableId, null])
		comprehension_records!: list.UniqueItems() & [...#comprehensionRecord]
		selected_comprehension_id!: matchN(1, [#stableId, null])
		evidence_axes!:                     #evidenceAxes
		post_apply_editorial_verification!: #postApplyEvidence
		requested!:                         #requestedOutcome
		computed_decisions!:                #computedDecisions
		correction_refs!: list.UniqueItems() & [...#stableId]
		observability_refs!: list.UniqueItems() & [...#nonEmptyString]
		residue!: [...#residueItem]
	})

	#approvalRecord: close({
		approval_id!:     #stableId
		approval_kind!:   "editorial_audition"
		prompt_id!:       #stableId
		approver_kind!:   "operator" | "intended_reader" | "editor"
		transport_id!:    #stableId
		audience_id!:     #stableId
		artifact_sha256!: #sha256
		surface_sha256!:  #sha256
		decision!:        "approved" | "rejected"
		recorded_at!:     #timestamp
	})

	#artifactManifest: close({
		artifact_ref!:      #nonEmptyString
		auditioned_sha256!: #sha256
		applied_sha256!: matchN(1, [#sha256, null])
	})

	#audience: close({
		audience_id!: #stableId
		mode!:        "newcomer" | "experienced" | "mixed"
	})

	#comprehensionAnswer: close({
		question_id!:  #stableId
		response_ref!: #nonEmptyString
	})

	#comprehensionEvidenceAxis: matchN(1, [close({
		status!:            #humanEvidenceStatus
		artifact_sha256!:   #sha256
		surface_sha256!:    #sha256
		comprehension_ref!: #stableId
		receipts!: list.UniqueItems() & [...#nonEmptyString] & [_, ...]
	}), close({
		status!:   "absent" | "not_required"
		receipts!: list.MaxItems(0)
	})])

	#comprehensionRecord: close({
		comprehension_id!: #stableId
		reviewer_kind!:    "operator" | "intended_reader"
		transport_id!:     #stableId
		audience_id!:      #stableId
		artifact_sha256!:  #sha256
		surface_sha256!:   #sha256
		question_ids!: list.UniqueItems() & [...#stableId] & [_, ...]
		answers!: list.UniqueItems() & [...#comprehensionAnswer] & [_, ...]
		outcome!:     "understood" | "partially_understood" | "not_understood"
		recorded_at!: #timestamp
	})

	#computedDecisions: close({
		generation!: #decision
		status!:     #statusDecision
	})

	#decision: close({
		decision!: "allow" | "block"
		reasons!: list.UniqueItems() & [...#stableId]
	})

	#editorialEvidenceAxis: matchN(1, [close({
		status!:          #humanEvidenceStatus
		artifact_sha256!: #sha256
		surface_sha256!:  #sha256
		approval_ref!:    #stableId
		receipts!: list.UniqueItems() & [...#nonEmptyString] & [_, ...]
	}), close({
		status!:   "absent" | "not_required"
		receipts!: list.MaxItems(0)
	})])

	#evidenceAxes: close({
		source_and_structure_validation!:  #machineEvidenceAxis
		editorial_language_audition!:      #editorialEvidenceAxis
		operator_or_reader_comprehension!: #comprehensionEvidenceAxis
		implementation_render_validation!: #machineEvidenceAxis
	})

	#evidenceStatus: "pass" | "flag" | "block" | "absent"

	#humanEvidenceStatus: "pass" | "flag" | "block"

	#intent: close({
		intent_id!: #stableId
		state!:     "forming" | "volatile" | "frozen"
		correction_refs!: list.UniqueItems() & [...#stableId]
	})

	#machineEvidenceAxis: matchN(2, [matchIf({
		status!: "absent"
	}, {
		receipts?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "pass" | "flag" | "block"
	}, {
		receipts?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		status!: #evidenceStatus
		receipts!: list.UniqueItems() & [...#nonEmptyString]
	})

	#nonEmptyString: strings.MinRunes( 1)

	#postApplyEvidence: matchN(1, [close({
		review_id!:       #stableId
		status!:          #humanEvidenceStatus
		reviewer_kind!:   "operator" | "intended_reader" | "editor"
		artifact_sha256!: #sha256
		surface_sha256!:  #sha256
		producer_stage!:  #stableId
		review_stage!:    "post_apply_editorial_verification"
		recorded_at!:     #timestamp
	}), close({
		status!: "absent" | "not_required"
	})])

	#requestedOutcome: close({
		output_kind!: "bounded-audition" | "bounded-trial" | "full-derivative"
		status!:      "pass" | "flag" | "block"
	})

	#residueItem: {
		code!:    #stableId
		message!: #nonEmptyString
		owner?:   #nonEmptyString
		...
	}

	#sha256: =~"^[a-f0-9]{64}$"

	#stableId: =~"^[A-Za-z0-9][A-Za-z0-9._:/-]*$"

	#statusDecision: close({
		status_ceiling!: "pass" | "flag" | "block"
		final_status!:   "pass" | "flag" | "block"
		reasons!: list.UniqueItems() & [...#stableId]
	})

	#surfaceItem: close({
		block_id!:        #stableId
		role!:            #stableId
		source_selector!: #nonEmptyString
		text_sha256!:     #sha256
	})

	#surfaceManifest: close({
		surface_id!:      #stableId
		artifact_ref!:    #nonEmptyString
		artifact_sha256!: #sha256
		selection_kind!:  "source_order_role_set" | "explicit_manifest"
		items!: list.UniqueItems() & [...#surfaceItem] & [_, ...]
		surface_sha256!: #sha256
	})

	#timestamp: time.Time

	#transportProfile: close({
		transport_id!:                #stableId
		proof_status!:                "proven" | "candidate" | "unproven"
		editorial_approval_required!: bool
		comprehension_gate!: matchIf({
			required!: true
		}, {
			question_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {} & close({
			required!: bool
			question_ids!: list.UniqueItems() & [...#stableId]
		})
		post_apply_review_required!: bool
		derivative_policy!: close({
			full_generation_requires!: list.UniqueItems() & [..."intent_frozen" | "editorial_audition_approved" | "surface_accounted"] & [_, ...]
		})
	})
}
