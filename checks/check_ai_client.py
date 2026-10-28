"""Lead check: the AI fallback chain, without any network or real key.  Run:  python checks/check_ai_client.py"""
import json
import os

for name in ("NEBIUS_API_KEY", "NEBIUS_MODEL", "OPENROUTER_API_KEY", "OPENROUTER_MODEL", "GROQ_API_KEY",
             "GROQ_MODEL", "GOOGLE_API_KEY", "GOOGLE_MODEL"):
    os.environ[name] = ""  # start with no keys, whatever is in .env

from common import PASS, load_findings, main
from vulnpilot import ai_client
from vulnpilot.models import RiskResult

GOOD = ('Here you go: {"summary": "S", "confirmed": [{"claim": "real fact", "evidence_line": "%s"}, '
        '{"claim": "invented fact", "evidence_line": "this line does not exist in the log at all"}], '
        '"hypotheses": ["h"], "actions": ["a"]}')


def check():
    findings = load_findings()
    real_line = findings[0].evidence_lines[0]
    risk = RiskResult("high", 60, ["r"])
    calls = []
    original_ask = ai_client._ask

    def run(behaviour):
        ai_client.clear_cache()
        calls.clear()

        def fake_ask(provider, model, system_prompt, user_prompt, timeout):
            calls.append(f"{provider['name']}:{model}")
            return behaviour(provider, model)
        ai_client._ask = fake_ask
        return ai_client.investigate(findings, risk, "system", "user")

    try:
        # 1) no key -> offline sample, no call at all
        result = run(lambda p, m: GOOD % real_line)
        assert result.source == ai_client.OFFLINE and calls == [], "With no keys the answer must be the OFFLINE SAMPLE"

        # 2) keys for OpenRouter and Groq; OpenRouter always fails -> Groq answers
        os.environ["OPENROUTER_API_KEY"] = "x"
        os.environ["GROQ_API_KEY"] = "y"

        def openrouter_down(provider, model):
            if provider["name"] == "OpenRouter":
                raise RuntimeError("rate limit")
            return GOOD % real_line
        result = run(openrouter_down)
        assert result.source.endswith("via Groq"), f"Groq should have answered, got {result.source!r}"
        assert calls[:3] == ["OpenRouter:" + m for m in ai_client.OPENROUTER_MODELS], f"All OpenRouter models must be tried first: {calls}"
        assert len(result.notes) == 3, f"3 failed attempts should be noted, got {result.notes}"

        # 3) grounding: the real quote stays confirmed, the invented one moves to hypotheses
        assert len(result.confirmed) == 1 and real_line in result.confirmed[0], f"Only the real quote may be confirmed: {result.confirmed}"
        assert any("invented fact" in h and "unverified" in h for h in result.hypotheses), "The invented claim must become a hypothesis"

        # 4) broken answers (not JSON, empty summary) are skipped like errors
        result = run(lambda p, m: "sorry, I cannot do that" if p["name"] == "OpenRouter" else GOOD % real_line)
        assert result.source.endswith("via Groq"), "A non-JSON answer must move on to the next service"
        result = run(lambda p, m: json.dumps({"summary": "", "confirmed": []}) if p["name"] == "OpenRouter" else GOOD % real_line)
        assert result.source.endswith("via Groq"), "An answer without a summary must move on to the next service"

        # 5) everything fails -> offline sample, not an exception
        def all_down(provider, model):
            raise TimeoutError("down")
        result = run(all_down)
        assert result.source == ai_client.OFFLINE and result.notes, "When every service fails the OFFLINE SAMPLE must be used"

        # 6) <think> text before the JSON is ignored, and the answer is cached (second call makes no request)
        result = run(lambda p, m: "<think>maybe {not json}</think>" + GOOD % real_line)
        assert result.source.startswith(ai_client.OPENROUTER_MODELS[0]), f"The first OpenRouter model should answer, got {result.source!r}"
        before = len(calls)
        ai_client.investigate(findings, risk, "system", "user")
        assert len(calls) == before, "The same prompt must be served from the cache"
    finally:
        ai_client._ask = original_ask
        ai_client.clear_cache()
        for name in ("OPENROUTER_API_KEY", "GROQ_API_KEY"):
            os.environ[name] = ""
    return PASS


if __name__ == "__main__":
    main("ai_client (lead)", check)
