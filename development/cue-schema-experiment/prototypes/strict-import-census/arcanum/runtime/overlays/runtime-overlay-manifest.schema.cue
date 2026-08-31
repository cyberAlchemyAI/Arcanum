// Arcanum Runtime Overlay Manifest
package prototype

import (
	"list"
	"strings"
	"struct"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/schemas/runtime-overlay-manifest.v1.json")
	close({
		schema_version!: "arcanum.runtime-overlay-manifest.v1"
		target!:         =~"^[a-z][a-z0-9-]*$"
		canonical!:      #canonical
		generator!:      #generator
		payload_root!:   #relativePath
		runtime_targets!: [_, ...] & [...#runtimeTarget]
		allowed_metadata!: list.UniqueItems() & [_, ...] & [...=~"^[A-Za-z][A-Za-z0-9_-]*$"]
		fragments!: [...#fragment]
		presets!: [...#preset]
		protected_controls!: [_, ...] & [...#protectedControl]
		validation_command!: strings.MinRunes(1)
	})

	#canonical: close({
		source!:       #relativePath
		sha256!:       #sha256
		package_root!: #relativePath
	})

	#copiedFile: close({
		source!:      #relativePath
		destination!: #relativePath
		sha256!:      #sha256
	})

	#fragment: close({
		id!: =~"^[a-z][a-z0-9-]*$"
		preset_ids!: list.UniqueItems() & [_, ...] & [...=~"^[a-z][a-z0-9_]*$"]
		source!: #relativePath
		sha256!: #sha256
		mode!:   "insert_after_exact"
		anchor!: strings.MinRunes(1)
	})

	#generator: close({
		path!:             #relativePath
		version!:          strings.MinRunes(1)
		version_marker!:   strings.MinRunes(1)
		overlay_protocol!: "arcanum.runtime-overlay-manifest.v1"
	})

	#preset: close({
		id!:         =~"^[a-z][a-z0-9_]*$"
		source_dir!: #relativePath
		copied_files!: [_, ...] & [...#copiedFile]
	})

	#protectedControl: close({
		id!:    =~"^[a-z][a-z0-9-]*$"
		class!: "gate" | "status" | "authority" | "state"
		text!:  strings.MinRunes(1)
	})

	#relativePath: matchN(0, [null | bool | number | =~"(^/|(^|/)\\.\\.(/|$)|^[A-Za-z]:[\\\\/])" | [...] | {}]) & strings.MinRunes(1)

	#runtimeTarget: close({
		id!:           =~"^[a-z][a-z0-9-]*$"
		package_root!: #relativePath
		skill_path!:   #relativePath
		metadata!: struct.MinFields(1) & {
			[string]: string
		}
	})

	#sha256: =~"^[a-f0-9]{64}$"
}
