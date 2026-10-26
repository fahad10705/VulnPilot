# AGENTS.md - VulnPilot (instructions for any AI agent working in this repo)

Read `README.md` first for setup and the file list.

## Summary
VulnPilot is an AI security analyst whose incident reports are provably untampered.
Upload an auth log -> Python rules find suspicious patterns and keep the exact log lines as
evidence -> NVIDIA Nemotron (via Nebius Token Factory, OpenAI-compatible API) writes an
investigation grounded in those lines -> SHA-256 of report + evidence is anchored on Sepolia ->
a Verify button recomputes the hash and checks the chain.

Hackathon: Nebius x NVIDIA Global AI Hackathon (Devpost), track "Best Apps and Agents".
Deadline: 30 Oct 2026, 10:00 pm GMT+5. Student team; keep code simple and readable.

## Run it
`python3 start.py` (Windows: `python start.py`). It creates `.venv`, installs
`requirements.txt`, creates `.env`, and runs `streamlit run app.py`.

## Modules and owners
| File | Owner |
|---|---|
| vulnpilot/parser.py | TODO assign |
| vulnpilot/detections.py | TODO assign |
| vulnpilot/ioc.py | TODO assign |
| vulnpilot/mitre.py | TODO assign |
| vulnpilot/timeline.py | TODO assign |
| vulnpilot/ai_investigator.py | TODO assign |
| vulnpilot/report.py | TODO assign |
| vulnpilot/chain.py (+ contract) | TODO assign |
| vulnpilot/config.py, models.py, app.py, start.py | lead |

## Stub rules
- Every module has a header comment: purpose, inputs, outputs (with example data), owner, status.
- Every function has a docstring and returns realistic dummy data so the app runs end to end.
- Replace function bodies, but NEVER change function signatures. Shared shapes live in models.py.
- Plain, simple Python. No fancy patterns. Touch only your own file unless told otherwise.

## Safety rules
- The repo is public. Never commit secrets. Keys and the wallet private key go in `.env` (local, git-ignored) and Streamlit Secrets (deployed). `.env.example` lists names only.
- Use a throwaway testnet wallet, never a real one.
- Do not push to main, deploy, or rewrite history without the lead's OK.
- Do not guess the Nebius base URL or model name; they live in config.py / .env only.
