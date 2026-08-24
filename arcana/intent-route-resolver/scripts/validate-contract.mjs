#!/usr/bin/env node
import { readFile, readdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { digestJson } from "../src/canonical-json.mjs";
import { computeClosureDigest } from "./compute-closure-digest.mjs";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const check = process.argv[2] === "--check" ? process.argv[3] : "all";

async function json(relative) {
  return JSON.parse(await readFile(join(root, relative), "utf8"));
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const manifest = await json("addon-manifest.json");
const sourceReceipt = await json("SOURCE-LICENSE-API-RECEIPT.json");
const boundary = await json("PUBLIC-BOUNDARY.json");
const fixtures = await json("fixtures/synthetic-contract-cases.json");
const executableFixtures = await json("fixtures/executable-cases.json");
const schemaNames = (await readdir(join(root, "schemas")))
  .filter((name) => name.endsWith(".schema.json"))
  .sort();
const schemas = await Promise.all(schemaNames.map((name) => json(`schemas/${name}`)));

assert(manifest.schema_version === "intent-route.addon-manifest@1", "manifest schema mismatch");
assert(manifest.stage === "canonical-source", "manifest must identify the canonical source stage");
assert(manifest.authority_effect === "none", "manifest authority must be none");
assert(manifest.side_effects === false, "manifest side effects must be false");
assert(Array.isArray(manifest.required_permissions) && manifest.required_permissions.length === 0, "manifest permissions must be empty");
assert(Array.isArray(manifest.dependencies) && manifest.dependencies.length === 0, "manifest dependencies must be empty");
assert(manifest.entrypoints.core === "./src/index.mjs" && manifest.entrypoints.json_port === "./scripts/invoke-json-port.mjs", "entrypoint binding mismatch");
assert(/^[0-9a-f]{64}$/.test(manifest.closure_digest), "manifest closure digest must be lowercase SHA-256");
assert(schemaNames.length === 5, "exactly five contract schemas required");
for (const schema of schemas) {
  assert(schema.$schema === "https://json-schema.org/draft/2020-12/schema", "schema dialect mismatch");
  assert(schema.type === "object", "schema root must be object");
  assert(schema.additionalProperties === false, "schema root must be closed");
}
assert(boundary.authority_effect === "none", "boundary authority must be none");
assert(fixtures.state === "contract-only" && fixtures.cases.length === 4, "four contract cases required");
assert(new Set(fixtures.cases.map((item) => item.expected_kind)).size === 4, "all four dispositions required");
assert(fixtures.cases.every((item) => item.expected_authority_effect === "none"), "fixture authority must be none");
assert(executableFixtures.json_port_case_ids.length === 13, "13 JSON-port cases required");
assert(executableFixtures.public_core_case_ids.length === 8, "eight public-core cases required");
assert(executableFixtures.closure_digest === manifest.closure_digest, "fixture closure binding mismatch");
assert(await computeClosureDigest() === manifest.closure_digest, "computed closure digest mismatch");
const fixtureDigestInput = structuredClone(executableFixtures);
delete fixtureDigestInput.fixture_digest;
assert(digestJson(fixtureDigestInput) === executableFixtures.fixture_digest, "fixture digest mismatch");

const license = await readFile(join(root, sourceReceipt.license.path), "utf8");
assert(sourceReceipt.source.method === "fresh-behavior-only-authorship", "fresh-source declaration missing");
assert(sourceReceipt.source.copied_source_code === false, "copied source is forbidden");
assert(sourceReceipt.source.copied_private_prose === false, "copied private prose is forbidden");
assert(sourceReceipt.source.project_neutral === true, "package must be project neutral");
assert(sourceReceipt.api.authority_effect === "none", "API authority must be none");
assert(sourceReceipt.api.permissions.length === 0 && sourceReceipt.api.side_effects === false, "API must be zero permission and side-effect free");
assert(license.startsWith(`${sourceReceipt.license.required_notice}\n`), "Required Notice mismatch");
assert(license.includes("# PolyForm Noncommercial License 1.0.0"), "license text mismatch");

const result = {
  schema: "intent-route.contract-validation@1",
  check,
  status: "pass",
  schema_count: schemaNames.length,
  fixture_case_count: fixtures.cases.length,
  authority_effect: "none"
};
process.stdout.write(`${JSON.stringify(result)}\n`);
