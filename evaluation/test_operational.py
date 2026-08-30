import copy, unittest
from evaluation.operational import band, difficulty, evaluate
def sample():
 import json
 from pathlib import Path
 return json.loads(Path("evaluation/fixtures/operational-sample.json").read_text(encoding="utf-8"))[0]
class OperationalTests(unittest.TestCase):
 def test_model_blind_and_band_boundaries(self):
  a=sample(); b=copy.deepcopy(a); b["configuration"]["actual"]["model"]="other"
  self.assertEqual(difficulty(a["predicted_difficulty"])["total"],difficulty(b["predicted_difficulty"])["total"])
  self.assertEqual([band(x) for x in (3,4,7,8,11,12,15,16,18)],["Routine","Low","Low","Medium","Medium","High","High","Very High","Very High"])
 def test_calibration_normal_and_mismatch(self):
  a=sample(); self.assertFalse(difficulty(a["predicted_difficulty"])["calibration_warning"])
  a["predicted_difficulty"]["total"]=10; self.assertTrue(difficulty(a["predicted_difficulty"])["calibration_warning"])
  a=sample(); del a["predicted_difficulty"]["total"]; del a["predicted_difficulty"]["band"]; self.assertFalse(difficulty(a["predicted_difficulty"])["calibration_warning"])
 def test_configuration_unknown_and_different_are_more_data(self):
  a=sample(); a["configuration"]["actual"]={"unavailable_reason":"not available"}; self.assertEqual(evaluate([a]*3)["recommendation"]["decision"],"More Data Required")
  rows=[sample(),sample(),sample()]; rows[1]["configuration"]["actual"]["model"]="other"; self.assertEqual(evaluate(rows)["recommendation"]["decision"],"More Data Required")
 def test_quality_regression_sample_count_and_version(self):
  a=sample(); a["quality"]["regression"]=True; self.assertEqual(evaluate([a]*3)["recommendation"]["decision"],"More Data Required")
  self.assertEqual(evaluate([sample(),sample()])["recommendation"]["decision"],"More Data Required")
  a=sample(); a["predicted_difficulty"]["rubric_version"]="2"; self.assertEqual(evaluate([a]*3)["recommendation"]["decision"],"More Data Required")
 def test_waiting_friction_unavailable_evidence_and_report(self):
  report=evaluate([sample()]); row=report["records"][0]
  self.assertIn("active_seconds",row["process_waiting"]); self.assertIn("review_wait_seconds",row["process_waiting"]); self.assertIn("reverification",row["execution_friction"]); self.assertIn("tokens",row["unavailable_reason"]); self.assertEqual(row["realized"]["total"],12)
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
 def test_three_comparable_samples_retain_without_causal_claim(self):
  recommendation=evaluate([sample(),sample(),sample()])["recommendation"]; self.assertEqual(recommendation["decision"],"Retain"); self.assertIn("observational only",recommendation["constraints"])
if __name__=="__main__": unittest.main()
