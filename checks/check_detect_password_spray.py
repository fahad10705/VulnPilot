"""Check for vulnpilot/detect_password_spray.py.  Run:  python checks/check_detect_password_spray.py"""
from common import DUMMY, PASS, load_events, main
from vulnpilot.detect_password_spray import detect_password_spray
from vulnpilot.dummies import dummy_password_spray


def check():
    events = load_events("auth_attack")
    found = detect_password_spray(events)
    if found == dummy_password_spray():
        return DUMMY
    assert isinstance(found, list), f"detect_password_spray must return a list, got {type(found).__name__}"
    assert len(found) == 1, f"Expected exactly 1 password spray finding, got {len(found)}"
    finding = found[0]
    assert finding.finding_type == "password_spray", f"finding_type should be 'password_spray', got {finding.finding_type!r}"
    assert finding.source_ip == "198.51.100.7", f"source_ip should be 198.51.100.7, got {finding.source_ip!r}"
    expected_users = ["alice", "bob", "carol", "deploy", "git", "oracle", "postgres", "ubuntu"]
    assert sorted(finding.users) == expected_users, f"users should be {expected_users}, got {sorted(finding.users)}"
    expected_lines = [e.raw_line for e in events if e.line_number in range(15, 23)]
    assert finding.evidence_lines == expected_lines, (
        f"evidence_lines should be the 8 failed lines from 198.51.100.7 in log order. Got {len(finding.evidence_lines)} lines.")
    clean = detect_password_spray(load_events("clean"))
    assert clean == [], f"clean.log has no attacks, so the answer must be [] but you returned {len(clean)} finding(s)"
    assert detect_password_spray([]) == [], "An empty events list should give []"
    return PASS


if __name__ == "__main__":
    main("detect_password_spray", check)
