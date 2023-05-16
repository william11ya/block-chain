from web3 import Web3

w3 = Web3(Web3.HTTPProvider('HTTP://localhost:9545'))

print(w3.is_connected())