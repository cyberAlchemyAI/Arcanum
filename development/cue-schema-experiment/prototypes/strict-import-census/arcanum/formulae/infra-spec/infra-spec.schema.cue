// Arcanum Infra Spec (CANDIDATE — operational-contract spine)
//
// CANDIDATE schema produced by refine run
// 2026-06-08-infra-spec-mvp-design-refine. Describes the operational contract
// binding a project/environment to its services, boundaries, state namespaces,
// gates, status, and reversal obligations. Self-contained (gate_action
// inlined). Reuses dispatch-spec $def SHAPES by parity. NOT authoritative; not
// self-promoting; not a formulae package.
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/candidate/infra-spec/infra-spec.schema.json")
	matchN(0, [null | bool | number | string | [...] | {
		status!: _
	}]) & {
		infra_spec_id!:  strings.MinRunes( 1)
		schema_version!: strings.MinRunes( 1)
		project!:        strings.MinRunes( 1)
		status_class!:   "candidate"
		doc_status?:     "draft" | "active" | "deprecated"
		runtime_profile!: name!: "dev" | "single-vps" | "split-vps" | "ha"
		environments!: [_, ...] & [...{
			name!:           strings.MinRunes( 1)
			purpose?:        string
			url?:            string
			deploy_trigger?: "branch" | "push" | "manual"
			branch?:         string
		}]
		services!: [_, ...] & [...{
			name!:  strings.MinRunes( 1)
			owner!: strings.MinRunes(1)
			deployment?: {
				image?:             string
				registry?:          string
				internal_port?:     int
				exposed?:           bool
				generated?:         bool
				instance_evidence?: "present" | "absent"
			}
			dependencies?: [...{
				target!:    string
				direction!: "inbound" | "outbound" | "internal"
				must_not_depend_on?: [...string]
			}]
			reversal?: #reversal
		}]
		boundaries?: [...{
			boundary_id!: strings.MinRunes( 1)
			kind!:        "network" | "secret" | "data_store" | "tenant" | "policy" | "environment"
			from_owner?:  string
			to_owner?:    string
			applies_to_services?: [...string]
			contract!:     strings.MinRunes( 1)
			on_violation!: #gate_action
			reversal?:     #reversal
		}]
		authority?: {
			validation?: string
			evidence?:   string
			promotion?:  string
			deploy?:     string
			secrets?:    string
			state?:      string
			{[!~"^(validation|evidence|promotion|deploy|secrets|state)$"]: string}
		}
		state_namespaces?: [...{
			namespace!:    "source" | "runtime" | "generated" | "local" | "private" | "evidence"
			owner!:        strings.MinRunes( 1)
			write_policy!: strings.MinRunes( 1)
			retention?:    string
		}]
		observability?: {
			signal_refs?: [...string]
			scrape_targets?: [...string]
			slo_refs?: [...string]
		}
		receipts?: [...{
			receipt_id!: strings.MinRunes( 1)
			producer!:   strings.MinRunes( 1)
			required_fields!: [_, ...] & [..."run_id" | "artifacts" | "validation_result" | "status" | "residue" | "audit_reference"]
			stores?: [...string]
			on_missing!: #gate_action
		}]
		promotion_splits?: [...{
			source!:       strings.MinRunes( 1)
			target!:       strings.MinRunes( 1)
			rule!:         strings.MinRunes( 1)
			on_violation!: #gate_action
		}]
		gates!: [_, ...] & [...{
			gate_id!:   strings.MinRunes( 1)
			kind!:      "validation" | "promotion_guardrail" | "human_approval"
			owner!:     strings.MinRunes( 1)
			condition!: strings.MinRunes( 1)
			on_fail!:   #gate_action
		}]
		residue!: [_, ...] & [...{
			summary!:  strings.MinRunes( 1)
			kind!:     "failure_mode" | "unowned_state" | "drift" | "missing_receipt"
			severity!: "low" | "medium" | "high" | "severe"
			owner?:    string
		}]
		analogy_labels?: [...{
			claim!:    strings.MinRunes( 1)
			register!: "lean" | "reflection-tower" | "residue" | "cyberalchemy" | "categorical" | "thermodynamic"
			label!:    "analogy"
		}]
		promotion_status!: {
			stage!: "specified" | "implemented" | "deployed" | "observed" | "validated" | "reflected" | "promoted"
			evidence_refs?: [...string]
		}
		...
	}

	#gate_action: "block" | "flag" | "defer" | "ask" | "reroute"

	#reversal: {
		rollback?: {
			method?: string
			target?: string
		}
		migration?: {
			forward?: string
			reverse?: string
		}
		backup?: {
			schedule?: string
			target?:   string
		}
		retention?: {
			namespace?: string
			policy?:    string
		}
	}
}
