"""
ai_investigator.py - ask NVIDIA Nemotron (via Nebius Token Factory) to write the investigation.

Purpose: send the findings + evidence lines to the model and get a structured report back.
Function:
    investigate(findings: list[Finding]) -> Investigation
        returns an Investigation (see models.py): risk_level, summary,
        confirmed (backed by log lines), hypotheses (clearly guesses), actions.

Real version rules:
  - Use the openai SDK with base_url=get_setting("NEBIUS_BASE_URL"),
    api_key=get_setting("NEBIUS_API_KEY"), model=get_setting("NEBIUS_MODEL").
  - Tell the model to use ONLY the evidence lines given, and to quote them.
  - If no API key is set, fall back to the dummy answer so the app still runs.

Example:
    Investigation(risk_level="high", summary="...", confirmed=["7 failed logins ..."],
                  hypotheses=["Attacker may have used a password list"], actions=["Reset admin password"])

Owner: TODO assign
Status: STUB (returns dummy investigation, no API call yet)
"""

from vulnpilot.models import Investigation


def investigate(findings):
    """Return an Investigation. STUB: dummy data, no network call."""
    return Investigation(
        risk_level="high",
        summary="admin was brute-forced from 192.0.2.10 and then logged in and ran sudo.",
        confirmed=[
            "7 failed logins for admin from 192.0.2.10 (log lines 4-10).",
            "Successful login for admin from 192.0.2.10 at 10:13:08 (line 11).",
        ],
        hypotheses=["The attacker probably used a password list (guess, not proven by the log)."],
        actions=["Reset the admin password.", "Block 192.0.2.10.", "Review what admin did as root."],
    )
