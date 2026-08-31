// Invoke Design Profile v1
//
// Public machine contract for the generic six-view Design fact registry and view projection rules.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-profile/v1")
	close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-profile/v1"
		authority_effect!: "none"
		core_requirements!: [close({
			fact_kind!: "actor"
			minimum!:   0
		}), close({
			fact_kind!: "system"
			minimum!:   1
		}), close({
			fact_kind!: "relationship"
			minimum!:   0
		}), close({
			fact_kind!: "component"
			minimum!:   1
		}), close({
			fact_kind!: "rendered-surface"
			minimum!:   0
		}), close({
			fact_kind!: "contract"
			minimum!:   1
		}), close({
			fact_kind!: "interface"
			minimum!:   0
		}), close({
			fact_kind!: "workflow-step"
			minimum!:   0
		}), close({
			fact_kind!: "state"
			minimum!:   0
		}), close({
			fact_kind!: "decision"
			minimum!:   0
		}), close({
			fact_kind!: "dependency"
			minimum!:   0
		}), close({
			fact_kind!: "store"
			minimum!:   0
		}), close({
			fact_kind!: "queue"
			minimum!:   0
		}), close({
			fact_kind!: "writer"
			minimum!:   0
		}), close({
			fact_kind!: "normative-rule"
			minimum!:   0
		}), close({
			fact_kind!: "effect"
			minimum!:   0
		}), close({
			fact_kind!: "data-log-sink"
			minimum!:   0
		}), close({
			fact_kind!: "deployment"
			minimum!:   0
		}), close({
			fact_kind!: "compatibility-boundary"
			minimum!:   0
		}), close({
			fact_kind!: "quality-claim"
			minimum!:   0
		}), close({
			fact_kind!: "acceptance-readiness-claim"
			minimum!:   0
		}), close({
			fact_kind!: "risk"
			minimum!:   0
		})]
		fact_kinds!: ["actor", "system", "relationship", "component", "rendered-surface", "contract", "interface", "workflow-step", "state", "decision", "dependency", "store", "queue", "writer", "normative-rule", "effect", "data-log-sink", "deployment", "compatibility-boundary", "quality-claim", "acceptance-readiness-claim", "risk"]
		profile_digest!: =~"^[a-f0-9]{64}$"
		profile_id!:     "invoke.generic-design-baseline.v1"
		required_output_ids!: ["architecture"]
		schema_version!: "invoke.design-profile.v1"
		view_order!: ["view:context", "view:high-level-structure", "view:low-level-components", "view:workflow-process", "view:decision-flow", "view:dependency-interface"]
		view_rules!: list.MaxItems(6) & [matchN(2, [close({
			allow_evidence_backed_na!: true
			allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
			view_id!: string
		}), {
			allowed_fact_kinds?: ["actor", "system", "relationship", "rendered-surface"]
			view_id?: "view:context"
		}]), matchN(2, [close({
			allow_evidence_backed_na!: true
			allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
			view_id!: string
		}), {
			allowed_fact_kinds?: ["system", "component", "contract", "interface", "deployment"]
			view_id?: "view:high-level-structure"
		}]), matchN(2, [close({
			allow_evidence_backed_na!: true
			allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
			view_id!: string
		}), {
			allowed_fact_kinds?: ["component", "rendered-surface", "contract", "interface", "store", "queue", "writer", "data-log-sink"]
			view_id?: "view:low-level-components"
		}]), matchN(2, [close({
			allow_evidence_backed_na!: true
			allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
			view_id!: string
		}), {
			allowed_fact_kinds?: ["actor", "workflow-step", "state", "effect"]
			view_id?: "view:workflow-process"
		}]), matchN(2, [close({
			allow_evidence_backed_na!: true
			allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
			view_id!: string
		}), {
			allowed_fact_kinds?: ["decision", "normative-rule", "quality-claim", "acceptance-readiness-claim", "risk"]
			view_id?: "view:decision-flow"
		}]), matchN(2, [close({
			allow_evidence_backed_na!: true
			allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
			view_id!: string
		}), {
			allowed_fact_kinds?: ["relationship", "contract", "interface", "dependency", "compatibility-boundary"]
			view_id?: "view:dependency-interface"
		}])] & [_, _, _, _, _, _, ...]
	})

	#contextRule: matchN(2, [close({
		allow_evidence_backed_na!: true
		allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
		view_id!: string
	}), {
		allowed_fact_kinds?: ["actor", "system", "relationship", "rendered-surface"]
		view_id?: "view:context"
	}])

	#decisionRule: matchN(2, [close({
		allow_evidence_backed_na!: true
		allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
		view_id!: string
	}), {
		allowed_fact_kinds?: ["decision", "normative-rule", "quality-claim", "acceptance-readiness-claim", "risk"]
		view_id?: "view:decision-flow"
	}])

	#dependencyRule: matchN(2, [close({
		allow_evidence_backed_na!: true
		allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
		view_id!: string
	}), {
		allowed_fact_kinds?: ["relationship", "contract", "interface", "dependency", "compatibility-boundary"]
		view_id?: "view:dependency-interface"
	}])

	#digest: =~"^[a-f0-9]{64}$"

	#factKind: "actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"

	#highLevelRule: matchN(2, [close({
		allow_evidence_backed_na!: true
		allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
		view_id!: string
	}), {
		allowed_fact_kinds?: ["system", "component", "contract", "interface", "deployment"]
		view_id?: "view:high-level-structure"
	}])

	#lowLevelRule: matchN(2, [close({
		allow_evidence_backed_na!: true
		allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
		view_id!: string
	}), {
		allowed_fact_kinds?: ["component", "rendered-surface", "contract", "interface", "store", "queue", "writer", "data-log-sink"]
		view_id?: "view:low-level-components"
	}])

	#viewRule: close({
		allow_evidence_backed_na!: true
		allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
		view_id!: string
	})

	#workflowRule: matchN(2, [close({
		allow_evidence_backed_na!: true
		allowed_fact_kinds!: list.UniqueItems() & [..."actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"] & [_, ...]
		view_id!: string
	}), {
		allowed_fact_kinds?: ["actor", "workflow-step", "state", "effect"]
		view_id?: "view:workflow-process"
	}])
}
