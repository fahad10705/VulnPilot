# VulnPilot

An AI security analyst whose incident reports are provably untampered.

Upload an authentication log. Python rules find suspicious patterns and keep the exact log lines
as evidence. An NVIDIA Nemotron model (via Nebius Token Factory) writes an investigation report
grounded in those lines. A SHA-256 hash of report + evidence is anchored on the Sepolia testnet;
a Verify button recomputes the hash and checks the chain, so any edit to the logs or report makes
verification fail.

Built for the Nebius x NVIDIA Global AI Hackathon (track: Best Apps and Agents).

**Current status:** every module returns realistic *dummy data*, so the whole app runs end to end
from day one. Teammates replace the dummy function bodies with real logic, one file each.

---

## Quick start (Linux, Mac or Windows)

You need: **Git** and **Python 3.11 or newer** (check with `python3 --version`, on Windows `python --version`).

**Linux / Mac:**
```bash
git clone https://github.com/theamanullahdev/VulnPilot.git
cd VulnPilot
python3 start.py
```

**Windows (PowerShell or Command Prompt):**
```powershell
git clone https://github.com/theamanullahdev/VulnPilot.git
cd VulnPilot
python start.py
```

`start.py` does everything: creates a `.venv` folder, installs `requirements.txt`, creates `.env`
from `.env.example`, and starts the app. When it prints `Local URL: http://localhost:8501`, open
that link in your browser, then click **Use sample log**.

Next time, just run the same `start.py` command again (it skips what is already done).
Stop the app with `Ctrl + C`.

### If you prefer the manual steps (same result)

Linux / Mac:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```
(Command Prompt: use `.venv\Scripts\activate.bat` instead of the `Activate.ps1` line.
If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope Process Bypass` first.)

### Troubleshooting
- **`python3` not found (Windows):** use `python` or `py`. **`python` not found (Linux):** use `python3`.
- **Python too old:** install Python 3.11+ from python.org, then delete the `.venv` folder and rerun.
- **Install times out on a slow connection:** just run `python3 start.py` again. Downloads resume.
- **Port 8501 busy:** `.venv/bin/streamlit run app.py --server.port 8600` (Windows: `.venv\Scripts\streamlit run app.py --server.port 8600`).
- **Linux says venv is missing:** `sudo apt install python3-venv`, then rerun.

---

## Notes for AI agents (read this first)

If a human gave you this README and an empty folder, do exactly this:
1. `git clone https://github.com/theamanullahdev/VulnPilot.git` into the folder, then `cd` into the cloned folder.
2. Run `python3 start.py` (Windows: `python start.py`). It blocks while the app serves on
   http://localhost:8501, so run it in the background or in a separate terminal. For setup only, do
   the manual steps above and skip `streamlit run`.
3. Health check: `curl http://localhost:8501/_stcore/health` should print `ok`.
4. Read `AGENTS.md` before changing code. Do not commit `.env`, keys or private keys.

---

## What each file does

```
app.py                         Streamlit entry point, wires everything together
start.py                       one-command setup and run
vulnpilot/models.py            shared data shapes: Finding, IOC, TimelineEntry, Investigation
vulnpilot/parser.py            log text -> pandas table
vulnpilot/detections.py        suspicious-pattern rules -> findings with evidence lines
vulnpilot/ioc.py               extract attacker IPs and users
vulnpilot/mitre.py             map findings to MITRE ATT&CK (uses data/mitre_map.json)
vulnpilot/timeline.py          attack timeline + Plotly chart
vulnpilot/ai_investigator.py   Nemotron via Nebius Token Factory writes the investigation
vulnpilot/report.py            builds the downloadable Markdown incident report
vulnpilot/chain.py             SHA-256 hash, anchor and verify on Sepolia (web3.py)
vulnpilot/config.py            reads settings and secrets
contracts/EvidenceAnchor.sol   tiny Solidity contract: anchor(hash), verify(hash)
sample_logs/auth_attack.log    fake attack log for demos
```

Every `.py` file starts with a header comment: purpose, what each function takes and returns,
the owner and the status (STUB = dummy data, REAL = working).

## Working on a module (for teammates)

1. Pick **one** file from the list above (see the owner table in `AGENTS.md`).
2. Replace the dummy body of its functions with real logic. **Do not change function names,
   arguments or return shapes**; other files depend on them. Shared shapes live in `vulnpilot/models.py`.
3. Run the app and check it still works end to end with the sample log.
4. Work on your own branch and open a pull request:
   ```bash
   git checkout -b my-module-name
   git add vulnpilot/my_file.py
   git commit -m "Implement my_file"
   git push -u origin my-module-name
   ```
5. Keep code plain and readable. Use simple names. Update the header `Status:` line.

## Settings and secrets

Copy `.env.example` to `.env` (`start.py` does this for you) and fill in the values:

| Name | What it is |
|---|---|
| `NEBIUS_API_KEY` | your Nebius Token Factory key |
| `NEBIUS_BASE_URL` | `https://api.tokenfactory.nebius.com/v1/` (already the default) |
| `NEBIUS_MODEL` | exact Nemotron model id from the Nebius model catalog (not set yet) |
| `SEPOLIA_RPC_URL` | a Sepolia RPC endpoint |
| `WALLET_PRIVATE_KEY` | private key of a **throwaway testnet wallet only** |
| `CONTRACT_ADDRESS` | address of the deployed `EvidenceAnchor` contract |

**This repo is public. Never commit `.env`, API keys, or a private key.** `.env` is git-ignored.
Never use a real wallet. On Streamlit Community Cloud, put the same names in *Secrets* instead.
Without keys, the app still runs using dummy data.

## Team

See `CONTRIBUTORS.md`.
