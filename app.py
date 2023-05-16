# from flask import Flask, render_template
# from web3 import Web3
# import json

# # 建立與 Ganache 本地區塊鏈的連接
# w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# # 載入 Solidity 智能合約 ABI
# with open('bin/contracts/SimpleStorage.json') as f:
#     abi = json.load(f)['abi']

# # 設定智能合約地址
# contract_address = '0x72E6E4a21B68Efed620001Eda0F4bdC4df158d0B'

# app = Flask(__name__)

# # 建立智能合約實例
# contract = w3.eth.contract(address=contract_address, abi=abi)


# # 定義一個 API 接口，用於設置狀態變量的值
# @app.route('/set_value/<value>')
# def set_value(value):
#     tx_hash = contract.functions.setValue(value).transact()
#     w3.eth.waitForTransactionReceipt(tx_hash)
#     return 'Value set to ' + value

# # 定義一個 API 接口，用於讀取狀態變量的值
# @app.route('/get_value')
# def get_value():
#     value = contract.functions.value().call()
#     return 'Value is ' + str(value)

# # 定義一個路由，用於顯示狀態變量的值
# @app.route('/')
# def index():
#     value = contract.functions.value().call()
#     return render_template('index.html', value=value)

# @app.errorhandler(500)
# def server_error(e):
#     print(e)
#     return 'An internal server error occurred.', 500

# if __name__ == '__main__':
#     app.run(debug=True)

import json
from web3 import Web3
# Fill in your infura API key here
w3 = Web3(Web3.HTTPProvider('HTTP://172.20.224.1:7545'))

w3.eth.default_account = w3.eth.accounts[0]

compiled_contract_path = '/home/william11ya/IPad/block-chain/build/contracts/VotingSystem.json'

deployed_contract_address = '0xB8831C820d2101ec08d4E0B321D2F391c58de716'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = w3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)

#create = contract.functions.CreateVote("學生會2",["A","B"],2000).transact() 
#runcreater = w3.eth.wait_for_transaction_receipt(create)
exist = contract.functions.getVoteIndex("學生").call()

print(type(exist))
print(exist)

print(w3.is_connected())

