"""
parser.py - turn raw log text into a pandas table.

Purpose: read an authentication log (sshd style) into rows, one per log line.
Function:
    parse_log(text: str) -> pandas.DataFrame
        text = the whole log file as one string
        returns columns: line_number, time, user, source_ip, result, raw_line
        result is "failed" or "success"

Example row:
    line_number=8, time="Oct 24 10:13:08", user="admin",
    source_ip="192.0.2.10", result="success",
    raw_line="Oct 24 10:13:08 web01 sshd[2204]: Accepted password for admin from 192.0.2.10 ..."

Owner: TODO assign
Status: STUB (returns dummy rows, ignores the input)
"""

import pandas as pd


def parse_log(text):
    """Parse log text into a DataFrame. STUB: returns dummy rows."""
    rows = [
        (4, "Oct 24 10:12:47", "admin", "192.0.2.10", "failed",
         "Oct 24 10:12:47 web01 sshd[2190]: Failed password for admin from 192.0.2.10 port 40130 ssh2"),
        (5, "Oct 24 10:12:50", "admin", "192.0.2.10", "failed",
         "Oct 24 10:12:50 web01 sshd[2192]: Failed password for admin from 192.0.2.10 port 40138 ssh2"),
        (11, "Oct 24 10:13:08", "admin", "192.0.2.10", "success",
         "Oct 24 10:13:08 web01 sshd[2204]: Accepted password for admin from 192.0.2.10 port 40186 ssh2"),
        (14, "Oct 24 10:21:20", "alice", "198.51.100.23", "success",
         "Oct 24 10:21:20 web01 sshd[2262]: Accepted password for alice from 198.51.100.23 port 51904 ssh2"),
    ]
    columns = ["line_number", "time", "user", "source_ip", "result", "raw_line"]
    return pd.DataFrame(rows, columns=columns)
