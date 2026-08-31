#!/usr/bin/env python3
"""Run the real accepted-stream driver twice and compare semantic bytes."""
from __future__ import annotations
import argparse,json
from run_accepted_stream_driver import run
def main():
 p=argparse.ArgumentParser();p.add_argument("--validate-swu");a=p.parse_args();frontier=[f"SWU-{i:03d}" for i in range(1,15)];units=[{"unit_id":u,"ordinal":i,"status":"pass","result_digest":f"{i:064x}"} for i,u in enumerate(frontier)];q={"stream_id":"generic-stream","frontier":frontier,"units":units,"no_effect":True};r1=run(q);r2=run(json.loads(json.dumps(q)));assert json.dumps(r1,sort_keys=True,separators=(",",":"))==json.dumps(r2,sort_keys=True,separators=(",",":"));assert len(r1["ordered_units"])==14 and r1["status"]=="complete";print(json.dumps({"status":"pass","swu":a.validate_swu,"runs":2,"units_per_run":14,"retries":0,"no_effect":True},sort_keys=True))
if __name__=="__main__":main()
