import json
import os
from pathlib import Path
from web3 import Web3
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

# Load contract data
def load_contract_data():
    contract_file = Path(__file__).parent / 'contract_data' / 'Voting.json'
    
    if not contract_file.exists():
        return None, None
    
    with open(contract_file) as f:
        contract_data = json.load(f)
    
    return contract_data.get('address'), contract_data.get('abi')

# Connect to Ethereum network
def get_web3_connection():
    # Use environment variable or default to localhost
    provider_url = os.environ.get('WEB3_PROVIDER_URL', 'http://127.0.0.1:8545')
    
    try:
        web3 = Web3(Web3.HTTPProvider(provider_url))
        return web3
    except Exception as e:
        print(f"Error connecting to Ethereum network: {e}")
        return None

# Get contract instance
def get_contract():
    web3 = get_web3_connection()
    if not web3:
        return None
    
    address, abi = load_contract_data()
    if not address or not abi:
        return None
    
    try:
        # Create contract instance
        contract = web3.eth.contract(address=address, abi=abi)
        return contract
    except Exception as e:
        print(f"Error creating contract instance: {e}")
        return None

# API view to get candidate count from the contract
@api_view(['GET'])
def candidate_count_view(request):
    contract = get_contract()
    if not contract:
        return Response({"error": "Cannot connect to blockchain contract"}, status=500)
    
    try:
        # Call the smart contract function
        count = contract.functions.getCandidateCount().call()
        return Response({"candidate_count": count})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# Function to add a position to the contract
def add_position(name, private_key=None):
    web3 = get_web3_connection()
    contract = get_contract()
    
    if not web3 or not contract:
        return {"error": "Cannot connect to blockchain"}, False
    
    # Get account to use for transaction
    if private_key:
        account = web3.eth.account.from_key(private_key)
        sender_address = account.address
    else:
        # Use default account if no private key provided
        sender_address = web3.eth.accounts[0]
    
    try:
        # Build transaction
        tx = contract.functions.addPosition(name).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(sender_address),
        })
        
        # Sign and send transaction
        if private_key:
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        else:
            tx_hash = web3.eth.send_transaction(tx)
        
        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {"tx_hash": tx_hash.hex(), "status": receipt.status}, True
    except Exception as e:
        return {"error": str(e)}, False

# Function to add a candidate to the contract
def add_candidate(name, position_id, private_key=None):
    web3 = get_web3_connection()
    contract = get_contract()
    
    if not web3 or not contract:
        return {"error": "Cannot connect to blockchain"}, False
    
    # Get account to use for transaction
    if private_key:
        account = web3.eth.account.from_key(private_key)
        sender_address = account.address
    else:
        # Use default account if no private key provided
        sender_address = web3.eth.accounts[0]
    
    try:
        # Build transaction
        tx = contract.functions.addCandidate(name, position_id).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(sender_address),
        })
        
        # Sign and send transaction
        if private_key:
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        else:
            tx_hash = web3.eth.send_transaction(tx)
        
        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {"tx_hash": tx_hash.hex(), "status": receipt.status}, True
    except Exception as e:
        return {"error": str(e)}, False

# Function for a voter to cast a vote
def cast_vote(candidate_id, voter_address, private_key):
    web3 = get_web3_connection()
    contract = get_contract()
    
    if not web3 or not contract:
        return {"error": "Cannot connect to blockchain"}, False
    
    try:
        # Build transaction
        tx = contract.functions.vote(candidate_id).build_transaction({
            'from': voter_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(voter_address),
        })
        
        # Sign and send transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {"tx_hash": tx_hash.hex(), "status": receipt.status}, True
    except Exception as e:
        return {"error": str(e)}, False

# Get candidate vote count
def get_candidate_votes(candidate_id):
    contract = get_contract()
    if not contract:
        return None
    
    try:
        return contract.functions.getCandidateVotes(candidate_id).call()
    except Exception as e:
        print(f"Error getting candidate votes: {e}")
        return None