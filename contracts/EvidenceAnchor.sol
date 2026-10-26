// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Stores SHA-256 hashes of incident reports with the time they were anchored.
contract EvidenceAnchor {
    mapping(bytes32 => uint256) public anchoredAt; // 0 means "not anchored"

    event Anchored(bytes32 indexed hash, address indexed by, uint256 timestamp);

    function anchor(bytes32 hash) external {
        require(anchoredAt[hash] == 0, "already anchored");
        anchoredAt[hash] = block.timestamp;
        emit Anchored(hash, msg.sender, block.timestamp);
    }

    // Returns (found, timestamp)
    function verify(bytes32 hash) external view returns (bool, uint256) {
        uint256 t = anchoredAt[hash];
        return (t != 0, t);
    }
}
