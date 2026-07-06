import type { StagedCandidateRecord, StudioSessionStorePort } from "./ports.js";
import type {
  CommentEvent,
  HandoffBundle,
  MutationBatch,
  MutationTask,
  PrototypeVariant,
  RevisionManifestEntry,
  StudioSession,
} from "../domain/models.js";

export function createInMemoryStudioSessionStore(): StudioSessionStorePort {
  const sessions = new Map<string, StudioSession>();
  const variantsBySession = new Map<string, PrototypeVariant[]>();
  const commentsBySession = new Map<string, CommentEvent[]>();
  const batchesBySession = new Map<string, MutationBatch[]>();
  const revisionsBySession = new Map<string, RevisionManifestEntry[]>();
  const handoffBySession = new Map<string, HandoffBundle>();
  const stagedBySession = new Map<string, StagedCandidateRecord>();

  let sessionSequence = 0;
  let commentSequence = 0;
  let batchSequence = 0;
  let revisionSequence = 0;

  return {
    allocateSessionId() {
      sessionSequence += 1;
      return `ups-session-${String(sessionSequence).padStart(4, "0")}`;
    },
    allocateCommentId() {
      commentSequence += 1;
      return `ups-comment-${String(commentSequence).padStart(5, "0")}`;
    },
    allocateBatchId() {
      batchSequence += 1;
      return `ups-batch-${String(batchSequence).padStart(5, "0")}`;
    },
    allocateRevisionId(_parentRevisionId) {
      revisionSequence += 1;
      return `rev-${String(revisionSequence).padStart(4, "0")}`;
    },
    saveSession(session) {
      sessions.set(session.sessionId, cloneSession(session));
    },
    getSession(sessionId) {
      const session = sessions.get(sessionId);
      return session ? cloneSession(session) : null;
    },
    saveVariants(sessionId, variants) {
      variantsBySession.set(
        sessionId,
        variants.map((variant) => cloneVariant(variant)),
      );
    },
    listVariants(sessionId) {
      const variants = variantsBySession.get(sessionId) ?? [];
      return variants.map((variant) => cloneVariant(variant));
    },
    appendComment(comment) {
      const comments = commentsBySession.get(comment.sessionId) ?? [];
      comments.push(cloneComment(comment));
      commentsBySession.set(comment.sessionId, comments);
    },
    listComments(sessionId, revisionId) {
      const comments = commentsBySession.get(sessionId) ?? [];
      return comments
        .filter((comment) => comment.revisionId === revisionId)
        .map((comment) => cloneComment(comment));
    },
    saveBatch(batch) {
      const batches = batchesBySession.get(batch.sessionId) ?? [];
      const nextBatches = batches.filter(
        (candidate) => candidate.batchId !== batch.batchId,
      );
      nextBatches.push(cloneBatch(batch));
      batchesBySession.set(batch.sessionId, nextBatches);
    },
    getBatch(sessionId, batchId) {
      const batches = batchesBySession.get(sessionId) ?? [];
      const batch = batches.find((candidate) => candidate.batchId === batchId);
      return batch ? cloneBatch(batch) : null;
    },
    getDraftBatch(sessionId, batchId) {
      const batches = batchesBySession.get(sessionId) ?? [];
      const candidates = batches.filter((batch) => batch.status === "draft");

      if (batchId) {
        const batch = candidates.find(
          (candidate) => candidate.batchId === batchId,
        );
        return batch ? cloneBatch(batch) : null;
      }

      const latest = candidates[candidates.length - 1];
      return latest ? cloneBatch(latest) : null;
    },
    listBatches(sessionId) {
      const batches = batchesBySession.get(sessionId) ?? [];
      return batches.map((batch) => cloneBatch(batch));
    },
    appendRevision(entry) {
      const revisions = revisionsBySession.get(entry.sessionId) ?? [];
      revisions.push(cloneRevision(entry));
      revisionsBySession.set(entry.sessionId, revisions);
    },
    listRevisions(sessionId) {
      const revisions = revisionsBySession.get(sessionId) ?? [];
      return revisions.map((entry) => cloneRevision(entry));
    },
    saveHandoffBundle(bundle) {
      handoffBySession.set(bundle.sessionId, cloneHandoffBundle(bundle));
    },
    getHandoffBundle(sessionId) {
      const bundle = handoffBySession.get(sessionId);
      return bundle ? cloneHandoffBundle(bundle) : null;
    },
    saveStagedCandidate(sessionId, record) {
      stagedBySession.set(sessionId, { ...record });
    },
    getStagedCandidate(sessionId) {
      const record = stagedBySession.get(sessionId);
      return record ? { ...record } : null;
    },
    clearStagedCandidate(sessionId) {
      stagedBySession.delete(sessionId);
    },
  };
}

function cloneSession(session: StudioSession): StudioSession {
  return {
    ...session,
    variantLabels: [...session.variantLabels],
    baseline: session.baseline ? { ...session.baseline } : null,
    integration: {
      ...session.integration,
    },
  };
}

function cloneVariant(variant: PrototypeVariant): PrototypeVariant {
  return {
    ...variant,
    componentsUsed: [...variant.componentsUsed],
  };
}

function cloneComment(comment: CommentEvent): CommentEvent {
  return {
    ...comment,
    target: {
      ...comment.target,
    },
  };
}

function cloneTask(task: MutationTask): MutationTask {
  return {
    ...task,
  };
}

function cloneBatch(batch: MutationBatch): MutationBatch {
  return {
    ...batch,
    generatedFromCommentIds: [...batch.generatedFromCommentIds],
    tasks: batch.tasks.map((task) => cloneTask(task)),
    approval: {
      ...batch.approval,
    },
  };
}

function cloneRevision(entry: RevisionManifestEntry): RevisionManifestEntry {
  return {
    ...entry,
    baseline: {
      ...entry.baseline,
    },
    appliedTaskIds: [...entry.appliedTaskIds],
    unresolvedCommentIds: [...entry.unresolvedCommentIds],
    diffSummary: {
      ...entry.diffSummary,
    },
  };
}

function cloneHandoffBundle(bundle: HandoffBundle): HandoffBundle {
  return {
    ...bundle,
    baseline: {
      ...bundle.baseline,
    },
    storyRefs: [...bundle.storyRefs],
    requirementRefs: [...bundle.requirementRefs],
    acceptanceRefs: [...bundle.acceptanceRefs],
    sourceRefs: bundle.sourceRefs ? [...bundle.sourceRefs] : undefined,
    missingRefs: bundle.missingRefs ? [...bundle.missingRefs] : undefined,
  };
}
