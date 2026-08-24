import { canonicalJson } from "./canonical-json.mjs";
import { resolveIntentRoute } from "./resolve.mjs";
import {
  CAPABILITY_TOKEN, CLOSURE_DIGEST, CORE_VERSION, ERROR_PROTOCOL,
  MANIFEST_VERSION, REQUEST_PROTOCOL, RUNTIME_PORT_PROTOCOL,
  RUNTIME_PORT_REQUEST_PROTOCOL, DISPOSITION_PROTOCOL
} from "./version.mjs";

function output(exitCode, value) {
  return {exit_code: exitCode, stdout: `${canonicalJson(value)}\n`, stderr: ""};
}

function error(exitCode, reasonCode, message) {
  return output(exitCode, {schema: ERROR_PROTOCOL, reason_code: reasonCode, message, authority_effect: null});
}

export function resolveJsonValue(envelope) {
  if (!envelope || typeof envelope !== "object" || Array.isArray(envelope)) return error(2, "IR_TRANSPORT_MALFORMED_JSON", "input must be one JSON object");
  if (envelope.capability_token !== CAPABILITY_TOKEN) return error(3, "IR_CAPABILITY_DENIED", "local resolver capability denied");
  if (envelope.schema !== RUNTIME_PORT_REQUEST_PROTOCOL) return error(4, "IR_PORT_VERSION_UNSUPPORTED", "runtime-port request protocol unsupported");
  if (envelope.request?.schema !== REQUEST_PROTOCOL) return error(4, "IR_REQUEST_VERSION_UNSUPPORTED", "request protocol unsupported");
  if (envelope.expected_core_version !== CORE_VERSION) return error(4, "IR_CORE_VERSION_MISMATCH", "core version mismatch");
  if (envelope.expected_manifest_version !== MANIFEST_VERSION) return error(4, "IR_MANIFEST_VERSION_MISMATCH", "manifest version mismatch");
  if (envelope.request?.catalog_id !== envelope.catalog?.catalog_id || envelope.request?.catalog_digest !== envelope.catalog?.content_digest) return error(5, "IR_CATALOG_DIGEST_MISMATCH", "request and catalog binding mismatch");
  if (envelope.expected_closure_digest !== CLOSURE_DIGEST) return error(5, "IR_CONTENT_DIGEST_MISMATCH", "closure digest mismatch");
  const disposition = resolveIntentRoute(envelope.request, envelope.catalog);
  return output(0, {
    schema: RUNTIME_PORT_PROTOCOL,
    core_version: CORE_VERSION,
    manifest_version: MANIFEST_VERSION,
    request_protocol: REQUEST_PROTOCOL,
    disposition_protocol: DISPOSITION_PROTOCOL,
    closure_digest: CLOSURE_DIGEST,
    disposition,
    authority_effect: "none"
  });
}

export function resolveJson(text) {
  let value;
  try { value = JSON.parse(text); } catch {
    return error(2, "IR_TRANSPORT_MALFORMED_JSON", "stdin is not valid JSON");
  }
  return resolveJsonValue(value);
}
