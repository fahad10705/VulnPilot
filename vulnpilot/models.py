"""
models.py - the shared data shapes. Every module uses these, so they fit together.

Owner: lead (change only after telling the team)
Status: DONE

Example:
    Finding(title="Brute force then success", severity="high",
            description="...", evidence_lines=["Oct 24 10:12:47 ..."], mitre_id="T1110")
"""

from dataclasses import dataclass, field


@dataclass
class Finding:
    title: str                 # short name, e.g. "Brute force followed by success"
    severity: str              # "low", "medium", "high" or "critical"
    description: str           # one or two sentences
    evidence_lines: list = field(default_factory=list)  # exact raw log lines
    mitre_id: str = ""         # e.g. "T1110"


@dataclass
class IOC:
    kind: str                  # "ip" or "user"
    value: str                 # e.g. "192.0.2.10"
    count: int = 1             # how many log lines mention it


@dataclass
class TimelineEntry:
    time: str                  # e.g. "Oct 24 10:13:08"
    description: str           # e.g. "Login succeeded for admin from 192.0.2.10"
    line_number: int = 0       # line in the uploaded log (1 = first line)


@dataclass
class Investigation:
    risk_level: str            # "low", "medium", "high" or "critical"
    summary: str
    confirmed: list = field(default_factory=list)    # facts backed by log lines
    hypotheses: list = field(default_factory=list)   # guesses, clearly labelled
    actions: list = field(default_factory=list)      # recommended next steps
