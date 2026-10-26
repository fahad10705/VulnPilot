"""
mitre.py - map findings to MITRE ATT&CK techniques using data/mitre_map.json.

Purpose: add technique name and tactic to each finding.
Function:
    map_to_mitre(findings: list[Finding]) -> list[dict]
        returns one dict per finding:
        {"finding_title": str, "id": "T1110", "name": "Brute Force", "tactic": "Credential Access"}

Example:
    [{"finding_title": "Brute force followed by successful login",
      "id": "T1110", "name": "Brute Force", "tactic": "Credential Access"}]

Owner: TODO assign
Status: STUB (looks up the id in the JSON file; very simple)
"""

import json
import os

MAP_PATH = os.path.join(os.path.dirname(__file__), "data", "mitre_map.json")


def map_to_mitre(findings):
    """Return a list of technique dicts for the findings."""
    with open(MAP_PATH) as f:
        table = json.load(f)
    by_id = {entry["id"]: entry for entry in table.values()}
    results = []
    for finding in findings:
        entry = by_id.get(finding.mitre_id)
        if entry:
            results.append({
                "finding_title": finding.title,
                "id": entry["id"],
                "name": entry["name"],
                "tactic": entry["tactic"],
            })
    return results
