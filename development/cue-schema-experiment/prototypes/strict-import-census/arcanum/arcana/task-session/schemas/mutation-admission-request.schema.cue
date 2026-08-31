// TaskSessionMutationAdmissionRequest
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session/mutation-admission-request/1-3-0")
	matchN(3, [matchIf({
		schemaVersion!: "1.3.0"
	}, {
		transientOutputs!: _
	}, matchN(0, [null | bool | number | string | [...] | {
		transientOutputs!: _
	}]) & {}) & {}, matchIf({
		executionMode!: "routed-mutation" | "reusable-mutation"
	}, matchN(1, [{
		materialWrites?: null | bool | number | string | [_, ...] | {}
		materialPackage!:       _
		materialReceipt!:       _
		producerReceiptSchema!: _
	}, matchN(0, [matchN(>=1, [null | bool | number | string | [...] | {
		materialPackage!: _
	}, null | bool | number | string | [...] | {
		materialReceipt!: _
	}, null | bool | number | string | [...] | {
		producerReceiptSchema!: _
	}])]) & {
		materialWrites?: null | bool | number | string | list.MaxItems(0) | {}
		executionOutputs?: null | bool | number | string | [_, ...] | {}
	}]) & {
		taskId!:             _
		swuId!:              _
		controlArtifacts!:   _
		dependencyFrontier!: _
		materialWrites!:     _
		executionOutputs!:   _
		allowedWrites!:      _
		validationCommands!: _
		lifecycleOwner!:     _
		authorityClass!:     _
		publicationClass!:   _
	}, _) & {}, matchIf({
		admissionProfile!: "plan-once-selected-unit"
	}, {
		executionMode?: "routed-mutation" | "reusable-mutation"
		planAdmission!: _
	}, _) & {}]) & close({
		schemaVersion!:    "1.2.0" | "1.3.0"
		admissionProfile?: "plan-once-selected-unit"
		executionMode!:    "routed-mutation" | "reusable-mutation" | "standalone-nonmutating"
		taskId?:           strings.MinRunes( 1)
		swuId?:            strings.MinRunes( 1)
		controlArtifacts?: [_, _, _, ...] & [...#controlArtifact]
		dependencyFrontier?: [...#dependency]
		materialPackage?:       #exactArtifactRef
		materialReceipt?:       #exactArtifactRef
		producerReceiptSchema?: #exactArtifactRef
		materialWrites?: list.UniqueItems() & [...strings.MinRunes( 1)]
		executionOutputs?: list.UniqueItems() & [...strings.MinRunes( 1)]
		transientOutputs?: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		allowedWrites?: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		validationCommands?: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		lifecycleOwner?:   strings.MinRunes( 1)
		authorityClass?:   "public" | "private"
		publicationClass?: "public" | "private" | "internal"
		planAdmission?:    #planAdmission
	})

	#baselineEntry: matchN(2, [matchIf({
		state?: "absent"
	}, {
		sha256?:    null
		sizeBytes?: null
	}, _) & {}, matchIf({
		state?: "present"
	}, {
		sha256?:    =~"^[a-f0-9]{64}$"
		sizeBytes?: int & >=0
	}, _) & {}]) & close({
		path!:      strings.MinRunes( 1)
		state!:     "absent" | "present"
		sha256!:    null | =~"^[a-f0-9]{64}$"
		sizeBytes!: null | int & >=0
	})

	#controlArtifact: close({
		path!:           strings.MinRunes( 1)
		sha256!:         =~"^[a-f0-9]{64}$"
		sizeBytes!:      int & >=0
		role!:           "task-contract" | "work-pack" | "context-pack" | "source"
		authorityClass!: "public" | "private"
	})

	#dependency: close({
		dependencyId!: strings.MinRunes( 1)
		artifactRef!:  #exactArtifactRef
	})

	#exactArtifactRef: close({
		path!:      strings.MinRunes( 1)
		sha256!:    =~"^[a-f0-9]{64}$"
		sizeBytes!: int & >=0
	})

	#planAdmission: close({
		planManifest!:           #exactArtifactRef
		planManifestSchema!:     #exactArtifactRef
		selectionReceipt!:       #exactArtifactRef
		selectionReceiptSchema!: #exactArtifactRef
		planEpochId!:            =~"^epoch-[a-f0-9]{24}$"
		unitContractDigest!:     =~"^[a-f0-9]{64}$"
		attemptId!:              strings.MinRunes( 1)
		targetBaselines!: [_, ...] & [...#baselineEntry]
		validationContractDigest!: =~"^[a-f0-9]{64}$"
		structuredValidationContracts!: [_, ...] & [...#structuredValidationCommand]
	})

	#structuredValidationCommand: close({
		command_id!: strings.MinRunes( 1)
		argv!: [_, ...] & [...strings.MinRunes( 1)]
		cwd!:              strings.MinRunes( 1)
		timeout_seconds!:  int & >=1 & <=86400
		max_output_bytes!: int & >=1 & <=16777216
	})
}
