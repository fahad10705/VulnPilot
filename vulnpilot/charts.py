"""
charts.py - Plotly chart for the attack timeline.

WHO OWNS THIS: lead only.

make_timeline_chart(entries) takes the list of TimelineEntry from timeline.py and returns a Plotly figure.
"""

from datetime import datetime

import plotly.graph_objects as go

COLORS = {"info": "#4c78a8", "warning": "#f58518", "critical": "#e45756"}
HEIGHT = {"info": 1, "warning": 2, "critical": 3}


def _to_datetime(time_text, position):
    """Turn 'Oct 24 10:13:08' into a datetime. If that fails, use the position so the chart still draws."""
    try:
        return datetime.strptime("2026 " + time_text, "%Y %b %d %H:%M:%S")
    except ValueError:
        return position


def make_timeline_chart(entries):
    """Return a Plotly figure: time on the x axis, severity on the y axis."""
    fig = go.Figure()
    for number, entry in enumerate(entries):
        fig.add_trace(go.Scatter(
            x=[_to_datetime(entry.time, number)],
            y=[HEIGHT.get(entry.severity, 1)],
            mode="markers",
            marker=dict(size=14, color=COLORS.get(entry.severity, "#4c78a8")),
            hovertext=f"{entry.time} (line {entry.line_number}): {entry.description}",
            hoverinfo="text",
            showlegend=False,
        ))
    fig.update_yaxes(tickvals=[1, 2, 3], ticktext=["info", "warning", "critical"], range=[0.5, 3.5])
    fig.update_layout(title="Attack timeline", height=320, margin=dict(l=20, r=20, t=50, b=20))
    return fig
