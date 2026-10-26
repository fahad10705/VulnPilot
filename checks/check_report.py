"""Check for vulnpilot/report.py.  Run:  python checks/check_report.py"""
from common import DUMMY, PASS, load_findings, main
from vulnpilot.dummies import dummy_report_text
from vulnpilot.models import Indicator, Investigation, RiskResult, TimelineEntry
from vulnpilot.report import build_report


def check():
    findings = load_findings()
    indicators = [Indicator("ip", "192.0.2.10", 8), Indicator("user", "admin", 8)]
    timeline = [TimelineEntry("Oct 24 10:13:08", "Login succeeded for admin from 192.0.2.10", 13, "critical")]
    mitre = [{"finding_title": "Brute force", "id": "T1110.001", "name": "Brute Force: Password Guessing", "tactic": "Credential Access"}]
    risk = RiskResult("critical", 95, ["Brute force ended in a successful login (+50)"])
    ai = Investigation("FIXTURE SUMMARY TEXT", ["FIXTURE CONFIRMED ITEM"], ["FIXTURE HYPOTHESIS"], ["FIXTURE ACTION"], "fixture")
    text = build_report(findings, indicators, timeline, mitre, risk, ai)
    if text == dummy_report_text():
        return DUMMY
    assert isinstance(text, str), f"build_report must return a string, got {type(text).__name__}"
    assert text.startswith("# "), "The report must start with a markdown title line like '# VulnPilot Incident Report'"
    must_contain = ["critical", "Brute force ended in a successful login", "FIXTURE SUMMARY TEXT", "FIXTURE CONFIRMED ITEM",
                    "FIXTURE HYPOTHESIS", "FIXTURE ACTION", "192.0.2.10", "Login succeeded for admin", "T1110.001"]
    for finding in findings:
        must_contain.append(finding.title)
        must_contain += finding.evidence_lines
    for piece in must_contain:
        assert piece in text, f"The report is missing this text: {piece!r}"
    assert build_report(findings, indicators, timeline, mitre, risk, ai) == text, \
        "The same input must give exactly the same report every time (no dates or random values)"
    empty = build_report([], [], [], [], RiskResult("low", 0, []), Investigation("none", [], [], [], "x"))
    assert isinstance(empty, str) and empty.startswith("# "), "An empty analysis must still give a report that starts with '# '"
    return PASS


if __name__ == "__main__":
    main("report", check)
