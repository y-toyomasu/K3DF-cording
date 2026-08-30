"""Read-only operational evaluator; JSON report is written only to stdout."""
from __future__ import annotations
import json
from pathlib import Path
AXES=("change_surface","uncertainty","integration","verification","safety_risk","coordination")
def band(n): return "Routine" if n<=3 else "Low" if n<=7 else "Medium" if n<=11 else "High" if n<=15 else "Very High"
def rubric(d):
 v={a:int(d[a]) for a in AXES}
 if any(x<0 or x>3 for x in v.values()): raise ValueError("invalid sanitized record")
 n=sum(v.values()); return {"total":n,"band":band(n),"axes":v,"confidence":d.get("confidence","low")}
def check(r):
 keys=("configuration","predicted_difficulty","realized_difficulty","quality","performance","process_waiting","execution_friction","unavailable_reason","comparison_class")
 if any(k not in r for k in keys): return False,"missing required field"
 c=r["configuration"]; required=("recommended_model","recommended_reasoning","po_model","po_reasoning","actual_model","actual_reasoning","actual_source")
 if not all(c.get(k) for k in required): return False,"configuration unknown"
 q=r["quality"]
 if not q.get("passed") or not all(k in q for k in ("acceptance_criteria","build_test","rework","governance_violations")): return False,"quality insufficient"
 if not r["performance"].get("wall_time_seconds"): return False,"major metric unavailable"
 wait=("active_seconds","human_wait_seconds","dependency_wait_seconds","review_wait_seconds","retries","reverification","post_report_rework")
 if not all(k in r["process_waiting"] for k in wait): return False,"waiting incomplete"
 if r["predicted_difficulty"].get("rubric_version")!="1.0" or r["realized_difficulty"].get("rubric_version")!="1.0": return False,"rubric version mismatch"
 return True,""
def evaluate(records):
 rows=[]; valid=[]
 for r in records:
  ok,why=check(r)
  if not ok: rows.append({"unavailable_reason":why}); continue
  p,rn=rubric(r["predicted_difficulty"]),rubric(r["realized_difficulty"])
  rows.append({"comparison_class":r["comparison_class"],"predicted":p,"realized":rn,"prediction_error":rn["total"]-p["total"],"calibration_warning":p["total"]!=r["predicted_difficulty"].get("total") or rn["total"]!=r["realized_difficulty"].get("total")}); valid.append(r)
 classes={json.dumps(x["comparison_class"],sort_keys=True) for x in valid}
 return {"schema_version":"1.0","read_only":True,"automatic_actions":False,"records":rows,"recommendation":{"decision":"Retain" if len(valid)>=3 and len(classes)==1 else "More Data Required","sample_count":len(valid),"confidence":"low","constraints":"no approved threshold; no automatic changes"}}
def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument("--records",required=True,type=Path);a=p.parse_args();print(json.dumps(evaluate(json.loads(a.records.read_text(encoding="utf-8"))),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
