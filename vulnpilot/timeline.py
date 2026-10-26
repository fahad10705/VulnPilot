"""
timeline.py - build the attack timeline and its Plotly chart.

Purpose: order the key events of the attack in time.
Functions:
    build_timeline(findings: list[Finding], events: pandas.DataFrame) -> list[TimelineEntry]
    make_timeline_chart(entries: list[TimelineEntry]) -> plotly Figure

Example:
    TimelineEntry(time="Oct 24 10:13:08", description="Login succeeded for admin from 192.0.2.10", line_number=11)

Owner: TODO assign
Status: STUB (dummy entries, simple chart)
"""

import plotly.graph_objects as go

from vulnpilot.models import TimelineEntry


def build_timeline(findings, events):
    """Return a list of TimelineEntry. STUB: dummy data."""
    return [
        TimelineEntry("Oct 24 10:12:47", "First failed login for admin from 192.0.2.10", 4),
        TimelineEntry("Oct 24 10:13:05", "Last failed login (7th) for admin", 10),
        TimelineEntry("Oct 24 10:13:08", "Login succeeded for admin from 192.0.2.10", 11),
        TimelineEntry("Oct 24 10:13:40", "admin ran sudo bash (root shell)", 12),
    ]


def make_timeline_chart(entries):
    """Return a Plotly figure showing the entries in order. STUB: simple markers."""
    fig = go.Figure(go.Scatter(
        x=[e.time for e in entries],
        y=[1] * len(entries),
        mode="markers+text",
        text=[e.description for e in entries],
        textposition="top center",
    ))
    fig.update_yaxes(visible=False)
    fig.update_layout(title="Attack timeline", height=300)
    return fig
