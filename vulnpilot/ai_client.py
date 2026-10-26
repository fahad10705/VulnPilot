"""
ai_client.py - asks NVIDIA Nemotron (through Nebius Token Factory) to write the investigation.

WHO OWNS THIS: lead only. Beginners never edit this file and never need an API key.

investigate(findings, risk, system_prompt, user_prompt) -> Investigation

- Uses the openai Python SDK pointed at Nebius (base url, key and model come from config.py / .env).
- Never raises. If the key or model is missing, or the call fails, it returns a clearly labelled
  OFFLINE SAMPLE built from the findings, so demos and everyone's local run never break.
- Grounding check: every CONFIRMED claim must quote an evidence line that really exists.
  A claim whose quote is not in the evidence is moved to HYPOTHESES (the AI cannot invent evidence).
"""

import json

from vulnpilot.config import ai_is_configured, get_setting
from vulnpilot.models import Investigation

OFFLINE = "OFFLINE SAMPLE (not written by the AI)"
ONLINE = "Nebius Nemotron"


def investigate(findings, risk, system_prompt, user_prompt):
    """Return an Investigation. Falls back to the offline sample on any problem."""
    if not ai_is_configured():
        return offline_investigation(findings, risk, "NEBIUS_API_KEY or NEBIUS_MODEL is not set")
    try:
        from openai import OpenAI
        client = OpenAI(base_url=get_setting("NEBIUS_BASE_URL"), api_key=get_setting("NEBIUS_API_KEY"), timeout=60)
        response = client.chat.completions.create(
            model=get_setting("NEBIUS_MODEL"),
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            temperature=0.2,
        )
        answer_text = response.choices[0].message.content
        return parse_answer(answer_text, findings)
    except Exception as error:
        return offline_investigation(findings, risk, f"the AI call failed ({type(error).__name__})")


def parse_answer(answer_text, findings):
    """Turn the model's JSON text into an Investigation, checking every quote against the evidence."""
    start = answer_text.find("{")
    end = answer_text.rfind("}")
    data = json.loads(answer_text[start:end + 1])

    known_lines = []
    for finding in findings:
        known_lines += finding.evidence_lines

    confirmed = []
    hypotheses = list(data.get("hypotheses", []))
    for item in data.get("confirmed", []):
        claim = item.get("claim", "") if isinstance(item, dict) else str(item)
        quote = item.get("evidence_line", "").strip() if isinstance(item, dict) else ""
        if quote and quote in known_lines:
            confirmed.append(f"{claim}  [evidence: {quote}]")
        else:
            hypotheses.append(f"{claim} (unverified: the quoted log line was not found in the evidence)")
    return Investigation(
        summary=str(data.get("summary", "")),
        confirmed=confirmed,
        hypotheses=[str(item) for item in hypotheses],
        actions=[str(item) for item in data.get("actions", [])],
        source=ONLINE,
    )


def offline_investigation(findings, risk, reason):
    """A clearly labelled sample built straight from the findings (no AI involved)."""
    confirmed = []
    actions = []
    for finding in findings:
        if finding.evidence_lines:
            confirmed.append(f"{finding.title}: {finding.description}  [evidence: {finding.evidence_lines[0]}]")
    if findings:
        actions = ["Reset the passwords of the accounts involved.",
                   "Block the attacking IP addresses at the firewall.",
                   "Review what the logged-in account did after the successful login."]
    else:
        actions = ["No action needed. Keep monitoring."]
    summary = (f"OFFLINE SAMPLE ({reason}). Overall risk is {risk.level}. "
               f"{len(findings)} finding(s) were detected by the rules.")
    return Investigation(summary=summary, confirmed=confirmed,
                         hypotheses=["Offline mode: no AI hypotheses were generated."],
                         actions=actions, source=OFFLINE)
