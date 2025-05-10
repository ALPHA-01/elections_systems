import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import contractAddress from '../contracts/contract-address.json';
import VotingArtifact from '../contracts/Voting.json';

const useContract = () => {
  const [contract, setContract] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      const provider = new ethers.JsonRpcProvider("http://localhost:8545");
      const signer = await provider.getSigner(0);
      
      const votingContract = new ethers.Contract(
        contractAddress.Voting, // Using deployed address
        VotingArtifact.abi,
        signer
      );

      // Load candidates
      const count = await votingContract.getCandidateCount();
      const loadedCandidates = [];
      for (let i = 0; i < count; i++) {
        const candidate = await votingContract.candidates(i);
        loadedCandidates.push({
          id: Number(candidate.id),
          name: candidate.name,
          votes: Number(candidate.votes)
        });
      }
      
      setCandidates(loadedCandidates);
      setContract(votingContract);
      setLoading(false);
    };

    init();
  }, []);

  const castVote = async (candidateId) => {
    const tx = await contract.vote(candidateId);
    await tx.wait();
    // Refresh candidates after voting
    const candidate = await contract.candidates(candidateId);
    setCandidates(prev => prev.map(c => 
      c.id === candidateId ? { ...c, votes: Number(candidate.votes) } : c
    ));
  };

  return { candidates, castVote, loading };
};

export default useContract;