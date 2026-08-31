#!/usr/bin/env python3
"""Single-use, lock-protected Accepted Stream registry transitions."""
from __future__ import annotations
import argparse, fcntl, hashlib, json, os, tempfile
from pathlib import Path
from typing import Any
from accepted_stream_contract import canonical_bytes, child_id

class StateError(ValueError): pass
TERMINAL = {"completed", "blocked", "superseded"}

def _write_exclusive(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as out: out.write(canonical_bytes(value) + b"\n"); out.flush(); os.fsync(out.fileno())

def _atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as out: out.write(canonical_bytes(value) + b"\n"); out.flush(); os.fsync(out.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)

class Registry:
    def __init__(self, root: Path): self.root=root; self.state=root/"state.json"; self.lock=root/"state.lock"; self.consumption=root/"acceptance-consumption.json"
    def _locked(self):
        self.root.mkdir(parents=True, exist_ok=True); handle=self.lock.open("a+"); fcntl.flock(handle, fcntl.LOCK_EX); return handle
    def read(self) -> dict[str, Any]: return json.loads(self.state.read_text())
    def accept(self, stream_id: str, frontier: list[dict[str, Any]], payload: dict[str, Any]) -> dict[str, Any]:
        handle=self._locked()
        try:
            raw=canonical_bytes(payload); payload_digest=hashlib.sha256(raw).hexdigest()
            if self.consumption.exists():
                existing=json.loads(self.consumption.read_text())
                if existing != {"payload": payload, "payload_digest": payload_digest}: raise StateError("acceptance replay differs")
                if self.state.exists(): raise StateError("acceptance already consumed")
                # Exact crash recovery may finish the one transition whose
                # exclusive consumption record already exists.
                state={"schema_version":"invoke.accepted-stream-state.v1","stream_id":stream_id,"status":"current","next_ordinal":0,"active_child":None,"completed":[],"frontier":frontier}
                _atomic(self.state,state); return state
            if self.state.exists(): raise StateError("registry already initialized")
            _write_exclusive(self.consumption, {"payload":payload,"payload_digest":payload_digest})
            state={"schema_version":"invoke.accepted-stream-state.v1","stream_id":stream_id,"status":"current","next_ordinal":0,"active_child":None,"completed":[],"frontier":frontier}
            _atomic(self.state,state); return state
        finally: handle.close()
    def claim(self, ordinal: int, swu_id: str, baseline_digest: str) -> dict[str, Any]:
        handle=self._locked()
        try:
            state=self.read()
            if state["status"]!="current" or state["active_child"] is not None: raise StateError("stream not claimable")
            cursor=state["next_ordinal"]
            if cursor>=len(state["frontier"]): raise StateError("claim cursor is outside frontier")
            expected=state["frontier"][cursor]
            if ordinal!=expected["ordinal"]: raise StateError("claim ordinal is not next")
            if expected["swu_id"]!=swu_id: raise StateError("claim identity mismatch")
            claim={"child_id":child_id(state["stream_id"],ordinal,swu_id),"ordinal":ordinal,"swu_id":swu_id,"baseline_digest":baseline_digest,"status":"active"}
            state["active_child"]=claim; _atomic(self.state,state); return claim
        finally: handle.close()
    def finish(self, child: str, outcome: str) -> dict[str, Any]:
        if outcome not in {"completed","blocked"}: raise StateError("invalid child outcome")
        handle=self._locked()
        try:
            state=self.read(); active=state["active_child"]
            if not active or active["child_id"]!=child: raise StateError("child is not active")
            active["status"]=outcome; state["completed"].append(active); state["active_child"]=None
            if outcome=="blocked": state["status"]="blocked"
            else: state["next_ordinal"]+=1
            if state["next_ordinal"]==len(state["frontier"]): state["status"]="completed"
            _atomic(self.state,state); return state
        finally: handle.close()

def self_test() -> None:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); frontier=[{"ordinal":i,"swu_id":f"SWU-GENERIC-{i+1:03d}"} for i in (4,9,15)]; reg=Registry(root)
        state=reg.accept("a"*64,frontier,{"request_digest":"b"*64})
        claim=reg.claim(4,"SWU-GENERIC-005","c"*64); reg.finish(claim["child_id"],"completed")
        negatives=[lambda:reg.accept("a"*64,frontier,{"request_digest":"b"*64}),lambda:reg.accept("d"*64,frontier,{"request_digest":"e"*64}),lambda:reg.claim(15,"SWU-GENERIC-016","c"*64),lambda:reg.claim(9,"WRONG","c"*64)]
        claim2=reg.claim(9,"SWU-GENERIC-010","c"*64); negatives += [lambda:reg.claim(15,"SWU-GENERIC-016","c"*64),lambda:reg.finish("f"*64,"completed")]
        for case in negatives:
            try: case()
            except StateError: continue
            raise AssertionError("negative fixture passed")
        reg.finish(claim2["child_id"],"blocked")
    print("PASS SWU-MVLR-002 positive=1 negative=6")

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--validate-swu"); a=p.parse_args()
    if a.validate_swu!="SWU-MVLR-002": p.error("provide --validate-swu SWU-MVLR-002")
    try: self_test()
    except (StateError, AssertionError) as exc: print(f"BLOCK: {exc}"); return 2
    return 0
if __name__=="__main__": raise SystemExit(main())
