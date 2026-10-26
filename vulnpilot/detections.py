"""
detections.py - rules that find suspicious patterns and keep the log lines as evidence.

Purpose: look at the parsed log and return a list of Finding objects.
Function:
    run_detections(events: pandas.DataFrame) -> list[Finding]
        events = the table from parser.parse_log
        returns a list of Finding (see models.py)

Rules to build: many failed logins then a success (same user + IP),
login from a new IP, sudo to root right after login.

Example:
    Finding(title="Brute force followed by successful login", severity="high",
            description="7 failed logins for admin from 192.0.2.10, then a success.",
            evidence_lines=["Oct 24 10:12:47 web01 sshd[2190]: Failed password ..."],
            mitre_id="T1110")

Owner: TODO assign
Status: STUB (returns one dummy finding)
"""

from vulnpilot.models import Finding


def run_detections(events):
    """Return a list of Finding. STUB: always returns one dummy finding."""
    return [
        Finding(
            title="Brute force followed by successful login",
            severity="high",
            description="Repeated failed logins for admin from 192.0.2.10, then a success.",
            evidence_lines=[
                "Oct 24 10:12:47 web01 sshd[2190]: Failed password for admin from 192.0.2.10 port 40130 ssh2",
                "Oct 24 10:13:08 web01 sshd[2204]: Accepted password for admin from 192.0.2.10 port 40186 ssh2",
            ],
            mitre_id="T1110",
        )
    ]
