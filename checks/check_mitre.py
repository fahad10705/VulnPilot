"""Check for vulnpilot/mitre.py.  Run:  python checks/check_mitre.py"""
from common import DUMMY, PASS, load_findings, main
from vulnpilot.dummies import dummy_mitre
from vulnpilot.mitre import map_to_mitre
from vulnpilot.models import Finding


def check():
    findings = load_findings()
    rows = map_to_mitre(findings)
    if rows == dummy_mitre():
        return DUMMY
    assert isinstance(rows, list), f"map_to_mitre must return a list, got {type(rows).__name__}"
    assert len(rows) == 4, f"Expected 4 rows (one per finding), got {len(rows)}"
    ids = [row.get("id") for row in rows]
    assert ids == ["T1110.001", "T1110.003", "T1087", "T1087"], f"Wrong technique ids: {ids}"
    for row, finding in zip(rows, findings):
        for key in ("finding_title", "id", "name", "tactic"):
            assert key in row, f"Each row needs the key {key!r}. Got {row}"
        assert row["finding_title"] == finding.title, f"finding_title should be {finding.title!r}, got {row['finding_title']!r}"
    assert rows[1]["tactic"] == "Credential Access", "Password spray tactic should be 'Credential Access'"
    assert map_to_mitre([Finding(finding_type="something_unknown", title="x")]) == [], "Unknown finding types must be skipped"
    assert map_to_mitre([]) == [], "No findings should give []"
    return PASS


if __name__ == "__main__":
    main("mitre", check)
