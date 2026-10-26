"""Check for vulnpilot/prompts.py.  Run:  python checks/check_prompts.py"""
from common import DUMMY, PASS, load_findings, main
from vulnpilot.dummies import dummy_prompts
from vulnpilot.models import RiskResult
from vulnpilot.prompts import ANSWER_FORMAT, build_prompts


def check():
    findings = load_findings()
    risk = RiskResult("critical", 95, ["Brute force ended in a successful login (+50)"])
    answer = build_prompts(findings, risk)
    if answer == dummy_prompts():
        return DUMMY
    assert isinstance(answer, tuple) and len(answer) == 2, "build_prompts must return a pair: (system_prompt, user_prompt)"
    system_prompt, user_prompt = answer
    assert isinstance(system_prompt, str) and len(system_prompt) > 200, "system_prompt must be a text of at least 200 characters"
    lowered = system_prompt.lower()
    for word in ("confirmed", "hypothes", "json", "invent"):
        assert word in lowered, f"The system prompt must mention '{word}'"
    assert "evidence" in lowered, "The system prompt must tell the AI to use only the evidence"
    for key in ('"summary"', '"confirmed"', '"hypotheses"', '"actions"', '"evidence_line"'):
        assert key in system_prompt, f"The system prompt must include the answer format key {key} (use ANSWER_FORMAT)"
    assert isinstance(user_prompt, str), "user_prompt must be a string"
    assert "critical" in user_prompt, "The user prompt must include the risk level"
    for finding in findings:
        assert finding.title in user_prompt, f"The user prompt is missing the finding title {finding.title!r}"
        for line in finding.evidence_lines:
            assert line in user_prompt, f"The user prompt is missing an evidence line: {line!r}"
    empty = build_prompts([], RiskResult("low", 0, []))
    assert isinstance(empty[0], str) and isinstance(empty[1], str), "It must also work with no findings"
    return PASS


if __name__ == "__main__":
    main("prompts", check)
