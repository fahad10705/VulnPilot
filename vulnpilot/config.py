"""
config.py - one place for settings and secrets.

Purpose: read settings from the environment (.env locally, Streamlit Secrets when deployed).
Takes: nothing. Use get_setting("NAME") anywhere you need a value.
Returns: the value as a string, or "" if it is not set.

Example:
    get_setting("NEBIUS_BASE_URL")  ->  "https://api.tokenfactory.nebius.com/v1/"

Owner: TODO assign
Status: working (simple version)

NOTE: The Nebius base URL comes from docs.tokenfactory.nebius.com.
The exact Nemotron model id is NOT confirmed yet. Look it up in the model catalog
(tokenfactory.nebius.com) and set NEBIUS_MODEL in .env.
"""

import os

from dotenv import load_dotenv

load_dotenv()  # reads .env if it exists

DEFAULTS = {
    "NEBIUS_BASE_URL": "https://api.tokenfactory.nebius.com/v1/",
    "NEBIUS_MODEL": "",  # TODO: put the exact Nemotron model id here or in .env
}


def get_setting(name):
    """Return a setting from env vars, then Streamlit Secrets, then defaults."""
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
