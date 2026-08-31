// Invoke CLI Authoring Request v1
//
// Stage-bound authored values and explicit evidence selectors. Fixed fields,
// exact bytes, receipts, and authority effects are not authored here.
package prototype

import (
	"net"
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/cli-authoring-request/v1")
	close({
		$schema!: net.AbsURL
		document!: {}
		evidence_paths!: list.UniqueItems() & [...close({
			kind?:    "file" | "directory"
			path!:    string
			pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
		})]
		mode!:           "define" | "design"
		schema_version!: "invoke.cli-authoring-request.v1"
		stage!:          strings.MinRunes(1)
	})
}
