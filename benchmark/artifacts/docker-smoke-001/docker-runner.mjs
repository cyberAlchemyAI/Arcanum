
import { exec } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { promisify } from "node:util";

const execAsync = promisify(exec);
const [patchPath, oracleCommand] = process.argv.slice(2);

if (!patchPath || !oracleCommand) {
  console.error("usage: node runner.mjs <patch> <oracle-command>");
  process.exit(97);
}

const patch = readFileSync(patchPath, "utf8");
applyUnifiedPatch(patch);
const result = await runOracle(oracleCommand);
process.stdout.write(result.stdout);
process.stderr.write(result.stderr);
process.exit(result.exitCode ?? 1);

function applyUnifiedPatch(patchText) {
  const lines = patchText.split(/\r?\n/);
  let targetPath = null;
  for (const line of lines) {
    if (line.startsWith("+++ b/")) {
      targetPath = line.slice("+++ b/".length);
      break;
    }
  }
  if (!targetPath) {
    throw new Error("patch target not found");
  }

  const removeLines = [];
  const addLines = [];
  for (const line of lines) {
    if (line.startsWith("---") || line.startsWith("+++") || line.startsWith("@@") || line.startsWith("diff ") || line.startsWith("index ")) {
      continue;
    }
    if (line.startsWith("-")) {
      removeLines.push(line.slice(1));
    } else if (line.startsWith("+")) {
      addLines.push(line.slice(1));
    }
  }

  const current = readFileSync(targetPath, "utf8");
  const before = removeLines.join("\n");
  const after = addLines.join("\n");
  if (!current.includes(before)) {
    throw new Error("patch context not found in " + targetPath);
  }
  writeFileSync(targetPath, current.replace(before, after), "utf8");
}

async function runOracle(command) {
  try {
    const result = await execAsync(command);
    return { exitCode: 0, stdout: result.stdout, stderr: result.stderr };
  } catch (error) {
    return {
      exitCode: typeof error.code === "number" ? error.code : 1,
      stdout: error.stdout ?? "",
      stderr: error.stderr ?? error.message ?? ""
    };
  }
}
