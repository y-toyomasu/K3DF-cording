"""Read-only operational evaluator. It reads sanitized JSON and prints JSON."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

AXES = ("change_surface", "uncertainty", "integration", "verification", "safety_risk", "coordination")
BANDS = ((3, "Routine"), (7, "Low"), (11, "Medium"), (15, "High"), (18, "Very High"))
CONFIDENCE = {"low", "medium", "high"}
DECISIONS = {"Retain", "Change Candidate", "More Data Required"}
PROHIBITED_FIELDS = {"task_body", "prompt", "command", "error", "host_path", "secret", "credential", "token", "flag", "authentication", "execution_secret", "private_reasoning"}
REQUIRED_SECTIONS = {"comparison_class", "configuration", "predicted_difficulty", "realized_difficulty", "quality", "performance", "process_waiting", "execution_friction", "unavailable_reason"}

class ValidationError(ValueError):
    """Sanitized validation error that never includes raw values or paths."""

def band(total: int) -> str:
    for upper, name in BANDS:
        if total <= upper:
            return name
    raise ValidationError("difficulty total is outside rubric range")

def _reject_prohibited(value: Any) -> None:
    if isinstance(value, dict):
        if {str(key).lower() for key in value} & PROHIBITED_FIELDS:
            raise ValidationError("record contains a prohibited field")
        for child in value.values(): _reject_prohibited(child)
    elif isinstance(value, list):
        for child in value: _reject_prohibited(child)
    elif isinstance(value, str):
        drive_path = len(value) >= 3 and value[0].isalpha() and value[1] == ":" and value[2] in (chr(92), "/")
        user_root = value.startswith("/" + "Users" + "/") or value.startswith("/" + "home" + "/")
        secret_shape = "PRIVATE KEY-----" in value or re.search(r"://[^/\s:@]+:[^/\s@]+@", value)
        if drive_path or user_root or secret_shape:
            raise ValidationError("record contains prohibited content")

def difficulty(section: dict[str, Any]) -> dict[str, Any]:
    if section.get("rubric_version") != "1.0": raise ValidationError("rubric version mismatch")
    if section.get("confidence") not in CONFIDENCE: raise ValidationError("difficulty confidence is invalid")
    axes = {axis: section.get("axes", {}).get(axis) for axis in AXES}
    if any(type(value) is not int or not 0 <= value <= 3 for value in axes.values()): raise ValidationError("rubric axis is invalid")
    total = sum(axes.values()); computed_band = band(total)
    supplied_total, supplied_band = section.get("total"), section.get("band")
    warning = (supplied_total is not None and supplied_total != total) or (supplied_band is not None and supplied_band != computed_band)
    return {"rubric_version":"1.0", "axes":axes, "total":total, "band":computed_band, "confidence":section["confidence"], "calibration_warning":warning}

def _configuration(config: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    result, complete = {}, True
    for name in ("recommended", "po_selected", "actual"):
        item = config.get(name, {})
        unavailable = item.get("unavailable_reason")
        valid = bool(item.get("model") and item.get("reasoning") and item.get("source"))
        if not valid and not unavailable: raise ValidationError("configuration source is incomplete")
        complete &= valid
        result[name] = {"model":item.get("model"), "reasoning":item.get("reasoning"), "source":item.get("source"), "unavailable_reason":unavailable}
    return result, complete

def _validate(record: dict[str, Any]) -> dict[str, Any]:
    _reject_prohibited(record)
    if not REQUIRED_SECTIONS <= record.keys(): raise ValidationError("record is missing a required section")
    config, config_complete = _configuration(record["configuration"])
    predicted, realized = difficulty(record["predicted_difficulty"]), difficulty(record["realized_difficulty"])
    if not record["realized_difficulty"].get("structural_evidence"): raise ValidationError("realized difficulty evidence is unavailable")
    quality = record["quality"]
    required_quality = {"passed", "acceptance_criteria", "build_test", "rework", "governance_violations", "regression"}
    if not required_quality <= quality.keys(): raise ValidationError("quality record is incomplete")
    waiting = record["process_waiting"]
    required_waiting = {"active_seconds", "human_wait_seconds", "dependency_wait_seconds", "review_wait_seconds"}
    if not required_waiting <= waiting.keys(): raise ValidationError("waiting record is incomplete")
    friction = record["execution_friction"]
    if not {"tool_errors", "retries", "reverification", "post_report_rework"} <= friction.keys(): raise ValidationError("friction record is incomplete")
    metrics_complete = record["performance"].get("wall_time_seconds") is not None
    comparison = record["comparison_class"]
    if not {"role", "task_type", "difficulty_band", "risk", "agents_version"} <= comparison.keys(): raise ValidationError("comparison class is incomplete")
    return {"comparison_class":comparison, "configuration":config, "configuration_complete":config_complete, "predicted":predicted, "realized":realized,
            "prediction_error":realized["total"]-predicted["total"], "quality":quality, "performance":record["performance"],
            "process_waiting":waiting, "execution_friction":friction, "unavailable_reason":record["unavailable_reason"], "metrics_complete":metrics_complete}

def evaluate(records: list[dict[str, Any]]) -> dict[str, Any]:
    rendered, eligible = [], []
    for record in records:
        try:
            item = _validate(record); rendered.append(item)
            if item["configuration_complete"] and item["quality"]["passed"] and not item["quality"]["regression"] and item["metrics_complete"] and not item["predicted"]["calibration_warning"] and not item["realized"]["calibration_warning"]: eligible.append(item)
        except ValidationError as exc:
            rendered.append({"status":"unavailable", "unavailable_reason":str(exc)})
    classes={json.dumps(item["comparison_class"],sort_keys=True) for item in eligible}
    configs={json.dumps(item["configuration"],sort_keys=True) for item in eligible}
    comparable=len(eligible)>=3 and len(classes)==1 and len(configs)==1
    decision="Retain" if comparable else "More Data Required"
    reason="comparable quality-passing samples satisfy the minimum" if comparable else "comparison requirements are not satisfied"
    recommendation={"decision":decision,"comparison_class":eligible[0]["comparison_class"] if len(classes)==1 and eligible else None,"sample_count":len(eligible),
                    "quality_condition":"passed, no regression, complete validation","configuration":eligible[0]["configuration"] if len(configs)==1 and eligible else None,
                    "difficulty_range":[min((x["realized"]["total"] for x in eligible),default=None),max((x["realized"]["total"] for x in eligible),default=None)],
                    "metrics":["wall_time_seconds"],"reason":reason,"confidence":"low","constraints":"observational only; no causal claim, threshold, or automatic change"}
    assert recommendation["decision"] in DECISIONS
    return {"schema_version":"1.0","read_only":True,"external_send":False,"git_operations":False,"agent_start":False,"automatic_actions":False,"records":rendered,"recommendation":recommendation}

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--records",required=True,type=Path); args=parser.parse_args()
    try: report=evaluate(json.loads(args.records.read_text(encoding="utf-8")))
    except Exception: report={"schema_version":"1.0","read_only":True,"error":"sanitized input could not be evaluated"}
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
