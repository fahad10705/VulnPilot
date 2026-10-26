"""Check for vulnpilot/risk.py.  Run:  python checks/check_risk.py"""
from common import DUMMY, PASS, load_findings, main
from vulnpilot.dummies import dummy_risk
from vulnpilot.models import RiskResult
from vulnpilot.risk import score_risk


def check():
    findings = load_findings()
    risk = score_risk(findings)
    if risk == dummy_risk():
        return DUMMY
    assert isinstance(risk, RiskResult), f"score_risk must return a RiskResult, got {type(risk).__name__}"
    assert risk.level in ("high", "critical"), f"An attack with a successful brute force should be high or critical, got {risk.level!r}"
    assert isinstance(risk.score, int) and 0 <= risk.score <= 100, f"score must be a whole number from 0 to 100, got {risk.score!r}"
    assert isinstance(risk.reasons, list) and len(risk.reasons) >= 1 and all(isinstance(r, str) for r in risk.reasons), \
        "reasons must be a list with at least one sentence (text)"
    nothing = score_risk([])
    assert nothing.level == "low" and nothing.score == 0, f"No findings should be level 'low' and score 0, got {nothing.level!r}/{nothing.score}"
    assert isinstance(nothing.reasons, list), "reasons must be a list even when empty"
    assert score_risk(findings[:1]).score <= risk.score, "More findings must never give a LOWER score"
    return PASS


if __name__ == "__main__":
    main("risk", check)
