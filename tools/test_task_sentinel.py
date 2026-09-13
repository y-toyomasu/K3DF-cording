import io
import json
import msvcrt
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))

import task_sentinel
from task_sentinel import LockUnavailable, atomic_write, main, observe


NOW = datetime(2026, 9, 12, 10, tzinfo=timezone.utc)
DEFAULT_RUNTIME_DIR = task_sentinel.RUNTIME_DIR


def task(task_id, status, dependencies="none", classification="non-GUI", revision="", updated=None, model="gpt-5.6-terra", reasoning="medium"):
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
        self.runtime_patch = patch.object(task_sentinel, "RUNTIME_DIR", self.runtime)
        self.runtime_patch.start()

    def tearDown(self): self.runtime_patch.stop(); self.temporary.cleanup()
    def write(self, identifier, content): (self.tasks / f"{identifier}-sample.md").write_text(content, encoding="utf-8")

    def test_actual_windows_lock_conflict_leaves_state_unchanged(self):
        state = self.runtime / "state.json"; self.runtime.mkdir(parents=True); state.write_text('{"done":{},"reservations":{},"notifications":{}}')
        lock_path = self.runtime / "observer.lock"
        with lock_path.open("a+b") as holder:
            holder.write(b"0"); holder.flush(); holder.seek(0)
            msvcrt.locking(holder.fileno(), msvcrt.LK_NBLCK, 1)
            with self.assertRaises(LockUnavailable): observe(self.tasks, NOW, True)
            holder.seek(0); msvcrt.locking(holder.fileno(), msvcrt.LK_UNLCK, 1)
        self.assertEqual(json.loads(state.read_text()), {"done": {}, "reservations": {}, "notifications": {}})

    def test_atomic_write_uses_replace_and_leaves_complete_json(self):
        state = self.runtime / "state.json"; self.runtime.mkdir(parents=True); state.write_text('{"previous":true}', encoding="utf-8")
        with patch("task_sentinel.os.replace", wraps=__import__("os").replace) as replace:
            atomic_write(state, {"done": {"T-00001": "a" * 40}, "reservations": {}, "notifications": {}})
        replace.assert_called_once()
        self.assertEqual(json.loads(state.read_text(encoding="utf-8"))["done"], {"T-00001": "a" * 40})

    def test_done_is_cached_and_not_reread(self):
        revision = "a" * 40; self.write("T-00001", task("T-00001", "DONE", revision=revision))
        observe(self.tasks, NOW)
        self.assertEqual(json.loads((self.runtime / "state.json").read_text())["done"], {"T-00001": revision})
        (self.tasks / "T-00001-sample.md").write_text("not markdown", encoding="utf-8")
        self.assertEqual(observe(self.tasks, NOW), {"start_candidates": [], "review_candidates": [], "report_candidates": [], "notification_candidates": []})
        self.write("T-00004", task("T-00004", "READY", "T-00001"))
        self.assertEqual(observe(self.tasks, NOW)["start_candidates"][0]["task_id"], "T-00004")

    def test_review_revision_dedup_and_missing_revision(self):
        revision = "b" * 40; self.write("T-00002", task("T-00002", "ACCEPTANCE_REVIEW", revision=revision))
        self.assertEqual(len(observe(self.tasks, NOW, True)["review_candidates"]), 1)
        self.assertEqual(observe(self.tasks, NOW, True)["review_candidates"], [])
        self.write("T-00003", task("T-00003", "ACCEPTANCE_REVIEW"))
        self.assertIn({"kind": "missing_review_revision", "task_id": "T-00003"}, observe(self.tasks, NOW)["notification_candidates"])

    def test_start_requires_resolved_dependencies_claim_confirmation_and_capacity(self):
        self.write("T-00010", task("T-00010", "DONE", revision="c" * 40))
        self.write("T-00011", task("T-00011", "READY", "T-00010"))
        self.write("T-00012", task("T-00012", "READY", "T-09999"))
        first = observe(self.tasks, NOW, True)["start_candidates"]
        self.assertEqual([item["task_id"] for item in first], ["T-00011"])
        self.assertEqual(observe(self.tasks, NOW, True)["start_candidates"], [])
        self.write("T-00011", task("T-00011", "CLAIMED", "T-00010"))
        self.write("T-00013", task("T-00013", "READY"))
        self.assertEqual([item["task_id"] for item in observe(self.tasks, NOW, True)["start_candidates"]], ["T-00013"])

    def test_notifications_gui_and_sensitive_output_boundary(self):
        stale = NOW - timedelta(minutes=46)
        self.write("T-00020", task("T-00020", "IMPLEMENTING", updated=stale))
        self.write("T-00021", task("T-00021", "BLOCKED"))
        self.write("T-00022", task("T-00022", "READY", "T-99999"))
        self.write("T-00023", task("T-00023", "GUI_REVIEW", classification="GUI"))
        result = observe(self.tasks, NOW)
        self.assertEqual(result["report_candidates"], [{"kind": "gui_review", "task_id": "T-00023"}])
        self.assertNotIn("T-00022", str(result["notification_candidates"]))
        self.assertIn("stalled", str(result)); self.assertIn("blocked", str(result))
        self.assertEqual(observe(self.tasks, NOW + timedelta(hours=23))["notification_candidates"], [])
        self.assertIn("stalled", str(observe(self.tasks, NOW + timedelta(hours=24))["notification_candidates"]))
        text = (self.runtime / "state.json").read_text(encoding="utf-8")
        self.assertNotIn("# Task", text); self.assertNotIn(str(self.root), text)

    def test_invalid_model_and_reasoning_never_leave_task_metadata(self):
        unsafe = "C:" + chr(92) + "Users" + chr(92) + "operator" + chr(92) + "token-value"
        self.write("T-00030", task("T-00030", "READY", model=unsafe, reasoning="secret-value"))
        result = observe(self.tasks, NOW, True)
        self.assertEqual(result["start_candidates"], [])
        self.assertIn({"kind": "invalid_start_configuration", "task_id": "T-00030"}, result["notification_candidates"])
        self.assertNotIn(unsafe, json.dumps(result))
        state = (self.runtime / "state.json")
        self.assertFalse(state.exists() and unsafe in state.read_text(encoding="utf-8"))

    def test_dependency_inconsistency_prioritizes_active_and_review_states(self):
        self.write("T-00040", task("T-00040", "CLAIMED", "T-09999"))
        self.write("T-00041", task("T-00041", "ACCEPTANCE_REVIEW", "T-09999", revision="d" * 40))
        self.write("T-00042", task("T-00042", "BLOCKED", "T-09999"))
        result = observe(self.tasks, NOW)
        notifications = result["notification_candidates"]
        self.assertIn({"kind": "dependency_inconsistent", "task_id": "T-00040"}, notifications)
        self.assertIn({"kind": "dependency_inconsistent", "task_id": "T-00041"}, notifications)
        self.assertIn({"kind": "blocked", "task_id": "T-00042"}, notifications)
        self.assertNotIn({"kind": "acceptance_waiting", "task_id": "T-00041"}, notifications)

    def test_dependency_inconsistent_acceptance_review_returns_notification_only(self):
        self.write("T-00043", task("T-00043", "ACCEPTANCE_REVIEW", "T-09999", revision="e" * 40))
        result = observe(self.tasks, NOW, True)
        self.assertEqual(result["notification_candidates"], [{"kind": "dependency_inconsistent", "task_id": "T-00043"}])
        self.assertEqual(result["review_candidates"], [])
        self.assertEqual(result["start_candidates"], [])
        self.assertEqual(result["report_candidates"], [])

    def test_runtime_dir_is_fixed_and_cli_rejects_override(self):
        self.assertEqual(task_sentinel.RUNTIME_DIR, self.runtime)
        self.assertEqual(DEFAULT_RUNTIME_DIR, Path(task_sentinel.__file__).resolve().parent.parent / "runtime" / "task-observer")
        with patch.object(sys, "argv", ["task_sentinel.py", "--runtime-dir", "alternate-runtime"]), patch.object(sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit): main()


if __name__ == "__main__": unittest.main()
