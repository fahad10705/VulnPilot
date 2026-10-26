r"""
deploy_contract.py - deploys contracts/EvidenceAnchor.sol to the Sepolia testnet.

WHO RUNS THIS: lead only (needs a wallet key). Beginners never run this.
STATUS: written but NOT yet tested against the real network.

EASIEST ALTERNATIVE (no script): open https://remix.ethereum.org, paste contracts/EvidenceAnchor.sol,
compile with Solidity 0.8.20, choose "Injected Provider - MetaMask" on the Sepolia network, click Deploy,
then copy the contract address into CONTRACT_ADDRESS.

To use this script:
    .venv/bin/pip install py-solc-x        (Windows: .venv\Scripts\pip install py-solc-x)
    set SEPOLIA_RPC_URL and WALLET_PRIVATE_KEY in .env  (throwaway testnet wallet with Sepolia ETH only!)
    .venv/bin/python deploy/deploy_contract.py
It prints the contract address. Put it in .env as CONTRACT_ADDRESS (and in Streamlit Secrets).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solcx import compile_source, install_solc  # noqa: E402
from web3 import Web3  # noqa: E402

from vulnpilot.config import SEPOLIA_CHAIN_ID, get_setting  # noqa: E402

SOLC_VERSION = "0.8.20"
CONTRACT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "contracts", "EvidenceAnchor.sol")


def main():
    rpc_url = get_setting("SEPOLIA_RPC_URL")
    private_key = get_setting("WALLET_PRIVATE_KEY")
    if not rpc_url or not private_key:
        sys.exit("Set SEPOLIA_RPC_URL and WALLET_PRIVATE_KEY in .env first.")

    print("Compiling the contract ...")
    install_solc(SOLC_VERSION)
    with open(CONTRACT_FILE) as f:
        compiled = compile_source(f.read(), output_values=["abi", "bin"], solc_version=SOLC_VERSION)
    interface = compiled["<stdin>:EvidenceAnchor"]

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    account = w3.eth.account.from_key(private_key)
    print("Deploying from", account.address, "(needs Sepolia test ETH)")
    contract = w3.eth.contract(abi=interface["abi"], bytecode=interface["bin"])
    transaction = contract.constructor().build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "chainId": SEPOLIA_CHAIN_ID,
    })
    signed = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    print("Deployed! CONTRACT_ADDRESS =", receipt.contractAddress)
    print("Transaction: https://sepolia.etherscan.io/tx/" + tx_hash.hex())


if __name__ == "__main__":
    main()
