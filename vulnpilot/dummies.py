"""
dummies.py - the placeholder answers that every beginner module returns until it is written.

WHO OWNS THIS: lead only. Beginners never edit this file.

Why it exists: the app must run end to end from the first minute. Each beginner function starts by
returning one of these placeholders. The pipeline compares your function's answer with the
placeholder: if they are equal, your module is shown as "dummy" (not done yet).
The placeholders use real lines from sample_logs/auth_attack.log so the demo looks believable.
"""

from vulnpilot.models import Finding, Indicator, LogEvent, RiskResult, TimelineEntry

LINE_FAIL = "Oct 24 10:12:47 web01 sshd[2190]: Failed password for admin from 192.0.2.10 port 40130 ssh2"
LINE_OK = "Oct 24 10:13:08 web01 sshd[2204]: Accepted password for admin from 192.0.2.10 port 40186 ssh2"


def dummy_events():
    return [
        LogEvent(6, "Oct 24 10:12:47", "admin", "192.0.2.10", "failed", False, LINE_FAIL),
        LogEvent(13, "Oct 24 10:13:08", "admin", "192.0.2.10", "success", False, LINE_OK),
    ]


def dummy_bruteforce():
    return [Finding("brute_force", "[DUMMY] Brute force then successful login", "high",
                    "Placeholder finding. The real detector is not written yet.",
                    [LINE_FAIL, LINE_OK], "192.0.2.10", ["admin"])]


def dummy_password_spray():
    return [Finding("password_spray", "[DUMMY] Password spray", "medium",
                    "Placeholder finding. The real detector is not written yet.",
                    [LINE_FAIL], "192.0.2.10", ["admin"])]


def dummy_invalid_users():
    return [Finding("invalid_users", "[DUMMY] Attempts with non-existent usernames", "low",
                    "Placeholder finding. The real detector is not written yet.",
                    [LINE_FAIL], "192.0.2.10", ["admin"])]


def dummy_indicators():
    return [Indicator("ip", "192.0.2.10", 2), Indicator("user", "admin", 2)]


def dummy_mitre():
    return [{"finding_title": "[DUMMY] placeholder", "id": "T1110", "name": "Brute Force",
             "tactic": "Credential Access"}]


def dummy_timeline():
    return [TimelineEntry("Oct 24 10:12:47", "[DUMMY] First failed login for admin", 6, "warning"),
            TimelineEntry("Oct 24 10:13:08", "[DUMMY] Login succeeded for admin", 13, "critical")]


def dummy_risk():
    return RiskResult("medium", 50, ["[DUMMY] Risk scoring is not written yet."])


def dummy_report_text():
    return ("# Incident report [DUMMY]\n\nThe report builder is not written yet. "
            "This placeholder does not use your findings.\n")


def dummy_hash():
    return "dummy" + "0" * 59   # 64 characters, but obviously not a real hash


def dummy_prompts():
    """A decent starting prompt, so the AI step works even before prompts.py is written."""
    system_prompt = (
        "You are a careful security analyst. You are given findings from an SSH authentication log, "
        "each with the exact evidence log lines. Rules: (1) Use ONLY the evidence lines you are given. "
        "Never invent log lines, IP addresses, users or times. (2) Put facts that a log line proves under "
        "CONFIRMED and quote the exact line. (3) Put guesses under HYPOTHESES and say they are guesses. "
        "(4) Recommend practical actions. Answer with ONE JSON object only: "
        '{"summary": str, "confirmed": [{"claim": str, "evidence_line": str}], '
        '"hypotheses": [str], "actions": [str]}'
    )
    user_prompt = "Findings and evidence:\n(no findings were given)\n"
    return system_prompt, user_prompt


def dummy_hex_to_bytes32():
    return b"\x00" * 32


def dummy_explorer_link():
    return "https://example.invalid/dummy"
