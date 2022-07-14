import os
import json
from web3 import Web3

from dotenv import load_dotenv

load_dotenv()


# Loading environment variables
pvt_key: str = os.environ.get("PVT_KEY")
rpc_url: str = os.environ.get("RPC_URL")
contract_id: str = os.environ.get("CONTRACT_ID")
admin_account_id: str = os.environ.get("ADMIN_ACCOUNT_ID")

# Connecting using Infura Node
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Initialising the Contract
address = web3.toChecksumAddress(contract_id)
abi = ""
with open(os.getcwd() + "/MudrikaApi/mudrika.json", 'r') as j:
    abi = json.loads(j.read())["abi"]

contract = web3.eth.contract(address=address, abi=abi)

MAX_GAS_ETHER = 0.0005


def add_user_contract(account_id, access_level, name):
    """Adds Signed up user to the contract, using Adduser() signed by admin pvt key"""
    switcher = {
        "admin": 4,
        "national": 3,
        "state": 2,
        "volunteer": 1,
        "public": 0
    }

    account_id = web3.toChecksumAddress(account_id)
    user_type = switcher.get(access_level)

    nonce = web3.eth.get_transaction_count(
        admin_account_id)

    transaction = contract.functions.addUser(
        account_id, user_type, name).build_transaction({
            'chainId': 4,
            'gas': 70000,
            'maxFeePerGas': web3.toWei('2', 'gwei'),
            'maxPriorityFeePerGas': web3.toWei('1', 'gwei'),
            'nonce': nonce,
        })

    gas_price = float(web3.fromWei(web3.eth.gas_price, 'ether'))
    allowed_gas = int(MAX_GAS_ETHER/gas_price)

    transaction.update({'gas': allowed_gas})
    transaction.update({'from': admin_account_id})

    signed_tx = web3.eth.account.sign_transaction(transaction, pvt_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    send_gas_receipt = send_tokens_for_gas(account_id)
    print(send_gas_receipt)

    # print(tx_receipt)
    return tx_receipt


def send_tokens_for_gas(account_id):
    """
    Sends a small amount of tokens to be able to pay for gas for request fund transactions
    """

    nonce = web3.eth.get_transaction_count(admin_account_id)

    transaction = {
        'to': account_id,
        'value': web3.toWei('0.001', 'ether'),
        'chainId': 4,
        'gas': 70000,
        'maxFeePerGas': web3.toWei('2', 'gwei'),
        'maxPriorityFeePerGas': web3.toWei('1', 'gwei'),
        'nonce': nonce,
    }

    signed = web3.eth.account.sign_transaction(transaction, pvt_key)

    try:
        res = web3.eth.send_raw_transaction(signed.rawTransaction)
        print("success")
        return res.hex()

    except Exception as e:
        print(e)


# add_user_contract("0xeD1F0d3e0B33Fab9bc223cd19cE7CC13EA6De62b",
#                   "state", "State #1")
