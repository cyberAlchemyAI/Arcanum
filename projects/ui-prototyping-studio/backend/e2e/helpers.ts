import { execFileSync, spawn, type ChildProcess } from "node:child_process";
import { mkdtempSync } from "node:fs";
import net from "node:net";
import { tmpdir } from "node:os";
import { join } from "node:path";

/** A fresh, isolated STUDIO_DATA path per test (own dir ⇒ own artifacts root). */
export function newDataDir(): string {
  return join(mkdtempSync(join(tmpdir(), "ups-e2e-")), "studio.json");
}

export interface CliResult {
  stdout: string;
  json: any;
  code: number;
}

/** Run one studio CLI verb to completion via tsx; capture stdout JSON + exit code. */
export function cli(args: string[], dataDir: string): CliResult {
  const env = { ...process.env, STUDIO_DATA: dataDir, STUDIO_ACTOR: "agent:cycle" };
  try {
    const stdout = execFileSync("pnpm", ["exec", "tsx", "src/cli/studio.ts", ...args], { env, encoding: "utf8" });
    return { stdout, json: tryParse(stdout), code: 0 };
  } catch (e: any) {
    const stdout = (e.stdout?.toString?.() ?? "") + (e.stderr?.toString?.() ?? "");
    return { stdout, json: tryParse(e.stdout?.toString?.() ?? ""), code: typeof e.status === "number" ? e.status : 1 };
  }
}

function tryParse(s: string): any {
  try { return JSON.parse(s.trim()); } catch { return null; }
}

/** Seed a baseline-ready session (variantCount 1, baseline A) from the given fixture. */
export function seedBaseline(dataDir: string, fixture = "e2e/fixtures/base.html"): string {
  const open = cli(["session", "open", "--variants", "1"], dataDir);
  const sid = open.json.sessionId as string;
  cli(["prompt", "submit", sid, "p"], dataDir);
  cli(["variants", "register", sid, "--label", "A", "--file", fixture], dataDir);
  cli(["baseline", "select", sid, "A"], dataDir);
  return sid;
}

/** Scaffolding: reach the RevisionApplied (staged) screen — a candidate is staged, head NOT advanced. */
export function seedStaged(dataDir: string): string {
  const sid = seedBaseline(dataDir);
  cli(["comment", "add", sid, "--od-id", "cta.primary", "--selector", "[data-od-id=cta.primary]", "--label", "Primary button", "--intent", "reword", "--note", "say Continue"], dataDir);
  const syn = cli(["synthesize", sid], dataDir);
  const batchId = syn.json.batch.batchId as string;
  cli(["batch", "approve", sid, batchId], dataDir);
  cli(["apply", sid, batchId, "--candidate-from", "e2e/fixtures/continue.html"], dataDir);
  return sid;
}

export async function freePort(): Promise<number> {
  return new Promise((resolve) => {
    const s = net.createServer();
    s.listen(0, "127.0.0.1", () => {
      const port = (s.address() as net.AddressInfo).port;
      s.close(() => resolve(port));
    });
  });
}

export interface PreviewHandle {
  url: string;
  port: number;
  stop(): void;
}

/** Launch `studio preview` on an ephemeral port; resolve once it prints its URL. */
export async function startPreview(sid: string, dataDir: string): Promise<PreviewHandle> {
  const port = await freePort();
  const proc: ChildProcess = spawn("pnpm", ["exec", "tsx", "src/cli/studio.ts", "preview", sid, "--port", String(port)], {
    env: { ...process.env, STUDIO_DATA: dataDir },
  });
  await new Promise<void>((resolve, reject) => {
    let buf = "";
    const timer = setTimeout(() => reject(new Error("preview did not start in time")), 30_000);
    proc.stdout!.on("data", (d) => {
      buf += d.toString();
      if (buf.includes("\"preview\"")) { clearTimeout(timer); resolve(); }
    });
    proc.on("exit", () => { clearTimeout(timer); });
  });
  return { url: `http://127.0.0.1:${port}/preview/${sid}`, port, stop: () => proc.kill() };
}
