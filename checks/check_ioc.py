"""Check for vulnpilot/ioc.py.  Run:  python checks/check_ioc.py"""
from common import DUMMY, PASS, load_events, load_findings, main
from vulnpilot.dummies import dummy_indicators
from vulnpilot.ioc import extract_indicators
from vulnpilot.models import Indicator


def check():
    found = extract_indicators(load_events("auth_attack"), load_findings())
    if found == dummy_indicators():
        return DUMMY
    assert isinstance(found, list) and all(isinstance(i, Indicator) for i in found), "Return a list of Indicator objects"
    table = {(i.kind, i.value): i.count for i in found}
    expected = {("ip", "192.0.2.10"): 8, ("ip", "198.51.100.7"): 8, ("ip", "203.0.113.99"): 3}
    for key, count in expected.items():
        assert key in table, f"Missing indicator {key}. You found: {sorted(table)}"
        assert table[key] == count, f"Indicator {key} should have count {count}, you gave {table[key]}"
    assert ("user", "admin") in table, "Missing the username indicator ('user', 'admin')"
    assert ("ip", "203.0.113.45") not in table, "203.0.113.45 only appears in normal lines, it must not be listed"
    assert extract_indicators(load_events("auth_attack"), []) == [], "No findings should give []"
    return PASS


if __name__ == "__main__":
    main("ioc", check)
