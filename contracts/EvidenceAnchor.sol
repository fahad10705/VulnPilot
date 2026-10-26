// The next line says which open-source licence this code uses (MIT = anyone may reuse it).
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20; // tells the compiler which version of the Solidity language to use

// A "contract" is a tiny program that lives on the blockchain. Once deployed, nobody can edit its code.
// This one is a public notebook: it remembers WHEN a fingerprint (hash) was first written down.
contract EvidenceAnchor { // we name our contract EvidenceAnchor

    // A lookup table: the key is a hash (32 bytes), the value is the time it was saved. 0 means "never saved".
    mapping(bytes32 => uint256) public anchoredAt; // "public" lets anyone read the table

    // An "event" is a log entry that the blockchain stores for us, so apps and Etherscan can show it.
    event Anchored(bytes32 indexed hash, address indexed by, uint256 timestamp); // who saved which hash and when

    // anchor() writes a hash into the notebook. Anyone can call it. It costs a little (test) ETH on Sepolia.
    function anchor(bytes32 hash) external { // "external" means it is called from outside the contract
        require(anchoredAt[hash] == 0, "already anchored"); // stop with an error if this hash was saved before
        anchoredAt[hash] = block.timestamp; // save the current block time: this is the proof of "not later than"
        emit Anchored(hash, msg.sender, block.timestamp); // write the log entry (msg.sender = the wallet that called us)
    } // end of anchor()

    // verify() asks: was this hash ever saved? "view" means it only reads, so it is free to call.
    function verify(bytes32 hash) external view returns (bool, uint256) { // returns (found?, time it was saved)
        uint256 savedAt = anchoredAt[hash]; // look the hash up in the table (0 if it was never saved)
        return (savedAt != 0, savedAt); // found = the time is not 0; also hand back the time itself
    } // end of verify()
} // end of the contract
