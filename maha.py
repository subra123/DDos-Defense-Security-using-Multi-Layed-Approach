import random
from web3 import Web3
import pandas as pd
import json
from IPython.display import FileLink

def process_and_store_logs():
    # Load and process data from the CSV file
    df = pd.read_csv('traffic_logs.csv')

    # Define a list of mitigation strategies
    mitigation_strategies = [
        "IP blocking (Non Legit)",
        "Rate Limiting (Legit)",
        "Rerouting (Legit)",
        "Increase Bandwidth (Legit)",
        "Auto-Scaling for Legitimate Traffic (Legit)",
        "IP Blacklisting (Non Legit)",
        "DNS-based Blackhole List (Non Legit)"
    ]

    # Define a function to simulate reinforcement learning and return a mitigation strategy
    def get_mitigation_action(row):
        return random.choice(mitigation_strategies)

    # Initialize the mitigation_steps column with "No action"
    df['mitigation_steps'] = "No action"

    # Identify the anomalous traffic
    anomalous_traffic_indices = df[df['prediction'] == 1].index

    # Assign mitigation steps to anomalous traffic
    df.loc[anomalous_traffic_indices, 'mitigation_steps'] = df.loc[anomalous_traffic_indices].apply(get_mitigation_action, axis=1)

    # Save the updated DataFrame to a new CSV file
    updated_file = 'updated_ddos_traffic_logs.csv'
    df.to_csv(updated_file, index=False)

    # Provide a download link for the updated file (for Jupyter notebooks or similar environments)
    FileLink(updated_file)

    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    if not w3.is_connected():
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
    df = pd.read_csv(updated_file)

    # Log each entry onto the blockchain
    for _, row in df.iterrows():
        classification = "benign" if row['prediction'] == 0 else "attack"
        tx = contract.functions.logTrafficData(
            row['src_ip'], row['dst_ip'], classification, int(pd.Timestamp(row['timestamp']).timestamp())
        ).transact({'from': account})

        # Wait for transaction receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        
        # Print a formatted summary of the transaction
        print(f"Transaction Hash: {receipt['transactionHash'].hex()}")
        print(f"Block Number: {receipt['blockNumber']}")
        print(f"Gas Used: {receipt['gasUsed']}")
        print(f"Status: {'Success' if receipt['status'] == 1 else 'Failed'}")
        print("-" * 40)

    print("All logs have been sent to the blockchain.")

# Connect to Ganache (or any Ethereum node)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Check if connected to the Ethereum network
if w3.is_connected():
    print("Connected to Ethereum network.")
    
    # Get the latest block number
    latest_block = w3.eth.block_number
    print(f"Latest block number: {latest_block}")

    # Define the maximum number of blocks to process
    max_blocks = 10  # Change this to your desired number

    # Loop through blocks from genesis to the latest block, but stop after max_blocks
    for block_num in range(1, min(latest_block + 1, max_blocks + 1)):
        # Get the block details
        block = w3.eth.get_block(block_num)
        print(f"Processing block {block_num}...")

        # Randomly set trigger to True or False
        trigger = random.choice([True, False])

        # Select a random row from the dataset for each block
        df = pd.read_csv('dataset_without_predictions.csv')  # Reload the dataset inside the loop
        row = df.sample().iloc[0]
        mitigation = row['mitigation_steps']  # Fetch the mitigation steps from the CSV

        if trigger:
            print(f"Block {block_num}: Log exists on blockchain. Mitigation: {mitigation}")
        else:
            print(f"Block {block_num}: Log does not exist on blockchain. Processing with ML model...")
            process_and_store_logs()
else:
    print("Failed to connect to the Ethereum network. Stopping the operation.")


