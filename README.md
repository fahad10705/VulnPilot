# VulnPilot

**An AI security analyst whose incident reports are provably untampered.**

Built for the Nebius x NVIDIA Global AI Hackathon (track: Best Apps and Agents). A learning project by a university blockchain team.

## The 30 second pitch

Security reports can be edited after the fact. VulnPilot fixes that:

1. You upload an SSH authentication log.
2. Simple Python rules find attacks (brute force, password spray, fake usernames) and keep the **exact log lines** as evidence.
3. An NVIDIA Nemotron AI (through Nebius Token Factory) writes an investigation. It must quote real log lines, and it keeps **confirmed facts** apart from **guesses**.
4. We take a SHA-256 fingerprint of the report and its evidence and **anchor it on the Sepolia blockchain**.
5. A **Verify** button re-checks the fingerprint. Change one single character of the evidence ("Tamper test") and Verify fails.

*(Screenshots will go here: findings tab, attack timeline, AI investigation, Verify passing, Verify failing after tampering.)*

---

## Run it in 4 commands

You need **Git** and **Python 3.11 or newer**. Nothing else: no API keys, no wallet. Without keys the app runs in safe **demo mode** (offline sample AI text, simulated blockchain).

**Windows** (PowerShell or Command Prompt):
```powershell
git clone https://github.com/theamanullahdev/VulnPilot.git
cd VulnPilot
python start.py
```
**Mac or Linux:**
```bash
git clone https://github.com/theamanullahdev/VulnPilot.git
cd VulnPilot
python3 start.py
```
Then open http://localhost:8501 (the script opens it for you) and click **Run analysis**.
Stop with `Ctrl + C`. Next time just run `start.py` again.

`start.py` creates a `.venv` folder, installs `requirements.txt`, creates your `.env` file and starts the app.

### Check your own work (no browser needed)
```bash
.venv/bin/python checks/check_all.py          # Mac / Linux
.venv\Scripts\python checks\check_all.py      # Windows
```
It prints PASS, STILL DUMMY (not written yet, that is normal) or FAIL (with the reason) for every module. To check one file: `.venv/bin/python checks/check_parser.py`.

### Troubleshooting
- `python3` not found on Windows: use `python` or `py`. `python` not found on Linux: use `python3`.
- Python too old: install Python 3.11+ from python.org, delete the `.venv` folder, run `start.py` again.
- Install times out on a slow connection: just run `start.py` again (downloads resume).
- Port 8501 busy: `.venv/bin/streamlit run app.py --server.port 8600`.
- Linux says venv is missing: `sudo apt install python3-venv`.
- Manual steps if you prefer: `python3 -m venv .venv`, activate it, `pip install -r requirements.txt`, `streamlit run app.py`.

---

## How the project is built (read this if you are a teammate)

The app **always runs end to end**, even when nobody has written their file yet. Every beginner function starts by returning a placeholder ("dummy") answer. You replace the placeholder with real code in your one small file. `vulnpilot/pipeline.py` calls every module in a `try/except`: if your function crashes or is not written yet, the app falls back to the placeholder and the sidebar shows `dummy` or `error` next to your module. One broken file never breaks the app.

```
log text -> parser -> detect_bruteforce ------+
                      detect_password_spray ---+-> findings -> ioc, mitre, timeline, risk
                      detect_invalid_users ----+      -> prompts -> AI -> report -> hashing -> chain
```

| Who | Files |
|---|---|
| **Teammates** (one file each, see `docs/TASKS.md`) | `parser.py`, `detect_bruteforce.py`, `detect_password_spray.py`, `detect_invalid_users.py`, `ioc.py`, `mitre.py`, `timeline.py`, `risk.py`, `report.py`, `hashing.py`, `prompts.py`, `chain_helpers.py`, `contracts/EvidenceAnchor.sol` |
| **Lead only** (never edit) | `app.py`, `start.py`, `vulnpilot/pipeline.py`, `config.py`, `models.py`, `dummies.py`, `ai_client.py`, `chain.py`, `charts.py`, `deploy/`, `checks/` |

All Python files are in `vulnpilot/`. The shared data shapes (LogEvent, Finding, Indicator, ...) are in `vulnpilot/models.py`.

**Want to contribute? Read [CONTRIBUTING.md](CONTRIBUTING.md).** Unsure about a word? See [docs/GLOSSARY.md](docs/GLOSSARY.md).

---

## For the lead: keys, AI and blockchain

Everything below is optional for teammates. Settings live in `.env` locally (never commit it) and in Streamlit Secrets when deployed. `.env.example` lists the names only.

| Name | Meaning |
|---|---|
| `NEBIUS_API_KEY` | Nebius Token Factory key |
| `NEBIUS_BASE_URL` | defaults to `https://api.tokenfactory.nebius.com/v1/` |
| `NEBIUS_MODEL` | exact Nemotron model id from the Nebius model catalog (required for the AI step) |
| `SEPOLIA_RPC_URL` | a Sepolia RPC endpoint (Alchemy, Infura, QuickNode) |
| `WALLET_PRIVATE_KEY` | key of a **throwaway testnet wallet only**, funded with free Sepolia ETH |
| `CONTRACT_ADDRESS` | address of the deployed `EvidenceAnchor` contract |

- **AI mode:** needs `NEBIUS_API_KEY` and `NEBIUS_MODEL`. Otherwise (or if the call fails) the app shows a clearly labelled **OFFLINE SAMPLE** report. The AI's "confirmed" claims are checked: a quote that is not a real evidence line is moved to hypotheses.
- **Blockchain mode:** needs `SEPOLIA_RPC_URL`, `CONTRACT_ADDRESS` and `WALLET_PRIVATE_KEY`. Otherwise **demo mode**: the hash is saved in a local file (`.demo_chain.json`), Verify works against it, and the app shows a banner.

### Deploy the contract (once)
1. Easiest: open https://remix.ethereum.org, paste `contracts/EvidenceAnchor.sol`, compile with Solidity 0.8.20, deploy on Sepolia with MetaMask ("Injected Provider"), and copy the address into `CONTRACT_ADDRESS`.
2. Or use the script (untested, see its header): `pip install py-solc-x`, fill `SEPOLIA_RPC_URL` and `WALLET_PRIVATE_KEY` in `.env`, then run `python deploy/deploy_contract.py`.

### Deploy the app
Streamlit Community Cloud: connect this public repo, main file `app.py`, then paste the variables above into the app's **Secrets** (TOML format, `NAME = "value"`).
