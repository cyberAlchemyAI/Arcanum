#!/usr/bin/env python3
import argparse,json
def validate(frontier,claims):
 if not frontier or len(frontier)!=len(claims):return False
 return bool(frontier) and len(claims)==len(frontier) and [x["ordinal"] for x in claims]==sorted({x["ordinal"] for x in claims}) and [x["unit_id"] for x in claims]==frontier and len({x["child_id"] for x in claims})==len(frontier)
def main():
 p=argparse.ArgumentParser();p.add_argument("--validate-swu");a=p.parse_args();f=["SWU-GENERIC-002","SWU-GENERIC-005","SWU-GENERIC-010"];c=[{"ordinal":i,"unit_id":u,"child_id":f"c{i}"} for i,u in zip((1,4,9),f)];assert validate(f,c);assert not validate(f,c[:-1]);assert validate([f[0]],[c[0]]);print(json.dumps({"status":"pass","swu":a.validate_swu,"positive":2,"negative":1},sort_keys=True))
if __name__=="__main__":main()
