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
		analogy_labels?: [...{
			claim!:    strings.MinRunes(1)
			label!:    "analogy"
			register!: "lean" | "reflection-tower" | "residue" | "cyberalchemy" | "categorical" | "thermodynamic"
		}]
		authority?: {
			deploy?:     string
			evidence?:   string
			promotion?:  string
			secrets?:    string
			state?:      string
			validation?: string
			{[!~"^(deploy|evidence|promotion|secrets|state|validation)$"]: string}
		}
		boundaries?: [...{
			applies_to_services?: [...string]
			boundary_id!:  strings.MinRunes(1)
			contract!:     strings.MinRunes(1)
			from_owner?:   string
			kind!:         "network" | "secret" | "data_store" | "tenant" | "policy" | "environment"
			on_violation!: "block" | "flag" | "defer" | "ask" | "reroute"
			reversal?: {
				backup?: {
					schedule?: string
					target?:   string
				}
				migration?: {
					forward?: string
					reverse?: string
				}
				retention?: {
					namespace?: string
					policy?:    string
				}
				rollback?: {
					method?: string
					target?: string
				}
			}
			to_owner?: string
		}]
		doc_status?: "draft" | "active" | "deprecated"
		environments!: [...{
			branch?:         string
			deploy_trigger?: "branch" | "push" | "manual"
			name!:           strings.MinRunes(1)
			purpose?:        string
			url?:            string
		}] & [_, ...]
		gates!: [...{
			condition!: strings.MinRunes(1)
			gate_id!:   strings.MinRunes(1)
			kind!:      "validation" | "promotion_guardrail" | "human_approval"
			on_fail!:   "block" | "flag" | "defer" | "ask" | "reroute"
			owner!:     strings.MinRunes(1)
		}] & [_, ...]
		infra_spec_id!: strings.MinRunes(1)
		observability?: {
			scrape_targets?: [...string]
			signal_refs?: [...string]
			slo_refs?: [...string]
		}
		project!: strings.MinRunes(1)
		promotion_splits?: [...{
			on_violation!: "block" | "flag" | "defer" | "ask" | "reroute"
			rule!:         strings.MinRunes(1)
			source!:       strings.MinRunes(1)
			target!:       strings.MinRunes(1)
		}]
		promotion_status!: {
			evidence_refs?: [...string]
			stage!: "specified" | "implemented" | "deployed" | "observed" | "validated" | "reflected" | "promoted"
		}
		receipts?: [...{
			on_missing!: "block" | "flag" | "defer" | "ask" | "reroute"
			producer!:   strings.MinRunes(1)
			receipt_id!: strings.MinRunes(1)
			required_fields!: [..."run_id" | "artifacts" | "validation_result" | "status" | "residue" | "audit_reference"] & [_, ...]
			stores?: [...string]
		}]
		residue!: [...{
			kind!:     "failure_mode" | "unowned_state" | "drift" | "missing_receipt"
			owner?:    string
			severity!: "low" | "medium" | "high" | "severe"
			summary!:  strings.MinRunes(1)
		}] & [_, ...]
		runtime_profile!: name!: "dev" | "single-vps" | "split-vps" | "ha"
		schema_version!: strings.MinRunes(1)
		services!: [...{
			dependencies?: [...{
				direction!: "inbound" | "outbound" | "internal"
				must_not_depend_on?: [...string]
				target!: string
			}]
			deployment?: {
				exposed?:           bool
				generated?:         bool
				image?:             string
				instance_evidence?: "present" | "absent"
				internal_port?:     int
				registry?:          string
			}
			name!:  strings.MinRunes(1)
			owner!: strings.MinRunes(1)
			reversal?: {
				backup?: {
					schedule?: string
					target?:   string
				}
				migration?: {
					forward?: string
					reverse?: string
				}
				retention?: {
					namespace?: string
					policy?:    string
				}
				rollback?: {
					method?: string
					target?: string
				}
			}
		}] & [_, ...]
		state_namespaces?: [...{
			namespace!:    "source" | "runtime" | "generated" | "local" | "private" | "evidence"
			owner!:        strings.MinRunes(1)
			retention?:    string
			write_policy!: strings.MinRunes(1)
		}]
		status_class!: "candidate"
		...
	}

	#gate_action: "block" | "flag" | "defer" | "ask" | "reroute"

	#reversal: {
		backup?: {
			schedule?: string
			target?:   string
		}
		migration?: {
			forward?: string
			reverse?: string
		}
		retention?: {
			namespace?: string
			policy?:    string
		}
		rollback?: {
			method?: string
			target?: string
		}
	}
}
