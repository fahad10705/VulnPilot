    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Two dicts keyed by source IP:
    #   users_by_ip: which DIFFERENT usernames each IP tried (a set drops repeats)
    #   lines_by_ip: the exact raw log lines, kept as evidence
    users_by_ip = {}
    lines_by_ip = {}

    for event in events:
        # Only failed logins count; successes are not part of a spray.
        if event.result != "failed":
            continue
        users_by_ip.setdefault(event.source_ip, set()).add(event.user)
        lines_by_ip.setdefault(event.source_ip, []).append(event.raw_line)

    result = []
    for ip, users in users_by_ip.items():
        # 5+ different usernames = spray. One user hammered many times is
        # brute force, which a different detector handles, so it is skipped here.
        if len(users) >= 5:
            result.append(
                Finding(
                    finding_type="password_spray",
                    title="Password spray",
                    severity="medium",
                    description=f"{ip} tried {len(users)} different usernames.",
                    evidence_lines=lines_by_ip[ip],
                    source_ip=ip,
                    users=sorted(users),
                )
            )
    ### WRITE YOUR CODE ABOVE THIS LINE ###
