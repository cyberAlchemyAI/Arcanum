import {
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  writeFileSync,
} from "node:fs";
import { dirname } from "node:path";

import type { StagedCandidateRecord, StudioSessionStorePort } from "../application/ports.js";
import type {
  CommentEvent,
  HandoffBundle,
  MutationBatch,
  MutationTask,
  PrototypeVariant,
  RevisionManifestEntry,
  StudioSession,
} from "../domain/models.js";

interface PersistentStoreDocument {
  counters: {
    session: number;
    comment: number;
    batch: number;
    revision: number;
  };
  sessions: Record<string, StudioSession>;
  variantsBySession: Record<string, PrototypeVariant[]>;
  commentsBySession: Record<string, CommentEvent[]>;
  batchesBySession: Record<string, MutationBatch[]>;
  revisionsBySession: Record<string, RevisionManifestEntry[]>;
  handoffBySession: Record<string, HandoffBundle>;
  stagedBySession: Record<string, StagedCandidateRecord>;
}

interface CreateFileBackedStudioSessionStoreOptions {
  filePath: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.StudioSessionStore
 *     type: Adapter
 */
export function createFileBackedStudioSessionStore(
  options: CreateFileBackedStudioSessionStoreOptions,
): StudioSessionStorePort {
  const filePath = options.filePath;
  let documentState = loadDocument(filePath);

  const persist = () => {
    writeDocument(filePath, documentState);
  };

  return {
    allocateSessionId() {
      documentState.counters.session += 1;
      persist();
      return `ups-session-${String(documentState.counters.session).padStart(4, "0")}`;
    },
    allocateCommentId() {
      documentState.counters.comment += 1;
      persist();
      return `ups-comment-${String(documentState.counters.comment).padStart(5, "0")}`;
    },
    allocateBatchId() {
      documentState.counters.batch += 1;
      persist();
      return `ups-batch-${String(documentState.counters.batch).padStart(5, "0")}`;
    },
    allocateRevisionId(_parentRevisionId) {
      documentState.counters.revision += 1;
      persist();
      return `rev-${String(documentState.counters.revision).padStart(4, "0")}`;
    },
    saveSession(session) {
      documentState.sessions[session.sessionId] = cloneSession(session);
      persist();
    },
    getSession(sessionId) {
      const session = documentState.sessions[sessionId];
      return session ? cloneSession(session) : null;
    },
    saveVariants(sessionId, variants) {
      documentState.variantsBySession[sessionId] = variants.map((variant) =>
        cloneVariant(variant),
      );
      persist();
    },
    listVariants(sessionId) {
      const variants = documentState.variantsBySession[sessionId] ?? [];
      return variants.map((variant) => cloneVariant(variant));
    },
    appendComment(comment) {
      const comments = documentState.commentsBySession[comment.sessionId] ?? [];
      comments.push(cloneComment(comment));
      documentState.commentsBySession[comment.sessionId] = comments;
      persist();
    },
    listComments(sessionId, revisionId) {
      const comments = documentState.commentsBySession[sessionId] ?? [];
      return comments
        .filter((comment) => comment.revisionId === revisionId)
        .map((comment) => cloneComment(comment));
    },
    saveBatch(batch) {
      const batches = documentState.batchesBySession[batch.sessionId] ?? [];
      const nextBatches = batches.filter(
        (candidate) => candidate.batchId !== batch.batchId,
      );
      nextBatches.push(cloneBatch(batch));
      documentState.batchesBySession[batch.sessionId] = nextBatches;
      persist();
    },
    getBatch(sessionId, batchId) {
      const batches = documentState.batchesBySession[sessionId] ?? [];
      const batch = batches.find((candidate) => candidate.batchId === batchId);
      return batch ? cloneBatch(batch) : null;
    },
    getDraftBatch(sessionId, batchId) {
      const batches = documentState.batchesBySession[sessionId] ?? [];
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
      const batches = documentState.batchesBySession[sessionId] ?? [];
      return batches.map((batch) => cloneBatch(batch));
    },
    appendRevision(entry) {
      const revisions = documentState.revisionsBySession[entry.sessionId] ?? [];
      revisions.push(cloneRevision(entry));
      documentState.revisionsBySession[entry.sessionId] = revisions;
      persist();
    },
    listRevisions(sessionId) {
      const revisions = documentState.revisionsBySession[sessionId] ?? [];
      return revisions.map((entry) => cloneRevision(entry));
    },
    saveHandoffBundle(bundle) {
      documentState.handoffBySession[bundle.sessionId] =
        cloneHandoffBundle(bundle);
      persist();
    },
    getHandoffBundle(sessionId) {
      const bundle = documentState.handoffBySession[sessionId];
      return bundle ? cloneHandoffBundle(bundle) : null;
    },
    saveStagedCandidate(sessionId, record) {
      documentState.stagedBySession[sessionId] = { ...record };
      persist();
    },
    getStagedCandidate(sessionId) {
      const record = documentState.stagedBySession[sessionId];
      return record ? { ...record } : null;
    },
    clearStagedCandidate(sessionId) {
      delete documentState.stagedBySession[sessionId];
      persist();
    },
  };
}

function loadDocument(filePath: string): PersistentStoreDocument {
  if (!existsSync(filePath)) {
    return createEmptyDocument();
  }

  try {
    const raw = readFileSync(filePath, "utf8");
    const parsed = JSON.parse(raw) as Partial<PersistentStoreDocument>;
    return normalizeDocument(parsed);
  } catch {
    return createEmptyDocument();
  }
}

function writeDocument(
  filePath: string,
  documentState: PersistentStoreDocument,
): void {
  mkdirSync(dirname(filePath), { recursive: true });
  const tempPath = `${filePath}.tmp`;
  writeFileSync(tempPath, JSON.stringify(documentState, null, 2), "utf8");
  renameSync(tempPath, filePath);
}

function createEmptyDocument(): PersistentStoreDocument {
  return {
    counters: {
      session: 0,
      comment: 0,
      batch: 0,
      revision: 0,
    },
    sessions: {},
    variantsBySession: {},
    commentsBySession: {},
    batchesBySession: {},
    revisionsBySession: {},
    handoffBySession: {},
    stagedBySession: {},
  };
}

function normalizeDocument(
  parsed: Partial<PersistentStoreDocument>,
): PersistentStoreDocument {
  const fallback = createEmptyDocument();
  return {
    counters: {
      session: asNumber(parsed.counters?.session),
      comment: asNumber(parsed.counters?.comment),
      batch: asNumber(parsed.counters?.batch),
      revision: asNumber(parsed.counters?.revision),
    },
    sessions: asRecord(parsed.sessions, fallback.sessions),
    variantsBySession: asRecord(
      parsed.variantsBySession,
      fallback.variantsBySession,
    ),
    commentsBySession: asRecord(
      parsed.commentsBySession,
      fallback.commentsBySession,
    ),
    batchesBySession: asRecord(
      parsed.batchesBySession,
      fallback.batchesBySession,
    ),
    revisionsBySession: asRecord(
      parsed.revisionsBySession,
      fallback.revisionsBySession,
    ),
    handoffBySession: asRecord(
      parsed.handoffBySession,
      fallback.handoffBySession,
    ),
    stagedBySession: asRecord(
      parsed.stagedBySession,
      fallback.stagedBySession,
    ),
  };
}

function asNumber(value: unknown): number {
  return typeof value === "number" && Number.isInteger(value) && value >= 0
    ? value
    : 0;
}

function asRecord<T>(
  value: unknown,
  fallback: Record<string, T>,
): Record<string, T> {
  if (!value || typeof value !== "object") {
    return fallback;
  }
  return value as Record<string, T>;
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
  };
}
