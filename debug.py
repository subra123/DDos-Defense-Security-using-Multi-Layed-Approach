from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Check connection
if not w3.is_connected():
    print("Failed to connect to the Ethereum network")
    exit()

print("Connected to Ethereum network")

# Load ABI and contract address
try:
    with open('/home/subramanian/network-traffic-logger/build/contracts/TrafficLogger.json') as file:
        contract_data = json.load(file)
        abi = contract_data['abi']
        # Manually set contract address since network key is missing
        contract_address = "0xYourContractAddress"  # Replace with your contract address
except FileNotFoundError as e:
    print(f"Error loading ABI file: {e}")
    exit()
except json.JSONDecodeError as e:
    print(f"Error decoding JSON file: {e}")
    exit()
except KeyError as e:
    print(f"Missing key in ABI file: {e}")
    # Manually set contract address if network key is missing
    contract_address = "0xYourContractAddress"  # Replace with your contract address
    print("Using manual contract address")

# Get contract instance
try:
    contract = w3.eth.contract(address=contract_address, abi=abi)
    print("Contract instance created successfully")
except Exception as e:
    print(f"Error creating contract instance: {e}")
    exit()

# Test function calls

# Call trafficLogsLength
try:
    length = contract.functions.trafficLogsLength().call()
    print(f"Number of traffic logs in the contract: {length}")
except Exception as e:
    print(f"Error calling trafficLogsLength function: {e}")

# Call getTrafficData for a specific index
index = 0  # Example index, adjust as needed
try:
    if index < length:  # Ensure index is within bounds
        data = contract.functions.getTrafficData(index).call()
        print(f"Traffic data at index {index}: {data}")
    else:
        print(f"Index {index} is out of bounds. Length of logs: {length}")
except Exception as e:
    print(f"Error calling getTrafficData function: {e}")

# Call trafficLogs for a specific index (if needed)
try:
    if index < length:  # Ensure index is within bounds
        log = contract.functions.trafficLogs(index).call()
        print(f"Traffic log at index {index}: {log}")
except Exception as e:
    print(f"Error calling trafficLogs function: {e}")

# Example to log traffic data (for testing)
try:
    tx_hash = contract.functions.logTrafficData(
        "192.168.1.8", "10.0.0.6", "suspicious", 1725962411
    ).transact({'from': w3.eth.accounts[0]})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {receipt}")
except Exception as e:
    print(f"Error calling logTrafficData function: {e}")

