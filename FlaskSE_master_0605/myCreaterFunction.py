import json
from web3 import Web3

# Fill in your infura API key here
w3 = Web3(Web3.HTTPProvider('HTTP://172.20.224.1:7545'))

w3.eth.default_account = w3.eth.accounts[0]

compiled_contract_path = '/home/william11ya/IPad/block-chain/build/contracts/VotingSystem.json'

deployed_contract_address = '0x24733aad54221517DFc7d891bE0d577dc48ABf14'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = w3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)

def CreateVote(voteName, candidateNames, endTime):
    Create = contract.functions.CreateVote(voteName, candidateNames, endTime).transact()
    runCreate = w3.eth.wait_for_transaction_receipt(Create)

def getVoteIndex(voteName):
    exist = contract.functions.getVoteIndex(voteName).call()
    return exist

CreateVote("wdsd",["q","w"],1000)

print(getVoteIndex("wdsd"))

#create = contract.functions.CreateVote("學生會2",["A","B"],2000).transact() 
#runcreater = w3.eth.wait_for_transaction_receipt(create)

print(w3.is_connected())
