import unittest
from evaluation.operational import evaluate
def rec(): return {"configuration":{"actual_model":"m"},"difficulty":{"rubric_version":"1.0","change_surface":2,"uncertainty":2,"integration":2,"verification":2,"safety_risk":2,"coordination":1},"quality":{"passed":True},"performance":{},"process_waiting":{},"execution_friction":{},"unavailable_reason":{}}
class T(unittest.TestCase):
 def test_more_data(self): self.assertEqual(evaluate([rec()])["recommendation"]["decision"],"More Data Required")
 def test_retain(self): self.assertEqual(evaluate([rec(),rec(),rec()])["recommendation"]["decision"],"Retain")
if __name__=="__main__": unittest.main()
