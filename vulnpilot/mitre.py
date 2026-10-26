r"""
mitre.py - Map each finding to its MITRE ATT&CK technique using vulnpilot/data/mitre_map.json.

WHO OWNS THIS: TODO
DIFFICULTY: easy
TIME ESTIMATE: 1 hour

WHAT GOES IN
    findings: list of Finding. Use finding.finding_type ("brute_force", "password_spray", "invalid_users")
    and finding.title.
    The JSON file maps a finding type to a technique, e.g.
    "brute_force": {"id": "T1110.001", "name": "Brute Force: Password Guessing", "tactic": "Credential Access"}

WHAT MUST COME OUT
    A list of dicts, one per finding whose type is in the JSON file (unknown types are skipped):
    {"finding_title": "Password spray", "id": "T1110.003",
     "name": "Brute Force: Password Spraying", "tactic": "Credential Access"}
    Empty list [] for no findings.

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: json (already imported at the top).
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. MAP_PATH (below) already points at the JSON file. Open it with:  with open(MAP_PATH) as f:
    2. table = json.load(f)  gives you a dict. table["brute_force"] is the entry for brute force.
    3. Use table.get(finding.finding_type) so an unknown type gives None instead of crashing.
    4. For each finding with an entry, build the dict with the four keys shown above.
    5. EXTRA (spare unit): add more techniques to mitre_map.json, for example T1078 Valid Accounts.

Your own check:  python checks/check_mitre.py
"""

import json
import os

from vulnpilot.dummies import dummy_mitre


MAP_PATH = os.path.join(os.path.dirname(__file__), "data", "mitre_map.json")


def map_to_mitre(findings):
    """Return a list of dicts with the MITRE technique for every finding."""
    result = dummy_mitre()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# import json
# with open("settings.json") as f:          # open a file and close it again automatically
#     settings = json.load(f)               # {"theme": {"color": "blue"}}
# color = settings.get("theme", {}).get("color")   # .get() returns None instead of crashing
# Same pattern: load the JSON once, then look things up with .get().
#
# DONE WHEN
#   python checks/check_mitre.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
