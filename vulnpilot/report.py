r"""
report.py - Build the markdown incident report from the findings, indicators, timeline, MITRE rows, risk and AI text.

WHO OWNS THIS: TODO
DIFFICULTY: easy
TIME ESTIMATE: 1-2 hours

WHAT GOES IN
    findings: list of Finding
    indicators: list of Indicator
    timeline: list of TimelineEntry
    mitre: list of dicts like {"finding_title": ..., "id": "T1110.001", "name": ..., "tactic": ...}
    risk: a RiskResult (level, score, reasons)
    investigation: an Investigation (summary, confirmed, hypotheses, actions, source)

WHAT MUST COME OUT
    ONE string of markdown. It must start with a "# " title line and contain: the risk level and its
    reasons, the AI summary, the confirmed observations, the hypotheses, the recommended actions,
    every finding title with its exact evidence lines, the indicators, the timeline and the MITRE rows.
    IMPORTANT: it must be the same text every time for the same input. No dates or random values
    (the report is hashed and anchored on the blockchain).
    Example start:  "# VulnPilot Incident Report\n\n**Risk level:** critical (score 95)\n\n..."

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: nothing new (the imports already at the top are enough).
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. Start with lines = ["# VulnPilot Incident Report", ""] and keep adding strings with lines.append(...).
    2. At the end:  result = "\n".join(lines) + "\n"
    3. Use "## Findings" style headings. Put evidence lines in a code block (three backticks) or indent them 4 spaces.
    4. Loop over findings, then indicators, then timeline, then mitre. f-strings help:  f"- {t.time}: {t.description}"
    5. Print risk.level, risk.score and loop over risk.reasons.
    6. Do not add the current date or time, or the same input would give a different hash.

Your own check:  python checks/check_report.py
"""

from vulnpilot.dummies import dummy_report_text


def build_report(findings, indicators, timeline, mitre, risk, investigation):
    """Return the incident report as one markdown string."""
    result = dummy_report_text()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# lines = ["# Shopping list", ""]
# for item in ["milk", "eggs"]:
#     lines.append(f"- {item}")          # f-string: puts the value of item into the text
# lines.append("")
# lines.append("Total items: 2")
# text = "\n".join(lines) + "\n"          # join all lines with a newline between them
# Same pattern: append lines to a list, join once at the end.
#
# DONE WHEN
#   python checks/check_report.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
