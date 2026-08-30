"""Read-only operational evaluator. It reads sanitized JSON and prints JSON."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

AXES = ("change_surface", "uncertainty", "integration", "verification", "safety_risk", "coordination")
BANDS = ((3, "Routine"), (7, "Low"), (11, "Medium"), (15, "High"), (18, "Very High"))
CONFIDENCE = {"low", "medium", "high"}
DECISIONS = {"Retain", "Change Candidate", "More Data Required"}
PROHIBITED_FIELDS = {"task_body", "prompt", "command", "error", "host_path", "secret", "credential", "token", "flag", "authentication", "execution_secret", "private_reasoning"}
REQUIRED_SECTIONS = {"comparison_class", "configuration", "predicted_difficulty", "realized_difficulty", "quality", "performance", "process_waiting", "execution_friction", "unavailable_reason"}
CONFIG_FIELDS = {"model", "reasoning", "source", "unavailable_reason"}
QUALITY_FIELDS = {"passed", "acceptance_criteria", "build_test", "rework", "governance_violations", "regression"}
PERFORMANCE_FIELDS = {"wall_time_seconds", "time_to_first_tool_seconds", "tool_calls", "input_tokens", "output_tokens", "cost"}
WAITING_FIELDS = {"active_seconds", "human_wait_seconds", "dependency_wait_seconds", "review_wait_seconds"}
FRICTION_FIELDS = {"tool_errors", "retries", "reverification", "post_report_rework"}
COMPARISON_FIELDS = {"role", "task_type", "difficulty_band", "risk", "agents_version"}
UNAVAILABLE_FIELDS = PERFORMANCE_FIELDS | WAITING_FIELDS | FRICTION_FIELDS | {"tokens", "waiting_seconds", "actual_model", "actual_reasoning"}

class ValidationError(ValueError):
    """Sanitized validation error that never includes raw values or paths."""

def _allowlist(section: str, value: Any, allowed: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) - allowed:
        raise ValidationError(section + " contains an unknown field")
    return value

def _text(value: Any, label: str, maximum: int = 160) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum:
        raise ValidationError(label + " is invalid")
    _reject_prohibited(value)
    return value

def _number(value: Any, label: str, integer: bool = False) -> int | float:
    valid_type = type(value) is int if integer else type(value) in (int, float)
    if not valid_type or not math.isfinite(value) or value < 0:
        raise ValidationError(label + " is invalid")
    return value

def _measurements(section: str, value: Any, fields: set[str], unavailable: dict[str, str], integer: bool = False) -> dict[str, Any]:
    source = _allowlist(section, value, fields)
    if set(source) != fields:
        raise ValidationError(section + " record is incomplete")
    result = {}
    for key in fields:
        measured, reason = source[key], unavailable.get(key)
        if measured is None:
            if reason is None:
                raise ValidationError(section + " unavailable reason is missing")
            result[key] = None
        else:
            if reason is not None:
                raise ValidationError(section + " unavailable reason conflicts with a measured value")
            result[key] = _number(measured, key, integer)
    return result

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
    allowed = {"rubric_version", "axes", "total", "band", "confidence", "structural_evidence"}
    _allowlist("difficulty", section, allowed)
    if section.get("rubric_version") != "1.0": raise ValidationError("rubric version mismatch")
    if section.get("confidence") not in CONFIDENCE: raise ValidationError("difficulty confidence is invalid")
    axes_input = _allowlist("difficulty axes", section.get("axes"), set(AXES))
    axes = {axis: axes_input.get(axis) for axis in AXES}
    if any(type(value) is not int or not 0 <= value <= 3 for value in axes.values()): raise ValidationError("rubric axis is invalid")
    total = sum(axes.values()); computed_band = band(total)
    supplied_total, supplied_band = section.get("total"), section.get("band")
    if supplied_total is not None and (type(supplied_total) is not int or not 0 <= supplied_total <= 18): raise ValidationError("difficulty total is invalid")
    if supplied_band is not None and supplied_band not in {name for _, name in BANDS}: raise ValidationError("difficulty band is invalid")
    warning = (supplied_total is not None and supplied_total != total) or (supplied_band is not None and supplied_band != computed_band)
    return {"rubric_version":"1.0", "axes":axes, "total":total, "band":computed_band, "confidence":section["confidence"], "calibration_warning":warning}

def _configuration(config: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    _allowlist("configuration", config, {"recommended", "po_selected", "actual"})
    result, complete = {}, True
    for name in ("recommended", "po_selected", "actual"):
        item = _allowlist("configuration source", config.get(name), CONFIG_FIELDS)
        unavailable = item.get("unavailable_reason")
        valid = all(isinstance(item.get(key), str) and 0 < len(item[key]) <= 80 for key in ("model", "reasoning", "source"))
        if unavailable is not None: _text(unavailable, "configuration unavailable reason")
        if not valid and unavailable is None: raise ValidationError("configuration source is incomplete")
        if valid:
            for key in ("model", "reasoning", "source"): _text(item[key], "configuration value", 80)
        complete &= valid
        result[name] = {"model":item.get("model"), "reasoning":item.get("reasoning"), "source":item.get("source"), "unavailable_reason":unavailable}
    return result, complete

def _validate(record: dict[str, Any]) -> dict[str, Any]:
    _reject_prohibited(record)
    if not isinstance(record, dict) or set(record) != REQUIRED_SECTIONS: raise ValidationError("record sections are invalid")
    config, config_complete = _configuration(record["configuration"])
    predicted, realized = difficulty(record["predicted_difficulty"]), difficulty(record["realized_difficulty"])
    evidence = record["realized_difficulty"].get("structural_evidence")
    if not isinstance(evidence, list) or not 1 <= len(evidence) <= 8: raise ValidationError("realized difficulty evidence is unavailable")
    evidence = [_text(item, "structural evidence") for item in evidence]
    quality_input = _allowlist("quality", record["quality"], QUALITY_FIELDS)
    if set(quality_input) != QUALITY_FIELDS or type(quality_input["passed"]) is not bool or type(quality_input["regression"]) is not bool: raise ValidationError("quality record is incomplete")
    quality = {"passed":quality_input["passed"], "acceptance_criteria":_text(quality_input["acceptance_criteria"], "acceptance status", 40), "build_test":_text(quality_input["build_test"], "build test status", 40), "rework":_number(quality_input["rework"], "rework", True), "governance_violations":_number(quality_input["governance_violations"], "governance violations", True), "regression":quality_input["regression"]}
    unavailable_input = _allowlist("unavailable reason", record["unavailable_reason"], UNAVAILABLE_FIELDS)
    unavailable = {key:_text(value, "unavailable reason") for key,value in unavailable_input.items()}
    performance_input = _allowlist("performance", record["performance"], PERFORMANCE_FIELDS)
    performance = {key:_number(value, key) for key,value in performance_input.items() if value is not None}
    waiting = _measurements("process waiting", record["process_waiting"], WAITING_FIELDS, unavailable)
    friction = _measurements("execution friction", record["execution_friction"], FRICTION_FIELDS, unavailable, True)
    comparison_input = _allowlist("comparison class", record["comparison_class"], COMPARISON_FIELDS)
    if set(comparison_input) != COMPARISON_FIELDS: raise ValidationError("comparison class is incomplete")
    comparison = {key:_text(comparison_input[key], key, 80) for key in COMPARISON_FIELDS}
    metrics_complete = performance.get("wall_time_seconds") is not None
    return {"comparison_class":comparison, "configuration":config, "configuration_complete":config_complete, "predicted":predicted, "realized":realized,
            "prediction_error":realized["total"]-predicted["total"], "quality":quality, "performance":performance,
            "process_waiting":waiting, "execution_friction":friction, "unavailable_reason":unavailable, "realized_evidence":evidence, "metrics_complete":metrics_complete}

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
