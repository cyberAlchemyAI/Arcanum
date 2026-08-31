## Exact Evidence Cookbook

Run evidence commands from the repository root. Record paths relative to that
root, never absolute paths, URLs, or paths containing a `..` segment.

```sh
sha256sum path/to/file
wc -c < path/to/file
nl -ba path/to/file
```

Discovery artifact refs and required identity refs are exactly:

```json
{"path":"path/to/file","sha256":"<64 lowercase hex>","size":123}
```

Definition `source_refs` add semantic location fields:

```json
{
  "role": "evidence",
  "path": "path/to/file",
  "visibility": "public",
  "selector_type": "heading",
  "selector": "Exact Heading",
  "start_line": null,
  "end_line": null,
  "sha256": "<64 lowercase hex>",
  "size": 123
}
```

Roles are `normative`, `provenance`, `evidence`, or `example`. A normative,
provenance, or evidence ref requires current SHA-256 and size. An example ref
may use `null` for those two fields, but exact bindings are preferable.

Selector rules:

| `selector_type` | `selector` | line fields |
| --- | --- | --- |
| `heading` | exact Markdown heading text or slug-equivalent text | both `null` |
| `anchor` | Markdown heading slug, with or without leading `#` | both `null` |
| `line-span` | descriptive non-empty label | integer `start_line <= end_line`, within file |
| `json-pointer` | RFC 6901 pointer beginning `/`, such as `/concept/meaning` | both `null` |
| `yaml-path` | dotted path with optional zero-based indexes, such as `groups[0].id` | both `null` |
| `symbol` | exact text that occurs in the file | both `null` |

The selector resolves inside the whole referenced file; SHA-256 and size also
describe the whole file, not only the selected passage. Recompute both whenever
the file changes.
