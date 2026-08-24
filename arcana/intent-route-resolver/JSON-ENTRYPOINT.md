# JSON entrypoint contract

The executable stage exposes one local process entrypoint. It accepts exactly
one UTF-8 JSON document on stdin and emits exactly one canonical UTF-8 JSON
document plus a trailing newline on stdout. Successful execution emits zero
stderr bytes.

## Input envelope

The closed input object contains:

- `schema`: `intent-route.runtime-port.request@1`;
- `request`: one `intent-route.request@1` value;
- `catalog`: one `intent-route.catalog@1` value;
- `expected_core_version` and `expected_manifest_version`;
- `expected_closure_digest`;
- `capability_token`: an adapter-owned opaque token whose absence is rejected.

The entrypoint does not read environment variables, files, network resources,
models, clocks, randomness, or runtime registries to determine semantics.

## Output and exits

| Exit | Output schema | Meaning |
|---:|---|---|
| `0` | `intent-route.runtime-port@1` | trusted non-authorizing disposition |
| `2` | `intent-route.error@1` | malformed JSON |
| `3` | `intent-route.error@1` | missing or denied capability token |
| `4` | `intent-route.error@1` | unsupported protocol/core/manifest version |
| `5` | `intent-route.error@1` | catalog or closure digest mismatch |

Transport rejection never fabricates a disposition. Every trusted disposition
contains `authority_effect: none`.
