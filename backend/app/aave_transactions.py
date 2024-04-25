import pandas as pd
import json
from web3 import Web3
from datetime import datetime, timedelta
import time
import sys
import json
from collections import Counter

# Map token names to contract addresses
token_address_map = {
    'rETH': '0xae78736Cd615f374D3085123A210448E74Fc6393'
    # fill with rest
}

# Map market name to "Pool" contract address and abi filepath
contract_address_abi_map = {
    'AAVE': ('0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2', './AAVE_Pool_ABI.json')
    # fill with rest
}

# Connect to ETH blockchain with infura API key
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/7e4f5238262543919688a59d0fef4a1d'))

# Find block number closest to timestamp with binary search
def find_block_by_timestamp(target_timestamp):
    low, high = 0, w3.eth.block_number
    while low < high:
        mid = (low + high) // 2
        mid_block_timestamp = w3.eth.get_block(mid).timestamp
        if mid_block_timestamp < target_timestamp:
            low = mid+1
        else:
            high = mid
    return low


# Helper to convert block number to readable timestamp string
def get_block_timestamp(block_num):
    block = w3.eth.get_block(block_num)
    timestamp = block.timestamp
    
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')



# Lists transactions of supplying rETH to specified markets
def supply_transactions(markets = ['AAVE'], timeframe = 30, token = 'rETH'):
    """
    Returns all "Supply" transactions for rETH from the specified markets over a given timeframe expressed as days.
        (Example: supply_transactions(AAVE, 90, rETH) returns all supply transactions for rETH on the AAVE market in the past 90 days
        
    Parameters:
    - markets (str): The lending and borrowing market from which to fetch data. Defaults to 'AAVE'.
    - timeframe (int): The number of days back from the current date to fetch data. Defaults to 90 days.
    - token (str): The token we want to see supply transactions for. Defaults to rETH
    
    Returns:
    pandas.DataFrame: A DataFrame where each row corresponds to a unique supply transaction with the following columns:
        - 'User (Wallet Address)': The address for the user who initiated the transaction
        - 'Amount (Wei)': The amount supplied expressed in Wei
        - 'Amount (rETH)': The amount supplied expressed in rETH
        - 'Timestamp': The timestamp in 'YYYY-MM-DD HH:MM:SS' format.
        - 'LogIndex': The log index
        - 'TransactionIndex': The transaction index
        - 'TransactionHash': The hash for the transaction
        - 'BlockHash': The hash for the block
        - 'BlockNumber': The block number
    
    """
    # List for supply_lists of all markets
    all_market_supply_list = []
    
    # Lookup token address
    token_address = token_address_map[token]
    
    # Get timestamp of timeframe provided
    current_time = datetime.now()
    start_time = current_time - timedelta(days=timeframe)
    st_timestamp = int(start_time.timestamp())
    
    # Find the block associated with our start_time timestamp
    st_block = find_block_by_timestamp(st_timestamp)
    
    # Start processing supply API calls for each market
    for market in markets:
        # Make sure the requested market is supported
        if market in contract_address_abi_map.keys():
            # Set up contract address and ABI for each market
            contract_address, abi_filepath = contract_address_abi_map[market]
    
            # Web3 setup
            with open(abi_filepath) as f:
                abi = json.load(f)

            smart_contract = w3.eth.contract(address=contract_address, abi=abi)
            
            # Here we will need some sort of if/else or switching logic to process unique calls for each market
            # In the meantime, we simply check for the only supported market, 'AAVE'
            if market == 'AAVE':
                supplies = smart_contract.events.Supply().get_logs(fromBlock=st_block,
                                                           toBlock='latest',
                                                           argument_filters={'reserve': token_address})
                # Consider simplifying supply_list.. don't know what information future markets will return, 
                # ... Will most likely trim this down to: Reserve, User, Amount (in token, not Wei), Timestamp, and block number
                supply_list = [
                    {
                        'reserve': event['args']['reserve'],
                        'user': event['args']['user'],
                        'amount': event['args']['amount']/10**18,
                        'timestamp': get_block_timestamp(event['blockNumber']), # This particular line results in an aditional API call
                        'log_index': event['logIndex'],
                        'transaction_index': event['transactionIndex'],
                        'transaction_hash': event['transactionHash'].hex(),
                        'block_hash': event['blockHash'].hex(),
                        'block_number': event['blockNumber']
                    }
                    for event in supplies
                ]
                # Append each markets supply list results to a single all markets list
                all_market_supply_list.append(supply_list)
        # The market wasn't in our dictionary of supported markets
        else:
            print("UNSUPPORTED MARKET ENTERED")
            
    # Push withdrawls into dataframe
    recent_supplies = pd.DataFrame(all_market_supply_list[0])
    #recent_supplies['Timestamp'] = pd.to_datetime(recent_supplies[0]['Timestamp'])
    return recent_supplies


"""
The above and below functions are extremely similar, the only difference being the API call they use, 
One function could have been used with some flow control and an additional parameter (User passes in "Borrow" or "Supply"
and the program runs accordingly); however, without knowing how future markets will behave, what their API calls will
exactly look like, and what they will return, it was decided to keep the two separate in case more complex logic is 
needed in handling either case specifically. 
"""



# Lists transactions of borrowing rETH to specified markets
def borrow_transactions(markets = ['AAVE'], timeframe = 30, token = 'rETH'):
    """
    Returns all "Borrow" transactions for rETH from the specified markets over a given timeframe expressed as days.
        (Example: borrow_transactions(AAVE, 90, rETH) returns all borrow transactions for rETH on the AAVE market in the past 90 days
        
    Parameters:
    - markets (str): The lending and borrowing market from which to fetch data. Defaults to 'AAVE'.
    - timeframe (int): The number of days back from the current date to fetch data. Defaults to 90 days.
    - token (str): The token we want to see supply transactions for. Defaults to rETH
    
    Returns:
    pandas.DataFrame: A DataFrame where each row corresponds to a unique borrow transaction with the following columns:
        - 'User (Wallet Address)': The address for the user who initiated the transaction
        - 'Amount (Wei)': The amount supplied expressed in Wei
        - 'Amount (rETH)': The amount supplied expressed in rETH
        - 'Timestamp': The timestamp in 'YYYY-MM-DD HH:MM:SS' format.
        - 'LogIndex': The log index
        - 'TransactionIndex': The transaction index
        - 'TransactionHash': The hash for the transaction
        - 'BlockHash': The hash for the block
        - 'BlockNumber': The block number
    
    """
    # List for borrow_lists of all markets
    all_market_borrow_list = []
    
    # Lookup token address
    token_address = token_address_map[token]
    
    # Get timestamp of timeframe provided
    current_time = datetime.now()
    start_time = current_time - timedelta(days=timeframe)
    st_timestamp = int(start_time.timestamp())
    
    # Find the block associated with our start_time timestamp
    st_block = find_block_by_timestamp(st_timestamp)
    
    # Start processing supply API calls for each market
    for market in markets:
        # Make sure the requested market is supported
        if market in contract_address_abi_map.keys():
            # Set up contract address and ABI for each market
            contract_address, abi_filepath = contract_address_abi_map[market]
    
            # Web3 setup
            with open(abi_filepath) as f:
                abi = json.load(f)

            smart_contract = w3.eth.contract(address=contract_address, abi=abi)
            
            # Here we will need some sort of if/else or switching logic to process unique calls for each market
            # In the meantime, we simply check for the only supported market, 'AAVE'
            if market == 'AAVE':
                borrows = smart_contract.events.Borrow().get_logs(fromBlock=st_block,
                                                           toBlock='latest',
                                                           argument_filters={'reserve': token_address})
                # Consider simplifying borrow_list.. don't know what information future markets will return, 
                # ... Will most likely trim this down to: Reserve, User, Amount (in token, not Wei), Timestamp, and block number
                borrow_list = [
                    {
                        'reserve': event['args']['reserve'],
                        'user': event['args']['user'],
                        'amount': event['args']['amount']/10**18,
                        'timestamp': get_block_timestamp(event['blockNumber']), # This particular line results in an aditional API call
                        'log_index': event['logIndex'],
                        'transaction_index': event['transactionIndex'],
                        'transaction_hash': event['transactionHash'].hex(),
                        'block_hash': event['blockHash'].hex(),
                        'block_number': event['blockNumber']
                    }
                    for event in borrows
                ]
                # Append each markets supply list results to a single all markets list
                all_market_borrow_list.append(borrow_list)
        # The market wasn't in our dictionary of supported markets
        else:
            print("UNSUPPORTED MARKET ENTERED")
            
    # Push withdrawls into dataframe
    recent_borrows = pd.DataFrame(all_market_borrow_list[0])
    #recent_supplies['Timestamp'] = pd.to_datetime(recent_supplies[0]['Timestamp'])
    return recent_borrows
    
recent_supply = supply_transactions()
print(recent_supply)