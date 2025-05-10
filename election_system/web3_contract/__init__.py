from web3 import Web3
import json

# Connect to local Hardhat node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Replace with your actual contract address from deployment
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# Paste your ABI here or load from a .json file
abi = [ ... ]  # <-- Paste the ABI here

# Connect to contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# Check connection
print("Connected:", w3.isConnected())

# Call a public variable: candidatesCount
count = contract.functions.candidatesCount().call()
print("Number of candidates:", count)
