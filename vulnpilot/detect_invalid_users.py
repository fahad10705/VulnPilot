r"""
detect_invalid_users.py - Find IPs that keep trying usernames that do not exist on the server (like test, guest, deploy).

WHO OWNS THIS: TODO
DIFFICULTY: easy
TIME ESTIMATE: 1 hour

WHAT GOES IN
    events: the list of LogEvent from parser.py. Events with event.invalid_user == True are the interesting ones.
    [LogEvent(line_number=6, time="Oct 24 10:12:47", user="admin", source_ip="192.0.2.10",
              result="failed", invalid_user=False,
              raw_line="Oct 24 10:12:47 web01 sshd[2190]: Failed password for admin from 192.0.2.10 port 40130 ssh2"),
     LogEvent(line_number=13, ..., result="success", ...), ...]   (see vulnpilot/models.py)

WHAT MUST COME OUT
    A list of Finding, one for every source IP with 3 or more failed logins where invalid_user
    is True. Empty list [] if none. For auth_attack.log there are two (in log order):
    198.51.100.7 (5 invalid usernames) and 203.0.113.99 (3), for example:
    Finding(finding_type="invalid_users", title="Attempts with non-existent usernames",
            severity="low", description="203.0.113.99 tried 3 usernames that do not exist.",
            evidence_lines=[<3 raw lines>], source_ip="203.0.113.99", users=["guest", "support", "test"])

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: nothing new (the imports already at the top are enough).
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. Make two dicts keyed by IP: one for the raw lines and one for the usernames.
    2. Loop over events. Only use events where event.invalid_user is True.
    3. Append event.raw_line to that IP's list and event.user to its username list.
    4. Loop over the dict. If an IP has 3 or more lines, make a Finding with sorted(users).
    5. Dicts keep the order things were first added, so your findings come out in log order.

Your own check:  python checks/check_detect_invalid_users.py
"""

from vulnpilot.dummies import dummy_invalid_users
from vulnpilot.models import Finding


def detect_invalid_users(events):
    """Return a list of Finding, one per IP with 3 or more attempts on non-existent usernames."""
    result = dummy_invalid_users()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Group the raw lines and the usernames by source IP. Dicts keep insertion
    # order, so the findings will come out in the order IPs first appeared in the log.
    lines_by_ip = {}
    users_by_ip = {}

    for event in events:
        # Only attempts on usernames that do not exist on the server matter here.
        if event.invalid_user:
            if event.source_ip not in lines_by_ip:
                lines_by_ip[event.source_ip] = []
                users_by_ip[event.source_ip] = []
            lines_by_ip[event.source_ip].append(event.raw_line)
            users_by_ip[event.source_ip].append(event.user)

    result = []
    for ip in lines_by_ip:
        # 3 or more attempts from one IP looks like guessing, not a typo.
        if len(lines_by_ip[ip]) >= 3:
            # sorted(set(...)) removes repeats, so each username is listed once.
            usernames = sorted(set(users_by_ip[ip]))
            finding = Finding(
                finding_type="invalid_users",
                title="Attempts with non-existent usernames",
                severity="low",
                description=ip + " tried " + str(len(usernames)) + " usernames that do not exist.",
                evidence_lines=lines_by_ip[ip],
                source_ip=ip,
                users=usernames,
            )
            result.append(finding)
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# Job: list the raw lines of every successful login.
# success_lines = []
# for event in events:
#     if event.result == "success":
#         success_lines.append(event.raw_line)
# Same idea as yours: loop, test a field with "if", collect into a list (or a dict of lists).
#
# DONE WHEN
#   python checks/check_detect_invalid_users.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
