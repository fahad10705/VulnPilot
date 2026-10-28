# AGENTS.md - VulnPilot (instructions for any AI agent working in this repo)

Read `README.md` first for setup, then `docs/TASKS.md` for the work units.

## Summary
VulnPilot is an AI security analyst whose incident reports are provably untampered.
Upload an auth log -> Python rules find attacks and keep the exact log lines as evidence ->
NVIDIA Nemotron (via Nebius Token Factory, OpenAI-compatible API) writes an investigation grounded
in those lines -> SHA-256 of report + evidence is anchored on Sepolia -> a Verify button recomputes
the hash and checks the chain (the Tamper test shows Verify failing after a 1 character edit).

Hackathon: Nebius x NVIDIA Global AI Hackathon (Devpost), track "Best Apps and Agents".
Deadline: Fri 30 Oct 2026, 10:00 pm GMT+5. Team of 10, mostly beginners. Learning matters more than winning.

## Run it
`python3 start.py` (Windows: `python start.py`): creates `.venv`, installs `requirements.txt`, creates `.env`, starts Streamlit.
Checks (no browser): `.venv/bin/python checks/check_all.py` or one file, e.g. `checks/check_parser.py`.

## Module layout (all in `vulnpilot/`)
Beginner modules, one small function each. Each starts with a header (WHAT GOES IN / WHAT MUST COME OUT / RULES / HINTS),
returns a dummy placeholder from `dummies.py`, and has a marked block `### WRITE YOUR CODE BELOW THIS LINE ###`:

| File | Function | Owner |
|---|---|---|
| parser.py | `parse_log(text)` -> list[LogEvent] | TODO |
| detect_bruteforce.py | `detect_bruteforce(events)` -> list[Finding] | TODO |
| detect_password_spray.py | `detect_password_spray(events)` -> list[Finding] | TODO |
| detect_invalid_users.py | `detect_invalid_users(events)` -> list[Finding] | TODO |
| ioc.py | `extract_indicators(events, findings)` -> list[Indicator] | TODO |
| mitre.py | `map_to_mitre(findings)` -> list[dict] | TODO |
| timeline.py | `build_timeline(events, findings)` -> list[TimelineEntry] | TODO |
| risk.py | `score_risk(findings)` -> RiskResult | TODO |
| report.py | `build_report(findings, indicators, timeline, mitre, risk, investigation)` -> str | TODO |
| hashing.py | `make_hash(report_text, evidence_lines)` -> 64 hex chars | TODO |
| prompts.py | `build_prompts(findings, risk)` -> (system_prompt, user_prompt) | Fahad |
| chain_helpers.py | `hex_to_bytes32(hash_hex)`, `explorer_tx_link(tx_hash)` | TODO (blockchain pair) |
| contracts/EvidenceAnchor.sol | commented Solidity contract | TODO (blockchain pair) |

Lead-only files (beginners and their agents never edit them): `app.py`, `start.py`, `pipeline.py`, `config.py`, `models.py`,
`dummies.py`, `ai_client.py` (AI call with a fallback chain), `chain.py` (web3 + wallet, demo mode when keys are missing), `charts.py`, `deploy/`, `checks/`.

## Pipeline fallback (important)
`pipeline.py` calls every beginner function inside try/except and compares the result with the placeholder in `dummies.py`.
Status per module: `real`, `dummy` (still the placeholder), `error` (crashed or wrong return type; the placeholder is used instead).
The Streamlit sidebar shows this table, so one broken file never breaks the app. `ai_client.py` tries Nebius, OpenRouter, Groq and Google in order (whichever have a key) and returns an OFFLINE SAMPLE
if none works; `chain.py` runs in DEMO MODE without keys; `hashing.py` falls back to a built-in SHA-256 if it is not finished.

## Check scripts
`checks/check_<module>.py` runs one module against `sample_logs/auth_attack.log` (28 events, 4 findings) and `clean.log`
(7 events, 0 findings) and prints PASS, FAIL (with a plain reason) or STILL DUMMY. `checks/check_all.py` prints one table.
Checks use ready-made fixtures in `checks/fixtures/`, so every module can be tested on its own.

## Rules for code
- Replace only the marked block in your own file. NEVER rename functions or change arguments. Shared shapes live in models.py.
- Plain, simple Python: plain names, short functions, comments that explain why. No decorators, no clever patterns.
- No imports beyond those listed in the file header. No new libraries.

## Safety rules
- The repo is public. Never commit secrets. Keys and the wallet private key go in `.env` (git-ignored) and Streamlit Secrets (deployed). `.env.example` lists names only.
- Use a throwaway testnet wallet, never a real one.
- Do not push to main, deploy, or rewrite history without the lead's OK.
- Do not guess the Nebius base URL or model name; they live in config.py / .env only.
- Never paste an API key into chat, issues, code or commits. Keys live only in `.env` and Streamlit Secrets.
