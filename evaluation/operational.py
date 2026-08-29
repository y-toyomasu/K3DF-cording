"""Read-only operational evaluator."""
from __future__ import annotations
import json
from pathlib import Path
AXES=("change_surface","uncertainty","integration","verification","safety_risk","coordination")
def band(n): return "Routine" if n<=3 else "Low" if n<=7 else "Medium" if n<=11 else "High" if n<=15 else "Very High"
def evaluate(records):
 out=[]
 for r in records:
  required=("configuration","difficulty","quality","performance","process_waiting","execution_friction","unavailable_reason")
  if any(x not in r for x in required): raise ValueError("record sections required")
  d=r["difficulty"]; values={x:int(d[x]) for x in AXES}
  if any(x<0 or x>3 for x in values.values()): raise ValueError("rubric axis must be 0..3")
  out.append({"total":sum(values.values()),"band":band(sum(values.values())),"confidence":d.get("confidence","low")})
 valid=[r for r in records if r["quality"].get("passed") and r["configuration"].get("actual_model") and r["difficulty"].get("rubric_version")=="1.0"]
 decision="Retain" if len(valid)>=3 else "More Data Required"
 return {"schema_version":"1.0","read_only":True,"automatic_actions":False,"records":out,"recommendation":{"decision":decision,"sample_count":len(valid)}}
def main():
 import argparse
 p=argparse.ArgumentParser(); p.add_argument("--records",required=True,type=Path); a=p.parse_args()
 print(json.dumps(evaluate(json.loads(a.records.read_text(encoding="utf-8"))),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
