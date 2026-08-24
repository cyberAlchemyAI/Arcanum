#!/usr/bin/env node
import { readFile, writeFile } from "node:fs/promises";
import { basename, resolve } from "node:path";
import { canonicalJson, sha256Hex, sha256HexText } from "../src/canonical-json.mjs";
import { resolveIntentRoute } from "../src/resolve.mjs";
import { CLOSURE_DIGEST, CORE_VERSION, MANIFEST_VERSION } from "../src/version.mjs";
import { makeCatalog, makeRequest } from "../test/fixture-factory.mjs";

const outputIndex = process.argv.indexOf("--output");
if (outputIndex < 0 || !process.argv[outputIndex + 1]) throw new Error("--output is required");
const catalog = makeCatalog();
const cases = ["candidate", "ambiguous", "no-match", "invalid"].map((kind) => {
  const response = resolveIntentRoute(makeRequest(kind, catalog), catalog);
  const bytes = canonicalJson(response);
  return {case_id: `NODE-${kind.toUpperCase()}`, expected_kind: kind, observed_kind: response.kind, response_sha256: sha256HexText(bytes), response_bytes: new TextEncoder().encode(bytes).length, status: response.kind === kind ? "pass" : "fail"};
});
const report = {
  schema: "intent-route.node-witness@1",
  status: cases.every((item) => item.status === "pass") ? "pass" : "fail",
  runtime: {name: "node", version: process.version, executable: basename(process.execPath), executable_sha256: sha256Hex(await readFile(process.execPath))},
  core_version: CORE_VERSION,
  manifest_version: MANIFEST_VERSION,
  closure_digest: CLOSURE_DIGEST,
  catalog_digest: catalog.content_digest,
  case_count: cases.length,
  cases,
  authority_effect: "none",
  claim_ceiling: "canonical-source-local Node portability only"
};
await writeFile(resolve(process.argv[outputIndex + 1]), `${JSON.stringify(report, null, 2)}\n`, "utf8");
process.stdout.write(`${canonicalJson({schema: report.schema, status: report.status, case_count: report.case_count, authority_effect: "none"})}\n`);
if (report.status !== "pass") process.exitCode = 1;
