import pandas as pd
from web3 import Web3
from datetime import datetime, timedelta
import time
import json
import os
from dotenv import load_dotenv


# Map token names to contract addresses
token_address_map = {
    'rETH': '0xae78736Cd615f374D3085123A210448E74Fc6393'
    # fill with rest
}

# Map market name to "Pool" contract address and abi filepath
contract_address_abi_map = {
    'AAVE': ('0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2', './abi/AAVE_Pool_ABI.json'),
    'COMPOUND': ('0xA17581A9E3356d9A858b789D68B4d866e593aE94', './abi/Compound_ABI.json'),
    'PRISMA': (['0x0d6741f1A3A538F78009ca2e3a13F9cB1478B2d0', './abi/Prisma_TroveManagerNew_ABI.json'],
              ['0xe0e255FD5281bEc3bB8fa1569a20097D9064E445', './abi/Prisma_TroveManagerOld_ABI.json'])
    # fill with rest
}

# Connect to ETH blockchain with infura API key
load_dotenv()
api_key = os.getenv('API_KEY')
infura_url = f'https://mainnet.infura.io/v3/{api_key}'
w3 = Web3(Web3.HTTPProvider(infura_url))


# Find block number closest to timestamp with binary search
def find_block_by_timestamp(target_timestamp):
    low, high = 13325306, w3.eth.block_number
    while low < high:
        mid = (low + high) // 2
        mid_block_timestamp = w3.eth.get_block(mid).timestamp
        if mid_block_timestamp < target_timestamp:
            low = mid + 1
        else:
            high = mid
    return low


# Helper to convert block number to readable timestamp string
def get_block_timestamp(block_num):
    block = w3.eth.get_block(block_num)
    timestamp = block.timestamp

    return timestamp


# Lists transactions of supplying rETH to specified markets
def supply_transactions(market, timeframe=30, token='rETH'):
    """
    Returns all "Supply" transactions for rETH from the specified market over a given timeframe expressed as days.
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
    supply_list = []
    # Lookup token address
    token_address = token_address_map[token]

    # Get timestamp of timeframe provided
    current_time = datetime.now()
    start_time = current_time - timedelta(days=timeframe)
    st_timestamp = int(start_time.timestamp())

    # Find the block associated with our start_time timestamp
    st_block = find_block_by_timestamp(st_timestamp)

    # Make sure the requested market is supported
    if market in contract_address_abi_map.keys():
        # Set up contract address and ABI for each market
        contract_address, abi_filepath = contract_address_abi_map[market]

        if (market != 'PRISMA'):
            # Web3 setup
            with open(abi_filepath) as f:
                abi = json.load(f)

            smart_contract = w3.eth.contract(address=contract_address, abi=abi)
        else:
            smart_contract = []
            with open(contract_address[1]) as f:
                abi = json.load(f)
            smart_contract.append(w3.eth.contract(address=contract_address[0], abi=abi))
            with open(abi_filepath[1]) as f:
                abi = json.load(f)
            smart_contract.append(w3.eth.contract(address=abi_filepath[0], abi=abi))

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
                    'Reserve': event['args']['reserve'],
                    'User (Wallet Address)': event['args']['user'],
                    'Amount (Wei)': event['args']['amount'],
                    'Amount (rETH)': event['args']['amount'] / 10 ** 18,
                    'Timestamp': get_block_timestamp(event['blockNumber']),
                    # This particular line results in an aditional API call
                    'LogIndex': event['logIndex'],
                    'TransactionIndex': event['transactionIndex'],
                    'TransactionHash': event['transactionHash'].hex(),
                    'BlockHash': event['blockHash'].hex(),
                    'BlockNumber': event['blockNumber']
                }
                for event in supplies
            ]
        elif market == 'COMPOUND':
            supplies = smart_contract.events.SupplyCollateral().get_logs(fromBlock=st_block,
                                                                         toBlock='latest',
                                                                         argument_filters={
                                                                             'asset': '0xae78736Cd615f374D3085123A210448E74Fc6393'})
            supply_list = [
                {
                    'Reserve': event['args']['asset'],
                    'User (Wallet Address)': event['args']['from'],
                    'Amount (Wei)': event['args']['amount'],
                    'Amount (rETH)': event['args']['amount'] / 10 ** 18,
                    'Timestamp': get_block_timestamp(event['blockNumber']),
                    # This particular line results in an aditional API call
                    'LogIndex': event['logIndex'],
                    'TransactionIndex': event['transactionIndex'],
                    'TransactionHash': event['transactionHash'].hex(),
                    'BlockHash': event['blockHash'].hex(),
                    'BlockNumber': event['blockNumber']
                }
                for event in supplies
            ]
        elif market == 'PRISMA':
            all_supplies = []
            for contract in smart_contract:
                supplies = contract.events.CollateralSent().get_logs(fromBlock=st_block,
                                                                     toBlock='latest')
                supply_list = [
                    {
                        'Reserve': '0xae78736Cd615f374D3085123A210448E74Fc6393',
                        'User (Wallet Address)': event['args']['_to'],
                        'Amount (Wei)': event['args']['_amount'],
                        'Amount (rETH)': event['args']['_amount'] / 10 ** 18,
                        'Timestamp': get_block_timestamp(event['blockNumber']),
                        # This particular line results in an aditional API call
                        'LogIndex': event['logIndex'],
                        'TransactionIndex': event['transactionIndex'],
                        'TransactionHash': event['transactionHash'].hex(),
                        'BlockHash': event['blockHash'].hex(),
                        'BlockNumber': event['blockNumber']
                    }
                    for event in supplies
                ]
                all_supplies.extend(supply_list)

            supply_list = all_supplies
        else:
            print("UNSUPPORTED MARKET ENTERED")
            return

        # Push supply into dataframe
        recent_supplies = pd.DataFrame(supply_list)
        # recent_supplies['Timestamp'] = pd.to_datetime(recent_supplies[0]['Timestamp'])
        return recent_supplies

    # The market wasn't in our dictionary of supported markets
    else:
        print("UNSUPPORTED MARKET ENTERED")
        return []


"""
The above and below functions are extremely similar, the only difference being the API call they use, 
One function could have been used with some flow control and an additional parameter (User passes in "Borrow" or "Supply"
and the program runs accordingly); however, without knowing how future markets will behave, what their API calls will
exactly look like, and what they will return, it was decided to keep the two separate in case more complex logic is 
needed in handling either case specifically. 
"""


# Lists transactions of borrowing rETH to specified markets
def borrow_transactions(market, timeframe=30, token='rETH'):
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
                    'Reserve': event['args']['reserve'],
                    'User (Wallet Address)': event['args']['user'],
                    'Amount (Wei)': event['args']['amount'],
                    'Amount (rETH)': event['args']['amount'] / 10 ** 18,
                    'Timestamp': get_block_timestamp(event['blockNumber']),
                    # This particular line results in an aditional API call
                    'LogIndex': event['logIndex'],
                    'TransactionIndex': event['transactionIndex'],
                    'TransactionHash': event['transactionHash'].hex(),
                    'BlockHash': event['blockHash'].hex(),
                    'BlockNumber': event['blockNumber']
                }
                for event in borrows
            ]
        elif market == 'COMPOUND':
            print("Compound currently doesn't support borrowing of rETH")
            return
        elif market == 'PRISMA':
            print("Prisma currently doesn't support borrowing of rETH")
            return
        else:
            print("FUTURE MARKETS HERE")
            return

        # Push borrows into dataframe
        recent_borrows = pd.DataFrame(borrow_list)
        # recent_supplies['Timestamp'] = pd.to_datetime(recent_supplies[0]['Timestamp'])
        return recent_borrows
    # The market wasn't in our dictionary of supported markets
    else:
        print("UNSUPPORTED MARKET ENTERED")
        return []

