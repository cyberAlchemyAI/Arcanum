#!/usr/bin/env python3
"""Build a live-entry projection only from owner-produced, digest-bound inputs."""
from __future__ import annotations
import argparse, hashlib, json

def dg(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def produce(request):
    required=("stream_id","child_id","ordinal","baseline","write_scope","owner_receipts")
    if any(k not in request for k in required): raise ValueError("missing live-entry input")
    owners=[r.get("owner") for r in request["owner_receipts"]]
    if not owners or len(owners)!=len(set(owners)) or any(r.get("join_count")!=1 for r in request["owner_receipts"]): raise ValueError("owner join closure")
    if len(request["write_scope"])!=len(set(request["write_scope"])): raise ValueError("duplicate write")
    return {"schema_version":"task-session.accepted-stream-live-entry/v1","stream_id":request["stream_id"],"child_id":request["child_id"],"ordinal":request["ordinal"],"baseline_digest":dg(request["baseline"]),"owner_joins":[dg(r) for r in request["owner_receipts"]],"write_scope":sorted(request["write_scope"])}
def main():
    p=argparse.ArgumentParser();p.add_argument("--validate-swu");a=p.parse_args()
    q={"stream_id":"s","child_id":"c","ordinal":0,"baseline":{},"write_scope":["a"],"owner_receipts":[{"owner":"wpra","join_count":1}]}
    assert produce(q)
    negatives=0
    for b in ({**q,"owner_receipts":[]},{**q,"write_scope":["a","a"]}):
        try: produce(b)
        except ValueError: negatives+=1
    print(json.dumps({"status":"pass","swu":a.validate_swu,"positive":1,"negative":negatives},sort_keys=True))
if __name__=="__main__":main()
