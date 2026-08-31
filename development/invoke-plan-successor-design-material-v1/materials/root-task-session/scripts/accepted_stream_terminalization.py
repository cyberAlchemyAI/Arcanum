#!/usr/bin/env python3
"""Deterministic closeout ordering for an accepted-stream child."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def canonical_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def terminalize(precloseout, owner_closeout):
    if precloseout.get("schema_version") != "task-session.precloseout-source/v2": raise ValueError("invalid precloseout")
    if owner_closeout.get("schema_version") != "invoke.owner-closeout/v2": raise ValueError("invalid owner closeout")
    if precloseout["stream_id"] != owner_closeout["stream_id"] or precloseout["child_id"] != owner_closeout["child_id"]: raise ValueError("cross-child closeout")
    if owner_closeout["precloseout_digest"] != canonical_digest(precloseout): raise ValueError("stale owner closeout")
    return {"schema_version":"task-session.final-terminal/v2","stream_id":precloseout["stream_id"],"child_id":precloseout["child_id"],"precloseout_digest":canonical_digest(precloseout),"owner_closeout_digest":canonical_digest(owner_closeout),"status":"pass" if precloseout["status"]==owner_closeout["status"]=="pass" else "block"}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--precloseout"); p.add_argument("--owner-closeout"); p.add_argument("--validate-swu"); a=p.parse_args()
    if a.validate_swu:
        pre={"schema_version":"task-session.precloseout-source/v2","stream_id":"s","child_id":"c","reconciliation_digest":"0"*64,"observed_writes":[],"status":"pass"}
        close={"schema_version":"invoke.owner-closeout/v2","stream_id":"s","child_id":"c","precloseout_digest":canonical_digest(pre),"owner":"invoke:refresh","status":"pass"}
        assert terminalize(pre,close)["status"]=="pass"
        try: terminalize(pre,{**close,"child_id":"x"})
        except ValueError: pass
        else: raise SystemExit("cross-child negative failed")
        print(json.dumps({"status":"pass","swu":a.validate_swu,"positive":1,"negative":1},sort_keys=True)); return
    print(json.dumps(terminalize(json.loads(Path(a.precloseout).read_text()),json.loads(Path(a.owner_closeout).read_text())),sort_keys=True,indent=2))
if __name__ == "__main__": main()
