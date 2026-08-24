#!/usr/bin/env node
import { resolveJson } from "../src/json-port.mjs";

let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => { input += chunk; });
process.stdin.on("end", () => {
  const result = resolveJson(input);
  process.stdout.write(result.stdout);
  process.exitCode = result.exit_code;
});
