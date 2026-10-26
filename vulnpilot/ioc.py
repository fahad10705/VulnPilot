"""
ioc.py - extract indicators of compromise (IPs and usernames) from findings/events.

Purpose: list the IPs and users involved in suspicious activity.
Function:
    extract_iocs(findings: list[Finding], events: pandas.DataFrame) -> list[IOC]
        returns a list of IOC (see models.py)

Example:
    IOC(kind="ip", value="192.0.2.10", count=8)

Owner: TODO assign
Status: STUB (returns dummy IOCs)
"""

from vulnpilot.models import IOC


def extract_iocs(findings, events):
    """Return a list of IOC. STUB: returns dummy data."""
    return [
        IOC(kind="ip", value="192.0.2.10", count=8),
        IOC(kind="user", value="admin", count=8),
    ]
