import { createUiPrototypingStudioError } from "../domain/errors.js";
import { admitScope, type ScopeVerdict } from "./admission.js";
import type { ArtifactContentPort } from "./artifact-content-port.js";

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.TwoGateApply
 *     type: Service
 *
 * M2 (core) — the two-gate apply machine (DEC-MUTATION-EXEC-015):
 *   propose → VALIDATE (M1 admitScope) → STAGE (M0b) → [human accept-diff] → RECORD.
 * Gate 1 (approve-intent) is upstream (batch must be approved). This module owns the
 * admission boundary: a candidate is staged at a temp ref (RevisionApplied, NOT head)
 * only if the pure validator admits it; the human then accepts the EXACT staged hash
 * (idempotency-at-verdict, seen == recorded) and only then is it committed.
 *
 * This is the pure machine over (currentHtml, candidateHtml, taskScope, artifact port).
 * Full session wiring (variant HTML content + odId-bearing MutationTasks) is M0a-gated
 * and tracked separately; the contract here is verified in isolation.
 */
export interface StagedRevision {
  verdict: Extract<ScopeVerdict, "NOT_REJECT">;
  /** temp ref — staged, not head (RevisionApplied) */
  stagedRef: string;
  /** the hash the human previews and must accept */
  candidateHtmlHash: string;
}
export interface RejectedRevision {
  verdict: Extract<ScopeVerdict, "REJECT">;
}
export type ApplyStageResult = StagedRevision | RejectedRevision;

/**
 * Gate-2 step A: propose (external) is already done — caller passes candidateHtml.
 * Validate against the scope fence; on admit, stage at a temp ref. On reject, write nothing.
 */
export function validateAndStage(
  currentHtml: string,
  candidateHtml: string,
  taskScopeOdIds: readonly string[],
  artifact: ArtifactContentPort,
): ApplyStageResult {
  const verdict = admitScope(currentHtml, candidateHtml, taskScopeOdIds);
  if (verdict === "REJECT") return { verdict: "REJECT" };
  const staged = artifact.stageHtml(candidateHtml);
  return { verdict: "NOT_REJECT", stagedRef: staged.stagedRef, candidateHtmlHash: staged.hash };
}

/**
 * Gate-2 step B: the human accept-diff. Commit EXACTLY the previewed candidate hash
 * (idempotency-at-verdict). A mismatch between the accepted hash and the staged ref's
 * hash is fail-closed.
 */
export function acceptStaged(
  stagedRef: string,
  acceptedHash: string,
  artifact: ArtifactContentPort,
): { committedRef: string; candidateHtmlHash: string } {
  const refHash = stagedRef.split(":")[1];
  if (!refHash || refHash !== acceptedHash) {
    throw createUiPrototypingStudioError(
      "CANDIDATE_HASH_MISMATCH",
      "Accepted hash does not match the staged candidate (seen != recorded)",
      { stagedRef, acceptedHash },
    );
  }
  if (artifact.readHtml(stagedRef) === null) {
    throw createUiPrototypingStudioError(
      "NO_STAGED_CANDIDATE",
      "No staged candidate to accept",
      { stagedRef },
    );
  }
  const committedRef = artifact.commitHtml(stagedRef);
  return { committedRef, candidateHtmlHash: acceptedHash };
}

/** Reject the accept-diff gate: drop the staged candidate, no trace. */
export function discardStaged(stagedRef: string, artifact: ArtifactContentPort): void {
  artifact.discardStagedHtml(stagedRef);
}
