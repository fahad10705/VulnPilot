"""
chain.py - hash the report + evidence and anchor/verify it on Sepolia.

Functions:
    make_hash(report_text: str, evidence_lines: list[str]) -> str
        SHA-256 hex string (64 chars) of report + evidence. Real, works now.
    anchor_hash(hash_hex: str) -> dict
        sends anchor(hash) to the EvidenceAnchor contract on Sepolia.
        returns {"tx_hash": "0x...", "explorer_url": "https://sepolia.etherscan.io/tx/0x..."}
    verify_hash(hash_hex: str) -> dict
        calls verify(hash) on the contract.
        returns {"found": True, "timestamp": 1761300000}

Real version: web3.py, SEPOLIA_RPC_URL, WALLET_PRIVATE_KEY, CONTRACT_ADDRESS from
config.get_setting. Use a throwaway testnet wallet only. Contract: contracts/EvidenceAnchor.sol

Owner: TODO assign
Status: make_hash REAL; anchor_hash and verify_hash are STUBS (fake chain, kept in memory)
"""

import hashlib
import time

_FAKE_CHAIN = {}  # STUB storage: hash -> timestamp. Lost when the app restarts.


def make_hash(report_text, evidence_lines):
    """Return the SHA-256 hex digest of the report plus evidence."""
    data = report_text + "\n---EVIDENCE---\n" + "\n".join(evidence_lines)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def anchor_hash(hash_hex):
    """Anchor the hash. STUB: stores it in memory and returns a fake tx."""
    _FAKE_CHAIN[hash_hex] = int(time.time())
    fake_tx = "0x" + hash_hex
    return {"tx_hash": fake_tx, "explorer_url": "https://sepolia.etherscan.io/tx/" + fake_tx}


def verify_hash(hash_hex):
    """Check the hash. STUB: looks in the in-memory fake chain."""
    timestamp = _FAKE_CHAIN.get(hash_hex)
    return {"found": timestamp is not None, "timestamp": timestamp}
