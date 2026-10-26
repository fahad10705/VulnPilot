"""
models.py - the shared data shapes. Every module uses these, so everything fits together.

WHO OWNS THIS: lead only. Beginners never edit this file.
Status: DONE

Each shape is a plain "dataclass": a box with named fields. Example of making one:
    event = LogEvent(line_number=13, time="Oct 24 10:13:08", user="admin",
                     source_ip="192.0.2.10", result="success", invalid_user=False,
                     raw_line="Oct 24 10:13:08 web01 sshd[2204]: Accepted password for admin ...")
    event.user      ->  "admin"
"""

from dataclasses import dataclass, field


# One parsed line of the log.
# Example: LogEvent(13, "Oct 24 10:13:08", "admin", "192.0.2.10", "success", False, "<the full line>")
@dataclass
class LogEvent:
    line_number: int = 0        # which line of the log file (the first line is 1)
    time: str = ""              # as written in the log, e.g. "Oct 24 10:13:08"
    user: str = ""              # username used, e.g. "admin"
    source_ip: str = ""         # where the attempt came from, e.g. "192.0.2.10"
    result: str = ""            # "failed" or "success"
    invalid_user: bool = False  # True if the log says "invalid user" (that account does not exist)
    raw_line: str = ""          # the exact original line, kept as evidence


# Something suspicious that a detector found, with the exact log lines as proof.
# Example: Finding("brute_force", "Brute force then login", "high", "7 failed logins ...",
#                  ["<line 6>", "<line 13>"], "192.0.2.10", ["admin"])
@dataclass
class Finding:
    finding_type: str = ""      # "brute_force", "password_spray" or "invalid_users"
    title: str = ""             # short name shown in the UI
    severity: str = "low"       # "low", "medium", "high" or "critical"
    description: str = ""       # one or two plain sentences
    evidence_lines: list = field(default_factory=list)  # exact raw log lines (list of str)
    source_ip: str = ""         # the attacking IP
    users: list = field(default_factory=list)           # usernames involved (list of str)


# An indicator of compromise (IOC): an IP, a username, a domain, a URL or a file hash.
# Example: Indicator("ip", "192.0.2.10", 8)
@dataclass
class Indicator:
    kind: str = ""              # "ip", "user", "domain", "url" or "hash"
    value: str = ""             # e.g. "192.0.2.10"
    count: int = 1              # how many evidence lines mention it


# One point on the attack timeline.
# Example: TimelineEntry("Oct 24 10:13:08", "Login succeeded for admin from 192.0.2.10", 13, "critical")
@dataclass
class TimelineEntry:
    time: str = ""              # e.g. "Oct 24 10:13:08"
    description: str = ""       # one plain sentence
    line_number: int = 0        # line in the log file
    severity: str = "info"      # "info", "warning" or "critical" (used for the chart colour)


# The risk score with the reasons behind it (explainable on purpose).
# Example: RiskResult("critical", 85, ["Brute force ended in a successful login (+50)"])
@dataclass
class RiskResult:
    level: str = "low"          # "low", "medium", "high" or "critical"
    score: int = 0              # 0 to 100
    reasons: list = field(default_factory=list)        # plain sentences (list of str)


# What the AI wrote. Lead-only (made by ai_client.py).
# Example: Investigation("Admin was brute forced ...", ["7 failed logins [line 6-12]"], ["May be a bot"], ["Reset password"], "Nebius")
@dataclass
class Investigation:
    summary: str = ""
    confirmed: list = field(default_factory=list)      # facts backed by a log line (list of str)
    hypotheses: list = field(default_factory=list)     # guesses, clearly labelled (list of str)
    actions: list = field(default_factory=list)        # recommended next steps (list of str)
    source: str = ""            # "Nebius Nemotron" or "OFFLINE SAMPLE"


# The finished report plus its fingerprint. Lead-only (made by pipeline.py).
# Example: Report("# Incident report ...", ["<line 6>", "<line 13>"], "8b6901c9dcbd...")
@dataclass
class Report:
    text: str = ""              # the markdown report
    evidence_lines: list = field(default_factory=list)  # every evidence line, no duplicates
    sha256: str = ""            # 64 character fingerprint of text + evidence
