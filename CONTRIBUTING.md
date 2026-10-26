# How to contribute (beginner guide)

You will edit **one file**. You do not need to understand Streamlit, API keys, the AI or the blockchain. Take it step by step and copy the commands.

## 0. Before you start
- Install **Git** (https://git-scm.com) and **Python 3.11+** (https://python.org).
- Make a free **GitHub** account. Tell Amanullah your username.
- Find your file in [docs/TASKS.md](docs/TASKS.md). Open it. Read the top: it explains what goes in, what must come out, and gives hints.

## 1. Get the project (once)
```bash
git clone https://github.com/theamanullahdev/VulnPilot.git
cd VulnPilot
python3 start.py        # Windows: python start.py   (press Ctrl+C when the page opens, setup is done)
```

## 2. Every time you work
```bash
git pull                                   # get the newest version first
```
1. Open **only your file** and write code between `### WRITE YOUR CODE BELOW THIS LINE ###` and `### WRITE YOUR CODE ABOVE THIS LINE ###`. Do not rename the function, do not change its arguments, do not edit other files.
2. Run your check (use your own file's name):
   ```bash
   .venv/bin/python checks/check_parser.py        # Mac / Linux
   .venv\Scripts\python checks\check_parser.py    # Windows
   ```
   `STILL DUMMY` = not written yet. `FAIL` = read the reason, fix, run again. `PASS` = you are done.
3. Save your work and send it:
   ```bash
   git add vulnpilot/parser.py                # only YOUR file (Windows works the same)
   git commit -m "Write parser"
   git pull
   git push
   ```
   If `git push` says you are not allowed (because you are not a collaborator yet), use the fork way below.

## The fork way (works for everyone, no permission needed)
With the GitHub CLI (`gh auth login` once):
```bash
gh repo fork theamanullahdev/VulnPilot --clone
cd VulnPilot
git checkout -b parser-module
git add vulnpilot/parser.py
git commit -m "Write parser"
git push -u origin parser-module
gh pr create --fill
```
No `gh`? On https://github.com/theamanullahdev/VulnPilot click **Fork**, clone YOUR fork, push your branch, then click **Compare & pull request**.
Amanullah reviews and merges your pull request.

## No Git? Use the GitHub website instead
1. Open your file on https://github.com/theamanullahdev/VulnPilot (for example `vulnpilot/parser.py`).
2. Click the **pencil** icon (Edit). GitHub will offer to make a copy for you (a fork): accept.
3. Write your code, then click **Commit changes** and choose "Create a new branch and start a pull request".
4. Click **Create pull request**.
You cannot run the check this way, so ask a teammate or Amanullah to run it.

## If something goes wrong
- **`git push` is rejected** ("rejected", "non-fast-forward" or "fetch first"): someone else pushed before you. Run `git pull`, then `git push` again. If Git opens a text editor for a merge message, just save and close it (in Vim: press Esc, type `:wq`, press Enter).
- **Merge conflict** ("CONFLICT" in the text): you probably edited a file that is not yours. Ask Amanullah. Do not try random fixes.
- **You edited the wrong file**: `git restore path/to/that_file.py` puts it back.
- **You are completely stuck**: write in the team chat with the exact error text and a screenshot.
- **The app shows your module as `error`**: your code crashed. Run your check script, it tells you the line.

## Golden rules
- **Never commit `.env`** or any key, password or wallet key. The repo is public: everybody on the internet can read it.
- Do not add libraries. Use only the imports listed at the top of your file.
- Keep code plain: short functions, clear names, comments that explain why.
- Never edit `app.py`, `pipeline.py`, `models.py`, `dummies.py`, `config.py`, `ai_client.py`, `chain.py`, `checks/`.
- Finished early? Ask for a spare task (see the end of docs/TASKS.md).
