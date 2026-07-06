import { createHash } from "node:crypto";

import type { ArtifactContentPort } from "./artifact-content-port.js";
import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import { admitScope, diffByOdId, odIdsIn } from "./admission.js";
import { resolveCurrentHtml } from "./current-html.js";
import type { RevisionManifestEntry, StudioSession } from "../domain/models.js";

export type CycleMode = "explore" | "exploit";

/** An agent-proposed candidate. The generative act + the self-critique score are the agent's (ML2 lighter
 *  fitness = self-critique vs the human objective); the core does the gate + auto-accept bookkeeping. */
export interface CycleCandidate {
  html: string;
  /** self-critique fitness vs the objective (higher = better); explore scores for diversity, exploit for fit. */
  score: number;
  rationale?: string;
}

export interface RunCycleInput {
  sessionId: string;
  mode: CycleMode;
  /** The human-owned objective. AUTO refuses an empty objective (the start gate) — exploit toward something. */
  objective: string;
  candidates: CycleCandidate[];
  requestedBy: string;
  at: string;
  /** N7 — max AUTO cycles per session enforced IN THE CORE (not just the agent loop). Default 25. */
  maxCycles?: number;
}

const DEFAULT_MAX_CYCLES = 25;

export interface RunCycleResult {
  session: StudioSession;
  mode: CycleMode;
  staged: number;
  rejected: number;
  /** the auto-accepted winner, or null when no candidate cleared the fence. */
  chosen: { candidateHtmlHash: string; score: number; revisionId: string } | null;
  revision: RevisionManifestEntry | null;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.RunCycle
 *     type: Operation
 *
 * ML1+ML2+ML3 (AUTO mode core) — one bounded exploit/explore cycle. The agent supplies candidate HTML
 * + a self-critique score against the human objective; the core gates each candidate through the M1 scope
 * fence, then AUTO-ACCEPTS the top-scoring admitted candidate (advances head). Safe because reversible
 * (CL5 `revert`) + visible (preview) — control is reversibility, not gating (DEC-026). The two modes differ
 * in the fence: EXPLOIT may only refine od-ids already in the head (converge within the structure); EXPLORE
 * may introduce new od-ids (diverge), with integrity still enforced (no re-tag/forge of a baseline od-id).
 * Stop dials (loop_cap / max_loops / plateau) live in the DRIVER (`studio watch` / the agent `/loop`), not here.
 */
export function makeRunCycleUseCase(
  store: StudioSessionStorePort,
  artifact: ArtifactContentPort | null,
) {
  return function runCycle(input: RunCycleInput): RunCycleResult {
    if (!artifact) {
      throw createUiPrototypingStudioError(
        "ARTIFACT_CONTENT_PORT_UNAVAILABLE",
        "A cycle requires an artifact content store",
        { sessionId: input.sessionId },
      );
    }
    if (input.objective.trim().length === 0) {
      throw createUiPrototypingStudioError(
        "AUTO_OBJECTIVE_REQUIRED",
        "AUTO mode refuses an empty objective — there is nothing to exploit toward",
        { sessionId: input.sessionId, mode: input.mode },
      );
    }
    if (input.candidates.length === 0) {
      throw createUiPrototypingStudioError(
        "CYCLE_CANDIDATES_REQUIRED",
        "A cycle needs at least one agent-proposed candidate",
        { sessionId: input.sessionId, mode: input.mode },
      );
    }
    // N6 (F9): a self-critique score must be a finite number — reject NaN/missing/±Inf so a malformed or
    // gamed score can't silently auto-win (tie-break is documented: first-seen among equal top scores).
    for (const candidate of input.candidates) {
      if (typeof candidate.score !== "number" || !Number.isFinite(candidate.score)) {
        throw createUiPrototypingStudioError(
          "CYCLE_SCORE_INVALID",
          "Each candidate needs a finite self-critique score",
          { sessionId: input.sessionId, score: candidate.score },
        );
      }
    }

    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError("SESSION_NOT_FOUND", "Session not found", {
        sessionId: input.sessionId,
      });
    }
    if (session.selectionGate !== "satisfied" || !session.baseline) {
      throw createUiPrototypingStudioError(
        "BASELINE_GATE_UNSATISFIED",
        "Baseline gate must be satisfied before a cycle",
        { sessionId: session.sessionId },
      );
    }

    // N7 (F10): the stop dial is enforced in the CORE, not only the agent loop — count prior AUTO cycles
    // (revisions stamped `cycle:*`) and refuse beyond the ceiling so an unattended loop cannot run unbounded.
    const ceiling = input.maxCycles ?? DEFAULT_MAX_CYCLES;
    const priorCycles = store
      .listRevisions(session.sessionId)
      .filter((entry) => entry.appliedBatchId.startsWith("cycle:")).length;
    if (priorCycles >= ceiling) {
      throw createUiPrototypingStudioError(
        "CYCLE_CEILING_REACHED",
        "AUTO cycle ceiling reached for this session",
        { sessionId: session.sessionId, priorCycles, ceiling },
      );
    }

    const currentHtml = resolveCurrentHtml(session, store, artifact);
    if (currentHtml === null) {
      throw createUiPrototypingStudioError(
        "CURRENT_HTML_UNRESOLVABLE",
        "Current head HTML is unresolvable (register variants with real HTML — MR1)",
        { sessionId: session.sessionId },
      );
    }
    const headOdIds = odIdsIn(currentHtml);

    // Gate every candidate; keep only the admitted, ranked by self-critique score.
    let rejected = 0;
    const admitted: CycleCandidate[] = [];
    for (const candidate of input.candidates) {
      // exploit fence = head od-ids only; explore fence = head ∪ candidate's own (free divergence, integrity kept).
      const scope =
        input.mode === "exploit"
          ? headOdIds
          : [...new Set([...headOdIds, ...odIdsIn(candidate.html)])];
      if (admitScope(currentHtml, candidate.html, scope) === "REJECT") {
        rejected += 1;
        continue;
      }
      admitted.push(candidate);
    }

    if (admitted.length === 0) {
      return { session, mode: input.mode, staged: 0, rejected, chosen: null, revision: null };
    }

    const winner = admitted.reduce((best, c) => (c.score > best.score ? c : best), admitted[0]!);

    // AUTO-accept the winner (reversible via CL5). Append exactly one revision; advance head.
    const committedRef = artifact.commitHtml(artifact.stageHtml(winner.html).stagedRef);
    const candidateHtmlHash = committedRef.replace(/^artifact:/, "");
    const honest = diffByOdId(currentHtml, winner.html);
    const previousCount = store.listRevisions(session.sessionId).length;
    const parentRevisionId = session.revisionHeadId ?? "rev-0000";
    const revisionId = store.allocateRevisionId(parentRevisionId);

    const revision: RevisionManifestEntry = {
      revisionId,
      parentRevisionId,
      sessionId: session.sessionId,
      variantCount: session.variantCount,
      baseline: session.baseline,
      appliedBatchId: `cycle:${input.mode}`,
      appliedTaskIds: [],
      unresolvedCommentIds: [],
      diffSummary: { added: honest.added, changed: honest.changed, removed: honest.removed },
      diffSummaryHonest: honest,
      candidateHtmlHash,
      executionProvenance: {
        proposer: input.requestedBy,
        promptHash: hash(input.objective),
        inputHtmlHash: hash(currentHtml),
        candidateHtmlHash,
        verdictHash: hash(`${input.mode}:${winner.score}`),
      },
      createdAt: input.at,
    };

    const nextSession: StudioSession = {
      ...session,
      revisionHeadId: revisionId,
      applyGate: "satisfied",
      state: "RevisionRecorded",
    };

    store.appendRevision(revision);
    store.saveSession(nextSession);

    const nextCount = store.listRevisions(session.sessionId).length;
    if (nextCount !== previousCount + 1) {
      throw createUiPrototypingStudioError(
        "VARIANT_GENERATION_COUNT_MISMATCH",
        "A cycle must append exactly one revision manifest entry",
        { previousCount, nextCount, sessionId: session.sessionId },
      );
    }

    return {
      session: nextSession,
      mode: input.mode,
      staged: admitted.length,
      rejected,
      chosen: { candidateHtmlHash, score: winner.score, revisionId },
      revision,
    };
  };
}

function hash(text: string): string {
  return createHash("sha256").update(text).digest("hex");
}
