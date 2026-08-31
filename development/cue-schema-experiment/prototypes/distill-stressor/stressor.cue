@experiment(explicitopen)

package distillstressor

import "strings"

#NonEmpty: string & strings.MinRunes(1) & =~".*\\S.*"
#Identifier: #NonEmpty & =~"^[a-z][a-z0-9_]*$"

#ActivationPredicate: {
	kind: "mode"
	mode_id: #Identifier
} | {
	kind: "risk"
	minimum: "low" | "medium" | "high"
} | {
	kind: "user_request"
	technique_id: #Identifier
} | {
	kind: "input_present"
	group: "identity" | "intent" | "policy" | "discovery" | "constraints" | "artifacts" | "lineage" | "evidence_context"
}

#Activation: {
	operator: "all" | "any"
	predicates: [#ActivationPredicate, #ActivationPredicate, ...#ActivationPredicate]
}

#ScalarValue: {
	kind: "scalar"
	value_type: "string" | "integer" | "number" | "boolean"
}

#ArrayValue: {
	kind: "array"
	item_type: "string" | "integer" | "number" | "boolean"
	minimum_items: int & >=0
}

#ObjectValue: {
	kind: "object"
	required_fields: [#Identifier, ...#Identifier]
	field_types: [string]: "string" | "integer" | "number" | "boolean"
}

#EmittedValue: #ScalarValue | #ArrayValue | #ObjectValue

#FailureAction: {
	kind: "block"
	code: #NonEmpty
} | {
	kind: "flag"
	code: #NonEmpty
} | {
	kind: "skip"
	reason: #NonEmpty
} | {
	kind: "route"
	route: #Identifier
}

#Technique: {
	technique_id: #Identifier
	activation: #Activation
	emits: [string]: #EmittedValue
	failure_actions: [#FailureAction, ...#FailureAction]
}

#RoleStep: {
	sequence: int & >=1
	role: "proposer" | "balancer" | "human"
	action: #Identifier
	condition?: #NonEmpty
}

#TechniqueRule: {
	technique_id: #Identifier
	state: "required" | "risk_triggered" | "evolution_triggered" | "user_requested" | "not_applicable"
	reason_required: bool
}

#HumanGate: {
	gate: "blocker" | "periodic" | "final" | "readiness"
	frequency?: int & >=1
}

#PitchOff: {
	enabled: false
	dimensions?: []
} | {
	enabled: true
	dimensions: [#NonEmpty, ...#NonEmpty]
}

#Mode: {
	mode_id: #Identifier
	role_program: [#RoleStep, ...#RoleStep]
	technique_policy: [#TechniqueRule, ...#TechniqueRule]
	human_gate_policy: {
		gates: [#HumanGate, ...#HumanGate]
	}
	pitch_off: #PitchOff
}

#Source: {
	identity: {
		run_id: #Identifier
	}
	intent: {
		statement: #NonEmpty
	}
	artifacts?: [...#NonEmpty]
	requested_techniques?: [...#Identifier]
	evidence_context?: {
		notes?: [...#NonEmpty]
	}
}

#DistillW2Stressor: {
	technique: #Technique
	mode: #Mode
	source: #Source
}
