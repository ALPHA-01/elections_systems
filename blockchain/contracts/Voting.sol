// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Voting {
    event Voted(uint indexed candidateId, uint newVoteCount);
    
    struct Candidate {
        uint id;
        string name;
        uint votes;
    }

    Candidate[] public candidates;
    address public owner;

    constructor() {
        owner = msg.sender;
        // Initialize with default candidates
        candidates.push(Candidate(0, "Alice", 0));
        candidates.push(Candidate(1, "Bob", 0));
    }

    function addCandidate(string memory name) public {
        require(msg.sender == owner, "Only owner can add candidates");
        candidates.push(Candidate(candidates.length, name, 0));
    }

    function vote(uint candidateId) public {
        require(candidateId < candidates.length, "Invalid candidate ID");
        candidates[candidateId].votes++;
        emit Voted(candidateId, candidates[candidateId].votes);
    }

    function getAllCandidates() public view returns (Candidate[] memory) {
        return candidates;
    }

    function getCandidateCount() public view returns (uint) {
        return candidates.length;
    }
}