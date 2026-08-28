"""Read-only baseline report generator for sanitized benchmark records."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

KNOWN_METRICS = {
    "wall_time_seconds": "seconds",
    "tool_calls": "count",
    "retries": "count",
}


def metric(values: list[float], unit: str, source: str) -> dict[str, Any]:
    if not values:
        return {"value": None, "unit": unit, "source": source,
                "quality_condition": "not measured", "unavailable_reason": "not available in sanitized execution record"}
    return {"value": statistics.median(values), "unit": unit, "source": source,
            "quality_condition": "quality-passing runs only", "unavailable_reason": None,
            "variability": statistics.pstdev(values) if len(values) > 1 else 0.0}


def build_report(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a report without writing files or invoking external systems."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["benchmark"]].append(record)

    benchmarks = []
    for benchmark, runs in sorted(grouped.items()):
        passing = [run for run in runs if run.get("quality_pass") is True]
        performance = {name: metric([float(run[name]) for run in passing if name in run], unit, "sanitized execution record")
                       for name, unit in KNOWN_METRICS.items()}
        unavailable = ["input_tokens", "output_tokens", "cost", "private_reasoning"]
        benchmarks.append({
            "benchmark": benchmark,
            "runs": len(runs),
            "quality": {"passing_runs": len(passing), "result": "pass" if len(passing) == len(runs) else "review required"},
            "performance": performance,
            "process": {"source": "sanitized execution record", "unavailable_reason": "process events were not supplied"},
            "unavailable": {name: "not inferred from unavailable data" for name in unavailable},
        })
    return {"contract_version": "1.0", "read_only": True, "automatic_actions": False, "benchmarks": benchmarks}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a read-only evaluator report.")
    parser.add_argument("--records", required=True, type=Path, help="Sanitized JSON execution records to read")
    args = parser.parse_args()
    records = json.loads(args.records.read_text(encoding="utf-8"))
    print(json.dumps(build_report(records), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
