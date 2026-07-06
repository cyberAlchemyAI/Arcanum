import type { ArtifactContentPort } from "./artifact-content-port.js";
import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import { diffByOdId } from "./admission.js";
import { resolveCurrentHtml } from "./current-html.js";
import type { RevisionManifestEntry, StudioSession } from "../domain/models.js";

export interface RevertRevisionInput {
  sessionId: string;
  /**
   * Where to restore content from:
   *  - a revisionId in the manifest → restore that revision's committed HTML,
   *  - "baseline" (or omitted with no parent revision) → restore the committed baseline variant,
   *  - omitted → undo one step (restore the head revision's parent).
   */
  targetRevisionId?: string;
  requestedBy: string;
  revertedAt: string;
}

export interface RevertRevisionResult {
  session: StudioSession;
  revision: RevisionManifestEntry;
  revertedTo: string;
}

const BASELINE_TARGETS = new Set(["baseline", "rev-0000"]);

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.RevertRevision
 *     type: Operation
 *
 * CL5 — the reversibility guarantee (DEC-REVERSIBILITY-NOT-GATING-026). Undo is NOT a
 * destructive head rewind: we append exactly ONE new revision whose committed HTML equals a
 * PRIOR state (a target revision's content, or the baseline). Head moves FORWARD; content goes
 * BACK; the append-only manifest stays a complete, auditable history; the revert is itself
 * re-revertible. Content-addressing means restoring a prior hash re-commits the same artifact.
 */
export function makeRevertRevisionUseCase(
  store: StudioSessionStorePort,
  artifact: ArtifactContentPort | null,
) {
  return function revertRevision(
    input: RevertRevisionInput,
  ): RevertRevisionResult {
    if (!artifact) {
      throw createUiPrototypingStudioError(
        "ARTIFACT_CONTENT_PORT_UNAVAILABLE",
        "Revert requires an artifact content store",
        { sessionId: input.sessionId },
      );
    }
    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError("SESSION_NOT_FOUND", "Session not found", {
        sessionId: input.sessionId,
      });
    }
    const head = session.revisionHeadId;
    if (!head) {
      throw createUiPrototypingStudioError(
        "NO_REVISION_TO_REVERT",
        "No recorded revision to revert",
        { sessionId: session.sessionId },
      );
    }
    const revisions = store.listRevisions(session.sessionId);
    const headRevision = revisions.find((entry) => entry.revisionId === head);

    // Resolve which prior state to restore, and a label for the audit record.
    let restoreFromHash: string | null = null;
    let revertedTo: string;
    if (input.targetRevisionId && !BASELINE_TARGETS.has(input.targetRevisionId)) {
      const target = revisions.find((entry) => entry.revisionId === input.targetRevisionId);
      if (!target) {
        throw createUiPrototypingStudioError(
          "REVISION_NOT_FOUND",
          "Target revision not found in this session's manifest",
          { sessionId: session.sessionId, targetRevisionId: input.targetRevisionId },
        );
      }
      // N4 (F5): a found target with no committed content must ERROR, not silently restore the baseline.
      if (!target.candidateHtmlHash) {
        throw createUiPrototypingStudioError(
          "REVISION_NOT_FOUND",
          "Target revision has no committed content to restore (no candidateHtmlHash)",
          { sessionId: session.sessionId, targetRevisionId: input.targetRevisionId },
        );
      }
      restoreFromHash = target.candidateHtmlHash;
      revertedTo = target.revisionId;
    } else if (input.targetRevisionId) {
      revertedTo = "baseline";
    } else {
      // Undo one step: the head revision's parent.
      const parentId = headRevision?.parentRevisionId;
      const parent =
        parentId && !BASELINE_TARGETS.has(parentId)
          ? revisions.find((entry) => entry.revisionId === parentId)
          : undefined;
      if (parent) {
        restoreFromHash = parent.candidateHtmlHash ?? null;
        revertedTo = parent.revisionId;
      } else {
        revertedTo = "baseline";
      }
    }

    // Read the HTML to restore: a prior committed candidate, or the baseline variant.
    const restoredHtml =
      restoreFromHash !== null
        ? artifact.readHtml(`artifact:${restoreFromHash}`)
        : resolveBaselineHtml(session, store, artifact);
    const currentHtml = resolveCurrentHtml(session, store, artifact);
    if (restoredHtml === null || currentHtml === null) {
      throw createUiPrototypingStudioError(
        "CURRENT_HTML_UNRESOLVABLE",
        "Cannot resolve the HTML to restore or the current head HTML",
        { sessionId: session.sessionId, revertedTo },
      );
    }

    const honest = diffByOdId(currentHtml, restoredHtml);
    const committedRef = artifact.commitHtml(artifact.stageHtml(restoredHtml).stagedRef);
    const candidateHtmlHash = committedRef.replace(/^artifact:/, "");

    const previousCount = revisions.length;
    const revisionId = store.allocateRevisionId(head);
    const revision: RevisionManifestEntry = {
      revisionId,
      parentRevisionId: head,
      sessionId: session.sessionId,
      variantCount: session.variantCount,
      baseline: session.baseline!,
      appliedBatchId: `revert:${revertedTo}`,
      appliedTaskIds: [],
      unresolvedCommentIds: [],
      diffSummary: { added: honest.added, changed: honest.changed, removed: honest.removed },
      diffSummaryHonest: honest,
      candidateHtmlHash,
      createdAt: input.revertedAt,
    };

    const nextSession: StudioSession = {
      ...session,
      revisionHeadId: revisionId,
      state: "RevisionRecorded",
    };

    store.appendRevision(revision);
    store.saveSession(nextSession);

    const nextCount = store.listRevisions(session.sessionId).length;
    if (nextCount !== previousCount + 1) {
      throw createUiPrototypingStudioError(
        "VARIANT_GENERATION_COUNT_MISMATCH",
        "Revert must append exactly one revision manifest entry",
        { previousCount, nextCount, sessionId: session.sessionId },
      );
    }

    return { session: nextSession, revision, revertedTo };
  };
}

function resolveBaselineHtml(
  session: StudioSession,
  store: StudioSessionStorePort,
  artifact: ArtifactContentPort,
): string | null {
  if (!session.baseline) return null;
  const baselineVariant = store
    .listVariants(session.sessionId)
    .find((variant) => variant.variantLabel === session.baseline!.label);
  if (!baselineVariant) return null;
  return artifact.readHtml(baselineVariant.htmlArtifactRef);
}
