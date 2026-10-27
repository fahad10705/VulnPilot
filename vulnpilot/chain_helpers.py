# r"""
# chain_helpers.py - Two tiny pure helpers for the blockchain part: hex hash to 32 bytes, and a link to see a transaction.

# WHO OWNS THIS: TODO
# DIFFICULTY: easy
# TIME ESTIMATE: 1 hour

# WHAT GOES IN
#     hex_to_bytes32(hash_hex): a 64 character hex string, with or without a "0x" start.
#         Example: "8b6901c9dcbd7a4f1e2d3c4b5a69788796a5b4c3d2e1f00112233445566778899"
#     explorer_tx_link(tx_hash): a transaction hash string, with or without "0x".
#         Example: "0xabc123..."

# WHAT MUST COME OUT
#     hex_to_bytes32 returns exactly 32 bytes (a bytes object), e.g. b"\x8b\x69\x01...". If the
#     input is not 64 hex characters it must raise ValueError("hash must be 64 hex characters").
#     explorer_tx_link returns the Sepolia Etherscan link:
#     "https://sepolia.etherscan.io/tx/0xabc123..."  (add the 0x if it is missing).
#     No network calls in this file. It is just text work.

# RULES
#     - Do not rename the function(s).
#     - Do not change the arguments.
#     - Do not edit any other file.
#     - Do not import anything except: nothing new (the import already at the top is enough).
#     - Write only between the two ### lines. Plain, simple Python. Comments that explain WHY are welcome.

# HINTS
#     1. hex_to_bytes32: if the text starts with "0x", cut it off:  hash_hex[2:]
#     2. Then check len(...) == 64, otherwise  raise ValueError("hash must be 64 hex characters")
#     3. bytes.fromhex(text) turns hex text into bytes. It raises ValueError itself for bad characters.
#     4. explorer_tx_link: if not tx_hash.startswith("0x"): tx_hash = "0x" + tx_hash
#     5. Then return EXPLORER_BASE + tx_hash  (EXPLORER_BASE is already defined below).

# Your own check:  python checks/check_chain_helpers.py
# """

# from vulnpilot.dummies import dummy_explorer_link, dummy_hex_to_bytes32


# EXPLORER_BASE = "https://sepolia.etherscan.io/tx/"


# def hex_to_bytes32(hash_hex):
#     """Return the hash as exactly 32 bytes. Raise ValueError if it is not 64 hex characters."""
#     result = dummy_hex_to_bytes32()  # placeholder, so the whole app works from the first minute

#     ### WRITE YOUR CODE BELOW THIS LINE ###
#     # Replace the placeholder by building your own `result` here, step by step.
#     ### WRITE YOUR CODE ABOVE THIS LINE ###

#     return result


# def explorer_tx_link(tx_hash):
#     """Return the Sepolia Etherscan link for a transaction hash."""
#     result = dummy_explorer_link()  # placeholder, so the whole app works from the first minute

#     ### WRITE YOUR CODE BELOW THIS LINE ###
#     # Replace the placeholder by building your own `result` here, step by step.
#     ### WRITE YOUR CODE ABOVE THIS LINE ###

#     return result


# # ---------------------------------------------------------------------------
# # WORKED EXAMPLE (a different, smaller job in the same style. Copy the pattern, not the task.)
# # word = "0xHELLO"
# # if word.startswith("0x"):          # .startswith() asks "does the text begin with this?"
# #     word = word[2:]                # [2:] cuts off the first two characters -> "HELLO"
# # link = "https://example.com/item/" + word
# # Same pattern: tidy the text first, then build the answer from it.
# #
# # DONE WHEN
# #   python checks/check_chain_helpers.py   prints PASS.
# #   (Right now it prints STILL DUMMY. That is normal: you have not written your code yet.)
# #   Then run  python checks/check_all.py  to see every module, and open a pull request.
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