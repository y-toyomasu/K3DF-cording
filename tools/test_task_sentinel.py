import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))

from task_sentinel import LockUnavailable, observe


NOW = datetime(2026, 9, 12, 10, tzinfo=timezone.utc)


def task(task_id, status, dependencies="none", classification="non-GUI", revision="", updated=None, model="gpt-x", reasoning="medium"):
    lines = [
        f"# Task: {task_id}", f"- Status: `{status}`", f"- Dependencies: `{dependencies}`",
        f"- Task Record Updated At: `{(updated or NOW).isoformat()}`", f"- Review Classification: `{classification}`",
        f"- Recommended Codex Model: `{model}`", f"- Recommended Reasoning Effort: `{reasoning}`",
    ]
    if revision:
        lines.append(f"- Review Main Revision: `{revision}`")
    return "\n".join(lines)


class TaskSentinelTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.tasks = self.root / "tasks"; self.tasks.mkdir()
        self.runtime = self.root / "runtime" / "task-observer"

    def tearDown(self): self.temporary.cleanup()
    def write(self, identifier, content): (self.tasks / f"{identifier}-sample.md").write_text(content, encoding="utf-8")

    def test_lock_conflict_leaves_state_unchanged(self):
        state = self.runtime / "state.json"; self.runtime.mkdir(parents=True); state.write_text('{"done":{},"reservations":{},"notifications":{}}')
        with patch("task_sentinel.exclusive_lock", side_effect=LockUnavailable()):
            with self.assertRaises(LockUnavailable): observe(self.tasks, self.runtime, NOW, True)
        self.assertEqual(json.loads(state.read_text()), {"done": {}, "reservations": {}, "notifications": {}})

    def test_done_is_cached_and_not_reread(self):
        revision = "a" * 40; self.write("T-00001", task("T-00001", "DONE", revision=revision))
        observe(self.tasks, self.runtime, NOW)
        self.assertEqual(json.loads((self.runtime / "state.json").read_text())["done"], {"T-00001": revision})
        (self.tasks / "T-00001-sample.md").write_text("not markdown", encoding="utf-8")
        self.assertEqual(observe(self.tasks, self.runtime, NOW), {"start_candidates": [], "review_candidates": [], "report_candidates": [], "notification_candidates": []})
        self.write("T-00004", task("T-00004", "READY", "T-00001"))
        self.assertEqual(observe(self.tasks, self.runtime, NOW)["start_candidates"][0]["task_id"], "T-00004")

    def test_review_revision_dedup_and_missing_revision(self):
        revision = "b" * 40; self.write("T-00002", task("T-00002", "ACCEPTANCE_REVIEW", revision=revision))
        self.assertEqual(len(observe(self.tasks, self.runtime, NOW, True)["review_candidates"]), 1)
        self.assertEqual(observe(self.tasks, self.runtime, NOW, True)["review_candidates"], [])
        self.write("T-00003", task("T-00003", "ACCEPTANCE_REVIEW"))
        self.assertIn({"kind": "missing_review_revision", "task_id": "T-00003"}, observe(self.tasks, self.runtime, NOW)["notification_candidates"])

    def test_start_requires_resolved_dependencies_claim_confirmation_and_capacity(self):
        self.write("T-00010", task("T-00010", "DONE", revision="c" * 40))
        self.write("T-00011", task("T-00011", "READY", "T-00010"))
        self.write("T-00012", task("T-00012", "READY", "T-09999"))
        first = observe(self.tasks, self.runtime, NOW, True)["start_candidates"]
        self.assertEqual([item["task_id"] for item in first], ["T-00011"])
        self.assertEqual(observe(self.tasks, self.runtime, NOW, True)["start_candidates"], [])
        self.write("T-00011", task("T-00011", "CLAIMED", "T-00010"))
        self.write("T-00013", task("T-00013", "READY"))
        self.assertEqual([item["task_id"] for item in observe(self.tasks, self.runtime, NOW, True)["start_candidates"]], ["T-00013"])

    def test_notifications_gui_and_sensitive_output_boundary(self):
        stale = NOW - timedelta(minutes=46)
        self.write("T-00020", task("T-00020", "IMPLEMENTING", updated=stale))
        self.write("T-00021", task("T-00021", "BLOCKED"))
        self.write("T-00022", task("T-00022", "READY", "T-99999"))
        self.write("T-00023", task("T-00023", "GUI_REVIEW", classification="GUI"))
        result = observe(self.tasks, self.runtime, NOW)
        self.assertEqual(result["report_candidates"], [{"kind": "gui_review", "task_id": "T-00023"}])
        self.assertNotIn("T-00022", str(result["notification_candidates"]))
        self.assertIn("stalled", str(result)); self.assertIn("blocked", str(result))
        self.assertEqual(observe(self.tasks, self.runtime, NOW + timedelta(hours=23))["notification_candidates"], [])
        self.assertIn("stalled", str(observe(self.tasks, self.runtime, NOW + timedelta(hours=24))["notification_candidates"]))
        text = (self.runtime / "state.json").read_text(encoding="utf-8")
        self.assertNotIn("# Task", text); self.assertNotIn(str(self.root), text)


if __name__ == "__main__": unittest.main()
