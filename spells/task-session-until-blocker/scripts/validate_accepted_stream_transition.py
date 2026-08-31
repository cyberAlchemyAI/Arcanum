#!/usr/bin/env python3
import argparse,json
from run_accepted_stream_driver import run
def main():
 p=argparse.ArgumentParser();p.add_argument("--validate-swu");a=p.parse_args();q={"stream_id":"s","frontier":["a","b"],"units":[{"unit_id":"a","ordinal":0,"status":"pass"},{"unit_id":"b","ordinal":1,"status":"pass"}]};assert run(q)["status"]=="complete"
 try:run({**q,"frontier":["b","a"]})
 except ValueError:pass
 else:raise SystemExit("negative failed")
 print(json.dumps({"status":"pass","swu":a.validate_swu,"positive":1,"negative":1},sort_keys=True))
if __name__=="__main__":main()
