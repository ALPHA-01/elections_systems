import { useState } from 'react';
import useContract from '../hooks/useContract';

const Voting = () => {
  const { candidates, castVote, addCandidate, loading, error } = useContract();
  const [newCandidateName, setNewCandidateName] = useState('');
  const [activeVote, setActiveVote] = useState(null);

  const handleVote = async (candidateId) => {
    setActiveVote(candidateId);
    try {
      await castVote(candidateId);
    } catch (err) {
      alert(err.message);
    } finally {
      setActiveVote(null);
    }
  };

  const handleAddCandidate = async () => {
    if (!newCandidateName.trim()) return;
    try {
      await addCandidate(newCandidateName);
      setNewCandidateName('');
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="voting-container">
      <h1>Voting System</h1>
      
      {/* Add Candidate Form */}
      <div className="add-candidate">
        <input
          value={newCandidateName}
          onChange={(e) => setNewCandidateName(e.target.value)}
          placeholder="New candidate name"
        />
        <button onClick={handleAddCandidate}>Add Candidate</button>
      </div>

      {/* Candidates List */}
      <div className="candidates-grid">
        {candidates.map(candidate => (
          <div key={candidate.id} className="candidate-card">
            <h3>{candidate.name}</h3>
            <p>Votes: {candidate.votes.toString()}</p>
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

export default Voting;