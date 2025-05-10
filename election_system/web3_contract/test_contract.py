from web3 import Web3
from django.conf import settings
import json

def get_web3_instance():
    return Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))

def get_contract_instance(web3_instance=None):
    if not web3_instance:
        web3_instance = get_web3_instance()
    contract_address = Web3.to_checksum_address(settings.SMART_CONTRACT_ADDRESS)
    contract_abi = json.loads(settings.SMART_CONTRACT_ABI)
    return web3_instance.eth.contract(address=contract_address, abi=contract_abi)

def get_candidate_count_from_contract(position_id):
    w3 = get_web3_instance()
    contract = get_contract_instance(w3)
    return contract.functions.getCandidateCountForPosition(position_id).call()

def get_candidate_details_from_contract(position_id, candidate_id):
    w3 = get_web3_instance()
    contract = get_contract_instance(w3)
    return contract.functions.getCandidate(position_id, candidate_id).call()

def prepare_vote_transaction_data(voter_address, position_id, candidate_id):
    w3 = get_web3_instance()
    contract = get_contract_instance(w3)
    checksum_voter_address = Web3.to_checksum_address(voter_address)
    # This builds the transaction data, but does NOT send it
    transaction_data = contract.functions.vote(position_id, candidate_id).build_transaction({
        'from': checksum_voter_address,
        'nonce': w3.eth.get_transaction_count(checksum_voter_address),
        'chainId': w3.eth.chain_id
        # Gas can often be estimated by the wallet, or you can provide estimates
    })
    # Remove fields the wallet should handle, like 'gas', 'gasPrice'
    # if 'gas' in transaction_data: del transaction_data['gas']
    # if 'gasPrice' in transaction_data: del transaction_data['gasPrice']
    return transaction_data