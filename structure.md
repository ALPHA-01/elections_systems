# Blockchain Election System

A decentralized voting application built with Django, React, and Ethereum smart contracts (using Hardhat).

## Project Structure

```
election-system/
├── backend/                     # Django backend
│   ├── election_system/         # Django project
│   │   ├── core/                # Core app
│   │   │   ├── voting_main/     # Main voting functionality
│   │   │   │   ├── ethereum_interface.py  # Interface to interact with smart contracts
├── frontend/                    # Vite + React frontend
│   ├── src/
│   │   ├── contracts/           # Contract ABIs after compilation
│   │   ├── hooks/               # React hooks for contract interaction
├── blockchain/                  # Hardhat project for smart contracts
│   ├── contracts/               # Solidity contracts
│   ├── scripts/                 # Deployment scripts
```

## Prerequisites

1. Node.js (v16+ recommended)
2. Python 3.8+
3. Django 4.0+
4. MetaMask browser extension

## Installation

### 1. Set up environment variables

Copy the example environment file and fill in your details:

```bash
cd blockchain
cp .env.example .env
# Edit .env with your values
```

### 2. Install dependencies

From the project root:

```bash
# Install blockchain dependencies
npm run setup:blockchain

# Install frontend dependencies
npm run setup:frontend

# Create and activate Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Django dependencies
cd backend
pip install -r requirements.txt
```

### 3. Initialize the database

```bash
cd backend
python manage.py migrate
```

## Running the Development Environment

The easiest way to run everything is with our development script:

```bash
npm run dev
```

This will:
1. Start a local Hardhat node
2. Deploy the contracts to the local node
3. Start the Django backend server
4. Start the Vite development server for the frontend

Alternatively, you can run each component separately:

```bash
# Run the blockchain node
npm run blockchain

# In a separate terminal, deploy contracts
npm run deploy

# In a separate terminal, run the Django backend
npm run backend

# In a separate terminal, run the frontend
npm run frontend
```

## Connecting MetaMask

1. Open MetaMask in your browser
2. Add a new network with these settings:
   - Network Name: Hardhat Local
   - New RPC URL: http://127.0.0.1:8545
   - Chain ID: 1337
   - Currency Symbol: ETH

3. Import one of the test accounts that Hardhat generates with its corresponding private key

## Usage

1. Visit http://localhost:5173 in your browser
2. Connect your MetaMask wallet when prompted
3. Browse available positions and candidates
4. Cast your vote!

## Smart Contract Interaction

The application interacts with the Voting smart contract through:

1. Django's `ethereum_interface.py` - For admin functions like adding positions and candidates
2. React's `useContract.js` hook - For voter functions like casting votes

## Production Deployment

For production deployment:

1. Deploy your contracts to a testnet or mainnet:
   ```bash
   cd blockchain
   npx hardhat run scripts/deploy.js --network sepolia
   ```

2. Update the contract address in your Django settings
3. Configure your Django app for production (HTTPS, proper settings, etc.)
4. Build your React app with `npm run build` in the frontend directory
5. Serve both Django and React from a production web server (like Nginx)

## License

MIT