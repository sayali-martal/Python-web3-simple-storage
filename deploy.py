from __future__ import nested_scopes
from eth_typing import Address
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")

# Compile the solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# Save compiled solidity code
with open("CompiledCode.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# For connecting to Ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/9bc8e378720b42338ae7b57e2f7e8e29")
)
chain_id = 4
my_address = "0xE00C7Dc45875099E49CE2415b7604eb69A4B41f1"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build te contract deploy transaction
# 2. Sign the transaction
# 3. Send  the transaction
# 3. Wait  for the transaction receipt
print("Deploying Contract")
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Deployed")

# Working with contract needs
# 1. Address
# 2. ABI
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)
# Initial value of favorite number
print("Initial value: " + str(simple_storage.functions.retrieve().call()))
print("Updating contract")
store_transaction = simple_storage.functions.store(20).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,  # As nonce is already used
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("Updated")
print("Updated value: " + str(simple_storage.functions.retrieve().call()))
