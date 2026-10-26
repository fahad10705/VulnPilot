"""
start.py - one command to set up and run VulnPilot. Works on Linux, Mac and Windows.

Run:  python3 start.py      (on Windows: python start.py)

What it does, in order:
  1. creates a .venv folder (only the first time)
  2. installs everything in requirements.txt into that .venv
  3. copies .env.example to .env if you do not have a .env yet
  4. starts the app with Streamlit

Owner: lead
Status: written, not yet tested with a real install
"""

import os
import shutil
import subprocess
import threading
import venv
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(ROOT, ".venv")

if os.name == "nt":  # Windows
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
else:
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")


def make_venv():
    """Create the .venv folder if it is not there yet."""
    if not os.path.exists(VENV_PYTHON):
        print("Creating virtual environment (.venv) ...")
        venv.create(VENV_DIR, with_pip=True)


def install_requirements():
    """Install the packages from requirements.txt into the .venv."""
    print("Installing requirements (first time can take a few minutes) ...")
    # newest pip first: older pip cannot resume a download that stalls on a slow connection
    subprocess.call([VENV_PYTHON, "-m", "pip", "install", "--quiet", "--upgrade", "pip"])
    # long timeout, many retries and resume, so a slow connection does not fail the install
    subprocess.check_call([VENV_PYTHON, "-m", "pip", "install", "--default-timeout", "60", "--retries", "10",
                           "--resume-retries", "30", "-r", os.path.join(ROOT, "requirements.txt")])


def make_env_file():
    """Copy .env.example to .env so there is a file to fill in."""
    env_path = os.path.join(ROOT, ".env")
    if not os.path.exists(env_path):
        shutil.copy(os.path.join(ROOT, ".env.example"), env_path)
        print("Created .env from .env.example. Fill in your keys there (never commit it).")


def run_app():
    """Start the Streamlit app."""
    print("Starting VulnPilot at http://localhost:8501 (stop with Ctrl+C) ...")
    # headless skips Streamlit's first-run email question, which would hang scripts and AI agents
    env = dict(os.environ, STREAMLIT_SERVER_HEADLESS="true", STREAMLIT_BROWSER_GATHER_USAGE_STATS="false")
    threading.Timer(4, webbrowser.open, ["http://localhost:8501"]).start()  # open the browser ourselves
    subprocess.call([VENV_PYTHON, "-m", "streamlit", "run", os.path.join(ROOT, "app.py")], cwd=ROOT, env=env)


if __name__ == "__main__":
    make_venv()
    install_requirements()
    make_env_file()
    run_app()
