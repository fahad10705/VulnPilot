r"""
detect_bruteforce.py - Find a user who failed to log in many times from one IP and then got in (brute force that worked).

WHO OWNS THIS: TODO
DIFFICULTY: medium
TIME ESTIMATE: 2 hours

WHAT GOES IN
    events: the list of LogEvent from parser.py, in log order.
    [LogEvent(line_number=6, time="Oct 24 10:12:47", user="admin", source_ip="192.0.2.10",
              result="failed", invalid_user=False,
              raw_line="Oct 24 10:12:47 web01 sshd[2190]: Failed password for admin from 192.0.2.10 port 40130 ssh2"),
     LogEvent(line_number=13, ..., result="success", ...), ...]   (see vulnpilot/models.py)

WHAT MUST COME OUT
    A list of Finding, one for every (IP, user) pair with 5 or more FAILED logins that is later
    followed by a SUCCESS from the same IP for the same user. Empty list [] if none.
    For auth_attack.log there is exactly one:
    Finding(finding_type="brute_force", title="Brute force followed by successful login",
            severity="high", description="7 failed logins for admin from 192.0.2.10, then a success.",
            evidence_lines=[<the 7 failed raw lines>, <the success raw line>],
            source_ip="192.0.2.10", users=["admin"])

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: nothing new (the imports already at the top are enough).
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. Make a dict called failed_by_pair. Its key is a pair (event.source_ip, event.user).
       Its value is a list of the failed events so far.
    2. Loop over events in order. If event.result == "failed": add the event to that pair's list.
       Tip: failed_by_pair.setdefault(pair, []).append(event)
    3. If event.result == "success" and that pair already has 5 or more failures: you found one.
    4. evidence_lines = the raw_line of every failed event, then the raw_line of the success.
    5. Create Finding("brute_force", title, "high", description, evidence_lines, ip, [user]) and add it to result.
    6. After a finding, remove the pair from the dict so it is not reported twice.

Your own check:  python checks/check_detect_bruteforce.py
"""

from vulnpilot.dummies import dummy_bruteforce
from vulnpilot.models import Finding


def detect_bruteforce(events):
    """Return a list of Finding for brute force attacks that ended in a successful login."""
    result = dummy_bruteforce()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# Job: find users with 3 or more failed logins (a simpler version of your task).
# counts = {}
# for event in events:
#     if event.result == "failed":
#         counts[event.user] = counts.get(event.user, 0) + 1   # .get(key, 0) = "0 if not seen yet"
# busy_users = []
# for user, number in counts.items():
#     if number >= 3:
#         busy_users.append(user)
#
# DONE WHEN
#   python checks/check_detect_bruteforce.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
