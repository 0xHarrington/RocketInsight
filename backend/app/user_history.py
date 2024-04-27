import pandas as pd
from web3 import Web3
import time
import sys
import json
import os
from dotenv import load_dotenv

# Map token names to contract addresses
token_address_map = {
    'rETH': '0xae78736Cd615f374D3085123A210448E74Fc6393'
    # fill with rest
}

# Map market name to contract address and abi filepath
contract_address_abi_map = {
    'AAVE': ('0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2', './abi/AAVE_Pool_ABI.json'),
    'COMPOUND': ('0xA17581A9E3356d9A858b789D68B4d866e593aE94', './abi/Compound_ABI.json'),
    'PRISMA': [('0x4591DBfF62656E7859Afe5e45f6f47D3669fBB28', './abi/mkUSD_ABI.json'), ('0xae78736Cd615f374D3085123A210448E74Fc6393', './abi/rETH_ABI.json')]
    # fill with rest
}

# Connect to ETH blockchain with infura API key
load_dotenv()
api_key = os.getenv('API_KEY')
infura_url = f'https://mainnet.infura.io/v3/{api_key}'
w3 = Web3(Web3.HTTPProvider(infura_url))


def get_initial_depo_blockNum(market, market_contract, user_wallet_address, token='rETH'):
    """
    Finds the lowest block number for rETH supply events related to a given user wallet address for a particular market.

    Parameters:
    - market: The specific market from our list of supported markets to analyze.
    - market_contract: The market pool contract instance from Web3.py.
    - user_wallet_address: The wallet address of the user as a string.
    - token: The specific reserve token to analyze (Defaults to rETH).

    Returns:
    - The lowest block number for the given user wallet address. Returns None if the user has no supply events.
    """
    # Lookup token address
    token_address = token_address_map[token]

    # Make sure the requested market is supported
    if market in contract_address_abi_map.keys():

        if market == 'AAVE':
            # For some reason it doesnt work when user filter vs onBehalfOf
            log_filter = {
                'reserve': token_address,  # rETH token address
                'onBehalfOf': user_wallet_address,
            }

            # Get logs for all supply events for rETH on behalf of this particular user_wallet_address
            logs = market_contract.events.Supply().get_logs(fromBlock='earliest',
                                                            toBlock='latest',
                                                            argument_filters=log_filter)
            # In the case that there were no events
            if not logs:
                return 0

        elif market == 'COMPOUND':
            log_filter = {
                'asset': token_address,  # rETH token address
                'from': user_wallet_address,
            }

            # Get logs for all supply events for rETH on behalf of this particular user_wallet_address
            logs = market_contract.events.SupplyCollateral().get_logs(fromBlock='earliest',
                                                                      toBlock='latest',
                                                                      argument_filters=log_filter)
            # In the case that there were no events
            if not logs:
                return 0

        elif market == 'PRISMA':
            # Using rETH token contract as market_contract here

            # Gather logs of rETH transfers to the two rETH trove managers
            logs = market_contract.events.Transfer().get_logs(fromBlock='earliest',
                                                              toBlock='latest',
                                                              argument_filters={'from': user_wallet_address,
                                                                                'to': '0x0d6741f1A3A538F78009ca2e3a13F9cB1478B2d0'})

            logs += market_contract.events.Transfer().get_logs(fromBlock='earliest',
                                                               toBlock='latest',
                                                               argument_filters={'from': user_wallet_address,
                                                                                 'to': '0xe0e255FD5281bEc3bB8fa1569a20097D9064E445'})

            # In the case that there were no events
            if not logs:
                return 0

    # The market wasn't in our dictionary of supported markets
    else:
        # print("UNSUPPORTED MARKET ENTERED")
        return

    return min(log['blockNumber'] for log in logs)


def fetch_logs(market, market_contract, user_address_filter, event_name, block_step=100000):
    """
    Fetches logs for transactions filtered by user address and event type, from the latest block down to initial rETH deposit.

    Parameters:
    - market: The particular market we want to fetch logs from.
    - market_contract: The contract object to fetch logs from.
    - user_address_filter: The user wallet address to filter the logs.
    - event_name: The name of the event to fetch {'Borrow', 'Repay', 'Withdraw', 'FlashLoan'}
    - block_step: The number of blocks to step back in each iteration (default is 100000).

    Returns:
    - A dataframe of formatted logs.
    """

    # Get target block
    if market == 'PRISMA':
        target_block = get_initial_depo_blockNum(market, market_contract[1], user_address_filter)
    else:
        target_block = get_initial_depo_blockNum(market, market_contract, user_address_filter)

    if target_block == 0:
        # print(f'User: {user_address_filter} returned no events of type: {event_name}')
        return pd.DataFrame()

    # print(f'For User: {user_address_filter}\nFrom Block: {target_block}')

    # Dynamic print
    # print(f'Fetching {event_name} events', end='')
    sys.stdout.flush()

    # Variables for looping
    logged_results = []
    target_log_count = float('inf')
    current_block = w3.eth.block_number  # Latest Block Number

    # Time
    start = time.time()

    # Loop counter
    iter_count = 0

    # Use while loop based on market --> possible event types (No reason to search for aave market events when we know we're looking for compound events)
    if market == 'AAVE':
        # Loop until target number reached or at first block
        while (len(logged_results) < target_log_count and current_block > target_block):
            # print('.', end='')

            from_block = max(current_block - block_step, target_block)

            try:
                # Access event
                event = getattr(market_contract.events, event_name)()

                # Fetch logs for the current block -- AAVE
                if (event_name == 'FlashLoan'):
                    current_logs = event.get_logs(
                        fromBlock=from_block,
                        toBlock=current_block,
                        argument_filters={'initiator': user_address_filter}
                    )
                elif (event_name == 'Supply'):
                    current_logs = event.get_logs(
                        fromBlock=from_block,
                        toBlock=current_block,
                        argument_filters={'user': user_address_filter}
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
                elif (event_name == 'Repay'):
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
                # print(f"\nError fetching logs for block {current_block}: {e}")
                break

            # Increment iter
            iter_count += 1

    elif market == 'COMPOUND':
        # Loop until target number reached or at first block
        while (len(logged_results) < target_log_count and current_block > target_block):
            # print('.', end='')

            from_block = max(current_block - block_step, target_block)

            try:
                # Access event
                event = getattr(market_contract.events, event_name)()

                # Fetch logs from the current block -- COMPOUND
                if (event_name == 'Withdraw'):
                    current_logs = event.get_logs(
                        fromBlock=from_block,
                        toBlock=current_block,
                        argument_filters={'to': user_address_filter}
                    )
                elif (event_name == 'SupplyCollateral'):
                    current_logs = event.get_logs(
                        fromBlock=from_block,
                        toBlock=current_block,
                        argument_filters={'from': user_address_filter}
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
                # print(f"\nError fetching logs for block {current_block}: {e}")
                break

            # Increment iter
            iter_count += 1

    elif market == 'PRISMA':
        # Loop until target number reached or at first block
        while (len(logged_results) < target_log_count and current_block > target_block):
            # USING mkUSD token contract here to track interactions with stability pool
            # print('.', end='')

            from_block = max(current_block - block_step, target_block)

            try:
                # Access event
                event = getattr(market_contract[0].events, event_name)()

                # Fetch logs from the current block -- PRISMA
                if (event_name == 'Transfer'):
                    # Catch provide events
                    provide_logs = event.get_logs(
                        fromBlock=from_block,
                        toBlock=current_block,
                        argument_filters={'from': user_address_filter,
                                          'to': '0xed8B26D99834540C5013701bB3715faFD39993Ba'}
                    )

                    # Catch withdraw events
                    withdraw_logs = event.get_logs(
                        fromBlock=from_block,
                        toBlock=current_block,
                        argument_filters={'from': '0xed8B26D99834540C5013701bB3715faFD39993Ba',
                                          'to': user_address_filter}
                    )

                # Format event logs
                for event in provide_logs:
                    formatted_log = format_event_log(event, 'provide-sp')

                    # Add to aggregate log list
                    logged_results.append(formatted_log)

                for event in withdraw_logs:
                    formatted_log = format_event_log(event, 'withdraw-sp')

                    # Add to aggregate log list
                    logged_results.append(formatted_log)

                # Decrement block number
                current_block = from_block - 1

            except Exception as e:
                # Print exception and block number and break
                # print(f"\nError fetching logs for block {current_block}: {e}")
                break

            # Increment iter
            iter_count += 1

    # Print time
    # print('\nFetching complete.')
    # print(f'Time Elapsed: {time.time() - start}\n')

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
        'Event Type': event_name,
        'Transaction Hash': event['transactionHash'].hex(),
        'Address': event['address'],
        'Block Hash': event['blockHash'].hex(),
        'Block Number': event['blockNumber'],
    }

    # if else tree for event specific attrs -- AAVE
    if event_name == 'Withdraw':
        cETH_addr = '0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5'
        reserve = event['args'].get('reserve', cETH_addr)
        user = event['args'].get('user', event['args']['to'])

        log.update({
            'Reserve': reserve,
            'User': user,
            'To': user,
            'Amount': event['args']['amount']
        })

    elif event_name == 'Supply':
        log.update({
            'Reserve': event['args']['reserve'],
            'User': event['args']['user'],
            'Amount': event['args']['amount']
        })

    elif event_name == 'Borrow':
        log.update({
            'Reserve': event['args']['reserve'],
            'On Behalf Of': event['args']['onBehalfOf'],
            'User': event['args']['user'],
            'Amount': event['args']['amount'],
            'Borrow Rate': event['args']['borrowRate']
        })

    elif event_name == 'Repay':
        log.update({
            'Reserve': event['args']['reserve'],
            'User': event['args']['user'],
            'Repayer': event['args']['repayer'],
            'Amount': event['args']['amount'],
            'useAtokens': str(event['args']['useATokens']),

        })

    elif event_name == 'FlashLoan':
        log.update({
            'Target': event['args']['target'],
            'Asset': event['args']['asset'],
            'Referral Code': str(event['args']['referralCode']),
            'Initiator': event['args']['initiator'],
            'Amount': event['args']['amount'],
            'Premium': event['args']['premium']
        })

    elif event_name == 'SupplyCollateral':
        log.update({
            'Reserve': event['args']['asset'],
            'User': event['args']['from'],
            'To': event['args']['dst'],
            'Amount': event['args']['amount']
        })

    elif event_name == 'withdraw-sp':
        log['Event Type'] = 'Withdraw(Prisma)'
        log.update({
            'Reserve': '0x4591DBfF62656E7859Afe5e45f6f47D3669fBB28',
            'User': event['args']['to'],
            'Address': event['args']['from'],
            'Amount': event['args']['value']
        })

    elif event_name == 'provide-sp':
        log['Event Type'] = 'Provide'
        log.update({
            'Reserve': '0x4591DBfF62656E7859Afe5e45f6f47D3669fBB28',
            'User': event['args']['from'],
            'Address': event['args']['to'],
            'Amount': event['args']['value']
        })

    return log


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
    aave_event_types = ['Supply', 'Withdraw', 'Borrow', 'Repay', 'FlashLoan']
    compound_event_types = ['Withdraw', 'SupplyCollateral']
    prisma_event_types = ['Transfer']
    # Loop markets
    for market in markets:
        # Verify market entry is valid
        if market not in contract_address_abi_map.keys():
            print("UNSUPPORTED MARKET ENTERED")
            return []

        if market == 'PRISMA':
            smart_contract = []

            # Need to configure two separate contracts
            market_tups = contract_address_abi_map[market]

            # mkUSD contract for fetch logs function
            mkUSD_address, mkUSD_abi = market_tups[0]

            with open(mkUSD_abi) as f:
                abi = json.load(f)

            smart_contract.append(w3.eth.contract(address=mkUSD_address, abi=abi))

            # rETH contract for earliest depot function
            rETH_address, rETH_abi = market_tups[1]

            with open(rETH_abi) as f:
                abi = json.load(f)

            smart_contract.append(w3.eth.contract(address=rETH_address, abi=abi))

        else:
            # Lookup contract address and abi filepath
            contract_address, abi_filepath = contract_address_abi_map[market]

            # Web3 setup
            with open(abi_filepath) as f:
                abi = json.load(f)

            smart_contract = w3.eth.contract(address=contract_address, abi=abi)

        if market == 'AAVE':
            # Loop user addresses
            for user_address in user_addresses:
                # Loop event types
                for event_type in aave_event_types:
                    logs_df = fetch_logs(market, smart_contract, user_address, event_type, block_step=75000)

                    if logs_df.empty:
                        pass
                    else:
                        interaction_history[user_address].append(logs_df)

        elif market == 'COMPOUND':
            # Loop user addresses
            for user_address in user_addresses:
                # Loop event types
                for event_type in compound_event_types:
                    logs_df = fetch_logs(market, smart_contract, user_address, event_type, block_step=75000)

                    if logs_df.empty:
                        pass
                    else:
                        interaction_history[user_address].append(logs_df)

        elif market == 'PRISMA':
            # Loop user addresses
            for user_address in user_addresses:
                # Loop event types
                for event_type in prisma_event_types:
                    logs_df = fetch_logs(market, smart_contract, user_address, event_type, block_step=75000)

                    if logs_df.empty:
                        pass
                    else:
                        interaction_history[user_address].append(logs_df)

    return interaction_history
