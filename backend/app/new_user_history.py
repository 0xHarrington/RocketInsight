import pandas as pd
import json
from web3 import Web3
from datetime import datetime, timedelta
import time
import sys
import json
from collections import Counter

# Connect to ETH blockchain with infura API key
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/5f0c4998d7544ee1bb3f0dc297a6821c'))

# AAVE V3 ETH Mainnet Market Pool Address
contract_addr = '0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2'

# Load ABI
with open("./AAVE_Pool_ABI.json") as f:
    pool_abi = json.load(f)
    
# Load Contract
aave_pool_contract = w3.eth.contract(address=contract_addr, abi=pool_abi)

def get_initial_depo_blockNum(aave_pool_contract, user_wallet_address):
    """
    Finds the lowest block number for rETH supply events related to a given user wallet address for AAVE v3.

    Parameters:
    - aave_pool_contract: The Aave pool contract instance from Web3.py.
    - user_wallet_address: The wallet address of the user as a string.

    Returns:
    - The lowest block number for the given user wallet address. Returns None if the user has no supply events.
    """
    # For some reason it doesnt work when user filter vs onBehalfOf
    log_filter = {
        'reserve': '0xae78736Cd615f374D3085123A210448E74Fc6393', #rETH token address
        'onBehalfOf': user_wallet_address,
    }
    
    logs = aave_pool_contract.events.Supply().get_logs(fromBlock='earliest',
                                                       toBlock='latest',
                                                       argument_filters=log_filter)
    if not logs:
        return 0
    
    return min(log['blockNumber'] for log in logs)

def fetch_logs(user_address_filter, aave_pool_contract, event_name, block_step = 100000):
    """
    Fetches logs for transactions filtered by user address and event type, from the latest block down to initial rETH deposit.

    Parameters:
    - user_address_filter: The user wallet address to filter the logs.
    - aave_pool_contract: The contract object to fetch logs from.
    - event_name: The name of the event to fetch {'Borrow', 'Repay', 'Withdraw', 'FlashLoan'}
    - block_step: The number of blocks to step back in each iteration (default is 100000).

    Returns:
    - A dataframe of formatted logs.
    """
    
    # Get target block
    target_block = get_initial_depo_blockNum(aave_pool_contract, user_address_filter)
    
    print(f'For User: {user_address_filter}\nFrom Block: {target_block}')

    # Dynamic print
    print(f'Fetching {event_name} events', end='')
    sys.stdout.flush()

    # Variables for looping
    logged_results = []
    target_log_count = float('inf')
    current_block = w3.eth.block_number    # Latest Block Number

    # Time
    start = time.time()

    # Loop counter
    iter_count = 0

    # Loop until target number reached or at first block
    while (len(logged_results) < target_log_count and current_block > target_block):
        print('.', end='')

        from_block = max(current_block - block_step, target_block)
        time.sleep(0.2)
        
        try:
            # Access event
            event = getattr(aave_pool_contract.events, event_name)()
            
            # Fetch logs for the current block
            if (event_name == 'FlashLoan'):
                current_logs = event.get_logs(
                    fromBlock=from_block,
                    toBlock=current_block,
                    argument_filters={'initiator': user_address_filter}
                )
            elif (event_name == 'Borrow'):
                current_logs = event.get_logs(
                    fromBlock=from_block,
                    toBlock=current_block,
                    argument_filters={'onBehalfOf': user_address_filter}
                )
            elif (event_name == 'Withdraw'):
                current_logs = event.get_logs(
                    fromBlock=from_block,
                    toBlock=current_block,
                    argument_filters={'to': user_address_filter}
                )
            else: #repay
                current_logs = event.get_logs(
                    fromBlock=from_block,
                    toBlock=current_block,
                    argument_filters={'user': user_address_filter}
                )

            # Format event logs
            for event in current_logs:
                formatted_log = format_event_log(event, event_name)

                # Add to aggregate log list
                logged_results.append(formatted_log)

            # Decrement block number
            current_block = from_block - 1

        except Exception as e:
            # Print exception and block number and break
            print(f"\nError fetching logs for block {current_block}: {e}")
            break

        # Increment iter
        iter_count += 1

    # Print time
    print('\nFetching complete.')
    print(f'Time Elapsed: {time.time() - start}\n')

    # Trim list
    if len(logged_results) > target_log_count:
           logged_results = logged_results[-target_log_count:]

    # Return dataframed logs
    return pd.DataFrame(logged_results)

def format_event_log(event, event_name):
    """
    Formats the log of an event based on its type.

    Parameters:
    - event: The event log to format.
    - event_name: The name of the event.

    Returns:
    - A dictionary containing formatted log attributes.
    """
    
    # Format common attrs
    log = {
        'event_type': event_name,
        'transaction_hash': event['transactionHash'].hex(),
        'address': event['address'],
        'block_hash': event['blockHash'].hex(),
        'block_number': event['blockNumber'],
    }
    
    # if else tree for event specific attrs
    if event_name == 'Withdraw':
        log.update({
            'reserve': event['args']['reserve'],
            'user': event['args']['user'],
            'to': event['args']['to'],
            'amount': event['args']['amount']/10**18
        })
        
    elif event_name == 'Borrow':
        log.update({
            'reserve': event['args']['reserve'],
            'on_behalf_of': event['args']['onBehalfOf'],
            'user': event['args']['user'],
            'amount': event['args']['amount']/10**18,
            'borrow_rate': event['args']['borrowRate']/10**27
        })
        
    elif event_name == 'Repay':
        log.update({
            'reserve': event['args']['reserve'],
            'user': event['args']['user'],
            'repayer': event['args']['repayer'],
            'amount': event['args']['amount']/10**18,
            'use_atokens': str(event['args']['useATokens']),
            
        })
        
    elif event_name == 'FlashLoan':
        log.update({
            'target': event['args']['target'],
            'asset': event['args']['asset'],
            'referral_code': str(event['args']['referralCode']),
            'initiator': event['args']['initiator'],
            'amount': event['args']['amount']/10**18,
            'premium': event['args']['premium']
        })
    
    return log

# Map market name to pool contract address and abi filepath
contract_address_abi_map = {
    'AAVE': ('0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2', './AAVE_Pool_ABI.json')
    # fill with rest
}

def user_history(user_addresses, markets):
    """
    Fetches the interaction history of users with specified lending and borrowing markets.
    
    Parameters:
    - user_addresses: List of user wallet addresses.
    - markets: List of market names to scrape.
    
    Returns:
    - A dictionary mapping each user address to a list of dataframes (one for each interaction type).
    """
    interaction_history = {user: [] for user in user_addresses}
    event_types = ['Withdraw', 'Borrow', 'Repay', 'FlashLoan']
    
    # Loop markets
    for market in markets:
        # Lookup contract address and abi filepath
        contract_address, abi_filepath = contract_address_abi_map[market]
        
        # Web3 setup
        with open(abi_filepath) as f:
            abi = json.load(f)

        smart_contract = w3.eth.contract(address=contract_address, abi=abi)
        
        # Loop user addresses
        for user_address in user_addresses:
            # Loop event types
            for event_type in event_types:
                logs_df = fetch_logs(user_address, smart_contract, event_type, block_step = 250000)
                interaction_history[user_address].append(logs_df)
            
    return interaction_history
    
    # TEST USER HISTORY

# Load wallet address data for testing
user_wallet_addresses = ['0xc83894aC498289E54FBE523c0ABFcbac8CeB1CaB',
                         '0x1A415A3b77ED38B683Db945dc83F53ECda26F716',
                         '0xecCaCB54ffF224316f0ba589760624186FcbeA27']

interaction_list = user_history(user_wallet_addresses, ['AAVE'])

all_dfs = []

for key, dfs_list in interaction_list.items():
    # Concatenate all DataFrames in the list for the current wallet address
    combined_df = pd.concat(dfs_list, ignore_index=True)
    all_dfs.append(combined_df)

# Concatenate all combined DataFrames into one
final_df = pd.concat(all_dfs, ignore_index=True)
print(final_df.head())