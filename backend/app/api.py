from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from models import *

api = Blueprint('api', __name__)

@api.route('/all_markets', methods=['GET'])
def all_markets():
    # This endpoint might not need arguments based on the initial description
    markets_data = {"market1": {"url": "https://market1.example.com"}, "market2": {"url": "https://market2.example.com"}}
    return jsonify(markets_data)

@api.route('/historical_leverage', methods=['GET'])
def historical_leverage():
    market = request.args.get('market', 'mainnet aave v3')
    timeframe = request.args.get('timeframe', '1 year')
    # Here you would adjust your data fetching logic based on market and timeframe
    leverage_data = {"timestamp": "2023-01-01", "leverage": 2.5, "market": market, "timeframe": timeframe}
    return jsonify(leverage_data)

@api.route('/historical_data', methods=['GET'])
def historical_data():
    market = request.args.get('market', 'AAVE')
    timeframe = request.args.get('timeframe', 365) # To be handled in HistoricalData query
    market_data = HistoricalData.query.filter_by(Market=market).all()
    data_list = [data.to_dict() for data in market_data]
    return jsonify(data_list)

@api.route('/supply_transactions', methods=['GET'])
def supply_transactions():
    market = request.args.get('market', 'aave v3')
    timeframe = request.args.get('timeframe', '1 year')
    # Implement logic to fetch supply transactions based on market and timeframe
    transactions = [{"id": 1, "amount": 100, "timestamp": "2023-01-01"}]
    return jsonify(transactions)

@api.route('/borrow_transactions', methods=['GET'])
def borrow_transactions():
    market = request.args.get('market', 'aave v3')
    timeframe = request.args.get('timeframe', '1 year')
    # Implement logic to fetch borrow transactions based on market and timeframe
    transactions = [{"id": 1, "amount": 50, "timestamp": "2023-01-01"}]
    return jsonify(transactions)

@api.route('/leveraged_users', methods=['GET'])
def leveraged_users():
    aum_threshold = request.args.get('AUM_threshold', 25)
    market = request.args.get('market', 'mainnet aave v3')
    # Implement logic to fetch leveraged users based on AUM threshold and market
    users = [{"user_id": "user1", "leverage_amount": 25}]
    return jsonify(users)

@api.route('/user_history', methods=['GET'])
def user_history():
    user_addresses = request.args.getlist('user_address')
    markets = request.args.getlist('market')
    # Implement logic to fetch user history based on user addresses and markets
    history = [{"timestamp": "2023-01-01", "action": "supplied", "amount": 100}]
    return jsonify(history)
