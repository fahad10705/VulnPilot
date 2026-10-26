"""Check for vulnpilot/detect_invalid_users.py.  Run:  python checks/check_detect_invalid_users.py"""
from common import DUMMY, PASS, load_events, main
from vulnpilot.detect_invalid_users import detect_invalid_users
from vulnpilot.dummies import dummy_invalid_users


def check():
    events = load_events("auth_attack")
    found = detect_invalid_users(events)
    if found == dummy_invalid_users():
        return DUMMY
    assert isinstance(found, list), f"detect_invalid_users must return a list, got {type(found).__name__}"
    assert len(found) == 2, f"Expected 2 findings (198.51.100.7 and 203.0.113.99), got {len(found)}"
    by_ip = {finding.source_ip: finding for finding in found}
    assert set(by_ip) == {"198.51.100.7", "203.0.113.99"}, f"Wrong IPs flagged: {sorted(by_ip)}"
    for finding in found:
        assert finding.finding_type == "invalid_users", f"finding_type should be 'invalid_users', got {finding.finding_type!r}"
    assert len(by_ip["198.51.100.7"].evidence_lines) == 5, "198.51.100.7 should have 5 evidence lines"
    assert sorted(by_ip["198.51.100.7"].users) == ["deploy", "git", "oracle", "postgres", "ubuntu"], "Wrong users for 198.51.100.7"
    assert len(by_ip["203.0.113.99"].evidence_lines) == 3, "203.0.113.99 should have 3 evidence lines"
    assert sorted(by_ip["203.0.113.99"].users) == ["guest", "support", "test"], "Wrong users for 203.0.113.99"
    clean = detect_invalid_users(load_events("clean"))
    assert clean == [], f"clean.log has no attacks, so the answer must be [] but you returned {len(clean)} finding(s)"
    assert detect_invalid_users([]) == [], "An empty events list should give []"
    return PASS


if __name__ == "__main__":
    main("detect_invalid_users", check)
