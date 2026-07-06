#!/usr/bin/env tsx
import { mkdirSync, readFileSync } from "node:fs";
import { createServer } from "node:http";
import { dirname, join, resolve } from "node:path";

import { diffByOdId } from "../modules/ui-prototyping-studio/application/admission.js";
import { resolveCurrentHtml } from "../modules/ui-prototyping-studio/application/current-html.js";

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
    case "preview": {
      // P1+P2: an ephemeral loopback HTTP server that renders the session's variants (and, when a
      // candidate is staged, the before/after + honest diff) as a no-build page. Open the printed URL
      // in VSCode "Simple Browser". Served via node:http (NOT the scoped fastify app) and bound to
      // 127.0.0.1 only. State is read fresh per request, so refresh the page after each CLI command.
      const sessionId = args[1]!;
      const port = flags["port"] ? Number(flags["port"]) : 0; // N11: 0 = OS-assigned free port (no fixed-port EADDRINUSE)
      const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      const stateSentence: Record<string, string> = {
        SessionInitialized: "Session open. Submit a prompt, then register variants.",
        PromptCaptured: "Prompt recorded. Register variants (real HTML with data-od-id).",
        VariantsReady: "Variants are in. Pick a baseline: studio baseline select <sid> <A|B|C>.",
        BaselineReady: "Baseline chosen. Comment on a component, then synthesize.",
        CommentsCaptured: "Comments captured. Synthesize a mutation batch.",
        MutationDrafted: "Batch drafted. Approve it: studio batch approve <sid> <bid>.",
        MutationApproved: "Batch approved. Apply a candidate: studio apply <sid> <bid> --candidate-from <file>.",
        RevisionApplied: "A candidate is STAGED (head not advanced). Review the diff below, then studio accept <sid> (or studio discard <sid>).",
        RevisionRecorded: "Revision recorded. Comment again to iterate, or studio handoff export <sid>.",
        SessionCompleted: "Session complete.",
      };
      const renderPage = (): string => {
        const session = studio.getSessionSnapshot({ sessionId });
        const variants = studio.listSessionVariants({ sessionId });
        const staged = store.getStagedCandidate(sessionId);
        const cards = variants.map((v) => {
          const isBaseline = session.baseline?.label === v.variantLabel;
          return `<figure class="card"><figcaption>${v.variantLabel}${isBaseline ? " · baseline" : ""} <span class="muted">${esc(v.status)}</span></figcaption>`
            + `<iframe sandbox src="/raw/variant/${v.variantLabel}" title="variant ${v.variantLabel}"></iframe></figure>`;
        }).join("");
        let pending = "";
        if (staged) {
          const current = resolveCurrentHtml(session, store, artifactContentStore);
          const candidate = artifactContentStore.readHtml(staged.stagedRef);
          const diff = current !== null && candidate !== null ? diffByOdId(current, candidate) : null;
          const frags = diff ? diff.fragments.map((f) => `<li><code>${esc(String(f.odId))}</code>: +${f.added} ~${f.changed} -${f.removed}</li>`).join("") : "<li>(diff unavailable)</li>";
          pending = `<section class="pending"><h2>Pending change — review before you accept</h2>`
            + `<p class="muted">Honest per-component diff: ${diff ? `+${diff.added} added · ~${diff.changed} changed · -${diff.removed} removed` : "n/a"}</p>`
            + `<ul class="diff">${frags}</ul>`
            + `<div class="grid two"><figure class="card"><figcaption>before (current)</figcaption><iframe sandbox src="/raw/baseline"></iframe></figure>`
            + `<figure class="card"><figcaption>after (candidate)</figcaption><iframe sandbox src="/raw/staged"></iframe></figure></div>`
            // N3: complete the loop IN the browser — accept/discard are reversible, so they get buttons.
            // Export (the one irreversible edge) deliberately has NO button; it stays terminal + --confirm.
            + `<p><button id="btn-accept">Accept this change</button> <button id="btn-discard">Discard</button> <span id="act-msg" class="muted"></span></p>`
            + `<p class="muted">Export (the one irreversible step) stays terminal-only: <code>studio handoff export ${esc(sessionId)} --confirm</code></p></section>`;
        }
        // N3: on a recorded head, offer Revert in-browser (reversible). Export still has no button here.
        const recorded = (!staged && session.revisionHeadId && session.revisionHeadId !== "rev-0000")
          ? `<section class="recorded"><p>Head is at <code>${esc(session.revisionHeadId)}</code>. <button id="btn-revert">Revert last change</button> <span id="act-msg2" class="muted"></span></p></section>`
          : "";
        // CL1: annotate panel — click a component in the (trusted, script-injected) baseline wrapper to comment.
        const annotate = session.baseline
          ? `<section class="annotate"><h2>Annotate <span class="muted">— click a component to comment</span></h2>`
            + `<iframe id="annot" sandbox="allow-scripts" src="/annotate/variant/${session.baseline.label}" title="annotate"></iframe>`
            + `<form id="cf" class="cf" hidden><p>Target: <code id="cf-od"></code></p>`
            + `<input name="severity" value="medium"><input name="intent" placeholder="intent (e.g. reword)">`
            + `<input name="note" placeholder="note"><button type="submit">Add comment</button> <span id="cf-msg" class="muted"></span></form></section>`
          : "";
        // CL4: poll /state; reload only when state/head/staged changes (no janky full meta-refresh).
        const pollScript = `<script>let last=null;setInterval(async()=>{try{const r=await fetch('/state');const s=await r.json();`
          + `const sig=s.state+'|'+s.head+'|'+s.stagedHash;if(last!==null&&last!==sig)location.reload();last=sig;}catch(e){}},1500);</script>`;
        const cfScript = session.baseline
          ? `<script>const cf=document.getElementById('cf'),od=document.getElementById('cf-od'),msg=document.getElementById('cf-msg');let cur=null;`
            + `window.addEventListener('message',e=>{if(e.data&&e.data.odId){cur=e.data;od.textContent=e.data.odId;cf.hidden=false;}});`
            + `cf&&cf.addEventListener('submit',async ev=>{ev.preventDefault();const f=new FormData(cf);`
            + `const body={odId:cur.odId,selector:cur.selector,elementLabel:cur.label||cur.odId,severity:f.get('severity'),intent:f.get('intent'),note:f.get('note')};`
            + `const r=await fetch('/comment',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});`
            + `msg.textContent=r.ok?'captured ✓':('error '+r.status);if(r.ok)cf.reset();});</script>`
          : "";
        // N3: wire the in-browser Accept/Discard/Revert buttons to their POST routes (reversible verbs only).
        const actScript = `<script>function post(u,m){return fetch(u,{method:'POST'}).then(r=>{var e=document.getElementById(m);`
          + `if(e)e.textContent=r.ok?'done ✓':('error '+r.status);if(r.ok)setTimeout(()=>location.reload(),300);});}`
          + `var a=document.getElementById('btn-accept');a&&a.addEventListener('click',()=>post('/accept','act-msg'));`
          + `var d=document.getElementById('btn-discard');d&&d.addEventListener('click',()=>post('/discard','act-msg'));`
          + `var v=document.getElementById('btn-revert');v&&v.addEventListener('click',()=>post('/revert','act-msg2'));</script>`;
        return `<!doctype html><html><head><meta charset="utf-8"><title>studio · ${esc(sessionId)}</title>`
          + `<style>body{font-family:system-ui;margin:0;background:#fafafa;color:#111}header{padding:16px 24px;background:#111;color:#fff}`
          + `.muted{color:#888;font-weight:400}main{padding:24px}.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}.two{grid-template-columns:1fr 1fr}`
          + `.card{margin:0;border:1px solid #e5e5e5;border-radius:10px;background:#fff;overflow:hidden}figcaption{padding:8px 12px;font-weight:600;border-bottom:1px solid #eee}`
          + `iframe{width:100%;height:340px;border:0;background:#fff}.pending{margin-top:32px;padding:16px;border:2px solid #f0b000;border-radius:12px;background:#fffdf5}`
          + `.annotate{margin-top:32px;padding:16px;border:1px solid #cdd;border-radius:12px;background:#f5fbff}.cf{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}.cf input{padding:6px 8px;border:1px solid #ccc;border-radius:6px}`
          + `.diff{font-family:ui-monospace,monospace}code{background:#f0f0f0;padding:1px 5px;border-radius:4px}</style></head><body>`
          + `<header><strong>ui-prototyping-studio</strong> · ${esc(sessionId)} · <span class="muted">${esc(session.state)}</span><br>`
          + `<span class="muted">${esc(stateSentence[session.state] ?? "")}</span></header>`
          + `<main><div class="grid">${cards || "<p>No variants yet — register some.</p>"}</div>${annotate}${pending}${recorded}</main>${pollScript}${cfScript}${actScript}</body></html>`;
      };
      // CL1: inject ONLY a trusted click→postMessage handler into the (already-trusted, registered)
      // variant HTML. Raw /raw/* stays fully sandboxed; this wrapper alone gets sandbox="allow-scripts".
      const annotateClickScript = `<script>document.addEventListener('click',function(e){let n=e.target;`
        + `while(n&&n!==document.documentElement){if(n.getAttribute&&n.getAttribute('data-od-id')){var id=n.getAttribute('data-od-id');`
        + `parent.postMessage({odId:id,selector:'[data-od-id='+id+']',label:(n.textContent||'').trim().slice(0,40)},'*');e.preventDefault();return;}n=n.parentNode;}},true);</script>`;
      const server = createServer((req, res) => {
        try {
          const url = (req.url ?? "/").split("?")[0]!;
          const sendHtml = (html: string | null) => {
            if (html === null) { res.writeHead(404, { "content-type": "text/plain" }); res.end("not found"); return; }
            res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); res.end(html);
          };
          const sendJson = (code: number, value: unknown) => {
            res.writeHead(code, { "content-type": "application/json" }); res.end(JSON.stringify(value));
          };
          // CL1: capture a comment from the annotate overlay (browser → studio write).
          if (req.method === "POST" && url === "/comment") {
            let raw = "";
            req.on("data", (c) => { raw += c; });
            req.on("end", () => {
              try {
                const b = JSON.parse(raw || "{}");
                const snap = studio.getSessionSnapshot({ sessionId });
                const c = studio.captureCommentEvent({
                  sessionId,
                  revisionId: snap.revisionHeadId ?? "rev-0000",
                  target: { selector: String(b.selector ?? ""), elementLabel: String(b.elementLabel ?? ""), odId: b.odId ?? null },
                  severity: String(b.severity ?? "medium"),
                  intent: String(b.intent ?? ""),
                  note: String(b.note ?? ""),
                  createdBy: "web-ui",
                });
                sendJson(200, { ok: true, commentId: c.commentId });
              } catch (err) {
                sendJson(isUiPrototypingStudioError(err) ? 400 : 500, { ok: false, error: isUiPrototypingStudioError(err) ? err.code : String(err) });
              }
            });
            return;
          }
          // N3: complete the loop in-browser — accept/discard/revert are reversible, so the preview drives them.
          // Export is NOT here: it stays terminal-only (`handoff export --confirm`), the one irreversible edge.
          if (req.method === "POST" && (url === "/accept" || url === "/discard" || url === "/revert")) {
            try {
              if (url === "/accept") studio.acceptStagedRevision({ sessionId, acceptedAt: new Date().toISOString(), requestedBy: "web-ui" });
              else if (url === "/discard") studio.discardStagedRevision({ sessionId, requestedBy: "web-ui" });
              else studio.revertRevision({ sessionId, requestedBy: "web-ui", revertedAt: new Date().toISOString() });
              sendJson(200, { ok: true });
            } catch (err) {
              sendJson(isUiPrototypingStudioError(err) ? 400 : 500, { ok: false, error: isUiPrototypingStudioError(err) ? err.code : String(err) });
            }
            return;
          }
          const session = studio.getSessionSnapshot({ sessionId });
          if (url === "/state") {
            // CL4: cheap change signal for the page's poll-refresh.
            const staged = store.getStagedCandidate(sessionId);
            sendJson(200, { state: session.state, head: session.revisionHeadId, stagedHash: staged?.candidateHtmlHash ?? null });
          } else if (url.startsWith("/annotate/variant/")) {
            const label = url.slice("/annotate/variant/".length);
            const v = studio.listSessionVariants({ sessionId }).find((x) => x.variantLabel === label);
            const html = v ? artifactContentStore.readHtml(v.htmlArtifactRef) : null;
            sendHtml(html === null ? null : html + annotateClickScript);
          } else if (url.startsWith("/raw/variant/")) {
            const label = url.slice("/raw/variant/".length);
            const v = studio.listSessionVariants({ sessionId }).find((x) => x.variantLabel === label);
            sendHtml(v ? artifactContentStore.readHtml(v.htmlArtifactRef) : null);
          } else if (url === "/raw/staged") {
            const staged = store.getStagedCandidate(sessionId);
            sendHtml(staged ? artifactContentStore.readHtml(staged.stagedRef) : null);
          } else if (url === "/raw/baseline") {
            sendHtml(resolveCurrentHtml(session, store, artifactContentStore));
          } else {
            sendHtml(renderPage());
          }
        } catch (e) {
          res.writeHead(500, { "content-type": "text/plain" });
          res.end(isUiPrototypingStudioError(e) ? `${e.code}: ${e.message}` : String(e));
        }
      });
      // N11: surface bind failures (e.g. an explicit --port already in use) instead of an unhandled throw.
      server.on("error", (e) => {
        process.stderr.write(`preview server failed to start: ${String(e)}\n`);
        process.exit(1);
      });
      server.listen(port, "127.0.0.1", () => {
        const actualPort = (server.address() as { port: number }).port; // N11: real (OS-assigned when port=0)
        out({ preview: `http://127.0.0.1:${actualPort}/preview/${sessionId}`, hint: "open in VSCode: Command Palette → 'Simple Browser: Show' → paste the URL. Ctrl-C to stop." });
      });
      break; // keep the process alive (server holds the event loop)
    }
    case "revert": {
      // CL5: append an inverse revision restoring a prior state (DEC-026). Head moves forward,
      // content goes back, history intact, re-revertible. `--to <revId|baseline>` or undo one step.
      const rv = studio.revertRevision({
        sessionId: args[1]!,
        targetRevisionId: flags["to"],
        requestedBy: ACTOR,
        revertedAt: new Date().toISOString(),
      });
      const restoredRef = rv.revision.candidateHtmlHash ? `artifact:${rv.revision.candidateHtmlHash}` : null;
      out({ ...rv, openPath: restoredRef ? artifactContentStore.pathForRef(restoredRef) : null });
      break;
    }
    case "pending":
      // CL2: comments on the head not yet folded into a batch — the agent-pickup drain.
      out(studio.listPendingComments({ sessionId: args[1]! }));
      break;
    case "watch": {
      // ML4 driver tick (single-shot — the agent's /loop calls this each interval). Generation +
      // synthesis are the AGENT's act; this reports what's pending + the recommended next action.
      // Stop dials (loop_cap/max_loops/plateau) live in the agent loop, not here.
      const sessionId = args[1]!;
      const snap = studio.getSessionSnapshot({ sessionId });
      const pending = studio.listPendingComments({ sessionId });
      out({
        sessionId,
        state: snap.state,
        head: snap.revisionHeadId,
        pendingComments: pending.length,
        suggestion: pending.length
          ? `synthesize → propose candidate → studio cycle ${sessionId} exploit --objective "<obj>" --candidate <file>:<score>`
          : "no pending comments; idle",
      });
      break;
    }
    case "cycle": {
      // ML1/ML2/ML3: one AUTO exploit/explore cycle. The agent supplies candidate HTML files + a
      // self-critique score (path:score); the core gates each through the M1 fence and AUTO-ACCEPTS the
      // top-scoring admitted candidate (reversible via `studio revert`). Empty objective is refused.
      const sessionId = args[1]!;
      const mode = (args[2] ?? "exploit") as "explore" | "exploit";
      const candidates: { html: string; score: number; rationale?: string }[] = [];
      for (let i = 0; i < rest.length; i++) {
        if (rest[i] === "--candidate") {
          const spec = rest[i + 1] ?? "";
          const ix = spec.lastIndexOf(":");
          const path = ix > 0 ? spec.slice(0, ix) : spec;
          const score = ix > 0 ? Number(spec.slice(ix + 1)) : 0;
          candidates.push({ html: readFileSync(resolve(path), "utf8"), score });
        }
      }
      const rc = studio.runCycle({
        sessionId,
        mode,
        objective: flags["objective"] ?? "",
        candidates,
        requestedBy: ACTOR,
        at: new Date().toISOString(),
      });
      const ref = rc.chosen ? `artifact:${rc.chosen.candidateHtmlHash}` : null;
      out({ ...rc, openPath: ref ? artifactContentStore.pathForRef(ref) : null });
      break;
    }
    case "revisions":
      out(studio.listRevisionManifest({ sessionId: args[1]! }));
      break;
    case "handoff export": {
      // CL5: export/handoff is the one IRREVERSIBLE edge (downstream consumption). It requires an
      // explicit human confirm (`--confirm`); without it we refuse and show what WOULD be exported.
      // This is the reversibility model's single human checkpoint — not an identity gate.
      const sessionId = args[2]!;
      if (flags["confirm"] !== "true") {
        const snapshot = studio.getSessionSnapshot({ sessionId });
        out({
          refused: "HANDOFF_CONFIRMATION_REQUIRED",
          reason: "Export is the one irreversible edge (downstream consumption). Re-run with --confirm to proceed.",
          wouldExport: { sessionId, revisionHeadId: snapshot.revisionHeadId, state: snapshot.state },
        });
        process.exitCode = 3;
        break;
      }
      out(studio.exportDesignHandoff({
        sessionId,
        exportProfile: flags["profile"],
        requestedBy: ACTOR,
        confirmedBy: ACTOR,
      }));
      break;
    }
    default:
      process.stderr.write(
        "studio <session open|prompt submit|variants generate|baseline select|baseline commit|state|comment add|synthesize|batch approve|batch apply|apply|accept|discard|revert|preview|revisions|handoff export --confirm> ...\n",
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
