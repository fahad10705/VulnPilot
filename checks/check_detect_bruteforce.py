
from vulnpilot.models import Finding

def detect_bruteforce(events):
    """Return a list of Finding for brute force attacks that ended in a successful login."""
    result = []
    failed_by_pair = {}
    
    for event in events:
        pair = (event.source_ip, event.user)
        
        if event.result == "failed":
            failed_by_pair.setdefault(pair, []).append(event)
        elif event.result == "success":
            if pair in failed_by_pair and len(failed_by_pair[pair]) >= 5:
                failed_events = failed_by_pair[pair]
                evidence_lines = [e.raw_line for e in failed_events] + [event.raw_line]
                count = len(failed_events)
                description = f"{count} failed logins for {event.user} from {event.source_ip}, then a success."
                title = "Brute force followed by successful login"
                
                finding = Finding(
                    finding_type="brute_force",
                    title=title,
                    severity="high",
                    description=description,
                    evidence_lines=evidence_lines,
                    source_ip=event.source_ip,
                    users=[event.user]
                )
                result.append(finding)
                del failed_by_pair[pair]

    return result