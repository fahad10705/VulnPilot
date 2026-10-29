# Work units

Each unit is ONE file with ONE small job. Open your file and read its top comment first.
Check command (Mac/Linux): `.venv/bin/python checks/<check>`. Windows: `.venv\Scripts\python checks\<check>`.
Status values: `todo`, `in progress`, `review`, `done`. Update the Owner and Status columns in your pull request.

| # | File | Owner | Difficulty | Time | What you write | Check | Status |
|---|---|---|---|---|---|---|---|
| 1 | `vulnpilot/parser.py` | mubeenfatimaz9882-svg | easy | 1-2 h | turn raw log text into a list of `LogEvent` (regex) | `check_parser.py` | done |
| 2 | `vulnpilot/detect_bruteforce.py` | mubeenfatimaz9882-svg | medium | 2 h | many failed logins from one IP, then a success | `check_detect_bruteforce.py` | done |
| 3 | `vulnpilot/detect_password_spray.py` | AYESHA-81 | medium | 2 h | one IP trying many different usernames | `check_detect_password_spray.py` | done |
| 4 | `vulnpilot/detect_invalid_users.py` | TODO | easy | 1 h | attempts with usernames that do not exist | `check_detect_invalid_users.py` | todo |
| 5 | `vulnpilot/ioc.py` | TODO | easy | 1-2 h | extract attacker IPs and usernames from the findings | `check_ioc.py` | todo |
| 6 | `vulnpilot/mitre.py` | TODO | easy | 1 h | map findings to MITRE ATT&CK using the JSON file | `check_mitre.py` | todo |
| 7 | `vulnpilot/timeline.py` | TODO | easy | 1-2 h | sort suspicious events into timeline entries | `check_timeline.py` | todo |
| 8 | `vulnpilot/risk.py` | TODO | medium | 2 h | explainable risk score: level, score, reasons | `check_risk.py` | todo |
| 9 | `vulnpilot/report.py` | TODO | easy | 1-2 h | build the markdown incident report | `check_report.py` | todo |
| 10 | `vulnpilot/hashing.py` | TODO | easy | 1 h | canonical SHA-256 of report + evidence | `check_hashing.py` | todo |
| 11 | `vulnpilot/prompts.py` | Fahad | medium | 2 h | write the AI instructions (writing, not heavy code) | `check_prompts.py` | todo |
| 12 | `vulnpilot/chain_helpers.py` | mubeenfatimaz9882-svg | easy | 1 h | hex to 32 bytes, Etherscan link (no network) | `check_chain_helpers.py` | done |
| 13 | `contracts/EvidenceAnchor.sol` | TODO (blockchain pair) | easy | 1-2 h | read the commented contract, deploy it on Remix's test chain, call `anchor` and `verify`, write what you learned in `docs/BLOCKCHAIN_NOTES.md` | (manual, see below) | todo |

**Contract unit (13) in plain steps:** open https://remix.ethereum.org, paste the file, compile with 0.8.20, deploy on "Remix VM", call `anchor` with `0x` + 64 hex characters, then call `verify` with the same value (you should see `true` and a time), then with a different value (you should see `false`, `0`). Write the steps and screenshots into `docs/BLOCKCHAIN_NOTES.md`.

## Lead only (nobody else edits)
`app.py`, `start.py`, `vulnpilot/pipeline.py`, `vulnpilot/config.py`, `vulnpilot/models.py`, `vulnpilot/dummies.py`, `vulnpilot/ai_client.py` (Nebius), `vulnpilot/chain.py` (web3, wallet), `vulnpilot/charts.py`, `deploy/`, `checks/`.

## Spare tasks for fast finishers
| File | What | Time |
|---|---|---|
| `vulnpilot/data/mitre_map.json` | add more MITRE techniques (for example T1078 Valid Accounts) and tell the `mitre.py` owner | 30 min |
| `docs/GLOSSARY.md` | add 5 more words in plain English that a beginner would not know | 30 min |
| `vulnpilot/ioc.py` | extra: also extract domains, URLs and 64-character hashes with more regex | 1 h |
| `sample_logs/` | invent a third small log (for example a slow brute force over hours) using only documentation IPs (192.0.2.x, 198.51.100.x, 203.0.113.x), and tell the lead | 1 h |
| `docs/BLOCKCHAIN_NOTES.md` | write a one-page "how our anchoring works" for the demo video | 1 h |
