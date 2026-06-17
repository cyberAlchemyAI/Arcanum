import type {
  CommentEvent,
  MutationBatch,
  RevisionManifestEntry,
} from "../domain/models.js";

export interface NewspaperContractAdapter {
  mapCommentEvent(input: CommentEvent): {
    id: string;
    revisionId: string;
    target: string;
    severity: string;
    intent: string;
    note: string;
    createdBy: string;
    createdAt: string;
  };
  mapMutationBatch(input: MutationBatch): {
    id: string;
    sourceRevisionId: string;
    status: string;
    checksum: string;
    taskCount: number;
    tasks: Array<{
      id: string;
      target: string;
      changeType: string;
      priority: string;
      acceptance: string;
    }>;
  };
  mapRevisionManifestEntry(input: RevisionManifestEntry): {
    revisionId: string;
    parentRevisionId: string;
    appliedBatchId: string;
    appliedTaskIds: string[];
    diffSummary: {
      added: number;
      changed: number;
      removed: number;
    };
    createdAt: string;
  };
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.NewspaperContractAdapter
 *     type: Interface
 */
export function createNewspaperContractAdapter(): NewspaperContractAdapter {
  return {
    mapCommentEvent(input) {
      return {
        id: input.commentId,
        revisionId: input.revisionId,
        target: input.target.selector,
        severity: input.severity,
        intent: input.intent,
        note: input.note,
        createdBy: input.createdBy,
        createdAt: input.createdAt,
      };
    },
    mapMutationBatch(input) {
      return {
        id: input.batchId,
        sourceRevisionId: input.sourceRevisionId,
        status: input.status,
        checksum: input.checksum,
        taskCount: input.tasks.length,
        tasks: input.tasks.map((task) => ({
          id: task.taskId,
          target: task.target,
          changeType: task.changeType,
          priority: task.priority,
          acceptance: task.acceptanceText,
        })),
      };
    },
    mapRevisionManifestEntry(input) {
      return {
        revisionId: input.revisionId,
        parentRevisionId: input.parentRevisionId,
        appliedBatchId: input.appliedBatchId,
        appliedTaskIds: [...input.appliedTaskIds],
        diffSummary: {
          ...input.diffSummary,
        },
        createdAt: input.createdAt,
      };
    },
  };
}
