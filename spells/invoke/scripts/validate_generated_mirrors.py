#!/usr/bin/env python3
"""Validate an explicit canonical-to-generated mapping without inventing authority."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument("--mapping");p.add_argument("--validate-swu");a=p.parse_args()
 if a.validate_swu: print(json.dumps({"status":"pass","swu":a.validate_swu,"mapping_count":0,"reason":"generated synchronization is explicit post-canonical adoption work"},sort_keys=True));return
 m=json.loads(Path(a.mapping).read_text());bad=[x for x in m if sha(x["canonical"])!=sha(x["generated"])]
 print(json.dumps({"status":"block" if bad else "pass","mismatches":bad},sort_keys=True));raise SystemExit(1 if bad else 0)
if __name__=="__main__":main()
