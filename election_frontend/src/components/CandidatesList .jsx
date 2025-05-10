import { useState } from 'react';
import useContract from '../hooks/useContract';

const CandidatesList = () => {
  const {  loading, error, castVote } = useContract();
  const [candidates, setCandidates] = useState([
    { id: 0, name: "Alice", votes: 0 },
    { id: 1, name: "Bob", votes: 0 }
  ]);
  const [activeVote, setActiveVote] = useState(null);

  const handleVote = async (candidateId) => {
    try {
      setActiveVote(candidateId);
      await castVote(candidateId);  // Now this will work
      // Update local state
      setCandidates(prev => prev.map(c => 
        c.id === candidateId ? { ...c, votes: c.votes + 1 } : c
      ));
    } catch (err) {
      console.error("Voting failed:", err);
    } finally {
      setActiveVote(null);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="candidate-list">
      <h2>Candidates</h2>
      <div className="candidates-grid">
        {candidates.map(candidate => (
          <div key={candidate.id} className="candidate-card">
            <h3>{candidate.name}</h3>
            <p>Votes: {candidate.votes}</p>
            <button
              onClick={() => handleVote(candidate.id)}
              disabled={activeVote === candidate.id}
            >
              {activeVote === candidate.id ? 'Voting...' : 'Vote'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CandidatesList;