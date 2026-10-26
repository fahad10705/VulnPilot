"""
config.py - one place for settings and secrets.

WHO OWNS THIS: lead only. Beginners never edit this file and never need any keys.

get_setting("NAME") returns the value from the environment (.env locally, Streamlit Secrets when
deployed), or "" if it is not set. Without keys the app runs in safe demo mode.

NOTE: the Nebius base URL is from docs.tokenfactory.nebius.com. The exact Nemotron model id is NOT
confirmed in those docs: copy it from the Token Factory model catalog into NEBIUS_MODEL (in .env).
"""

import os

from dotenv import load_dotenv

load_dotenv()  # reads .env if it exists

DEFAULTS = {
    "NEBIUS_BASE_URL": "https://api.tokenfactory.nebius.com/v1/",
    "NEBIUS_MODEL": "",  # TODO(lead): exact Nemotron model id from the Nebius model catalog
}

SEPOLIA_CHAIN_ID = 11155111
SEPOLIA_EXPLORER = "https://sepolia.etherscan.io/tx/"


def get_setting(name):
    """Return a setting from env vars, then Streamlit Secrets, then defaults ("" if unset)."""
    value = os.environ.get(name)
    if value:
        return value
    try:
        import streamlit as st
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass  # no secrets file locally, that is fine
    return DEFAULTS.get(name, "")


def ai_is_configured():
    """True only if both the API key and the model id are set."""
    return bool(get_setting("NEBIUS_API_KEY")) and bool(get_setting("NEBIUS_MODEL"))


def chain_is_configured():
    """True only if RPC url, contract address and wallet key are all set (otherwise demo mode)."""
    names = ["SEPOLIA_RPC_URL", "CONTRACT_ADDRESS", "WALLET_PRIVATE_KEY"]
    return all(get_setting(name) for name in names)
