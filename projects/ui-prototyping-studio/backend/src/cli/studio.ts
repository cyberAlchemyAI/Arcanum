#!/usr/bin/env tsx
import { mkdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

import { isUiPrototypingStudioError } from "../modules/ui-prototyping-studio/domain/errors.js";
import type { VariantLabel } from "../modules/ui-prototyping-studio/domain/models.js";
import { createStudioOrchestrationModule } from "../modules/ui-prototyping-studio/application/studio-orchestration-module.js";
import { createFileBackedStudioSessionStore } from "../modules/ui-prototyping-studio/infrastructure/file-studio-session-store.js";
import { createFileArtifactContentStore } from "../modules/ui-prototyping-studio/infrastructure/file-artifact-content-store.js";

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.StudioCli
 *     type: Interface
 *
 * SWU-X2 — the `studio` CLI: the single operation surface for both Claude Code and
 * the human (DEC-CLI-NOT-MCP-012). Wraps the orchestration module; gate enforcement
 * lives in the core, not in flags. JSON to stdout; non-zero exit on error.
 *
 * Drift note: the two-gate apply (`apply`→stage→`accept`) is SWU-M2; here `batch apply`
 * uses the existing applyApprovedBatch (L0 bookkeeping). `variants generate` uses the
 * deterministic stub generator (the `--fake` testable-surface path; real generation is
 * Claude Code via `variants register`, M-later).
 */
const ACTOR = process.env.STUDIO_ACTOR ?? "cli-user";
const DATA_PATH = process.env.STUDIO_DATA ?? join(process.cwd(), ".data/studio.json");
const DOCS_ROOT = process.env.STUDIO_DOCS_ROOT ?? process.cwd();

function parse(argv: string[]): { args: string[]; flags: Record<string, string> } {
  const args: string[] = [];
  const flags: Record<string, string> = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith("--")) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = "true";
      }
    } else {
      args.push(a);
    }
  }
  return { args, flags };
}

function out(value: unknown): void {
  process.stdout.write(JSON.stringify(value, null, 2) + "\n");
}

function main(): void {
  mkdirSync(dirname(DATA_PATH), { recursive: true });
  const store = createFileBackedStudioSessionStore({ filePath: DATA_PATH });
  const artifactContentStore = createFileArtifactContentStore({
    rootDir: resolve(dirname(DATA_PATH), "artifacts"),
  });
  const studio = createStudioOrchestrationModule(store, {
    featureDocsRootDir: resolve(DOCS_ROOT),
    artifactContentStore,
  });

  const [, , ...rest] = process.argv;
  const { args, flags } = parse(rest);
  const GROUPS = new Set(["session", "prompt", "variants", "baseline", "batch", "comment", "handoff"]);
  const cmd = GROUPS.has(args[0] ?? "") ? `${args[0]} ${args[1] ?? ""}`.trim() : (args[0] ?? "");
  const sid = (n: number) => args[n] ?? flags["session"] ?? "";
  const activeRevision = (sessionId: string): string => {
    const session = studio.getSessionSnapshot({ sessionId });
    return session.revisionHeadId ?? "rev-0000";
  };

  switch (cmd) {
    case "session open":
      out(studio.initializeSession({
        requestedVariantCount: flags["variants"] ? Number(flags["variants"]) : undefined,
        requestedBy: ACTOR,
      }));
      break;
    case "prompt submit":
      out(studio.submitPrompt({ sessionId: args[2]!, prompt: args.slice(3).join(" ") || flags["text"]!, submittedBy: ACTOR }));
      break;
    case "variants generate":
      out(studio.generateVariants({ sessionId: args[2]!, requestedBy: ACTOR }));
      break;
    case "variants register": {
      // MR1 + GAP-018: real registration. Two equivalent ingestion forms:
      //   --from <dir>                      reads <label>.html per session label, OR
      //   --label A --file a.html (repeat)  ordered pairs scanned from raw argv (parser is last-wins).
      const sessionId = args[2]!;
      const fromDir = flags["from"];
      let variants: { label: VariantLabel; html: string }[];
      if (fromDir) {
        const snapshot = studio.getSessionSnapshot({ sessionId });
        variants = snapshot.variantLabels.map((label) => ({
          label,
          html: readFileSync(join(resolve(fromDir), `${label.toLowerCase()}.html`), "utf8"),
        }));
      } else {
        // Walk raw argv for ordered --label X --file path pairs.
        const pairs: { label: VariantLabel; file: string }[] = [];
        for (let i = 0; i < rest.length; i++) {
          if (rest[i] === "--label" && rest[i + 2] === "--file") {
            pairs.push({ label: rest[i + 1] as VariantLabel, file: rest[i + 3]! });
            i += 3;
          }
        }
        if (pairs.length === 0) {
          process.stderr.write(
            JSON.stringify({ code: "OD_ID_MISSING", message: "variants register needs --from <dir> OR repeated --label X --file path", details: {} }) + "\n",
          );
          process.exit(2);
        }
        variants = pairs.map((p) => ({ label: p.label, html: readFileSync(resolve(p.file), "utf8") }));
      }
      const reg = studio.registerVariants({ sessionId, variants, requestedBy: ACTOR });
      out({ ...reg, openPaths: reg.variants.map((v) => artifactContentStore.pathForRef(v.htmlArtifactRef)).filter(Boolean) });
      break;
    }
    case "baseline select":
      out(studio.selectOrCommitBaseline({ sessionId: args[2]!, selectedLabel: args[3] ?? flags["label"], requestedBy: ACTOR }));
      break;
    case "baseline commit":
      out(studio.selectOrCommitBaseline({ sessionId: args[2]!, requestedBy: ACTOR }));
      break;
    case "state":
      out({
        session: studio.getSessionSnapshot({ sessionId: args[1]! }),
        variants: studio.listSessionVariants({ sessionId: args[1]! }),
      });
      break;
    case "comment add":
      out(studio.captureCommentEvent({
        sessionId: args[2]!,
        revisionId: flags["revision"] ?? activeRevision(args[2]!),
        target: { selector: flags["selector"]!, elementLabel: flags["label"] ?? "", odId: flags["od-id"] ?? null },
        severity: flags["severity"] ?? "medium",
        intent: flags["intent"] ?? "",
        note: flags["note"] ?? "",
        createdBy: ACTOR,
      }));
      break;
    case "synthesize":
      out(studio.synthesizeMutationBatch({ sessionId: args[1]!, sourceRevisionId: flags["revision"] ?? activeRevision(args[1]!), requestedBy: ACTOR }));
      break;
    case "batch approve":
      out(studio.approveMutationBatch({ sessionId: args[2]!, batchId: args[3]!, approvedBy: ACTOR, approvedAt: new Date().toISOString() }));
      break;
    case "batch apply":
      out(studio.applyApprovedBatch({ sessionId: args[2]!, batchId: args[3]!, applyRequestedBy: ACTOR }));
      break;
    case "apply": {
      // MW1 two-gate: stage an agent-proposed candidate (does NOT advance head).
      const ap = studio.applyAndStage({
        sessionId: args[1]!,
        batchId: args[2]!,
        candidateHtml: readFileSync(resolve(flags["candidate-from"]!), "utf8"),
        requestedBy: ACTOR,
      });
      out(ap.verdict === "NOT_REJECT" ? { ...ap, openPath: artifactContentStore.pathForRef(ap.stagedRef) } : ap);
      break;
    }
    case "accept": {
      // MW1 two-gate B: human accepts the previewed candidate; head advances by one.
      const ac = studio.acceptStagedRevision({ sessionId: args[1]!, acceptedAt: new Date().toISOString(), requestedBy: ACTOR });
      const acceptedRef = ac.revision.candidateHtmlHash ? `artifact:${ac.revision.candidateHtmlHash}` : null;
      out({ ...ac, openPath: acceptedRef ? artifactContentStore.pathForRef(acceptedRef) : null });
      break;
    }
    case "discard":
      out(studio.discardStagedRevision({ sessionId: args[1]!, requestedBy: ACTOR }));
      break;
    case "revisions":
      out(studio.listRevisionManifest({ sessionId: args[1]! }));
      break;
    case "handoff export":
      out(studio.exportDesignHandoff({ sessionId: args[2]!, requestedBy: ACTOR }));
      break;
    default:
      process.stderr.write(
        "studio <session open|prompt submit|variants generate|baseline select|baseline commit|state|comment add|synthesize|batch approve|batch apply|revisions|handoff export> ...\n",
      );
      process.exit(2);
  }
}

try {
  main();
} catch (err) {
  if (isUiPrototypingStudioError(err)) {
    process.stderr.write(JSON.stringify({ code: err.code, message: err.message, details: err.details }, null, 2) + "\n");
    process.exit(2);
  }
  process.stderr.write(String(err instanceof Error ? err.stack : err) + "\n");
  process.exit(1);
}
