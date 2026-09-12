# Task Sentinel helper

`task_sentinel.py` reads only the lifecycle metadata required by Task Sentinel. It never changes Task files, Git, documents, or agent settings. Its sole write location is the ignored `runtime/task-observer/` directory, where it keeps atomic reservation, notification, and completed-task metadata.

Run an observation without changing runtime state:

```powershell
python tools/task_sentinel.py
```

Persist only the returned start or review reservations:

```powershell
python tools/task_sentinel.py --reserve
```

The JSON result contains safe task identifiers, lifecycle decisions, configured model/reasoning, and review revisions. It intentionally excludes Task content and sensitive or host-specific data. The helper does not start agents, perform reviews, accept work, or transition Tasks to `DONE`.
