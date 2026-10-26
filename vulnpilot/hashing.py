r"""
hashing.py - Make the SHA-256 fingerprint of the report plus its evidence, the same way every time.

WHO OWNS THIS: TODO
DIFFICULTY: easy
TIME ESTIMATE: 1 hour

WHAT GOES IN
    report_text: the markdown report (a string).
    evidence_lines: a list of exact log lines (strings), in any order.

WHAT MUST COME OUT
    A string of 64 lowercase hex characters (a SHA-256 hash), for example
    "8b6901c9dcbd7a4f...".
    Rules for "the same way every time" (the checker tests every one):
    - the same input always gives the same hash
    - spaces at the END of a line and Windows line endings (\r\n) do not change the hash
    - the ORDER of the evidence lines does not change the hash
    - changing even one character of the report OR of one evidence line changes the hash

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: hashlib (already imported at the top).
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. Clean the report: replace "\r\n" with "\n", cut the spaces off the end of every line with line.rstrip(), then .strip() the whole text.
    2. Clean the evidence: rstrip() every line, then sorted(...) the list so the order does not matter.
    3. Join into one text:  clean_report + "\n---EVIDENCE---\n" + "\n".join(clean_evidence)
    4. hashlib.sha256(text.encode("utf-8")).hexdigest() gives the 64 character answer.
    5. Use plain for loops to clean the lines (no tricks needed).

Your own check:  python checks/check_hashing.py
"""

import hashlib

from vulnpilot.dummies import dummy_hash


def make_hash(report_text, evidence_lines):
    """Return the canonical SHA-256 hex string of the report plus the evidence lines."""
    result = dummy_hash()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# import hashlib
# words = ["pear  ", "apple", "fig "]
# clean = []
# for word in words:
#     clean.append(word.rstrip())            # remove spaces at the end: ["pear", "apple", "fig"]
# clean = sorted(clean)                      # ["apple", "fig", "pear"]
# text = ",".join(clean)                     # "apple,fig,pear"
# fingerprint = hashlib.sha256(text.encode("utf-8")).hexdigest()   # 64 hex characters
# Same pattern: clean, sort, join, hash.
#
# DONE WHEN
#   python checks/check_hashing.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
