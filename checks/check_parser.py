# """Check for vulnpilot/parser.py.  Run:  python checks/check_parser.py"""
# from common import DUMMY, PASS, first_difference, load_events, main, read_text
# from vulnpilot.dummies import dummy_events
# from vulnpilot.parser import parse_log


# def check():
#     attack_text = read_text("sample_logs/auth_attack.log")
#     events = parse_log(attack_text)
#     if events == dummy_events():
#         return DUMMY
#     assert isinstance(events, list), f"parse_log must return a list, got {type(events).__name__}"
#     assert len(events) == 28, f"Expected 28 events from auth_attack.log, got {len(events)}"
#     first = events[0]
#     assert (first.line_number, first.user, first.source_ip, first.result) == (1, "alice", "198.51.100.23", "success"), \
#         f"First event should be line 1, alice, 198.51.100.23, success. Got {first!r}"
#     assert first.raw_line == attack_text.splitlines()[0], "raw_line must be the exact original line"
#     assert first.time == "Oct 24 09:58:02", f"time should be 'Oct 24 09:58:02', got {first.time!r}"
#     deploy = [e for e in events if e.line_number == 18]
#     assert deploy, "No event for line 18 (the 'invalid user deploy' line)"
#     assert deploy[0].user == "deploy" and deploy[0].invalid_user is True and deploy[0].result == "failed", \
#         f"Line 18 should be user=deploy, failed, invalid_user=True. Got {deploy[0]!r}"
#     assert sum(1 for e in events if e.invalid_user) == 8, "Expected 8 events with invalid_user=True"
#     expected = load_events("auth_attack")
#     assert events == expected, "Events differ from the expected list: " + first_difference(events, expected)
#     clean = parse_log(read_text("sample_logs/clean.log"))
#     assert len(clean) == 7, f"Expected 7 events from clean.log, got {len(clean)}"
#     assert parse_log("") == [], "An empty log should give an empty list []"
#     return PASS
import re
from vulnpilot.models import LogEvent

def parse_log(text):
    """Parse the log text into a list of LogEvent."""
    result = []
    lines = text.splitlines()
    
    for line_number, line in enumerate(lines, start=1):
        if "Failed password" not in line and "Accepted" not in line:
            continue
        
        time_str = line[:15]
        match = re.search(r"(Failed|Accepted) \w+ for (invalid user )?(\S+) from (\S+)", line)
        
        if match:
            status = match.group(1)
            invalid_flag = match.group(2) is not None
            username = match.group(3)
            ip = match.group(4)
            
            res_val = "failed" if status == "Failed" else "success"
            
            event = LogEvent(
                line_number=line_number,
                time=time_str,
                user=username,
                source_ip=ip,
                result=res_val,
                invalid_user=invalid_flag,
                raw_line=line
            )
            result.append(event)

    return result

