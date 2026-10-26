"""Check for vulnpilot/hashing.py.  Run:  python checks/check_hashing.py"""
import re

from common import DUMMY, PASS, main
from vulnpilot.dummies import dummy_hash
from vulnpilot.hashing import make_hash


def check():
    report = "# Report\n\nSome text.\n"
    evidence = ["line one", "line two"]
    base = make_hash(report, evidence)
    if base == dummy_hash():
        return DUMMY
    assert isinstance(base, str) and re.fullmatch(r"[0-9a-f]{64}", base), f"Must return 64 lowercase hex characters, got {base!r}"
    assert make_hash(report, evidence) == base, "The same input must always give the same hash"
    assert make_hash(report, ["line two", "line one"]) == base, "The ORDER of the evidence lines must not change the hash"
    assert make_hash("# Report   \n\nSome text.   \n\n", evidence) == base, "Spaces at the end of lines (and trailing blank lines) must not change the hash"
    assert make_hash("# Report\r\n\r\nSome text.\r\n", evidence) == base, "Windows line endings (\\r\\n) must not change the hash"
    assert make_hash(report, ["line one  ", "line two"]) == base, "Trailing spaces on an evidence line must not change the hash"
    assert make_hash("# Report\n\nSome text!\n", evidence) != base, "Changing one character of the report MUST change the hash"
    assert make_hash(report, ["line onE", "line two"]) != base, "Changing one character of an evidence line MUST change the hash"
    assert make_hash(report, ["line one"]) != base, "Removing an evidence line MUST change the hash"
    return PASS


if __name__ == "__main__":
    main("hashing", check)
