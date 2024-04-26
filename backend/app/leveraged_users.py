# Imports
import time
import pandas as pd
import json
from web3 import Web3
from datetime import datetime, timedelta
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
    'AAVE_WBP': ('0xC7be5307ba715ce89b152f3Df0658295b3dbA8E2', './abi/WalletBalanceProvider_ABI.json'),
    'COMPOUND': ('0xA17581A9E3356d9A858b789D68B4d866e593aE94', './abi/Compound_ABI.json'),
    'PRISMA': (['0x0d6741f1A3A538F78009ca2e3a13F9cB1478B2d0', './abi/Prisma_TroveManagerNew_ABI.json'],
               ['0xe0e255FD5281bEc3bB8fa1569a20097D9064E445', './abi/Prisma_TroveManagerOld_ABI.json']),
    'PRISMA_MTG': ('0x58fa5521f48b258B5e48A56b9B1bd95bFFA1eb1C', './abi/Prisma_MultiTroveGetter_ABI.json'),
    'mkUSD': ('0x4591DBfF62656E7859Afe5e45f6f47D3669fBB28', './abi/mkUSD_ABI.json')
    # fill with rest
}

# The address for the token we are trying to see the balances for, in this case the receipt token of rETH - "aethrETH"
# Verified --> Pulled "AaveV3Ethereum" contract address from AAVE address book: https://search.onaave.com/
# When V3 isn't available, next active version is used
receipt_tokens = {
    'AAVE': {
        'rETH': ('0xCc9EE9483f662091a1de4795249E24aC0aC2630f', 'aethrETH'),
        # Verified https://etherscan.io/token/0xcc9ee9483f662091a1de4795249e24ac0ac2630f
        'USDT': ('0x23878914EFE38d27C4D67Ab83ed1b93A74D4086a', 'aEthUSDT'),
        # Verified https://etherscan.io/address/0x23878914EFE38d27C4D67Ab83ed1b93A74D4086a
        'USDC': ('0xBcca60bB61934080951369a648Fb03DF4F96263C', 'aUSDC'),
        # No V3 version available on address book: https://etherscan.io/address/0xBcca60bB61934080951369a648Fb03DF4F96263C
        'DAI': ('0x018008bfb33d285247A21d44E50697654f754e63', 'aEthDAI'),
        # Verified: https://etherscan.io/address/0x018008bfb33d285247A21d44E50697654f754e63
        'WBTC': ('0x5Ee5bf7ae06D1Be5997A1A72006FE6C607eC6DE8', 'aEthWBTC'),
        # Verified: https://etherscan.io/address/0x5Ee5bf7ae06D1Be5997A1A72006FE6C607eC6DE8
        'WETH': ('0x030bA81f1c18d280636F32af80b9AAd02Cf0854e', 'aWETH')
        # No V3 version available on address book: https://etherscan.io/address/0x030bA81f1c18d280636F32af80b9AAd02Cf0854e
    },

    'COMPOUND': {
        # Couldn't find "Compound rETH" contract so currently using a generic "Compound Collateral" contract
        'rETH': ('0xae78736Cd615f374D3085123A210448E74Fc6393', 'rETH'),
        # Verified, has "balanceOf": https://etherscan.io/token/0x70e36f6BF80a52b3B46b3aF8e106CC0ed743E8e4
        'cETH': ('0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5', 'cETH'),
        # Verified, has "balanceOf": https://etherscan.io/token/0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5#code
        'cWETH': ('0xA17581A9E3356d9A858b789D68B4d866e593aE94', 'cWETHv3'),
        # Doesn't include "balanceOf". Seems like an administrative contract, every interaction involves a NULL address
        'WETH': ('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH')
        # Found that this is included in the Compound GitHub: https://github.com/compound-finance/comet/blob/main/deployments/mainnet/weth/configuration.json

    },

    'PRISMA': {
        'mkUSD': ('0x4591DBfF62656E7859Afe5e45f6f47D3669fBB28', 'mkUSD'),
        'ETH': ('filler nonsense', 'ETH')
    }
}

# Connect to ETH blockchain with infura API key
load_dotenv()
api_key = os.getenv('API_KEY')
infura_url = f'https://mainnet.infura.io/v3/{api_key}'
w3 = Web3(Web3.HTTPProvider(infura_url))

import re

code = '''
AAVE: POOL_ADDRESSES_PROVIDER = IPoolAddressesProvider(0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e);
AAVE: POOL = IPool(0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2);
AAVE: POOL_IMPL = 0x5FAab9E1adbddaD0a08734BE8a52185Fd6558E14;
AAVE: POOL_CONFIGURATOR = IPoolConfigurator(0x64b761D848206f447Fe2dd461b0c635Ec39EbB27);
AAVE: POOL_CONFIGURATOR_IMPL = 0xFDA7ffA872bDc906D43079EA134ebC9a511db0c2;
AAVE: ORACLE = IAaveOracle(0x54586bE62E3c3580375aE3723C145253060Ca0C2);
AAVE: PROTOCOL_DATA_PROVIDER = IPoolDataProvider(0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3);
AAVE: ACL_MANAGER = IACLManager(0xc2aaCf6553D20d1e9d78E365AAba8032af9c85b0);
AAVE: ACL_ADMIN = 0x5300A1a15135EA4dc7aD5a167152C01EFc9b192A;
AAVE: COLLECTOR = ICollector(0x464C71f6c2F760DdA6093dCB91C24c39e5d6e18c);
AAVE: DEFAULT_INCENTIVES_CONTROLLER = 0x8164Cc65827dcFe994AB23944CBC90e0aa80bFcb;
AAVE: DEFAULT_A_TOKEN_IMPL_REV_1 = 0x7EfFD7b47Bfd17e52fB7559d3f924201b9DbfF3d;
AAVE: DEFAULT_VARIABLE_DEBT_TOKEN_IMPL_REV_1 = 0xaC725CB59D16C81061BDeA61041a8A5e73DA9EC6;
AAVE: DEFAULT_STABLE_DEBT_TOKEN_IMPL_REV_1 = 0x15C5620dfFaC7c7366EED66C20Ad222DDbB1eD57;
AAVE: EMISSION_MANAGER = 0x223d844fc4B006D67c0cDbd39371A9F73f69d974;
AAVE: CAPS_PLUS_RISK_STEWARD = 0x82dcCF206Ae2Ab46E2099e663F70DeE77caE7778;
AAVE: FREEZING_STEWARD = 0x2eE68ACb6A1319de1b49DC139894644E424fefD6;
AAVE: DEBT_SWAP_ADAPTER = 0x8761e0370f94f68Db8EaA731f4fC581f6AD0Bd68;
AAVE: DELEGATION_AWARE_A_TOKEN_IMPL_REV_1 = 0x21714092D90c7265F52fdfDae068EC11a23C6248;
AAVE: CONFIG_ENGINE = 0xA3e44d830440dF5098520F62Ebec285B1198c51E;
AAVE: POOL_ADDRESSES_PROVIDER_REGISTRY = 0xbaA999AC55EAce41CcAE355c77809e68Bb345170;
AAVE: RATES_FACTORY = 0xcC47c4Fe1F7f29ff31A8b62197023aC8553C7896;
AAVE: REPAY_WITH_COLLATERAL_ADAPTER = 0x02e7B8511831B1b02d9018215a0f8f500Ea5c6B3;
AAVE: STATIC_A_TOKEN_FACTORY = 0x411D79b8cC43384FDE66CaBf9b6a17180c842511;
AAVE: SWAP_COLLATERAL_ADAPTER = 0xADC0A53095A0af87F3aa29FE0715B5c28016364e;
AAVE: UI_GHO_DATA_PROVIDER = 0x379c1EDD1A41218bdbFf960a9d5AD2818Bf61aE8;
AAVE: UI_INCENTIVE_DATA_PROVIDER = 0x162A7AC02f547ad796CA549f757e2b8d1D9b10a6;
AAVE: UI_POOL_DATA_PROVIDER = 0x91c0eA31b49B69Ea18607702c5d9aC360bf3dE7d;
AAVE: WALLET_BALANCE_PROVIDER = 0xC7be5307ba715ce89b152f3Df0658295b3dbA8E2;
AAVE: WETH_GATEWAY = 0x893411580e590D62dDBca8a703d61Cc4A8c7b2b9;
AAVE: WITHDRAW_SWAP_ADAPTER = 0x78F8Bd884C3D738B74B420540659c82f392820e0;
AAVE: SAVINGS_DAI_TOKEN_WRAPPER = 0xE28E2c8d240dd5eBd0adcab86fbD79df7a052034;
AAVE: WRAPPED_TOKEN_GATEWAY = 0xD322A49006FC828F9B5B37Ab215F99B4E5caB19C;
COMPOUND: POOL = 0xA17581A9E3356d9A858b789D68B4d866e593aE94;
PRISMA: POOL = 0xed8B26D99834540C5013701bB3715faFD39993Ba;
'''

# Split the string into lines
lines = code.split('\n')

known_addresses = {}
for line in lines:
    # Splitting the line into variable name and the rest
    parts = line.split('=')
    if len(parts) == 2:
        variable_name = parts[0].strip()
        # Extracting the Ethereum address
        ethereum_address = re.search(r'0x[a-fA-F0-9]{40}', parts[1])
        if ethereum_address:
            known_addresses[ethereum_address.group()] = variable_name


# Find block number closest to timestamp with binary search
def find_block_by_timestamp(target_timestamp):
    low, high = 0, w3.eth.block_number
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

    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


# Lists transactions of supplying rETH to specified markets
def supply_transactions(market, timeframe=90, token='rETH'):
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

# Function was made due to an error in processing "WETH". Due to the coingecko returning a slighly different contract address value,
# ... A solution had to be made that assumed no knowledge of the dict key value (Couldn't use "WETH_price_data[receipt_tokens['WETH'][0].lower()]", because the key
# ... in "WETH_price_data" doesn't match our entry in "receipt_tokens['WETH'][0]"
def process_inner_dict(outer_dict):
    """
    Processes dictionary returned by coingecko API to return the USD value held in the inner dictionary

    Parameters:
    - dictionary returned by coingecko API

    Returns:
    - USD value from inner dict
    """
    for inner_dict in outer_dict.values():
        if 'usd' in inner_dict:
            usd_value = inner_dict['usd']
            return usd_value
        else:
            print("INVALID DICTIONARY - No 'usd' key found in inner dictionary")


import requests


def fetch_price(market, asset):
    time.sleep(15)
    """
    Given an asset from our dictionary of receipt_tokens (important assets), returns the current price of the asset on coingecko

    Parameters:
    - asset: The receipt token we want the price for

    Returns:
    - Current market price for the asset
    """
    # Verify asset parameter
    if asset not in receipt_tokens[market].keys():
        print("INVALID ASSET")
        return

    if ((market == 'PRISMA') and (asset == 'ETH')):
        price_response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
        price_data = price_response.json()
    else:
        price_response = requests.get(
            "https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses={}&vs_currencies=usd".format(
                receipt_tokens[market][asset][0]))
        price_data = price_response.json()
        # print(price_data)

    asset_price = process_inner_dict(price_data)
    # Another way that is more 'pythonic', but assumes knowledge of the key -- In the case that coingecko doesn't return exactly the same address as what we supplied, this method won't work
    # asset_price = price_data[receipt_tokens[asset][0].lower()]['usd']
    return asset_price


def leveraged_users_by_market(market, supplied_transactions, token='rETH'):
    """
    Creates dataframe of leveraged users from a particular market. This is a modified version of the above leveraged_users function which may be more useful.
    This function can be called once for each supported market to achieve a similar output as the original function, but with the ability to distinguish results by market.

    Parameters:
    - market: The market to analyze for leveraged users

    Returns:
    - A dataframe of formatted logs.
    """
    # List used for tracking significant wallets
    positive_balances = []
    USD_balances = []
    sus_users = []

    # Isolate user wallets from our list of recent supply transactions
    unique_users = list(set(supplied_transactions['User (Wallet Address)']))

    # If the passed in dataframe had no users --> No wallet addresses to process --> Return empty list
    if not unique_users:
        return []

    # Remove known/benign wallets: Only concerns AAVE for now
    for wallet in unique_users:
        if wallet in known_addresses.keys():
            unique_users.remove(wallet)

    # Make sure the requested market is supported - Our dictionary of receipt tokens contains one key for each supported market
    if market in receipt_tokens.keys():
        # Lookup token address, contract address, and abi filepath
        token_address = token_address_map[token]

        ############################# START: This line to the "Web3 setup" portion deals with loading contracts and their ABIs ###############
        if market == 'AAVE':
            contract_address, abi_filepath = contract_address_abi_map['AAVE_WBP']

        elif market == 'PRISMA':
            contract_address, abi_filepath = contract_address_abi_map['PRISMA_MTG']

            mk_address, mk_abi = contract_address_abi_map['mkUSD']
            with open(mk_abi) as f:
                abi = json.load(f)

            mk_contract = w3.eth.contract(address=mk_address, abi=abi)

        elif market == 'COMPOUND':
            contract_address, abi_filepath = contract_address_abi_map[market]

        # Shouldn't even possible to reach this else, as we've verified that the market entered is valid already
        else:
            print("INVALID MARKET ENTERED")
            return []

        # Web3 setup
        with open(abi_filepath) as f:
            abi = json.load(f)

        smart_contract = w3.eth.contract(address=contract_address, abi=abi)
        ############################ END: Finished processing contracts #######################################################################

        ############################ START: Processing "unique_users" based on market entered and the smart contract loaded ###################
        if market == 'PRISMA':
            # Retrieve real-time price information from assets for leverage calculation
            mkUSD_price = fetch_price('PRISMA', 'mkUSD')
            rETH_price = fetch_price('PRISMA', 'ETH')  # Isn't actually the rETH price but the price of ETH

            # Use MultiTroveGetter function: GetMultipleSortedTroves to retrieve all wallets w/ positive balances from both troves
            # Prisma is unique from other markets in the sense that it doesn't need to use the provided list of "unique_users"...
            # ... we can directly get the current list of users w/ positive balances
            trove1 = smart_contract.functions.getMultipleSortedTroves('0x0d6741f1A3A538F78009ca2e3a13F9cB1478B2d0', 0,
                                                                      1000000).call()
            trove2 = smart_contract.functions.getMultipleSortedTroves('0xe0e255FD5281bEc3bB8fa1569a20097D9064E445', 0,
                                                                      1000000).call()
            users = trove1 + trove2

            # For each user w/ a positive rETH balance...
            for user in users:
                # print("For User: " + str(user))
                # ...Calculate mkUSD and rETH balances using their trove
                mkUSD_USD_balance = ((mk_contract.functions.balanceOf(user[0]).call()) / 10 ** 18) * mkUSD_price
                # print("   mkUSD: " + str(mkUSD_USD_balance))

                rETH_USD_balance = (user[2] / 10 ** 18) * rETH_price
                # print("   rETH: " + str(rETH_USD_balance))

                # Checking for leveraged users based on our thresholds
                if ((rETH_USD_balance > 0.00) and (mkUSD_USD_balance > 0.00)):
                    formatted_log = {
                        'User (Wallet Address)': user[0],
                        'rETH Balance': user[2] / 10 ** 18,
                        'mkUSD Balance': mkUSD_USD_balance,
                    }
                    # Append the log to our record of USD balances and add the user to our list of sus users
                    USD_balances.append(formatted_log)
                    sus_users.append(user[0])

            # Turn USD balances into a dataframe and return our list of users
            sus_wallets_usd = pd.DataFrame(USD_balances)
            return sus_users

        if market == 'AAVE':
            # Retrieve real-time price information from assets for leverage calculation
            rETH_price = fetch_price('AAVE', 'rETH')
            USDT_price = 1.00
            USDC_price = 1.00
            DAI_price = 1.00
            WBTC_price = fetch_price('AAVE', 'WBTC')
            WETH_price = fetch_price('AAVE', 'WETH')

            # Iterate through each wallet address and get the balance for rETH token and critical assets in USD
            for wallet_address in unique_users:
                # print("For User: " + str(wallet_address))
                # Output from balanceOf is in wei, convert to true value using "/10**18"
                rETH_USD_balance = ((smart_contract.functions.balanceOf(wallet_address, receipt_tokens['AAVE']['rETH'][
                    0]).call()) / 10 ** 18) * rETH_price
                # print("   rETH: " + str(rETH_USD_balance))

                USDT_USD_balance = ((smart_contract.functions.balanceOf(wallet_address, receipt_tokens['AAVE']['USDT'][
                    0]).call()) / 10 ** 18) * USDT_price
                # print("   USDT: " + str(USDT_USD_balance))

                USDC_USD_balance = ((smart_contract.functions.balanceOf(wallet_address, receipt_tokens['AAVE']['USDC'][
                    0]).call()) / 10 ** 18) * USDC_price
                # print("   USDC: " + str(USDC_USD_balance))

                DAI_USD_balance = ((smart_contract.functions.balanceOf(wallet_address, receipt_tokens['AAVE']['DAI'][
                    0]).call()) / 10 ** 18) * DAI_price
                # print("   DAI: " + str(DAI_USD_balance))

                WBTC_USD_balance = ((smart_contract.functions.balanceOf(wallet_address, receipt_tokens['AAVE']['WBTC'][
                    0]).call()) / 10 ** 18) * WBTC_price
                # print("   WBTC: " + str(WBTC_USD_balance))

                WETH_USD_balance = ((smart_contract.functions.balanceOf(wallet_address, receipt_tokens['AAVE']['WETH'][
                    0]).call()) / 10 ** 18) * WETH_price
                # print("   WETH: " + str(WETH_USD_balance))

                net_asset_borrow = USDT_USD_balance + USDC_USD_balance + DAI_USD_balance + WBTC_USD_balance + WETH_USD_balance
                # print("   Net asset total: " + str(net_asset_borrow))

                # Checking for leveraged users based on our thresholds
                if ((rETH_USD_balance > 0.00) and (net_asset_borrow > 0.00)):
                    formatted_log = {
                        'User (Wallet Address)': wallet_address,
                        'rETH Balance': rETH_USD_balance,
                        'USDT Balance': USDT_USD_balance,
                        'USDC Balance': USDC_USD_balance,
                        'DAI Balance': DAI_USD_balance,
                        'WBTC Balance': WBTC_USD_balance,
                        'WETH Balance': WETH_USD_balance,
                        'Net Asset Borrow': net_asset_borrow
                    }
                    # Append the log to our record of USD balances and add the user to our list of sus users
                    USD_balances.append(formatted_log)
                    sus_users.append(wallet_address)

            # Turn USD balances into a dataframe and return our list of users
            sus_wallets_usd = pd.DataFrame(USD_balances)
            return sus_users

        elif market == 'COMPOUND':
            # Retrieve real-time price information from assets for leverage calculation
            rETH_price = fetch_price('COMPOUND', 'rETH')
            ETH_price = fetch_price('PRISMA',
                                    'ETH')  # Use these parameters whenever we want the actual price of ETH, not a "aToken" or "cToken", like "aeth" or "ceth".

            # Iterate through each wallet address and get the balance for rETH token and critical assets
            for wallet_address in unique_users:
                # print("For User: " + str(wallet_address))
                borrow_balance = ((smart_contract.functions.borrowBalanceOf(
                    wallet_address).call()) / 10 ** 18) * ETH_price
                # print("   borrow balance: " + str(borrow_balance))

                rETH_USD_balance = ((smart_contract.functions.collateralBalanceOf(wallet_address,
                                                                                  receipt_tokens['COMPOUND']['rETH'][
                                                                                      0]).call()) / 10 ** 18) * rETH_price
                # print("   rETH: " + str(rETH_USD_balance))

                # Checking for leveraged users based on our thresholds
                if ((rETH_USD_balance > 0.00) and (borrow_balance > 0.00)):
                    formatted_log = {
                        'User (Wallet Address)': wallet_address,
                        'rETH Balance': rETH_USD_balance,
                        'Net Asset Borrow': borrow_balance
                    }
                    # Append the log to our record of USD balances and add the user to our list of sus users
                    USD_balances.append(formatted_log)
                    sus_users.append(wallet_address)

            # If reached, we should have modified our USD_balances dictionary based on the market requested, return dataframe
            sus_wallets_usd = pd.DataFrame(USD_balances)
            return sus_users

        # Again, shouldn't be possible to reach this error...
        else:
            print("UNSUPPORTED MARKET ENTERED")
            return []
        ############################ END: Processing "unique_users" based on market entered and the smart contract loaded #####################

    # The market string entered didn't match any of the keys in our "receipt_tokens" dictionary --> Not a valid market
    else:
        print("UNSUPPORTED MARKET ENTERED")
        return []
