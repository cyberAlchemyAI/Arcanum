// Invoke CLI Command Result v1
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/cli-command-result/v1")
	close({
		$schema!:        "https://arcanum.dev/schemas/invoke/cli-command-result/v1"
		schema_version!: "invoke.cli-command-result.v1"
		command!:        "invoke"
		mode!:           null | string
		operation!:      "modes" | "describe" | "check" | "author" | "produce" | "admit" | "status"
		stage!:          null | string
		status!:         "pass" | "block" | "error"
		inputs!: [...#ref]
		outputs!: [...#ref]
		diagnostics!: [...#diagnostic]
		authority_effect!: "none"
		data!:             _
	})

	#diagnostic: close({
		code!:     =~"^[A-Z][A-Z0-9_]*$"
		location!: null | string
		message!:  strings.MinRunes( 1)
		causes!: [...strings.MinRunes( 1)]
		repair_route!: strings.MinRunes( 1)
	})

	#digest: =~"^[a-f0-9]{64}$"

	#ref: close({
		path!:   strings.MinRunes( 1)
		kind!:   "file" | "directory" | "stdout"
		sha256?: null | =~"^[a-f0-9]{64}$"
		size?:   null | int & >=0
	})
}
