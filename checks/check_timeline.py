"""Check for vulnpilot/timeline.py.  Run:  python checks/check_timeline.py"""
from common import DUMMY, PASS, load_events, load_findings, main
from vulnpilot.dummies import dummy_timeline
from vulnpilot.models import TimelineEntry
from vulnpilot.timeline import build_timeline


def check():
    events = load_events("auth_attack")
    entries = build_timeline(events, load_findings())
    if entries == dummy_timeline():
        return DUMMY
    assert isinstance(entries, list) and all(isinstance(e, TimelineEntry) for e in entries), "Return a list of TimelineEntry"
    assert len(entries) == 19, f"Expected 19 entries (one per suspicious event), got {len(entries)}"
    numbers = [e.line_number for e in entries]
    assert numbers == sorted(numbers), f"Entries must be sorted by line_number. Yours: {numbers}"
    success = [e for e in entries if e.line_number == 13]
    assert success, "No entry for line 13 (the successful admin login)"
    assert success[0].severity == "critical", f"A successful login should have severity 'critical', got {success[0].severity!r}"
    assert "admin" in success[0].description and "192.0.2.10" in success[0].description, \
        f"description should mention the user and IP, got {success[0].description!r}"
    failed = [e for e in entries if e.line_number == 6][0]
    assert failed.severity == "warning", f"A failed login should have severity 'warning', got {failed.severity!r}"
    assert build_timeline(events, []) == [], "No findings should give an empty timeline []"
    return PASS


if __name__ == "__main__":
    main("timeline", check)
