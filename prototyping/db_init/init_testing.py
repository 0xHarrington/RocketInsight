# Imports
import pandas as pd
import json

# Helpers
from historical_data import scrape_historic_all
from supply_and_borrow_transactions import supply_transactions
from user_history import user_history
from leveraged_users import leveraged_users_by_market
from transactions_network_generator import generate_network

global_all_markets = ['AAVE', 'COMPOUND', 'PRISMA']


if __name__ == '__main__':
    # Scrape Historic Data: (non-computed values)
    historic_data = scrape_historic_all(timeframe=1)

    # Get all leveraged users over all markets
    leveraged_users = []
    for market in global_all_markets:
        # Get suppliers of rETH for this market
        supply_data = supply_transactions(market=market, timeframe=1, token='rETH')

        # Grab leveraged user list for this market
        leveraged_users.extend(leveraged_users_by_market(market=market, supplied_transactions=supply_data))

    # Get user history for over-leveraged users
    interaction_dict = user_history(user_addresses=leveraged_users, markets=global_all_markets)
    all_dfs = []
    for key, dfs_list in interaction_dict.items():
        print(key)
        # Concatenate all DataFrames in the list for the current wallet address
        if len(dfs_list) != 0:
            combined_df = pd.concat(dfs_list, ignore_index=True)
            all_dfs.append(combined_df)

    # Concatenate all combined DataFrames into one
    transaction_df = pd.concat(all_dfs, ignore_index=True)

    # Generate network graph with user histories
    graph_data = generate_network(transaction_df)
    with open('./network_graph.json', 'w') as f:
        json.dump(graph_data, f, indent=4)

    print('DONE')
