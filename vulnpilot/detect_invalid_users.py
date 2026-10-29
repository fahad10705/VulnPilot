    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Group the raw lines and the usernames by source IP. Dicts keep insertion
    # order, so the findings will come out in the order IPs first appeared in the log.
    lines_by_ip = {}
    users_by_ip = {}

    for event in events:
        # Only attempts on usernames that do not exist on the server matter here.
        if event.invalid_user:
            if event.source_ip not in lines_by_ip:
                lines_by_ip[event.source_ip] = []
                users_by_ip[event.source_ip] = []
            lines_by_ip[event.source_ip].append(event.raw_line)
            users_by_ip[event.source_ip].append(event.user)

    result = []
    for ip in lines_by_ip:
        # 3 or more attempts from one IP looks like guessing, not a typo.
        if len(lines_by_ip[ip]) >= 3:
            # sorted(set(...)) removes repeats, so each username is listed once.
            usernames = sorted(set(users_by_ip[ip]))
            finding = Finding(
                finding_type="invalid_users",
                title="Attempts with non-existent usernames",
                severity="low",
                description=ip + " tried " + str(len(usernames)) + " usernames that do not exist.",
                evidence_lines=lines_by_ip[ip],
                source_ip=ip,
                users=usernames,
            )
            result.append(finding)
    ### WRITE YOUR CODE ABOVE THIS LINE ###
