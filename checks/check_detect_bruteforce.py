# """Check for vulnpilot/detect_bruteforce.py.  Run:  python checks/check_detect_bruteforce.py"""
# from common import DUMMY, PASS, load_events, main
# from vulnpilot.detect_bruteforce import detect_bruteforce
# from vulnpilot.dummies import dummy_bruteforce


# def check():
#     events = load_events("auth_attack")
#     found = detect_bruteforce(events)
#     if found == dummy_bruteforce():
#         return DUMMY
#     assert isinstance(found, list), f"detect_bruteforce must return a list, got {type(found).__name__}"
#     assert len(found) == 1, f"Expected exactly 1 brute force finding in auth_attack.log, got {len(found)}"
#     finding = found[0]
#     assert finding.finding_type == "brute_force", f"finding_type should be 'brute_force', got {finding.finding_type!r}"
#     assert finding.source_ip == "192.0.2.10", f"source_ip should be 192.0.2.10, got {finding.source_ip!r}"
#     assert finding.users == ["admin"], f"users should be ['admin'], got {finding.users!r}"
#     assert finding.severity in ("low", "medium", "high", "critical"), f"Bad severity {finding.severity!r}"
#     expected = [e.raw_line for e in events if e.line_number in range(6, 14)]
#     assert finding.evidence_lines == expected, (
#         f"evidence_lines should be the 7 failed lines then the success line (8 lines, log order). "
#         f"Got {len(finding.evidence_lines)} lines.")
#     clean = detect_bruteforce(load_events("clean"))
#     assert clean == [], f"clean.log has no attacks, so the answer must be [] but you returned {len(clean)} finding(s)"
#     assert detect_bruteforce([]) == [], "An empty events list should give []"
#     return PASS


# if __name__ == "__main__":
#     main("detect_bruteforce", check)
from vulnpilot.models import Finding

def detect_bruteforce(events):
    """Return a list of Finding for brute force attacks that ended in a successful login."""
    result = []
    failed_by_pair = {}
    
    for event in events:
        pair = (event.source_ip, event.user)
        
        if event.result == "failed":
            failed_by_pair.setdefault(pair, []).append(event)
        elif event.result == "success":
            if pair in failed_by_pair and len(failed_by_pair[pair]) >= 5:
                failed_events = failed_by_pair[pair]
                evidence_lines = [e.raw_line for e in failed_events] + [event.raw_line]
                count = len(failed_events)
                description = f"{count} failed logins for {event.user} from {event.source_ip}, then a success."
                title = "Brute force followed by successful login"
                
                finding = Finding(
                    finding_type="brute_force",
                    title=title,
                    severity="high",
                    description=description,
                    evidence_lines=evidence_lines,
                    source_ip=event.source_ip,
                    users=[event.user]
                )
                result.append(finding)
                del failed_by_pair[pair]

    return result