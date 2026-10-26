r"""
detect_password_spray.py - Find one IP address that tried many DIFFERENT usernames (a password spray).

WHO OWNS THIS: TODO
DIFFICULTY: medium
TIME ESTIMATE: 2 hours

WHAT GOES IN
    events: the list of LogEvent from parser.py.
    [LogEvent(line_number=6, time="Oct 24 10:12:47", user="admin", source_ip="192.0.2.10",
              result="failed", invalid_user=False,
              raw_line="Oct 24 10:12:47 web01 sshd[2190]: Failed password for admin from 192.0.2.10 port 40130 ssh2"),
     LogEvent(line_number=13, ..., result="success", ...), ...]   (see vulnpilot/models.py)

WHAT MUST COME OUT
    A list of Finding, one for every source IP whose FAILED logins used 5 or more different
    usernames. Empty list [] if none. For auth_attack.log there is exactly one:
    Finding(finding_type="password_spray", title="Password spray", severity="medium",
            description="198.51.100.7 tried 8 different usernames.",
            evidence_lines=[<the 8 failed raw lines from that IP>],
            source_ip="198.51.100.7", users=["alice", "bob", "carol", "deploy", ...])  (sorted)

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: nothing new (the imports already at the top are enough).
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. Make two dicts keyed by IP: users_by_ip (a set of usernames) and lines_by_ip (a list of raw lines).
    2. Loop over events. Only look at event.result == "failed".
    3. users_by_ip.setdefault(ip, set()).add(event.user)  -- a set keeps each name only once.
    4. lines_by_ip.setdefault(ip, []).append(event.raw_line)
    5. Then loop over users_by_ip.items(). If len(users) >= 5, make a Finding with sorted(users).
    6. Do NOT flag an IP that hammered ONE user (that is brute force, a different detector).

Your own check:  python checks/check_detect_password_spray.py
"""

from vulnpilot.dummies import dummy_password_spray
from vulnpilot.models import Finding


def detect_password_spray(events):
    """Return a list of Finding, one per IP that tried 5 or more different usernames."""
    result = dummy_password_spray()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# Job: find IPs that logged in successfully for 2 or more different users.
# users_by_ip = {}
# for event in events:
#     if event.result == "success":
#         users_by_ip.setdefault(event.source_ip, set()).add(event.user)   # a set drops repeats
# shared_ips = []
# for ip, users in users_by_ip.items():
#     if len(users) >= 2:
#         shared_ips.append(ip)
#
# DONE WHEN
#   python checks/check_detect_password_spray.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
