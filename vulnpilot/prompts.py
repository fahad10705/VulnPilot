r"""
prompts.py - Write the instructions (prompts) we send to the Nemotron AI so it writes an honest, evidence-based investigation.

WHO OWNS THIS: TODO
DIFFICULTY: medium
TIME ESTIMATE: 2 hours (writing and thinking, not heavy code)

WHAT GOES IN
    findings: list of Finding (use title, severity, description, evidence_lines).
    risk: a RiskResult (level, score, reasons).

WHAT MUST COME OUT
    A pair (system_prompt, user_prompt) of two non-empty strings.
    system_prompt: the AI's rules. It MUST say: use ONLY the evidence lines given and never invent
    anything; put facts a log line proves under CONFIRMED and quote the exact line; put guesses
    under HYPOTHESES; recommend actions; answer with one JSON object in the format ANSWER_FORMAT below.
    user_prompt: the data: the risk level and reasons, then every finding with its title, severity,
    description and ALL its evidence lines (exactly as they are in the log).
    Example start of user_prompt:  "Risk: critical (95)\nFinding 1: Brute force followed by successful login ..."

RULES
    - Do not rename the function(s).
    - Do not change the arguments.
    - Do not edit any other file.
    - Do not import anything except: nothing new (the import already at the top is enough).
    - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

HINTS
    1. Keep the AI's answer format EXACTLY as ANSWER_FORMAT below. ai_client.py reads those key names.
    2. The system prompt is plain English in a triple-quoted string. Say what to do AND what never to do.
    3. Think like a strict teacher: the AI must quote a log line for every fact, otherwise it is only a hypothesis.
    4. Build the user prompt with a loop over findings; number them (Finding 1, Finding 2).
    5. Print each evidence line on its own line, unchanged, so the AI can quote it exactly.
    6. Ask a friend to read your prompt. Would a stranger know exactly what to do? Test ideas on the Nebius playground if you have access.

Your own check:  python checks/check_prompts.py
"""

from vulnpilot.dummies import dummy_prompts


ANSWER_FORMAT = ('{"summary": "one short paragraph", '
                 '"confirmed": [{"claim": "a fact", "evidence_line": "the exact log line that proves it"}], '
                 '"hypotheses": ["a clearly labelled guess"], '
                 '"actions": ["a recommended next step"]}')


def build_prompts(findings, risk):
    """Return (system_prompt, user_prompt) for the Nemotron investigation."""
    result = dummy_prompts()  # placeholder, so the whole app works from the first minute

    ### WRITE YOUR CODE BELOW THIS LINE ###
    # Replace the placeholder by building your own `result` here, step by step.
    ### WRITE YOUR CODE ABOVE THIS LINE ###

    return result


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# name = "Sam"
# steps = ["wake up", "eat"]
# lines = [f"Daily plan for {name}:"]
# number = 0
# for step in steps:
#     number = number + 1
#     lines.append(f"{number}. {step}")       # "1. wake up", "2. eat"
# text = "\n".join(lines)
# Same pattern for the user prompt: a header line, then a numbered block per finding.
#
# DONE WHEN
#   python checks/check_prompts.py   prints PASS.
#   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
#   Then run  python checks/check_all.py  to see every module, and open a pull request.
