r"""
timeline.py - Build the attack timeline: the suspicious events, sorted, ready for the chart.

WHO OWNS THIS: TODO
DIFFICULTY: easy
TIME ESTIMATE: 1-2 hours

WHAT GOES IN
    events: list of LogEvent (all events from the log).
    findings: list of Finding. Their evidence_lines tell you which events matter.

WHAT MUST COME OUT
    A list of TimelineEntry for every event whose raw_line appears in ANY finding's evidence_lines,
    sorted by line_number (oldest first). Empty list [] if there are no findings.
    Example: TimelineEntry(time="Oct 24 10:13:08", line_number=13, severity="critical",
                           description="Login succeeded for admin from 192.0.2.10")
    A failed login gets severity "warning" and description like "Failed login for admin from 192.0.2.10".
    For auth_attack.log the list has 19 entries.

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: nothing new (the imports already at the top are enough).
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. Make an empty set called evidence and add every finding's evidence lines:  evidence.update(finding.evidence_lines)
    2. Sort the events:  sorted(events, key=lambda e: e.line_number)   (key= says what to sort by)
    3. Keep only events where event.raw_line in evidence.
    4. If event.result == "success": severity "critical" and say "Login succeeded"; else "warning" and "Failed login".
    5. description = f"Failed login for {event.user} from {event.source_ip}" (an f-string puts values into text).
    6. Make TimelineEntry(event.time, description, event.line_number, severity) and add it to the result.

Your own check:  python checks/check_timeline.py
"""

from vulnpilot.dummies import dummy_timeline
from vulnpilot.models import TimelineEntry


def build_timeline(events, findings):
    """Return a sorted list of TimelineEntry for the suspicious events."""
    result = dummy_timeline()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# people = [{"name": "Zoe", "age": 30}, {"name": "Adam", "age": 25}]
# by_age = sorted(people, key=lambda p: p["age"])     # Adam first, then Zoe
# names = []
# for person in by_age:
#     names.append(person["name"])                    # ["Adam", "Zoe"]
# Same pattern: sort by a field, then build a new list from it.
#
# DONE WHEN
#   python checks/check_timeline.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
