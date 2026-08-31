#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "arcanum.native-dispatch-runner.evidence-validation.v0.1"
VALIDATOR_NAME = "validate_run_evidence.py"
RUN_EVENT_SCHEMA_VERSIONS = {
    "arcanum.native-dispatch-runner.run-event.v0.1",
    "arcanum.native-dispatch-runner.run-event.v0.2",
    "arcanum.native-dispatch-runner.run-event.v0.3",
}
HOST_RESULTS = {"host_spawn_returned", "host_spawn_failed"}
EVENT_KINDS = {
    "action_attempted",
    "host_spawn_returned",
    "host_spawn_failed",
    "agent_binding_corrected",
    "agent_wait_registered",
    "wait_attempted",
    "agent_terminal",
    "agent_closed",
    "wait_timed_out",
    "agent_interrupted",
    "run_blocked",
    "receipt_joined",
    "gate_decided",
}
BASE_FIELDS = {"schema_version", "sequence", "event", "dispatch_id", "run_id", "wave_id", "action_id", "agent_id", "operation"}
EVENT_FIELDS = BASE_FIELDS | {
    "depends_on_gate_id",
    "receipt_status",
    "gate_id",
    "decision",
    "required_action_ids",
    "admitted_receipt_action_ids",
    "failed_action_ids",
    "cleaned_action_ids",
    "blocker_code",
    "prior_agent_id",
    "prepared_task_name",
    "supersedes_sequences",
    "reason_code",
    "domain_outcome",
}


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        value = json.loads(raw_line)
        if not isinstance(value, dict):
            raise ValueError(f"line {line_number}: event must be a JSON object")
        events.append(value)
    return events


def event_shape_violation(event: dict[str, Any]) -> str | None:
    missing = sorted(BASE_FIELDS - set(event))
    if missing:
        return "missing required fields: " + ", ".join(missing)
    unexpected = sorted(set(event) - EVENT_FIELDS)
    if unexpected:
        return "unexpected fields: " + ", ".join(unexpected)
    if event.get("schema_version") not in RUN_EVENT_SCHEMA_VERSIONS:
        return "unsupported schema_version"
    if event.get("event") not in EVENT_KINDS:
        return "unsupported event kind"
    if not isinstance(event.get("sequence"), int) or isinstance(event.get("sequence"), bool) or event["sequence"] < 1:
        return "sequence must be a positive integer"
    for field in ("dispatch_id", "run_id", "wave_id", "operation"):
        if not isinstance(event.get(field), str) or not event[field]:
            return f"{field} must be a non-empty string"
    kind = event["event"]
    event_version = event.get("schema_version")
    if event_version == "arcanum.native-dispatch-runner.run-event.v0.3" and kind != "gate_decided":
        return "run-event.v0.3 is reserved for typed gate_decided evidence"
    if event_version != "arcanum.native-dispatch-runner.run-event.v0.3" and "domain_outcome" in event:
        return "domain_outcome requires run-event.v0.3"
    correction_fields = {
        "prior_agent_id",
        "prepared_task_name",
        "supersedes_sequences",
        "reason_code",
    }
    if kind != "agent_binding_corrected" and correction_fields & set(event):
        return "binding-correction fields are only valid on agent_binding_corrected"
    if kind in {"gate_decided", "wait_attempted"}:
        if event.get("action_id") is not None or event.get("agent_id") is not None:
            return f"{kind} action_id and agent_id must be null"
        if kind == "wait_attempted":
            return None
        if not isinstance(event.get("gate_id"), str) or not event["gate_id"]:
            return "gate_decided requires gate_id"
        if event.get("decision") not in {"gate_pass", "gate_block", "gate_resolved"}:
            return "gate_decided requires a supported decision"
        domain_outcome = event.get("domain_outcome")
        if event_version == "arcanum.native-dispatch-runner.run-event.v0.3":
            if domain_outcome is not None:
                if not isinstance(domain_outcome, dict) or set(domain_outcome) != {"role_id", "source_field", "value", "classification"}:
                    return "typed gate_decided domain_outcome has invalid shape"
                if any(not isinstance(domain_outcome.get(field), str) or not domain_outcome[field] for field in ("role_id", "source_field", "value")):
                    return "typed gate_decided domain_outcome fields must be non-empty strings"
            if event.get("decision") == "gate_resolved" and (
                not isinstance(domain_outcome, dict) or domain_outcome.get("classification") != "resolved"
            ):
                return "gate_resolved requires a resolved domain_outcome"
            if event.get("decision") == "gate_pass" and isinstance(domain_outcome, dict) and domain_outcome.get("classification") != "pass":
                return "gate_pass domain_outcome must be classified pass"
            if event.get("decision") == "gate_block" and domain_outcome is not None:
                return "gate_block must not carry a domain_outcome"
        elif event.get("decision") == "gate_resolved":
            return "gate_resolved requires run-event.v0.3"
        for field in ("required_action_ids", "admitted_receipt_action_ids"):
            value = event.get(field)
            if not isinstance(value, list) or (field == "required_action_ids" and not value) or any(not isinstance(item, str) or not item for item in value):
                return f"gate_decided requires valid {field}"
            if len(set(value)) != len(value):
                return f"gate_decided requires unique {field}"
        return None
    if not isinstance(event.get("action_id"), str) or not event["action_id"]:
        return f"{kind} requires action_id"
    if kind == "action_attempted":
        if event.get("agent_id") is not None or "depends_on_gate_id" not in event:
            return "action_attempted requires null agent_id and depends_on_gate_id"
    elif kind == "host_spawn_failed":
        if event.get("agent_id") is not None:
            return "host_spawn_failed requires null agent_id"
    elif kind == "run_blocked":
        if event.get("agent_id") is not None:
            return "run_blocked requires null agent_id"
        if event.get("blocker_code") != "partial_wave_spawn_failure":
            return "run_blocked requires partial_wave_spawn_failure blocker_code"
        for field in ("failed_action_ids", "cleaned_action_ids"):
            value = event.get(field)
            if (
                not isinstance(value, list)
                or any(not isinstance(item, str) or not item for item in value)
                or len(set(value)) != len(value)
            ):
                return f"run_blocked requires unique string {field}"
        if not event["failed_action_ids"]:
            return "run_blocked requires at least one failed_action_id"
        if event.get("action_id") not in event["failed_action_ids"]:
            return "run_blocked action_id must identify a failed action"
    elif kind == "agent_binding_corrected":
        if event.get("schema_version") != "arcanum.native-dispatch-runner.run-event.v0.2":
            return "agent_binding_corrected requires run-event.v0.2"
        if not isinstance(event.get("agent_id"), str) or not event["agent_id"]:
            return "agent_binding_corrected requires corrected agent_id"
        if not isinstance(event.get("prior_agent_id"), str) or not event["prior_agent_id"]:
            return "agent_binding_corrected requires prior_agent_id"
        if event["prior_agent_id"] == event["agent_id"]:
            return "agent_binding_corrected requires a changed agent_id"
        task_name = event.get("prepared_task_name")
        if not isinstance(task_name, str) or not task_name:
            return "agent_binding_corrected requires prepared_task_name"
        if event["agent_id"].rsplit("/", 1)[-1] != task_name:
            return "corrected agent_id must end with the exact prepared_task_name"
        supersedes = event.get("supersedes_sequences")
        if (
            not isinstance(supersedes, list)
            or len(supersedes) != 2
            or len(set(supersedes)) != 2
            or any(
                not isinstance(item, int)
                or isinstance(item, bool)
                or item < 1
                for item in supersedes
            )
        ):
            return "agent_binding_corrected requires two unique positive supersedes_sequences"
        if event.get("reason_code") != "host_agent_id_transcription_error":
            return "agent_binding_corrected requires host_agent_id_transcription_error"
    elif not isinstance(event.get("agent_id"), str) or not event["agent_id"]:
        return f"{kind} requires agent_id"
    if kind == "receipt_joined" and event.get("receipt_status") not in {"pass", "block", "fail", "timed_out"}:
        return "receipt_joined requires a supported receipt_status"
    return None


def validate_events(
    events: list[dict[str, Any]],
    source: str,
    *,
    require_complete: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    attempts: dict[str, dict[str, Any]] = {}
    host_results: dict[str, dict[str, Any]] = {}
    registrations: dict[str, dict[str, Any]] = {}
    binding_corrections: dict[str, dict[str, Any]] = {}
    waits_by_wave: dict[str, list[dict[str, Any]]] = {}
    terminals: dict[str, dict[str, Any]] = {}
    closes: dict[str, dict[str, Any]] = {}
    timeouts: dict[str, dict[str, Any]] = {}
    interrupts: dict[str, dict[str, Any]] = {}
    joined: dict[str, dict[str, Any]] = {}
    gate_decisions: dict[str, int] = {}
    gate_passes: dict[str, int] = {}
    gate_decision_waves: set[str] = set()
    run_blocks: list[dict[str, Any]] = []
    dispatch_id: str | None = None
    run_id: str | None = None

    def reject(code: str, event: dict[str, Any] | None, message: str, action_id: str | None = None) -> None:
        errors.append(
            {
                "code": code,
                "sequence": event.get("sequence") if event else None,
                "action_id": action_id if action_id is not None else (event.get("action_id") if event else None),
                "message": message,
            }
        )

    if require_complete and not events:
        reject("empty_event_stream", None, "a complete run event stream must not be empty")

    for expected_sequence, event in enumerate(events, start=1):
        if event.get("sequence") != expected_sequence:
            reject("sequence_mismatch", event, f"expected sequence {expected_sequence}")

        shape_violation = event_shape_violation(event)
        if shape_violation:
            reject("event_schema_violation", event, shape_violation)
            continue

        if dispatch_id is None:
            dispatch_id = event.get("dispatch_id")
            run_id = event.get("run_id")
        elif event.get("dispatch_id") != dispatch_id or event.get("run_id") != run_id:
            reject("run_identity_mismatch", event, "event dispatch_id/run_id differs from the first event")

        kind = event.get("event")
        action_id = event.get("action_id")

        if kind == "action_attempted":
            if not isinstance(action_id, str) or not action_id:
                reject("invalid_action_identity", event, "action attempt requires a non-empty action_id")
                continue
            if action_id in attempts:
                reject("duplicate_action_attempt", event, "action was attempted more than once")
            else:
                attempts[action_id] = event
            dependency = event.get("depends_on_gate_id")
            if dependency is not None and dependency not in gate_passes:
                reject("dependent_action_before_gate", event, f"gate {dependency} has no earlier valid gate_pass")

        elif kind in HOST_RESULTS:
            if action_id not in attempts:
                reject("missing_action_attempt", event, "host result has no earlier action_attempted event")
            if action_id in host_results:
                reject("duplicate_host_result", event, "action has more than one host result")
            else:
                host_results[action_id] = event

        elif kind == "agent_wait_registered":
            host_result = host_results.get(action_id)
            registration_valid = True
            if host_result is None or host_result.get("event") != "host_spawn_returned":
                reject("registration_without_host_result", event, "wait registration has no earlier successful host result")
                registration_valid = False
            elif event.get("agent_id") != host_result.get("agent_id"):
                reject("registration_agent_mismatch", event, "registered agent_id differs from the host result")
                registration_valid = False
            elif event.get("wave_id") != host_result.get("wave_id"):
                reject("registration_wave_mismatch", event, "wait registration wave differs from the host result")
                registration_valid = False
            if action_id in registrations:
                reject("duplicate_wait_registration", event, "agent was registered for waiting more than once")
                registration_valid = False
            if registration_valid:
                registrations[action_id] = event

        elif kind == "agent_binding_corrected":
            correction_valid = True
            host_result = host_results.get(action_id)
            registration = registrations.get(action_id)
            prior_agent_id = event.get("prior_agent_id")
            corrected_agent_id = event.get("agent_id")
            if action_id in binding_corrections:
                reject(
                    "duplicate_agent_binding_correction",
                    event,
                    "action already has an agent binding correction",
                )
                correction_valid = False
            if host_result is None or host_result.get("event") != "host_spawn_returned":
                reject(
                    "correction_without_host_result",
                    event,
                    "binding correction has no earlier successful host result",
                )
                correction_valid = False
            elif host_result.get("agent_id") != prior_agent_id:
                reject(
                    "correction_prior_agent_mismatch",
                    event,
                    "prior_agent_id differs from the effective host result",
                )
                correction_valid = False
            elif host_result.get("wave_id") != event.get("wave_id"):
                reject(
                    "correction_wave_mismatch",
                    event,
                    "binding correction wave differs from the host result",
                )
                correction_valid = False
            if registration is None:
                reject(
                    "correction_without_registration",
                    event,
                    "binding correction has no earlier wait registration",
                )
                correction_valid = False
            elif registration.get("agent_id") != prior_agent_id:
                reject(
                    "correction_registration_agent_mismatch",
                    event,
                    "prior_agent_id differs from the effective wait registration",
                )
                correction_valid = False
            elif registration.get("wave_id") != event.get("wave_id"):
                reject(
                    "correction_registration_wave_mismatch",
                    event,
                    "binding correction wave differs from the wait registration",
                )
                correction_valid = False
            if host_result is not None and registration is not None:
                expected_sequences = [
                    host_result.get("sequence"),
                    registration.get("sequence"),
                ]
                if event.get("supersedes_sequences") != expected_sequences:
                    reject(
                        "correction_sequence_mismatch",
                        event,
                        "supersedes_sequences must name the effective host result then registration",
                    )
                    correction_valid = False
            same_wave_terminal_evidence = [
                candidate
                for collection in (
                    terminals,
                    closes,
                    timeouts,
                    interrupts,
                    joined,
                )
                for candidate in collection.values()
                if candidate.get("wave_id") == event.get("wave_id")
            ]
            if same_wave_terminal_evidence or event.get("wave_id") in gate_decision_waves:
                reject(
                    "correction_after_terminal_evidence",
                    event,
                    "binding correction must precede same-wave terminal, cleanup, join, and gate evidence",
                )
                correction_valid = False
            duplicate_owner = next(
                (
                    candidate_action_id
                    for candidate_action_id, candidate in host_results.items()
                    if candidate_action_id != action_id
                    and candidate.get("event") == "host_spawn_returned"
                    and candidate.get("agent_id") == corrected_agent_id
                ),
                None,
            )
            if duplicate_owner is not None:
                reject(
                    "correction_agent_id_not_unique",
                    event,
                    f"corrected agent_id is already bound to {duplicate_owner}",
                )
                correction_valid = False
            if correction_valid and host_result is not None and registration is not None:
                host_results[action_id] = {
                    **host_result,
                    "agent_id": corrected_agent_id,
                }
                registrations[action_id] = {
                    **registration,
                    "agent_id": corrected_agent_id,
                }
                binding_corrections[action_id] = event

        elif kind == "wait_attempted":
            wave_id = event.get("wave_id")
            known_actions = {
                known_action_id
                for known_action_id, host_result in host_results.items()
                if host_result.get("event") == "host_spawn_returned" and host_result.get("wave_id") == wave_id
            }
            registered_actions = {
                registered_action_id
                for registered_action_id, registration in registrations.items()
                if registration.get("wave_id") == wave_id
            }
            missing_registrations = sorted(known_actions - registered_actions)
            if not known_actions or missing_registrations:
                missing = ", ".join(missing_registrations) if missing_registrations else "the wave has no known agents"
                reject("wait_before_full_registration", event, f"wait attempted before full wave registration: {missing}")
            else:
                waits_by_wave.setdefault(wave_id, []).append(event)

        elif kind == "agent_terminal":
            host_result = host_results.get(action_id)
            terminal_valid = True
            if host_result is None or host_result.get("event") != "host_spawn_returned":
                reject("terminal_without_host_result", event, "terminal agent has no earlier successful host result")
                terminal_valid = False
            elif event.get("agent_id") != host_result.get("agent_id"):
                reject("terminal_agent_mismatch", event, "terminal agent_id differs from the host result")
                terminal_valid = False
            elif event.get("wave_id") != host_result.get("wave_id"):
                reject("terminal_wave_mismatch", event, "terminal wave differs from the host result")
                terminal_valid = False
            if terminal_valid:
                registration = registrations.get(action_id)
                prior_waits = waits_by_wave.get(event.get("wave_id"), [])
                if registration is None or not any(wait["sequence"] > registration["sequence"] for wait in prior_waits):
                    reject("terminal_without_wait", event, "terminal agent has no earlier valid wait observation")
                    terminal_valid = False
            if action_id in terminals:
                reject("duplicate_agent_terminal", event, "agent has more than one terminal event")
                terminal_valid = False
            if terminal_valid:
                terminals[action_id] = event

        elif kind == "agent_closed":
            terminal = terminals.get(action_id)
            close_valid = True
            if terminal is None:
                reject("close_before_terminal", event, "agent close has no earlier terminal event")
                close_valid = False
            elif event.get("agent_id") != terminal.get("agent_id"):
                reject("close_agent_mismatch", event, "closed agent_id differs from the terminal event")
                close_valid = False
            if action_id in closes:
                reject("duplicate_agent_close", event, "agent was closed more than once")
                close_valid = False
            if close_valid:
                closes[action_id] = event

        elif kind == "wait_timed_out":
            host_result = host_results.get(action_id)
            timeout_valid = True
            if host_result is None or host_result.get("event") != "host_spawn_returned":
                reject("timeout_without_host_result", event, "wait timeout has no earlier successful host result")
                timeout_valid = False
            elif event.get("agent_id") != host_result.get("agent_id"):
                reject("timeout_agent_mismatch", event, "timed-out agent_id differs from the host result")
                timeout_valid = False
            if timeout_valid:
                registration = registrations.get(action_id)
                prior_waits = waits_by_wave.get(event.get("wave_id"), [])
                if registration is None or not any(wait["sequence"] > registration["sequence"] for wait in prior_waits):
                    reject("timeout_without_wait", event, "timeout has no earlier valid wait attempt")
                    timeout_valid = False
            if action_id in timeouts:
                reject("duplicate_wait_timeout", event, "agent has more than one timeout event")
                timeout_valid = False
            if timeout_valid:
                timeouts[action_id] = event

        elif kind == "agent_interrupted":
            timeout = timeouts.get(action_id)
            interrupt_valid = True
            if timeout is None:
                reject("interrupt_without_timeout", event, "agent interrupt has no earlier timeout event")
                interrupt_valid = False
            elif event.get("agent_id") != timeout.get("agent_id"):
                reject("interrupt_agent_mismatch", event, "interrupted agent_id differs from the timeout event")
                interrupt_valid = False
            if action_id in interrupts:
                reject("duplicate_agent_interrupt", event, "agent was interrupted more than once")
                interrupt_valid = False
            if interrupt_valid:
                interrupts[action_id] = event

        elif kind == "receipt_joined":
            host_result = host_results.get(action_id)
            join_valid = True
            if host_result is None or host_result.get("event") != "host_spawn_returned":
                reject("join_without_host_result", event, "joined receipt has no earlier successful host result")
                join_valid = False
            elif event.get("agent_id") != host_result.get("agent_id"):
                reject("joined_agent_mismatch", event, "joined receipt agent_id differs from the host result")
                join_valid = False
            if join_valid:
                cleanup = closes.get(action_id) or interrupts.get(action_id)
                if cleanup is None:
                    reject("join_before_terminal_cleanup", event, "joined receipt has no completed terminal-close or timeout-interrupt branch")
                    join_valid = False
            if action_id in joined:
                reject("duplicate_joined_receipt", event, "action has more than one joined receipt")
                join_valid = False
            if join_valid:
                joined[action_id] = event

        elif kind == "run_blocked":
            block_valid = True
            if run_blocks:
                reject("duplicate_run_blocked", event, "run already has a blocked closeout")
                block_valid = False
            failed_action_ids = event.get("failed_action_ids", [])
            cleaned_action_ids = event.get("cleaned_action_ids", [])
            blocked_wave_id = event.get("wave_id")
            failed_spawn_action_ids = {
                candidate_action_id
                for candidate_action_id, host_result in host_results.items()
                if host_result.get("event") == "host_spawn_failed"
                and host_result.get("wave_id") == blocked_wave_id
            }
            if set(failed_action_ids) != failed_spawn_action_ids:
                reject("blocked_closeout_failure_set_mismatch", event, "blocked closeout must name every and only failed spawns in its wave")
                block_valid = False
            for failed_action_id in failed_action_ids:
                host_result = host_results.get(failed_action_id)
                if host_result is None or host_result.get("event") != "host_spawn_failed":
                    reject("blocked_closeout_missing_failed_spawn", event, "blocked closeout references an action without host_spawn_failed", failed_action_id)
                    block_valid = False
                elif host_result.get("wave_id") != blocked_wave_id:
                    reject("blocked_closeout_failed_spawn_wave_mismatch", event, "blocked closeout references a failed action from another wave", failed_action_id)
                    block_valid = False
            successful_action_ids = {
                candidate_action_id
                for candidate_action_id, host_result in host_results.items()
                if host_result.get("event") == "host_spawn_returned"
                and host_result.get("wave_id") == blocked_wave_id
            }
            if set(cleaned_action_ids) != successful_action_ids:
                reject("blocked_closeout_cleanup_set_mismatch", event, "blocked closeout must name every and only successfully spawned action")
                block_valid = False
            for cleaned_action_id in cleaned_action_ids:
                cleanup = closes.get(cleaned_action_id) or interrupts.get(cleaned_action_id)
                if cleanup is None:
                    reject("blocked_closeout_uncleaned_agent", event, "blocked closeout names an agent without terminal cleanup", cleaned_action_id)
                    block_valid = False
                elif cleanup.get("wave_id") != blocked_wave_id:
                    reject("blocked_closeout_cleanup_wave_mismatch", event, "blocked closeout cleanup belongs to another wave", cleaned_action_id)
                    block_valid = False
            if any(
                joined_receipt.get("wave_id") == blocked_wave_id
                for joined_receipt in joined.values()
            ):
                reject("blocked_closeout_after_join", event, "blocked closeout cannot follow a joined receipt")
                block_valid = False
            if blocked_wave_id in gate_decision_waves:
                reject("blocked_closeout_after_gate", event, "blocked closeout cannot follow a gate decision")
                block_valid = False
            if block_valid:
                run_blocks.append(event)

        elif kind == "gate_decided":
            gate_error_count = len(errors)
            gate_id = event.get("gate_id")
            required = event.get("required_action_ids", [])
            admitted = event.get("admitted_receipt_action_ids", [])
            if gate_id in gate_decisions:
                reject("duplicate_gate_decision", event, f"gate {gate_id} was already decided")
            for required_action_id in required:
                if required_action_id not in attempts:
                    reject("gate_missing_attempt", event, "required action has no earlier attempt", required_action_id)
                if required_action_id not in host_results:
                    reject("gate_missing_host_result", event, "required action has no earlier host result", required_action_id)
                if required_action_id not in joined:
                    reject("gate_missing_joined_receipt", event, "required action has no earlier joined receipt", required_action_id)
            if event.get("decision") in {"gate_pass", "gate_resolved"}:
                if set(admitted) != set(required):
                    reject("gate_receipt_set_mismatch", event, "successful gate decisions must admit exactly their required action receipts")
                for required_action_id in required:
                    receipt = joined.get(required_action_id)
                    if receipt is not None and receipt.get("receipt_status") != "pass":
                        reject("gate_admitted_non_pass", event, "successful gate decision admitted a non-pass receipt", required_action_id)
            if len(errors) == gate_error_count and isinstance(gate_id, str):
                gate_decisions[gate_id] = event.get("sequence")
                gate_decision_waves.add(str(event.get("wave_id")))
                if event.get("decision") == "gate_pass":
                    gate_passes[gate_id] = event.get("sequence")

    if run_blocks and events and events[-1].get("event") != "run_blocked":
        reject("blocked_closeout_not_terminal", run_blocks[-1], "run_blocked must be the final causal event")

    if require_complete:
        failed_results = [
            event
            for event in host_results.values()
            if event.get("event") == "host_spawn_failed"
        ]
        if failed_results and not run_blocks:
            reject(
                "missing_blocked_closeout",
                failed_results[0],
                "a host_spawn_failed action requires a terminal run_blocked closeout",
                failed_results[0].get("action_id"),
            )
        blocked_wave_id = run_blocks[0].get("wave_id") if run_blocks else None
        blocked_cleaned_action_ids = (
            set(run_blocks[0].get("cleaned_action_ids", [])) if run_blocks else set()
        )
        for action_id, attempt in attempts.items():
            host_result = host_results.get(action_id)
            if host_result is None:
                reject("missing_host_result", attempt, "attempted action has no host result", action_id)
            elif (
                host_result.get("event") == "host_spawn_returned"
                and action_id not in joined
                and not (
                    host_result.get("wave_id") == blocked_wave_id
                    and action_id in blocked_cleaned_action_ids
                )
            ):
                reject("missing_joined_receipt", host_result, "successful host result has no joined receipt", action_id)

    valid = not errors
    return {
        "schema_version": SCHEMA_VERSION,
        "validator": VALIDATOR_NAME,
        "source": source,
        "event_count": len(events),
        "valid": valid,
        "status": "pass" if valid else "block",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate causal ordering in a native dispatch JSONL event stream.")
    parser.add_argument("events", type=Path, help="Path to events.jsonl")
    parser.add_argument("--output", type=Path, required=True, help="Path for the validation receipt")
    args = parser.parse_args()

    try:
        receipt = validate_events(load_events(args.events), str(args.events))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        receipt = {
            "schema_version": SCHEMA_VERSION,
            "validator": VALIDATOR_NAME,
            "source": str(args.events),
            "event_count": 0,
            "valid": False,
            "status": "block",
            "errors": [{"code": "unreadable_event_stream", "sequence": None, "action_id": None, "message": str(exc)}],
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"valid": receipt["valid"], "status": receipt["status"], "receipt": str(args.output)}, sort_keys=True))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
