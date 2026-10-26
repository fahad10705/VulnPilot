r"""
ioc.py - List the indicators of compromise (attacker IPs and usernames) that appear in the findings.

WHO OWNS THIS: TODO
DIFFICULTY: easy
TIME ESTIMATE: 1-2 hours

WHAT GOES IN
    events: list of LogEvent (you may not need it).
    findings: list of Finding. Use finding.evidence_lines and finding.users.
    Example finding evidence line: "Oct 24 10:13:08 web01 sshd[2204]: Accepted password for admin from 192.0.2.10 port 40186 ssh2"

WHAT MUST COME OUT
    A list of Indicator (kind, value, count): one "ip" Indicator per different IP and one "user"
    Indicator per different username found in the findings. count = how many different evidence
    lines mention it. Empty list [] if there are no findings.
    For auth_attack.log it includes: Indicator("ip", "192.0.2.10", 8), Indicator("ip", "198.51.100.7", 8),
    Indicator("ip", "203.0.113.99", 3), Indicator("user", "admin", ...).
    Do not list IPs that are only in the normal log lines (like 203.0.113.45).

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: re.
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. Collect every evidence line from every finding into one list, without duplicates (check with: if line not in lines).
    2. An IP looks like this in regex:  r"\b\d{1,3}(?:\.\d{1,3}){3}\b"   Use re.findall(pattern, line).
    3. Count with a dict: counts[ip] = counts.get(ip, 0) + 1  (once per line).
    4. Usernames: take finding.users from each finding (no regex needed).
    5. Make Indicator("ip", ip, count) and Indicator("user", name, count) and put them in the result list.
    6. EXTRA (spare unit for fast finishers): also find domains, URLs or 64-character hashes with more regex patterns.

Your own check:  python checks/check_ioc.py
"""

import re

from vulnpilot.dummies import dummy_indicators
from vulnpilot.models import Indicator


def extract_indicators(events, findings):
    """Return a list of Indicator for the IPs and usernames in the findings."""
    result = dummy_indicators()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# import re
# text = "from 192.0.2.10 and then 192.0.2.10 again, also 198.51.100.7"
# ips = re.findall(r"\d+\.\d+\.\d+\.\d+", text)   # ["192.0.2.10", "192.0.2.10", "198.51.100.7"]
# unique_ips = set(ips)                                # {"192.0.2.10", "198.51.100.7"}  (a set drops repeats)
# Your job is the same, but over every evidence line of every finding.
#
# DONE WHEN
#   python checks/check_ioc.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
