"""Runs every check and prints one table.  Run:  python checks/check_all.py"""
import sys

from common import FAIL, run_and_print
import check_ai_client
import check_chain_helpers
import check_detect_bruteforce
import check_detect_invalid_users
import check_detect_password_spray
import check_hashing
import check_ioc
import check_mitre
import check_parser
import check_pipeline
import check_prompts
import check_report
import check_risk
import check_timeline

CHECKS = [
    ("parser", check_parser), ("detect_bruteforce", check_detect_bruteforce),
    ("detect_password_spray", check_detect_password_spray), ("detect_invalid_users", check_detect_invalid_users),
    ("ioc", check_ioc), ("mitre", check_mitre), ("timeline", check_timeline), ("risk", check_risk),
    ("report", check_report), ("hashing", check_hashing), ("prompts", check_prompts),
    ("chain_helpers", check_chain_helpers), ("pipeline (lead)", check_pipeline), ("ai_client (lead)", check_ai_client),
]

print("MODULE CHECKS   (PASS = done, STILL DUMMY = not written yet, FAIL = read the reason)\n")
statuses = [run_and_print(name, module.check) for name, module in CHECKS]
print(f"\n{statuses.count('PASS')} PASS, {statuses.count('STILL DUMMY')} STILL DUMMY, {statuses.count(FAIL)} FAIL")
sys.exit(1 if FAIL in statuses else 0)
