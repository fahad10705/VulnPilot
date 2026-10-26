"""Check for vulnpilot/chain_helpers.py.  Run:  python checks/check_chain_helpers.py"""
from common import DUMMY, PASS, main
from vulnpilot.chain_helpers import explorer_tx_link, hex_to_bytes32
from vulnpilot.dummies import dummy_explorer_link, dummy_hex_to_bytes32

HASH = "8b6901c9dcbd7a4f1e2d3c4b5a69788796a5b4c3d2e1f00112233445566778899"[:64]


def check():
    as_bytes = hex_to_bytes32(HASH)
    link = explorer_tx_link("0xabc123")
    if as_bytes == dummy_hex_to_bytes32() or link == dummy_explorer_link():
        return DUMMY
    assert isinstance(as_bytes, bytes) and len(as_bytes) == 32, f"hex_to_bytes32 must return exactly 32 bytes, got {as_bytes!r}"
    assert as_bytes == bytes.fromhex(HASH), "hex_to_bytes32 returned the wrong bytes"
    assert hex_to_bytes32("0x" + HASH) == as_bytes, "A leading '0x' must be accepted and ignored"
    for bad in ("abc", HASH[:62], HASH + "00", ""):
        try:
            hex_to_bytes32(bad)
        except ValueError:
            continue
        raise AssertionError(f"hex_to_bytes32({bad!r}) must raise ValueError because it is not 64 hex characters")
    assert link == "https://sepolia.etherscan.io/tx/0xabc123", f"Wrong link: {link!r}"
    assert explorer_tx_link("abc123") == "https://sepolia.etherscan.io/tx/0xabc123", "A missing '0x' must be added"
    return PASS


if __name__ == "__main__":
    main("chain_helpers", check)
