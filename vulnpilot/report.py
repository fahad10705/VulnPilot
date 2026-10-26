"""
report.py - build the downloadable incident report (Markdown text).

Purpose: put findings, IOCs, timeline, MITRE and the AI investigation into one document.
Function:
    build_report(findings, iocs, timeline, mitre, investigation) -> str
        inputs are the outputs of the other modules; returns Markdown text.

The text returned here is what gets hashed and anchored, so keep it deterministic
(no "generated at" timestamps inside it).

Owner: TODO assign
Status: working simple version (teammate can make it prettier)
"""


def build_report(findings, iocs, timeline, mitre, investigation):
    """Return the incident report as Markdown."""
    lines = ["# VulnPilot Incident Report", ""]
    lines += [f"**Risk level:** {investigation.risk_level}", "", investigation.summary, ""]

    lines.append("## Confirmed observations")
    lines += [f"- {item}" for item in investigation.confirmed]
    lines += ["", "## Hypotheses (not proven)"]
    lines += [f"- {item}" for item in investigation.hypotheses]
    lines += ["", "## Recommended actions"]
    lines += [f"- {item}" for item in investigation.actions]

    lines += ["", "## Findings"]
    for f in findings:
        lines.append(f"### {f.title} ({f.severity}, {f.mitre_id})")
        lines.append(f.description)
        lines += [f"    {e}" for e in f.evidence_lines]

    lines += ["", "## Indicators of compromise"]
    lines += [f"- {i.kind}: {i.value} ({i.count} lines)" for i in iocs]
    lines += ["", "## Timeline"]
    lines += [f"- {t.time}: {t.description} (line {t.line_number})" for t in timeline]
    lines += ["", "## MITRE ATT&CK"]
    lines += [f"- {m['id']} {m['name']} ({m['tactic']})" for m in mitre]
    return "\n".join(lines) + "\n"
