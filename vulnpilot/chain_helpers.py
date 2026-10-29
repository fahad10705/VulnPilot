
EXPLORER_BASE = "https://sepolia.etherscan.io/tx/"

def hex_to_bytes32(hash_hex):
    """Return the hash as exactly 32 bytes. Raise ValueError if it is not 64 hex characters."""
    if hash_hex.startswith("0x"):
        hash_hex = hash_hex[2:]
    if len(hash_hex) != 64:
        raise ValueError("hash must be 64 hex characters")
    return bytes.fromhex(hash_hex)

def explorer_tx_link(tx_hash):
    """Return the Sepolia Etherscan link for a transaction hash."""
    if not tx_hash.startswith("0x"):
        tx_hash = "0x" + tx_hash
    return EXPLORER_BASE + tx_hash