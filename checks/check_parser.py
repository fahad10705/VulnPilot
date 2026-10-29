
import re
from vulnpilot.models import LogEvent

def parse_log(text):
    """Parse the log text into a list of LogEvent."""
    result = []
    lines = text.splitlines()
    
    for line_number, line in enumerate(lines, start=1):
        if "Failed password" not in line and "Accepted" not in line:
            continue
        
        time_str = line[:15]
        match = re.search(r"(Failed|Accepted) \w+ for (invalid user )?(\S+) from (\S+)", line)
        
        if match:
            status = match.group(1)
            invalid_flag = match.group(2) is not None
            username = match.group(3)
            ip = match.group(4)
            
            res_val = "failed" if status == "Failed" else "success"
            
            event = LogEvent(
                line_number=line_number,
                time=time_str,
                user=username,
                source_ip=ip,
                result=res_val,
                invalid_user=invalid_flag,
                raw_line=line
            )
            result.append(event)

    return result

