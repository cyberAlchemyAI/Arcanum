// InvokeDesignDenominatorReceipt
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-denominator-receipt/1-0-0")
	matchN(2, [matchIf({
		verdict!: "pass"
	}, {
		unbound_signal_ids?: null | bool | number | string | list.MaxItems(0) | {}
		missing_detector_inputs?: null | bool | number | string | list.MaxItems(0) | {}
		diagnostics?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		verdict!: "block"
	}, {
		diagnostics?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		schema_version!:        "1.0.0"
		manifest_id!:           #id
		manifest_input_digest!: #digest
		manifest_authored_by!: matchN(2, [#id, matchN(0, ["invoke-design-scope-extractor"])])
		detector_id!:      "invoke-design-scope-extractor"
		detector_version!: strings.MinRunes( 1)
		detector_owner!:   "spellcraft"
		inspected_selectors!: [_, ...] & [...#selector]
		extracted_signals!: [...#signal]
		authored_concern_ids!: list.UniqueItems() & [...#id]
		denominator_signal_ids!: list.UniqueItems() & [...#id]
		unbound_signal_ids!: list.UniqueItems() & [...#id]
		missing_detector_inputs!: list.UniqueItems() & [...strings.MinRunes( 1)]
		verdict!: "pass" | "block"
		diagnostics!: [...#diagnostic]
		receipt_digest!:  #digest
		validator_owner!: "invoke-design-selection-validator"
	})

	#diagnostic: close({
		code!:     "MANIFEST_NOT_CLOSED" | "MISSING_DETECTOR_INPUT" | "STALE_DENOMINATOR_RECEIPT" | "SELF_ISSUED_RECEIPT" | "UNBOUND_SIGNAL"
		message!:  strings.MinRunes( 1)
		selector!: null | string
		repair!:   strings.MinRunes( 1)
	})

	#digest: =~"^[a-f0-9]{64}$"

	#id: strings.MinRunes(1) & =~"^[a-zA-Z0-9][a-zA-Z0-9._:-]*$"

	#selector: close({
		selector!:      strings.MinRunes( 1)
		path!:          strings.MinRunes( 1)
		source_digest!: #digest
	})

	#signal: close({
		signal_id!:       #id
		signal_class!:    "human-actor" | "rendered-surface" | "interface" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility" | "quality-claim" | "acceptance-readiness-claim"
		source_selector!: strings.MinRunes( 1)
		source_digest!:   #digest
		attributes!: {}
	})
}
