#!/usr/bin/env python3
"""Validate continuity/successor and exactly-one-terminal invariants."""
from __future__ import annotations
import argparse, hashlib, json

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def validate(terminal, continuity, successor):
    ids={(x.get("stream_id"),x.get("child_id")) for x in (terminal,continuity,successor)}
    if len(ids)!=1: raise ValueError("cross-child evidence")
    if continuity.get("terminal_digest")!=digest(terminal): raise ValueError("terminal mismatch")
    count=successor.get("candidate_count"); candidate=successor.get("candidate")
    if count not in (0,1) or (count==0)!=(candidate is None): raise ValueError("candidate cardinality")
    if continuity.get("candidate_count")!=count: raise ValueError("continuity candidate mismatch")
    return {"schema_version":"task-session-until-blocker.continuity-successor-pair/v1","stream_id":terminal["stream_id"],"child_id":terminal["child_id"],"continuity_digest":digest(continuity),"successor_digest":digest(successor)}
def main():
    p=argparse.ArgumentParser();p.add_argument("--validate-swu");a=p.parse_args()
    t={"stream_id":"s","child_id":"c"};c={"stream_id":"s","child_id":"c","terminal_digest":digest(t),"candidate_count":0};s={"stream_id":"s","child_id":"c","candidate_count":0,"candidate":None}
    assert validate(t,c,s)
    negatives=0
    for bad in ({**s,"candidate_count":1},{**s,"child_id":"x"}):
        try: validate(t,c,bad)
        except ValueError: negatives+=1
    if negatives!=2: raise SystemExit("negative validation failed")
    print(json.dumps({"status":"pass","swu":a.validate_swu,"positive":1,"negative":negatives},sort_keys=True))
if __name__=="__main__": main()
