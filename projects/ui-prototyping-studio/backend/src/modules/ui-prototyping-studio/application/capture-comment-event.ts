import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import {
  parseCommentSeverity,
  type AnnotationTarget,
  type CommentEvent,
  type StudioSession,
} from "../domain/models.js";

export interface CaptureCommentEventInput {
  sessionId: string;
  revisionId: string;
  target: {
    selector: string;
    elementLabel: string;
    odId?: string | null;
  };
  severity: string;
  intent: string;
  note: string;
  createdBy: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.CaptureCommentEvent
 *     type: Operation
 */
export function makeCaptureCommentEventUseCase(store: StudioSessionStorePort) {
  return function captureCommentEvent(
    input: CaptureCommentEventInput,
  ): CommentEvent {
    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError(
        "SESSION_NOT_FOUND",
        "Session not found",
        {
          sessionId: input.sessionId,
        },
      );
    }

    if (session.selectionGate !== "satisfied") {
      throw createUiPrototypingStudioError(
        "BASELINE_GATE_UNSATISFIED",
        "Baseline gate must be satisfied before capturing comments",
        {
          sessionId: session.sessionId,
          selectionGate: session.selectionGate,
        },
      );
    }

    if (session.revisionHeadId && session.revisionHeadId !== input.revisionId) {
      throw createUiPrototypingStudioError(
        "SOURCE_REVISION_INVALID",
        "Comment revision does not match current revision head",
        {
          sessionId: session.sessionId,
          expectedRevisionId: session.revisionHeadId,
          actualRevisionId: input.revisionId,
        },
      );
    }

    const target = parseAnnotationTarget(input.target);
    const severity = parseCommentSeverity(input.severity);
    const intent = parseRequiredText(input.intent, "intent");
    const note = parseRequiredText(input.note, "note");

    const comment: CommentEvent = {
      commentId: store.allocateCommentId(),
      sessionId: session.sessionId,
      revisionId: input.revisionId,
      target,
      severity,
      intent,
      note,
      createdBy: normalizeActor(input.createdBy),
      createdAt: new Date().toISOString(),
    };

    const nextSession: StudioSession = {
      ...session,
      state: "CommentsCaptured",
    };

    store.appendComment(comment);
    store.saveSession(nextSession);

    return comment;
  };
}

function parseAnnotationTarget(
  target: CaptureCommentEventInput["target"],
): AnnotationTarget {
  const selector = parseRequiredText(target.selector, "target.selector");
  const elementLabel = parseRequiredText(
    target.elementLabel,
    "target.elementLabel",
  );
  const odId =
    typeof target.odId === "string" && target.odId.trim().length > 0
      ? target.odId.trim()
      : null;

  return {
    selector,
    elementLabel,
    odId,
  };
}

function parseRequiredText(rawValue: string, field: string): string {
  const normalized = rawValue.trim();
  if (normalized.length === 0) {
    throw createUiPrototypingStudioError(
      "COMMENT_SCHEMA_INVALID",
      "Comment payload is missing required fields",
      {
        field,
      },
    );
  }

  return normalized;
}

function normalizeActor(rawValue: string): string {
  const normalized = rawValue.trim();
  return normalized.length > 0 ? normalized : "web-ui";
}
