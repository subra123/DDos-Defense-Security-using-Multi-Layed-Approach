from web3 import Web3
import pandas as pd
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if not w3.is_connected():  # Correct method name
    raise ConnectionError("Failed to connect to the Ethereum network")

# Use the first account from Ganache
account = w3.eth.accounts[0]

# Load smart contract ABI and address
with open('/home/subramanian/network-traffic-logger/build/contracts/TrafficLogger.json') as file:
    contract_data = json.load(file)

abi = contract_data['abi']
contract_address = '0xcd2Ccf09f237C667acb25dB95f130Bd358DEfBb0'  # Your contract address

# Get the contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# Load the generated traffic logs from CSV
df = pd.read_csv('ddos_traffic_logs.csv')

# Log each entry onto the blockchain
for _, row in df.iterrows():
    classification = "benign" if row['prediction'] == 0 else "attack"
    tx = contract.functions.logTrafficData(
        row['src_ip'], row['dst_ip'], classification, int(pd.Timestamp(row['timestamp']).timestamp())
    ).transact({'from': account})

    # Wait for transaction receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    print(f"Logged traffic: {receipt}")

print("All logs have been sent to the blockchain.")

