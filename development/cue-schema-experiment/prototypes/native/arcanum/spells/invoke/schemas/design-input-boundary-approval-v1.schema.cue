// Invoke Design Input Boundary Approval v1
//
// Owner-issued, authority-free evidence that binds the finite roots and
// discovery rules within which Design input completeness may be claimed.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1")
	close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1"
		approval_digest!:  =~"^[a-f0-9]{64}$"
		approval_id!:      =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		approved_by!:      =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		authority_effect!: "none"
		boundary_digest!:  =~"^[a-f0-9]{64}$"
		discovery_rules!: [...close({
			include_globs!: list.UniqueItems() & [...string] & [_, ...]
			input_class!: "define-artifact" | "current-design" | "current-implementation" | "interface-contract" | "state-workflow" | "data-store" | "queue-writer" | "deployment-topology" | "authority-policy" | "security-policy" | "privacy-policy" | "compatibility-policy" | "quality-constraint" | "observability-contract" | "architecture-pattern" | "research-evidence" | "ux-evidence" | "owner-decision" | "other"
			root_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			rule_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})] & [_, ...]
		observation_epoch!: =~".*\\S.*"
		permitted_exclusions!: [...close({
			evidence_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			path!: string
		})]
		required_input_classes!: list.UniqueItems() & [..."define-artifact" | "current-design" | "current-implementation" | "interface-contract" | "state-workflow" | "data-store" | "queue-writer" | "deployment-topology" | "authority-policy" | "security-policy" | "privacy-policy" | "compatibility-policy" | "quality-constraint" | "observability-contract" | "architecture-pattern" | "research-evidence" | "ux-evidence" | "owner-decision" | "other"] & [_, ...]
		roots!: [...close({
			path!:    string
			root_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			sha256!:  =~"^[a-f0-9]{64}$"
			size!:    int & >=0
		})] & [_, ...]
		schema_version!:    "invoke.design-input-boundary-approval.v1"
		target_id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		target_visibility!: "public" | "private"
	})

	#digest: =~"^[a-f0-9]{64}$"

	#discoveryRule: close({
		include_globs!: list.UniqueItems() & [...string] & [_, ...]
		input_class!: "define-artifact" | "current-design" | "current-implementation" | "interface-contract" | "state-workflow" | "data-store" | "queue-writer" | "deployment-topology" | "authority-policy" | "security-policy" | "privacy-policy" | "compatibility-policy" | "quality-constraint" | "observability-contract" | "architecture-pattern" | "research-evidence" | "ux-evidence" | "owner-decision" | "other"
		root_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		rule_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#glob: string

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#inputKind: "define-artifact" | "current-design" | "current-implementation" | "interface-contract" | "state-workflow" | "data-store" | "queue-writer" | "deployment-topology" | "authority-policy" | "security-policy" | "privacy-policy" | "compatibility-policy" | "quality-constraint" | "observability-contract" | "architecture-pattern" | "research-evidence" | "ux-evidence" | "owner-decision" | "other"

	#nonEmpty: =~".*\\S.*"

	#permittedExclusion: close({
		evidence_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		path!: string
	})

	#relativePath: string

	#rootBinding: close({
		path!:    string
		root_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		sha256!:  =~"^[a-f0-9]{64}$"
		size!:    int & >=0
	})
}
