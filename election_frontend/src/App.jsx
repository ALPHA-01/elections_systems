// App.js
import './App.css';
import CandidatesList from './components/CandidatesList ';

function App() {
  return (
    <div className="App">
      <header>
        <h1>Decentralized Voting System</h1>
      </header>
      <main>
        <CandidatesList />
      </main>
    </div>
  );
}

export default App;