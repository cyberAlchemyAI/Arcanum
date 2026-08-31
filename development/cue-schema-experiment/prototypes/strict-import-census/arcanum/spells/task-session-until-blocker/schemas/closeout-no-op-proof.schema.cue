// CloseoutNoOpProof
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session-until-blocker/closeout-no-op-proof/1-0-0")
	close({
		schema_version!: "1.0.0"
		proof_id!:       strings.MinRunes( 1)
		unit_id!:        strings.MinRunes( 1)
		before_inventory!: [_, ...] & [...#inventoryEntry]
		after_inventory!: [_, ...] & [...#inventoryEntry]
		observed_delta!:        list.MaxItems(0)
		closeout_contract_ref!: #exactArtifactRef
		validator!: close({
			id!:                strings.MinRunes( 1)
			version!:           strings.MinRunes( 1)
			executable_sha256!: =~"^[a-f0-9]{64}$"
		})
		continuation_router_verification!: close({
			receipt_ref!:         #exactArtifactRef
			status!:              "verified"
			canonical_successor!: null | string
		})
		authority_effect!: "none"
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#inventoryEntry: close({
		path!:   strings.MinRunes( 1)
		sha256!: =~"^[a-f0-9]{64}$"
	})
}
