import pandas as pd
from flask import Blueprint, jsonify, request
from app.models import *
from app.transactions_network_generator import generate_network
from pprint import pprint

api = Blueprint("api", __name__)


@api.route("/historical_data", methods=["GET"])
def historical_data():
    market = request.args.get("market", "AAVE")
    timeframe = request.args.get(
        "timeframe", 365
    )  # To be handled in HistoricalData query
    market_data = HistoricalData.query.filter_by(Market=market).all()
    data_list = [data.to_dict() for data in market_data]
    pprint(data_list)
    return jsonify(data_list)


@api.route("/all_markets", methods=["GET"])
def all_markets():
    # This endpoint will populate the landing page table
    markets_data = {
        "market1": {"url": "https://market1.example.com"},
        "market2": {"url": "https://market2.example.com"},
    }
    return jsonify(markets_data)


@api.route("/user_history", methods=["GET"])
def user_history():
    user_address = request.args.get("user_address")
    market = request.args.get("market")

    # Dynamically apply filters based on query parameters
    query = UserHistory.query
    if user_address:
        query = query.filter_by(address=user_address)
    if market:
        query = query.filter_by(reserve=market)

    # Execute the query
    history_records = query.all()

    # Convert records to DataFrame for easier processing
    data = pd.DataFrame([record.to_dict() for record in history_records])

    # Generate network data
    graph_data = generate_network(data)

    return jsonify(graph_data)


## NOTE: Deprecated endpoints :(
# @api.route("/historical_leverage", methods=["GET"])
# def historical_leverage():
#     market = request.args.get("market", "mainnet aave v3")
#     timeframe = request.args.get("timeframe", "1 year")
#     # Here you would adjust your data fetching logic based on market and timeframe
#     leverage_data = {
#         "timestamp": "2023-01-01",
#         "leverage": 2.5,
#         "market": market,
#         "timeframe": timeframe,
#     }
#     return jsonify(leverage_data)


# @api.route("/supply_transactions", methods=["GET"])
# def supply_transactions():
#     market = request.args.get("market", "aave v3")
#     timeframe = request.args.get("timeframe", "1 year")

#     # Query supply transactions based on market and timeframe
#     supply_transactions = Transaction.query.filter_by(reserve=market).all()

#     # Initialize an empty list to store supply transaction data
#     transactions = []

#     # Process fetched supply transactions and append them to the transactions list
#     for transaction in supply_transactions:
#         transaction_data = {
#             "id": transaction.id,
#             "reserve": transaction.reserve,
#             "user": transaction.user,
#             "amount": transaction.amount,
#             "timestamp": transaction.timestamp,
#             "log_index": transaction.log_index,
#             "transaction_index": transaction.transaction_index,
#             "transaction_hash": transaction.transaction_hash,
#             "block_hash": transaction.block_hash,
#             "block_number": transaction.block_number,
#         }
#         transactions.append(transaction_data)

#     return jsonify(transactions)


# @api.route("/borrow_transactions", methods=["GET"])
# def borrow_transactions():
#     market = request.args.get("market", "aave v3")
#     timeframe = request.args.get("timeframe", "1 year")

#     # Query borrow transactions based on market and timeframe
#     borrow_transactions = Transaction.query.filter_by(reserve=market).all()

#     # Initialize an empty list to store borrow transaction data
#     transactions = []

#     # Process fetched borrow transactions and append them to the transactions list
#     for transaction in borrow_transactions:
#         transaction_data = {
#             "id": transaction.id,
#             "reserve": transaction.reserve,
#             "user": transaction.user,
#             "amount": transaction.amount,
#             "timestamp": transaction.timestamp,
#             "log_index": transaction.log_index,
#             "transaction_index": transaction.transaction_index,
#             "transaction_hash": transaction.transaction_hash,
#             "block_hash": transaction.block_hash,
#             "block_number": transaction.block_number,
#         }
#         transactions.append(transaction_data)

#     return jsonify(transactions)


# @api.route("/leveraged_users", methods=["GET"])
# def leveraged_users():
#     aum_threshold = request.args.get("AUM_threshold", 25)
#     market = request.args.get("market", "mainnet aave v3")
#     # Implement logic to fetch leveraged users based on AUM threshold and market
#     users = [{"user_id": "user1", "leverage_amount": 25}]
#     return jsonify(users)
