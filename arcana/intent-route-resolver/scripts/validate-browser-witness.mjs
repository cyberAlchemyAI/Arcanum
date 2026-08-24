#!/usr/bin/env node
import { readFile } from "node:fs/promises";

const path = process.argv[2];
if (!path) throw new Error("browser witness path required");
const witness = JSON.parse(await readFile(path, "utf8"));
const digest = witness.runtime?.executable_sha256;
if (witness.schema !== "intent-route.browser-witness@1" || witness.status !== "pass" || witness.case_count !== 6 || witness.passed !== 6 || !/^[0-9a-f]{64}$/.test(digest ?? "") || witness.authority_effect !== "none") throw new Error("browser witness is not passing and complete");
process.stdout.write(`${JSON.stringify({schema: "intent-route.browser-witness-validation@1", status: "pass", case_count: witness.case_count, authority_effect: "none"})}\n`);
