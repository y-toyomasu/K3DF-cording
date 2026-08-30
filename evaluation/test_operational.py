import unittest
from evaluation.operational import evaluate
def rec():
 return {"comparison_class":{"role":"e"},"configuration":{"recommended_model":"a","recommended_reasoning":"h","po_model":"a","po_reasoning":"h","actual_model":"a","actual_reasoning":"h","actual_source":"environment"},"predicted_difficulty":{"rubric_version":"1.0","change_surface":2,"uncertainty":2,"integration":2,"verification":2,"safety_risk":2,"coordination":1},"realized_difficulty":{"rubric_version":"1.0","change_surface":2,"uncertainty":2,"integration":2,"verification":2,"safety_risk":2,"coordination":1},"quality":{"passed":True,"acceptance_criteria":"p","build_test":"p","rework":0,"governance_violations":0},"performance":{"wall_time_seconds":1},"process_waiting":{"active_seconds":1,"human_wait_seconds":0,"dependency_wait_seconds":0,"review_wait_seconds":0,"retries":0,"reverification":0,"post_report_rework":0},"execution_friction":{},"unavailable_reason":{}}
class T(unittest.TestCase):
 def test_more_data_and_model_blind(self):
  a=rec(); b=rec(); b["configuration"]["actual_model"]="other"; self.assertEqual(evaluate([a,b])["records"][0]["predicted"]["total"],11); self.assertEqual(evaluate([a])["recommendation"]["decision"],"More Data Required")
 def test_three_same_class_retain(self): self.assertEqual(evaluate([rec(),rec(),rec()])["recommendation"]["decision"],"Retain")
if __name__=="__main__": unittest.main()
