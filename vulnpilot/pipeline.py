"""
pipeline.py - runs every module in order and never lets one broken file break the app.

WHO OWNS THIS: lead only. Beginners never edit this file.

How it works: each beginner function is called inside try/except.
  - If it crashes, we show a warning and use the placeholder answer instead (status "error").
  - If it still returns the placeholder, the status is "dummy" (not written yet).
  - Otherwise the status is "real".
The statuses are shown as a small table in the app sidebar. It doubles as our progress tracker.

Order: parse -> 3 detectors -> indicators -> MITRE -> timeline -> risk -> prompts -> AI -> report -> hash.
"""

import importlib
from dataclasses import dataclass, field

from vulnpilot import ai_client, dummies
from vulnpilot.models import Finding, Indicator, Investigation, LogEvent, RiskResult, TimelineEntry


@dataclass
class AnalysisResult:
    events: list = field(default_factory=list)
    findings: list = field(default_factory=list)
    indicators: list = field(default_factory=list)
    mitre: list = field(default_factory=list)
    timeline: list = field(default_factory=list)
    risk: RiskResult = field(default_factory=RiskResult)
    investigation: Investigation = field(default_factory=Investigation)
    report_text: str = ""
    evidence_lines: list = field(default_factory=list)
    report_hash: str = ""
    statuses: list = field(default_factory=list)   # list of {"module": ..., "status": ..., "note": ...}
    warnings: list = field(default_factory=list)   # plain sentences for the sidebar


def _looks_right(value, kind):
    """Cheap shape check so a wrong return type is caught and replaced by the placeholder."""
    if kind == "events":
        return isinstance(value, list) and all(isinstance(item, LogEvent) for item in value)
    if kind == "findings":
        return isinstance(value, list) and all(isinstance(item, Finding) for item in value)
    if kind == "indicators":
        return isinstance(value, list) and all(isinstance(item, Indicator) for item in value)
    if kind == "mitre":
        return isinstance(value, list) and all(isinstance(item, dict) for item in value)
    if kind == "timeline":
        return isinstance(value, list) and all(isinstance(item, TimelineEntry) for item in value)
    if kind == "risk":
        return isinstance(value, RiskResult)
    if kind == "text":
        return isinstance(value, str) and value != ""
    if kind == "prompts":
        return (isinstance(value, tuple) and len(value) == 2
                and all(isinstance(item, str) and item != "" for item in value))
    return True


def _call(result, module_name, function_name, args, placeholder, kind):
    """Run one beginner function safely. Returns (value, used_placeholder)."""
    try:
        module = importlib.import_module("vulnpilot." + module_name)
        module = importlib.reload(module)  # so edits made while the app is open are picked up
        value = getattr(module, function_name)(*args)
    except Exception as error:
        message = f"{module_name}.{function_name} crashed: {type(error).__name__}: {error}"
        result.warnings.append(message)
        result.statuses.append({"module": module_name, "status": "error", "note": str(error)[:80]})
        return placeholder, True
    if not _looks_right(value, kind):
        result.warnings.append(f"{module_name}.{function_name} returned the wrong kind of value, using the placeholder.")
        result.statuses.append({"module": module_name, "status": "error", "note": "wrong return type"})
        return placeholder, True
    if value == placeholder:
        result.statuses.append({"module": module_name, "status": "dummy", "note": "not written yet"})
        return value, True
    result.statuses.append({"module": module_name, "status": "real", "note": ""})
    return value, False


def _fallback_hash(report_text, evidence_lines):
    """Plain SHA-256 used only if hashing.py is dummy or broken, so Verify and the tamper test still work."""
    import hashlib
    combined = report_text.strip() + "\n---EVIDENCE---\n" + "\n".join(sorted(evidence_lines))
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def compute_hash(report_text, evidence_lines):
    """Hash with the team's hashing.py if it works, otherwise with the built-in fallback. Returns (hash, status)."""
    try:
        module = importlib.reload(importlib.import_module("vulnpilot.hashing"))
        value = module.make_hash(report_text, evidence_lines)
    except Exception as error:
        return _fallback_hash(report_text, evidence_lines), f"error: {error}"
    if value == dummies.dummy_hash() or not isinstance(value, str) or len(value) != 64:
        return _fallback_hash(report_text, evidence_lines), "dummy"
    return value, "real"


def _basic_prompts(findings, risk):
    """Built-in prompts, used only while prompts.py is not finished, so the AI still sees the real findings."""
    user_lines = [f"Overall risk: {risk.level} (score {risk.score})"]
    for reason in risk.reasons:
        user_lines.append(f"Reason: {reason}")
    number = 0
    for finding in findings:
        number = number + 1
        user_lines += ["", f"Finding {number}: {finding.title} (severity {finding.severity})", finding.description,
                       "Evidence lines:"] + list(finding.evidence_lines)
    return dummies.dummy_prompts()[0], "\n".join(user_lines) + "\n"


def _unique_evidence(findings):
    """Every evidence line once, in the order first seen."""
    lines = []
    for finding in findings:
        for line in finding.evidence_lines:
            if line not in lines:
                lines.append(line)
    return lines


def _check_helpers(result):
    """chain_helpers.py is used by the blockchain step: test it once with a sample hash and report its status."""
    sample = "ab" * 32
    try:
        module = importlib.reload(importlib.import_module("vulnpilot.chain_helpers"))
        as_bytes = module.hex_to_bytes32(sample)
        link = module.explorer_tx_link("0x" + sample)
    except Exception as error:
        result.statuses.append({"module": "chain_helpers", "status": "error", "note": str(error)[:80]})
        result.warnings.append(f"chain_helpers crashed: {error}")
        return
    if as_bytes == dummies.dummy_hex_to_bytes32() or link == dummies.dummy_explorer_link():
        result.statuses.append({"module": "chain_helpers", "status": "dummy", "note": "not written yet"})
    else:
        result.statuses.append({"module": "chain_helpers", "status": "real", "note": ""})


def run_analysis(log_text):
    """Run the whole analysis on the text of a log file and return an AnalysisResult."""
    result = AnalysisResult()

    events, _ = _call(result, "parser", "parse_log", (log_text,), dummies.dummy_events(), "events")
    result.events = events

    brute, _ = _call(result, "detect_bruteforce", "detect_bruteforce", (events,), dummies.dummy_bruteforce(), "findings")
    spray, _ = _call(result, "detect_password_spray", "detect_password_spray", (events,), dummies.dummy_password_spray(), "findings")
    invalid, _ = _call(result, "detect_invalid_users", "detect_invalid_users", (events,), dummies.dummy_invalid_users(), "findings")
    result.findings = brute + spray + invalid

    result.indicators, _ = _call(result, "ioc", "extract_indicators", (events, result.findings), dummies.dummy_indicators(), "indicators")
    result.mitre, _ = _call(result, "mitre", "map_to_mitre", (result.findings,), dummies.dummy_mitre(), "mitre")
    result.timeline, _ = _call(result, "timeline", "build_timeline", (events, result.findings), dummies.dummy_timeline(), "timeline")
    result.risk, _ = _call(result, "risk", "score_risk", (result.findings,), dummies.dummy_risk(), "risk")

    prompts, prompts_is_placeholder = _call(result, "prompts", "build_prompts", (result.findings, result.risk),
                                            dummies.dummy_prompts(), "prompts")
    if prompts_is_placeholder:
        prompts = _basic_prompts(result.findings, result.risk)  # the AI still gets the real findings

    # The AI step is the lead's. It never raises: without a key or on any error it returns an OFFLINE SAMPLE.
    result.investigation = ai_client.investigate(result.findings, result.risk, prompts[0], prompts[1])
    if result.investigation.source.startswith("OFFLINE"):
        result.statuses.append({"module": "ai_client", "status": "offline", "note": "sample text, no AI call"})
        result.warnings.append("AI is in offline mode: the investigation text is a sample, not written by an AI model.")
    else:
        note = result.investigation.source
        if result.investigation.notes:
            note += f" (after {len(result.investigation.notes)} failed attempt(s))"
        result.statuses.append({"module": "ai_client", "status": "real", "note": note})

    result.report_text, _ = _call(result, "report", "build_report",
                                  (result.findings, result.indicators, result.timeline, result.mitre,
                                   result.risk, result.investigation),
                                  dummies.dummy_report_text(), "text")

    result.evidence_lines = _unique_evidence(result.findings)
    result.report_hash, hash_status = compute_hash(result.report_text, result.evidence_lines)
    result.statuses.append({"module": "hashing", "status": hash_status.split(":")[0],
                            "note": "using the built-in hash" if hash_status != "real" else ""})
    if hash_status != "real":
        result.warnings.append("hashing.py is not finished, so the built-in SHA-256 is used.")

    _check_helpers(result)
    return result
