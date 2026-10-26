"""
common.py - small helpers shared by the check scripts. Lead only; beginners do not edit this.

Every check_*.py has a function check() that returns "PASS" or "STILL DUMMY", or raises
AssertionError with a plain-English reason (which is shown as FAIL).
"""

import json
import os
import sys
import traceback

CHECKS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CHECKS_DIR)
sys.path.insert(0, ROOT)  # so "import vulnpilot" works when you run: python checks/check_x.py

from vulnpilot.models import Finding, LogEvent  # noqa: E402

PASS = "PASS"
DUMMY = "STILL DUMMY"
FAIL = "FAIL"


def read_text(relative_path):
    with open(os.path.join(ROOT, relative_path)) as f:
        return f.read()


def _load(name):
    with open(os.path.join(CHECKS_DIR, "fixtures", name)) as f:
        return json.load(f)


def load_events(which):
    """which = 'auth_attack' or 'clean'. Ready-made LogEvents, so detectors do not depend on parser.py."""
    return [LogEvent(**item) for item in _load(which + "_events.json")]


def load_findings():
    """Ready-made Findings for auth_attack.log (brute force, spray, 2x invalid users)."""
    return [Finding(**item) for item in _load("auth_attack_findings.json")]


def first_difference(got, expected):
    """A short plain-English hint about where two lists first differ."""
    for number, (a, b) in enumerate(zip(got, expected)):
        if a != b:
            return f"item {number} is different. Yours: {a!r}  Expected: {b!r}"
    return f"your list has {len(got)} items, expected {len(expected)}"


def run_and_print(title, check_function):
    """Run one check, print a friendly line, and return the status."""
    try:
        status = check_function()
        message = {PASS: "all checks passed", DUMMY: "your function still returns the placeholder. Write your code between the two ### lines."}[status]
    except AssertionError as error:
        status, message = FAIL, str(error)
    except Exception as error:  # the student's code crashed
        status = FAIL
        last = traceback.extract_tb(error.__traceback__)[-1]
        message = f"your code crashed: {type(error).__name__}: {error} (file {os.path.basename(last.filename)}, line {last.lineno})"
    print(f"{status:12} {title}: {message}")
    return status


def main(title, check_function):
    status = run_and_print(title, check_function)
    sys.exit(1 if status == FAIL else 0)
