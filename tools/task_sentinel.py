"""Deterministic, read-only Task Sentinel observation helper."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path


TASK_ID = re.compile(r"^T-\d{5}$")
FIELD = re.compile(r"^- (?P<name>[A-Za-z][A-Za-z /-]*):\s*`?(?P<value>[^`\n]+?)`?\s*$", re.MULTILINE)
SAFE_REVISION = re.compile(r"^[0-9a-f]{7,64}$")
STATE_NAME = "state.json"


class LockUnavailable(RuntimeError):
    """Raised when the Windows-exclusive observer lock is already held."""


@contextmanager
def exclusive_lock(runtime_dir: Path):
    """Acquire an exclusive Windows byte-range lock without changing state on failure."""
    import msvcrt

    runtime_dir.mkdir(parents=True, exist_ok=True)
    lock_path = runtime_dir / "observer.lock"
    with lock_path.open("a+b") as handle:
        handle.seek(0)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise LockUnavailable("observer lock is held") from error
        try:
            yield
        finally:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def read_state(path: Path) -> dict:
    if not path.exists():
        return {"done": {}, "reservations": {}, "notifications": {}}
    with path.open(encoding="utf-8") as source:
        state = json.load(source)
    return {key: state.get(key, {}) for key in ("done", "reservations", "notifications")}


def atomic_write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as temporary:
        json.dump(value, temporary, sort_keys=True, separators=(",", ":"))
        temporary.flush()
        os.fsync(temporary.fileno())
        temporary_name = temporary.name
    os.replace(temporary_name, path)


def parse_task(path: Path) -> dict | None:
    task_id = path.name.split("-", 2)
    identifier = "-".join(task_id[:2])
    if not TASK_ID.fullmatch(identifier):
        return None
    fields = {match["name"].strip(): match["value"].strip() for match in FIELD.finditer(path.read_text(encoding="utf-8"))}
    return {
        "id": identifier,
        "status": fields.get("Status", ""),
        "dependencies": fields.get("Dependencies", "none"),
        "updated_at": fields.get("Task Record Updated At", ""),
        "classification": fields.get("Review Classification", "未判定"),
        "model": fields.get("Recommended Codex Model", ""),
        "reasoning": fields.get("Recommended Reasoning Effort", ""),
        "review_revision": fields.get("Review Main Revision") or fields.get("Task Review Revision") or "",
    }


def parse_time(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def dependencies_resolved(task: dict, statuses: dict[str, str]) -> bool:
    identifiers = TASK_ID.findall(task["dependencies"])
    return all(statuses.get(identifier) == "DONE" for identifier in identifiers)


def should_notify(state: dict, key: str, now: datetime) -> bool:
    previous = parse_time(state["notifications"].get(key, ""))
    return previous is None or now - previous >= timedelta(hours=24)


def observe(tasks_dir: Path, runtime_dir: Path, now: datetime, reserve: bool = False) -> dict:
    """Return safe candidates; optionally persist only explicit action reservations."""
    now = now.astimezone(timezone.utc)
    with exclusive_lock(runtime_dir):
        state_path = runtime_dir / STATE_NAME
        state = read_state(state_path)
        tasks = []
        for path in sorted(tasks_dir.glob("T-*.md")):
            identifier = "-".join(path.name.split("-", 2)[:2])
            if identifier in state["done"]:
                continue
            task = parse_task(path)
            if task:
                tasks.append(task)
        statuses = {task_id: "DONE" for task_id in state["done"]}
        statuses.update({task["id"]: task["status"] for task in tasks})
        result = {"start_candidates": [], "review_candidates": [], "report_candidates": [], "notification_candidates": []}
        changed = False
        active = [task for task in tasks if task["status"] in {"CLAIMED", "IMPLEMENTING"}]
        for task in active:
            reservation = state["reservations"].get(f"start:{task['id']}")
            if reservation and not reservation.get("claimed_confirmed"):
                reservation["claimed_confirmed"] = True
                changed = True
        for task in tasks:
            task_id = task["id"]
            status = task["status"]
            revision = task["review_revision"]
            if status == "DONE":
                if SAFE_REVISION.fullmatch(revision):
                    state["done"][task_id] = revision
                    changed = True
                else:
                    result["notification_candidates"].append({"kind": "missing_done_revision", "task_id": task_id})
                continue
            notification_kind = None
            if status in {"CLAIMED", "IMPLEMENTING"}:
                updated = parse_time(task["updated_at"])
                if updated and now - updated >= timedelta(minutes=45):
                    notification_kind = "stalled"
            elif status == "BLOCKED":
                notification_kind = "blocked"
            elif status == "ACCEPTANCE_REVIEW":
                notification_kind = "acceptance_waiting"
            elif status not in {"READY", "GUI_REVIEW", "DESIGN", ""} and not dependencies_resolved(task, statuses):
                notification_kind = "dependency_inconsistent"
            if notification_kind:
                key = f"{notification_kind}:{task_id}"
                if should_notify(state, key, now):
                    result["notification_candidates"].append({"kind": notification_kind, "task_id": task_id})
                    state["notifications"][key] = now.isoformat()
                    changed = True
            if status == "GUI_REVIEW":
                result["report_candidates"].append({"kind": "gui_review", "task_id": task_id})
            if status == "ACCEPTANCE_REVIEW" and task["classification"] == "non-GUI":
                if not SAFE_REVISION.fullmatch(revision):
                    result["notification_candidates"].append({"kind": "missing_review_revision", "task_id": task_id})
                else:
                    key = f"review:{task_id}:{revision}"
                    if key not in state["reservations"]:
                        candidate = {"task_id": task_id, "review_revision": revision}
                        result["review_candidates"].append(candidate)
                        if reserve:
                            state["reservations"][key] = {"at": now.isoformat()}
                            changed = True
        pending_start = any(not value.get("claimed_confirmed") for key, value in state["reservations"].items() if key.startswith("start:"))
        capacity = 2 - len(active)
        if not pending_start and capacity > 0:
            for task in tasks:
                if task["status"] != "READY" or not dependencies_resolved(task, statuses):
                    continue
                key = f"start:{task['id']}"
                if key in state["reservations"]:
                    continue
                candidate = {"task_id": task["id"], "model": task["model"], "reasoning": task["reasoning"]}
                result["start_candidates"].append(candidate)
                if reserve:
                    state["reservations"][key] = {"at": now.isoformat(), "claimed_confirmed": False}
                    changed = True
                break
        if changed:
            atomic_write(state_path, state)
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Observe task lifecycle metadata and reserve safe candidate actions.")
    parser.add_argument("--tasks-dir", type=Path, default=Path("tasks"))
    parser.add_argument("--runtime-dir", type=Path, default=Path("runtime/task-observer"))
    parser.add_argument("--reserve", action="store_true", help="Persist only returned action reservations.")
    parser.add_argument("--now", help="ISO 8601 timestamp for deterministic use and tests.")
    arguments = parser.parse_args()
    now = parse_time(arguments.now) if arguments.now else datetime.now(timezone.utc)
    if now is None:
        parser.error("--now must be ISO 8601")
    try:
        print(json.dumps(observe(arguments.tasks_dir, arguments.runtime_dir, now, arguments.reserve), sort_keys=True))
    except LockUnavailable:
        print(json.dumps({"lock_unavailable": True}))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
