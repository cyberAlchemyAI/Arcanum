#!/usr/bin/env python3
"""JSON command surface for the deterministic Work-Pack execution outer loop."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from execution_loop import decide_next_action, initialize_outer_loop, join_event, set_stop_decision
from readiness_execution import (
    compile_plan_once_context_entry,
    compile_plan_once_task_entry,
    decide_task_session_with_fresh_resume,
    initialize_from_readiness,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    operation = request["operation"]
    if operation == "initialize":
        policy = request["policy"]
        result = {
            "state": initialize_outer_loop(
                policy,
                request["entry"],
                source_invocation_id=request["source_invocation_id"],
                created_at=request["created_at"],
                execution_mode=request["execution_mode"],
                step_budget=request["step_budget"],
            )
        }
    elif operation == "initialize-readiness":
        policy, state = initialize_from_readiness(
            request["audit_config"],
            request["audit_report"],
            source_invocation_id=request["source_invocation_id"],
            created_at=request["created_at"],
            execution_mode=request["execution_mode"],
            step_budget=request["step_budget"],
        )
        result = {"policy": policy, "state": state}
    elif operation == "selection-context-entry":
        result = {
            "entry": compile_plan_once_context_entry(
                request["policy"],
                request["audit_config"],
                request["audit_report"],
                request["selection_receipt"],
                request["execution_binding"],
            )
        }
    elif operation == "selection-entry":
        result = {
            "entry": compile_plan_once_task_entry(
                request["policy"],
                request["audit_config"],
                request["audit_report"],
                request["selection_receipt"],
                request["mutation_admission_receipt"],
                request["execution_binding"],
            )
        }
    elif operation == "decide-fresh-resume":
        state, action, admission = decide_task_session_with_fresh_resume(
            request["state"],
            request["policy"],
            request["resume_request"],
            Path(request["repository_root"]),
            available_inputs=request["available_inputs"],
            installed_owner_routes=request["installed_owner_routes"],
        )
        result = {"state": state, "action": action, "admission": admission}
    elif operation == "decide":
        policy = request["policy"]
        state, action = decide_next_action(
            request["state"],
            policy,
            available_inputs=request["available_inputs"],
            installed_owner_routes=request["installed_owner_routes"],
        )
        result = {"state": state, "action": action}
    elif operation == "join":
        policy = request["policy"]
        result = {"state": join_event(request["state"], policy, request["event"])}
    elif operation == "stop":
        policy = request["policy"]
        result = {
            "state": set_stop_decision(
                request["state"], policy, request["stop_decision"]
            )
        }
    else:
        raise ValueError(f"unknown operation: {operation}")
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
