import unittest

from evaluation.evaluator import build_report


class EvaluatorTests(unittest.TestCase):
    def test_uses_median_for_quality_passing_records(self):
        report = build_report([
            {"benchmark": "fixture", "quality_pass": True, "wall_time_seconds": 1, "tool_calls": 2},
            {"benchmark": "fixture", "quality_pass": True, "wall_time_seconds": 7, "tool_calls": 3},
            {"benchmark": "fixture", "quality_pass": False, "wall_time_seconds": 99, "tool_calls": 99},
        ])
        item = report["benchmarks"][0]
        self.assertEqual(item["performance"]["wall_time_seconds"]["value"], 4.0)
        self.assertEqual(item["quality"]["result"], "review required")

    def test_unavailable_values_are_not_inferred(self):
        item = build_report([])
        self.assertTrue(item["read_only"])
        self.assertFalse(item["automatic_actions"])
        self.assertEqual(item["benchmarks"], [])


if __name__ == "__main__":
    unittest.main()
