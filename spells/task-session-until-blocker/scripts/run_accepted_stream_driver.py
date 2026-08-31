#!/usr/bin/env python3
"""Pure deterministic accepted-stream driver used for implementation tests and rehearsal."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
def dg(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def run(req):
    frontier=req["frontier"];units=req["units"]
    if len(frontier)!=len(units) or len(frontier)!=len(set(frontier)):raise ValueError("frontier mismatch")
    events=[]
    prior_ordinal=-1
    for i,(uid,u) in enumerate(zip(frontier,units)):
        ordinal=u.get("ordinal")
        if u.get("unit_id")!=uid or not isinstance(ordinal,int) or isinstance(ordinal,bool) or ordinal<=prior_ordinal:raise ValueError("unit order mismatch")
        if u.get("status")!="pass":return {"schema_version":"task-session-until-blocker.accepted-stream-driver-receipt/v1","stream_id":req["stream_id"],"status":"blocked","ordered_units":frontier[:i],"event_digests":events,"candidate_count":0}
        events.append(dg({"stream":req["stream_id"],"unit":uid,"ordinal":ordinal,"result":u.get("result_digest")}));prior_ordinal=ordinal
    return {"schema_version":"task-session-until-blocker.accepted-stream-driver-receipt/v1","stream_id":req["stream_id"],"status":"complete","ordered_units":frontier,"event_digests":events,"candidate_count":0}
def main():
 p=argparse.ArgumentParser();p.add_argument("--request");p.add_argument("--validate-swu");a=p.parse_args()
 if a.validate_swu:q={"stream_id":"s","frontier":["u"],"units":[{"unit_id":"u","ordinal":0,"status":"pass","result_digest":"0"*64}]}
 else:q=json.loads(Path(a.request).read_text())
 print(json.dumps(run(q),sort_keys=True,indent=2))
if __name__=="__main__":main()
