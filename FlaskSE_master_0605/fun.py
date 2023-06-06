import json
from web3 import Web3

# Fill in your infura API key here
w3 = Web3(Web3.HTTPProvider('HTTP://172.20.224.1:7545'))

w3.eth.default_account = w3.eth.accounts[4]

compiled_contract_path = '/home/william11ya/IPad/block-chain/build/contracts/VotingSystem.json'

deployed_contract_address = '0x4F3859C14be08c0274739D589Dcb9C4B970B42E2'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = w3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)

def CreateVote(voteName, candidateNames, endTime):
    Create = contract.functions.CreateVote(voteName, candidateNames, endTime).transact()
    runCreate = w3.eth.wait_for_transaction_receipt(Create)

def getVoteIndex(voteName):
    exist = contract.functions.getVoteIndex("").call()
    return exist

def getAllRunningVote():
    get = contract.functions.getAllEndedVote().call()
    return get

#votecandidate = contract.functions.vote(0, 1).transact()
#runvotecandidate = w3.eth.wait_for_transaction_receipt(votecandidate)
# Settle = contract.functions.settle(0).call()

x = getAllRunningVote()
for i in x:
    print(i)

# runCreate = w3.eth.wait_for_transaction_receipt(Create)
#create = contract.functions.CreateVote("學生會2",["A","B"],2000).transact() 
#runcreater = w3.eth.wait_for_transaction_receipt(create)

print(w3.is_connected())

