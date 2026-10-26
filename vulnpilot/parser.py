r"""
parser.py - Turn the raw text of an SSH authentication log into a list of LogEvent objects.

WHO OWNS THIS: TODO
DIFFICULTY: easy
TIME ESTIMATE: 1-2 hours

WHAT GOES IN
    text: the whole log file as ONE string (many lines separated by newlines). For example one line of
    sample_logs/auth_attack.log looks like this:
    "Oct 24 09:58:02 web01 sshd[2101]: Accepted password for alice from 198.51.100.23 port 51822 ssh2"

WHAT MUST COME OUT
    A list of LogEvent. One LogEvent for every line that contains "Failed password" or
    "Accepted". All other lines (CRON, sudo, "Connection closed") are skipped.
    For auth_attack.log the answer has 28 events. The first one is:
    LogEvent(line_number=1, time="Oct 24 09:58:02", user="alice", source_ip="198.51.100.23",
             result="success", invalid_user=False, raw_line="<the full original line>")
    A line like "Failed password for invalid user deploy from 198.51.100.7 ..." gives
    user="deploy", result="failed", invalid_user=True.

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: re.
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. text.splitlines() gives you the lines. enumerate(lines, start=1) gives a line number too.
    2. Skip a line quickly with:  if "Failed password" not in line and "Accepted" not in line: continue
    3. The time is just the first 15 characters of the line:  line[:15]
    4. re.search(r"(Failed|Accepted) \w+ for (invalid user )?(\S+) from (\S+)", line) finds the pieces.
       group(1) is Failed/Accepted, group(2) is "invalid user " or None, group(3) the user, group(4) the IP.
    5. result is "failed" if group(1) == "Failed", otherwise "success". invalid_user is True if group(2) is not None.
    6. Build LogEvent(number, time, user, ip, result, invalid_user, line) and append it to a list.

Your own check:  python checks/check_parser.py
"""

import re

from vulnpilot.dummies import dummy_events
from vulnpilot.models import LogEvent


def parse_log(text):
    """Parse the log text into a list of LogEvent."""
    result = dummy_events()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# import re
# line = "Jan 05 12:00:01 shop checkout for bob total 42"
# match = re.search(r"checkout for (\S+) total (\d+)", line)
# if match:
#     name = match.group(1)         # "bob"
#     total = int(match.group(2))   # 42  (int() turns text into a number)
# The same pattern (re.search + group) pulls the user and IP out of a log line.
#
# DONE WHEN
#   python checks/check_parser.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
