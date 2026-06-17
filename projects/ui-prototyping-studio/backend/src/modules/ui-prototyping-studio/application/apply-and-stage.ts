import type { ArtifactContentPort } from "./artifact-content-port.js";
import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import { diffByOdId } from "./admission.js";
import { validateAndStage } from "./two-gate-apply.js";
import { resolveCurrentHtml } from "./current-html.js";
import type { DiffSummaryHonest, StudioSession } from "../domain/models.js";

export interface ApplyAndStageInput {
  sessionId: string;
  batchId: string;
  candidateHtml: string;
  requestedBy: string;
}

export type ApplyAndStageResult =
  | { verdict: "REJECT" }
  | {
      verdict: "NOT_REJECT";
      session: StudioSession;
      stagedRef: string;
      candidateHtmlHash: string;
      diff: DiffSummaryHonest;
    };

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ApplyAndStage
 *     type: Operation
 *
 * MW1 — gate 2A. Resolve current head HTML, validate the agent-proposed candidate against the
 * scope fence (M1), and on admit STAGE it at a temp ref (RevisionApplied, head NOT advanced).
 * Returns the honest od-id diff for the human's accept-diff. On REJECT, writes nothing.
 */
export function makeApplyAndStageUseCase(
  store: StudioSessionStorePort,
  artifact: ArtifactContentPort | null,
) {
  return function applyAndStage(input: ApplyAndStageInput): ApplyAndStageResult {
    if (!artifact) {
      throw createUiPrototypingStudioError(
        "ARTIFACT_CONTENT_PORT_UNAVAILABLE",
        "Two-gate apply requires an artifact content store",
        { sessionId: input.sessionId },
      );
    }
    if (input.requestedBy.trim().toLowerCase() === "system:auto") {
      throw createUiPrototypingStudioError("AUTO_APPLY_FORBIDDEN", "Auto-apply is forbidden", {
        applyRequestedBy: input.requestedBy,
      });
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
        "Baseline gate must be satisfied before apply",
        { sessionId: session.sessionId },
      );
    }

    const batch = store.getBatch(session.sessionId, input.batchId);
    if (!batch) {
      throw createUiPrototypingStudioError("BATCH_NOT_FOUND", "Batch not found", {
        sessionId: session.sessionId,
        batchId: input.batchId,
      });
    }
    if (batch.status !== "approved") {
      throw createUiPrototypingStudioError(
        "BATCH_APPROVAL_REQUIRED",
        "Batch must be approved before apply",
        { batchId: batch.batchId, status: batch.status },
      );
    }
    if (session.revisionHeadId !== null && batch.sourceRevisionId !== session.revisionHeadId) {
      throw createUiPrototypingStudioError(
        "BATCH_STALE_FOR_HEAD",
        "Batch source revision is stale for current revision head",
        { revisionHeadId: session.revisionHeadId, sourceRevisionId: batch.sourceRevisionId },
      );
    }

    const currentHtml = resolveCurrentHtml(session, store, artifact);
    if (currentHtml === null) {
      throw createUiPrototypingStudioError(
        "CURRENT_HTML_UNRESOLVABLE",
        "Current head HTML is unresolvable (variants must be registered with real HTML — MR1)",
        { sessionId: session.sessionId },
      );
    }

    const scopeOdIds = batch.tasks
      .map((task) => task.odId)
      .filter((odId): odId is string => odId !== null && odId.length > 0);
    if (scopeOdIds.length === 0) {
      throw createUiPrototypingStudioError(
        "SCOPE_EMPTY",
        "Approved batch has no od-id task scope; cannot validate a candidate",
        { batchId: batch.batchId },
      );
    }

    const staged = validateAndStage(currentHtml, input.candidateHtml, scopeOdIds, artifact);
    if (staged.verdict === "REJECT") {
      return { verdict: "REJECT" };
    }

    store.saveStagedCandidate(session.sessionId, {
      stagedRef: staged.stagedRef,
      candidateHtmlHash: staged.candidateHtmlHash,
      batchId: batch.batchId,
    });
    const nextSession: StudioSession = { ...session, state: "RevisionApplied" };
    store.saveSession(nextSession);

    return {
      verdict: "NOT_REJECT",
      session: nextSession,
      stagedRef: staged.stagedRef,
      candidateHtmlHash: staged.candidateHtmlHash,
      diff: diffByOdId(currentHtml, input.candidateHtml),
    };
  };
}
