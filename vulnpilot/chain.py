"""
chain.py - anchor a report hash on the Sepolia testnet and verify it later.

WHO OWNS THIS: lead only. Beginners never edit this file and never need a wallet or keys.

Two modes:
  - LIVE: SEPOLIA_RPC_URL, CONTRACT_ADDRESS and WALLET_PRIVATE_KEY are all set -> uses web3.py and the
    EvidenceAnchor contract (contracts/EvidenceAnchor.sol).
  - DEMO: anything missing -> the hash is "anchored" in a local file (.demo_chain.json, git-ignored).
    Verify still works against that local record. The app shows a banner so nobody is fooled.

Functions:
    chain_mode() -> "live" or "demo"
    anchor(hash_hex) -> {"ok": bool, "mode": str, "tx_hash": str, "explorer_url": str, "timestamp": int, "message": str}
    verify(hash_hex) -> {"ok": bool, "mode": str, "found": bool, "timestamp": int or None, "message": str}

Use a throwaway testnet wallet only. Never hard-code keys.
"""

import json
import os
import time

from vulnpilot import chain_helpers, dummies
from vulnpilot.config import SEPOLIA_CHAIN_ID, chain_is_configured, get_setting

DEMO_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".demo_chain.json")
EXPLORER_BASE = "https://sepolia.etherscan.io/tx/"

# Only the two functions we call. This is the "ABI" of EvidenceAnchor.sol.
CONTRACT_ABI = [
    {"type": "function", "name": "anchor", "stateMutability": "nonpayable",
     "inputs": [{"name": "hash", "type": "bytes32"}], "outputs": []},
    {"type": "function", "name": "verify", "stateMutability": "view",
     "inputs": [{"name": "hash", "type": "bytes32"}],
     "outputs": [{"name": "", "type": "bool"}, {"name": "", "type": "uint256"}]},
]


def chain_mode():
    return "live" if chain_is_configured() else "demo"


def _to_bytes32(hash_hex):
    """Use the teammates' helper if it works, otherwise the built-in conversion."""
    try:
        value = chain_helpers.hex_to_bytes32(hash_hex)
        if value != dummies.dummy_hex_to_bytes32() and len(value) == 32:
            return value
    except Exception:
        pass
    return bytes.fromhex(hash_hex[2:] if hash_hex.startswith("0x") else hash_hex)


def _explorer_link(tx_hash):
    try:
        value = chain_helpers.explorer_tx_link(tx_hash)
        if value != dummies.dummy_explorer_link():
            return value
    except Exception:
        pass
    return EXPLORER_BASE + (tx_hash if tx_hash.startswith("0x") else "0x" + tx_hash)


# ---------- demo mode ----------

def _read_demo():
    try:
        with open(DEMO_FILE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _write_demo(record):
    with open(DEMO_FILE, "w") as f:
        json.dump(record, f)


def _anchor_demo(hash_hex):
    record = _read_demo()
    if hash_hex not in record:
        record[hash_hex] = int(time.time())
        _write_demo(record)
    return {"ok": True, "mode": "demo", "tx_hash": "demo-" + hash_hex[:16], "explorer_url": "",
            "timestamp": record[hash_hex], "message": "DEMO MODE: hash saved in a local file, nothing was sent to a blockchain."}


def _verify_demo(hash_hex):
    timestamp = _read_demo().get(hash_hex)
    return {"ok": True, "mode": "demo", "found": timestamp is not None, "timestamp": timestamp,
            "message": "DEMO MODE: checked against the local record."}


# ---------- live mode (Sepolia) ----------

def _connect():
    from web3 import Web3
    w3 = Web3(Web3.HTTPProvider(get_setting("SEPOLIA_RPC_URL")))
    contract = w3.eth.contract(address=Web3.to_checksum_address(get_setting("CONTRACT_ADDRESS")), abi=CONTRACT_ABI)
    return w3, contract


def _anchor_live(hash_hex):
    w3, contract = _connect()
    account = w3.eth.account.from_key(get_setting("WALLET_PRIVATE_KEY"))
    hash_bytes = _to_bytes32(hash_hex)
    found, timestamp = contract.functions.verify(hash_bytes).call()
    if found:
        return {"ok": True, "mode": "live", "tx_hash": "", "explorer_url": "", "timestamp": timestamp,
                "message": "This hash was already anchored earlier, so no new transaction was needed."}
    transaction = contract.functions.anchor(hash_bytes).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "chainId": SEPOLIA_CHAIN_ID,
    })
    signed = w3.eth.account.sign_transaction(transaction, get_setting("WALLET_PRIVATE_KEY"))
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction).hex()
    w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    found, timestamp = contract.functions.verify(hash_bytes).call()
    return {"ok": True, "mode": "live", "tx_hash": tx_hash, "explorer_url": _explorer_link(tx_hash),
            "timestamp": timestamp, "message": "Anchored on Sepolia."}


def _verify_live(hash_hex):
    w3, contract = _connect()
    found, timestamp = contract.functions.verify(_to_bytes32(hash_hex)).call()
    return {"ok": True, "mode": "live", "found": bool(found), "timestamp": timestamp if found else None,
            "message": "Checked on the Sepolia blockchain."}


# ---------- public functions ----------

def anchor(hash_hex):
    """Anchor the hash. Never raises: problems come back as ok=False with a message."""
    try:
        return _anchor_live(hash_hex) if chain_mode() == "live" else _anchor_demo(hash_hex)
    except Exception as error:
        return {"ok": False, "mode": chain_mode(), "tx_hash": "", "explorer_url": "", "timestamp": 0,
                "message": f"Anchoring failed: {type(error).__name__}: {error}"}


def verify(hash_hex):
    """Check the hash. Never raises: problems come back as ok=False with a message."""
    try:
        return _verify_live(hash_hex) if chain_mode() == "live" else _verify_demo(hash_hex)
    except Exception as error:
        return {"ok": False, "mode": chain_mode(), "found": False, "timestamp": None,
                "message": f"Verification failed: {type(error).__name__}: {error}"}
