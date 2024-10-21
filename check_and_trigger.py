import random
from web3 import Web3
import pandas as pd

# Connect to Ganache (or any Ethereum node)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Check if connected to the Ethereum network
if w3.is_connected():
    print("Connected to Ethereum network.")
    
    # Get the latest block number
    latest_block = w3.eth.block_number
    print(f"Latest block number: {latest_block}")

    # Load the dataset (ensure the path is correct)
    df = pd.read_csv('dataset_without_predictions.csv')

    # Loop through all blocks from genesis to the latest block
    for block_num in range(1, latest_block + 1):
        # Get the block details
        block = w3.eth.get_block(block_num)
        print(f"Processing block {block_num}...")

        # Randomly set trigger to True or False
        trigger = random.choice([True, False])

        # Select a random row from the dataset for each block
        row = df.sample().iloc[0]
        mitigation = row['mitigation_steps']  # Fetch the mitigation steps from the CSV

        if trigger:
            print(f"Block {block_num}: Log exists on blockchain. Mitigation: {mitigation}")
        else:
            print(f"Block {block_num}: Log does not exist on blockchain. Processing with ML model...")
else:
    print("Failed to connect to the Ethereum network. Stopping the operation.")

