from web3 import Web3

# Fill in your infura API key here
w3 = Web3(Web3.HTTPProvider('HTTP://172.20.224.1:7545'))

w3.eth.default_account = w3.eth.accounts[0]

compiled_contract_path = '/home/william11ya/IPad/block-chain/build/contracts/VotingSystem.json'

deployed_contract_address = '0xFa4DeC91f513cdBd7Cf22089a51da0C646e6775b'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = w3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)

def CreateVote(voteName, candidateNames, endTime):
    Create = contract.functions.CreateVote(voteName, candidateNames, endTime).transact()
    runCreate = w3.eth.wait_for_transaction_receipt(Create)

def getVoteIndex(voteName):
    exist = contract.functions.getVoteIndex("學生").call()
    return exist


#create = contract.functions.CreateVote("學生會2",["A","B"],2000).transact() 
#runcreater = w3.eth.wait_for_transaction_receipt(create)
print(type(exist))
print(exist)

print(w3.is_connected())
