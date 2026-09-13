# Task Sentinel helper

`task_sentinel.py` reads only the lifecycle metadata required by Task Sentinel. It never changes Task files, Git, documents, or agent settings. Its sole write location is the ignored `runtime/task-observer/` directory, where it keeps atomic reservation, notification, and completed-task metadata.

The runtime location is fixed by the helper to that repository-relative directory; no command-line option can redirect it.

Run an observation. It may persist only completed-task caching, notification cooldowns, and observed `CLAIMED` confirmations; it does not create a new action reservation:

```powershell
python tools/task_sentinel.py
```

Persist the returned start or review reservations as well as the normal lifecycle-observation state:

```powershell
python tools/task_sentinel.py --reserve
```

The JSON result contains safe task identifiers, lifecycle decisions, configured model/reasoning, and review revisions. It intentionally excludes Task content and sensitive or host-specific data. The helper does not start agents, perform reviews, accept work, or transition Tasks to `DONE`.
