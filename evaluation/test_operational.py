import copy, unittest
from evaluation.operational import band, difficulty, evaluate
def sample():
 import json
 from pathlib import Path
 return json.loads(Path("evaluation/fixtures/operational-sample.json").read_text(encoding="utf-8"))[0]
def comparison_rows(candidate_times=(8,9,10)):
 rows=[]
 for wall_time in (10,11,12):
  row=sample(); row["performance"]["wall_time_seconds"]=wall_time; rows.append(row)
 for wall_time in candidate_times:
  row=sample(); row["performance"]["wall_time_seconds"]=wall_time
  row["configuration"]["po_selected"]["model"]="candidate-model"
  row["configuration"]["actual"]["model"]="candidate-model"
  rows.append(row)
 return rows
def agents_rows(candidate_times=(8,9,10)):
 rows=[]; baseline=sample()["measurement_identity"]["agents_revision"]; candidate="f"*40
 for wall_time in (10,11,12):
  row=sample(); row["experiment_axis"]={"name":"agents_revision","baseline":baseline,"candidate":candidate}; row["performance"]["wall_time_seconds"]=wall_time; rows.append(row)
 for wall_time in candidate_times:
  row=sample(); row["experiment_axis"]={"name":"agents_revision","baseline":baseline,"candidate":candidate}; row["measurement_identity"]["agents_revision"]=candidate; row["performance"]["wall_time_seconds"]=wall_time; rows.append(row)
 return rows
class OperationalTests(unittest.TestCase):
 def test_measurement_identity_contract_and_report(self):
  row=evaluate([sample()])["records"][0]
  self.assertEqual(row["measurement_identity"],sample()["measurement_identity"])
  a=sample(); del a["measurement_identity"]; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); del a["measurement_identity"]["benchmark_id"]; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["measurement_identity"]["unknown"]="value"; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["measurement_identity"]["snapshot_version"]=""; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["measurement_identity"]["prompt_version"]="x"*81; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["measurement_identity"]["benchmark_id"]=1; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["measurement_identity"]["agents_revision"]="AGENTS.md body"; report=evaluate([a]); self.assertEqual(report["records"][0]["status"],"unavailable"); self.assertNotIn("AGENTS.md body",str(report))
 def test_model_blind_and_band_boundaries(self):
  a=sample(); b=copy.deepcopy(a); b["configuration"]["actual"]["model"]="other"
  self.assertEqual(difficulty(a["predicted_difficulty"])["total"],difficulty(b["predicted_difficulty"])["total"])
  self.assertEqual([band(x) for x in (3,4,7,8,11,12,15,16,18)],["Routine","Low","Low","Medium","Medium","High","High","Very High","Very High"])
 def test_calibration_normal_and_mismatch(self):
  a=sample(); self.assertFalse(difficulty(a["predicted_difficulty"])["calibration_warning"])
  a["predicted_difficulty"]["total"]=10; self.assertTrue(difficulty(a["predicted_difficulty"])["calibration_warning"])
  a=sample(); del a["predicted_difficulty"]["total"]; del a["predicted_difficulty"]["band"]; self.assertFalse(difficulty(a["predicted_difficulty"])["calibration_warning"])
 def test_configuration_unknown_and_different_are_more_data(self):
  rows=comparison_rows(); rows[0]["configuration"]["actual"]={"unavailable_reason":"not available"}; self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
  rows=comparison_rows(); rows[-1]["comparison_class"]["role"]="other"; self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
 def test_quality_regression_sample_count_and_version(self):
  rows=comparison_rows(); rows[-1]["quality"]["regression"]=True; self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
  rows=comparison_rows((8,9)); self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
  rows=comparison_rows(); rows[-1]["predicted_difficulty"]["rubric_version"]="2"; self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
  rows=comparison_rows(); rows[-1]["performance"]["wall_time_seconds"]=None; rows[-1]["unavailable_reason"]["wall_time_seconds"]="not available"; self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
 def test_waiting_friction_unavailable_evidence_and_report(self):
  report=evaluate([sample()]); row=report["records"][0]
  self.assertIn("active_seconds",row["process_waiting"]); self.assertIn("review_wait_seconds",row["process_waiting"]); self.assertIn("reverification",row["execution_friction"]); self.assertIn("time_to_first_tool_seconds",row["unavailable_reason"]); self.assertEqual(row["realized"]["total"],12)
  self.assertTrue(report["read_only"]); self.assertFalse(report["automatic_actions"])
 def test_prohibited_field_is_sanitized(self):
  a=sample(); a["prompt"]="sensitive"; row=evaluate([a])["records"][0]; self.assertEqual(row["status"],"unavailable"); self.assertNotIn("sensitive",str(row))
  a=sample(); a["unavailable_reason"]["path"]="X:"+chr(92)+"private"; row=evaluate([a])["records"][0]; self.assertEqual(row["status"],"unavailable"); self.assertNotIn("private",str(row))
  a=sample(); a["quality"]["operator_note"]="sensitive"; row=evaluate([a])["records"][0]; self.assertEqual(row["status"],"unavailable"); self.assertNotIn("sensitive",str(row))
 def test_type_range_and_length_validation(self):
  a=sample(); a["quality"]["rework"]=-1; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["comparison_class"]["role"]="x"*81; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["predicted_difficulty"]["total"]="11"; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["predicted_difficulty"]["total"]=99; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
 def test_unavailable_waiting_and_friction_require_matching_reasons(self):
  a=sample()
  unavailable_fields=("active_seconds","human_wait_seconds","dependency_wait_seconds","review_wait_seconds","tool_errors","retries","reverification","post_report_rework")
  for key in unavailable_fields: a["unavailable_reason"][key]="not available"
  for key in a["process_waiting"]: a["process_waiting"][key]=None
  for key in a["execution_friction"]: a["execution_friction"][key]=None
  row=evaluate([a])["records"][0]
  for key in a["process_waiting"]: self.assertIsNone(row["process_waiting"][key])
  for key in a["execution_friction"]: self.assertIsNone(row["execution_friction"][key])
  a=sample(); a["process_waiting"]["active_seconds"]=None; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["execution_friction"]["retries"]=None; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["unavailable_reason"]["retries"]="not available"; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["process_waiting"]["human_wait_seconds"]=-1; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["execution_friction"]["retries"]=-1; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
 def test_performance_contract_requires_all_fields_and_matching_reasons(self):
  row=evaluate([sample()])["records"][0]
  self.assertIsNone(row["performance"]["time_to_first_tool_seconds"])
  a=sample(); del a["performance"]["cost"]; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); del a["unavailable_reason"]["cost"]; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["performance"]["cost"]=1; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
  a=sample(); a["performance"]["wall_time_seconds"]=-1; self.assertEqual(evaluate([a])["records"][0]["status"],"unavailable")
 def test_cohort_evidence_and_change_candidate_path(self):
  recommendation=evaluate(comparison_rows())["recommendation"]
  self.assertEqual(recommendation["decision"],"Change Candidate")
  self.assertEqual(len(recommendation["configuration_cohorts"]),2)
  self.assertEqual([item["quality_passing_sample_count"] for item in recommendation["configuration_cohorts"]],[3,3])
  self.assertEqual([item["role"] for item in recommendation["experiment_cohorts"]],["baseline","candidate"])
  self.assertEqual(set(recommendation["experiment_cohorts"][0]["metrics"]),{"wall_time_seconds","retries","reverification","post_report_rework","governance_violations"})
  self.assertLess(recommendation["metric_evaluation"]["candidate_median"],recommendation["metric_evaluation"]["baseline_median"])
  self.assertIn("observational only",recommendation["constraints"])
 def test_retain_requires_evaluated_performance_not_sample_count(self):
  self.assertEqual(evaluate([sample(),sample(),sample()])["recommendation"]["decision"],"More Data Required")
  recommendation=evaluate(comparison_rows((12,13,14)))["recommendation"]
  self.assertEqual(recommendation["decision"],"Retain")
  self.assertGreaterEqual(recommendation["metric_evaluation"]["candidate_median"],recommendation["metric_evaluation"]["baseline_median"])
 def test_agents_revision_axis_keeps_configuration_fixed(self):
  recommendation=evaluate(agents_rows())["recommendation"]
  self.assertEqual(recommendation["decision"],"Change Candidate")
  self.assertEqual(recommendation["experiment_axis"]["name"],"agents_revision")
  self.assertEqual(recommendation["configuration"]["baseline"],recommendation["configuration"]["candidate"])
  self.assertEqual([item["quality_passing_sample_count"] for item in recommendation["experiment_cohorts"]],[3,3])
 def test_axis_fixed_conditions_multiple_change_and_unknown(self):
  rows=comparison_rows(); rows[-1]["measurement_identity"]["agents_revision"]="f"*40
  self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
  rows=comparison_rows(); rows[-1]["measurement_identity"]["snapshot_version"]="v2"
  self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
  rows=agents_rows(); rows[-1]["configuration"]["actual"]["model"]="other"
  self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
  a=sample(); a["experiment_axis"]["name"]="unknown"; report=evaluate([a])
  self.assertEqual(report["records"][0]["status"],"unavailable"); self.assertEqual(report["recommendation"]["decision"],"More Data Required")
 def test_quality_failure_is_retained_as_regression_and_excluded(self):
  rows=comparison_rows(); rows[-1]["quality"]["passed"]=False; recommendation=evaluate(rows)["recommendation"]
  self.assertEqual(recommendation["decision"],"More Data Required")
  candidate=next(item for item in recommendation["experiment_cohorts"] if item["role"]=="candidate")
  self.assertEqual(candidate["sample_count"],3); self.assertEqual(candidate["quality_passing_sample_count"],2); self.assertEqual(candidate["quality_regression_count"],1)
  self.assertEqual(candidate["metrics"]["wall_time_seconds"]["sample_count"],2)
 def test_secondary_metric_unavailable_reason_is_reported(self):
  rows=comparison_rows(); rows[-1]["execution_friction"]["retries"]=None; rows[-1]["unavailable_reason"]["retries"]="not available from execution record"
  recommendation=evaluate(rows)["recommendation"]; self.assertEqual(recommendation["decision"],"More Data Required")
  candidate=next(item for item in recommendation["experiment_cohorts"] if item["role"]=="candidate")
  retries=candidate["metrics"]["retries"]; self.assertEqual(retries["unavailable_count"],1); self.assertEqual(retries["unavailable_reasons"],["not available from execution record"])
if __name__=="__main__": unittest.main()
