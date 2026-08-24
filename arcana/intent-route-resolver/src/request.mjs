import { canonicalizeJson, deepFreeze } from "./canonical-json.mjs";
import { REQUEST_PROTOCOL } from "./version.mjs";

export class RequestAdmissionError extends Error {
  constructor(message) {
    super(message);
    this.name = "RequestAdmissionError";
    this.reasonCode = "IR_INVALID_REQUEST";
  }
}

function fail(message) {
  throw new RequestAdmissionError(message);
}

function string(value, label, { empty = false } = {}) {
  if (typeof value !== "string" || (!empty && value.length === 0)) fail(`${label} must be a nonempty string`);
}

export function admitRouteRequest(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("request must be an object");
  const allowed = new Set(["schema", "request_id", "intent", "support_evidence_refs", "constraints", "catalog_id", "catalog_digest", "supersedes_request_id"]);
  if (Object.keys(raw).some((key) => !allowed.has(key))) fail("request contains an unknown field");
  if (raw.schema !== REQUEST_PROTOCOL) fail("unsupported request protocol");
  string(raw.request_id, "request_id");
  string(raw.catalog_id, "catalog_id");
  if (!/^[0-9a-f]{64}$/.test(raw.catalog_digest ?? "")) fail("catalog_digest must be lowercase SHA-256");
  if (!raw.intent || typeof raw.intent !== "object" || Array.isArray(raw.intent)) fail("intent must be an object");
  if (Object.keys(raw.intent).some((key) => !["text", "discriminators"].includes(key))) fail("intent contains an unknown field");
  string(raw.intent.text, "intent.text");
  if (!raw.intent.discriminators || typeof raw.intent.discriminators !== "object" || Array.isArray(raw.intent.discriminators)) fail("intent.discriminators must be an object");
  for (const [key, entry] of Object.entries(raw.intent.discriminators)) {
    if (!/^[A-Za-z][A-Za-z0-9._-]{0,63}$/.test(key)) fail("invalid discriminator key");
    if (!entry || typeof entry !== "object" || Array.isArray(entry) || Object.keys(entry).some((field) => !["posture", "value"].includes(field))) fail(`invalid discriminator ${key}`);
    if (!["declared", "inferred", "unresolved"].includes(entry.posture)) fail(`invalid posture for ${key}`);
    if (entry.posture === "unresolved" && entry.value !== null) fail(`unresolved discriminator ${key} must have null value`);
    if (entry.posture !== "unresolved" && (entry.value === null || !["string", "number", "boolean"].includes(typeof entry.value))) fail(`resolved discriminator ${key} has invalid value`);
  }
  if (!Array.isArray(raw.support_evidence_refs)) fail("support_evidence_refs must be an array");
  for (const reference of raw.support_evidence_refs) {
    if (!reference || typeof reference !== "object" || Array.isArray(reference) || Object.keys(reference).sort().join(",") !== "artifact_ref,content_digest") fail("invalid evidence reference");
    string(reference.artifact_ref, "artifact_ref");
    if (!/^[0-9a-f]{64}$/.test(reference.content_digest ?? "")) fail("evidence digest must be lowercase SHA-256");
  }
  if (!raw.constraints || typeof raw.constraints !== "object" || Array.isArray(raw.constraints)) fail("constraints must be an object");
  if (Object.keys(raw.constraints).sort().join(",") !== "forbidden_route_ids,required_capabilities") fail("constraints shape is closed");
  for (const key of ["required_capabilities", "forbidden_route_ids"]) {
    if (!Array.isArray(raw.constraints[key]) || raw.constraints[key].some((item) => typeof item !== "string" || item.length === 0)) fail(`${key} must be a string array`);
    if (new Set(raw.constraints[key]).size !== raw.constraints[key].length) fail(`${key} must be unique`);
  }
  return deepFreeze(canonicalizeJson(raw));
}
