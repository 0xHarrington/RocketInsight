import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# db = SQLAlchemy(app)
db = SQLAlchemy()


class AllMarkets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.String(255))


class HistoricalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Timestamp = db.Column(db.Integer)
    Market = db.Column(db.String(255))
    Data_Type = db.Column(db.String(255))
    Value = db.Column(db.Float)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reserve = db.Column(db.String(255))
    user = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    log_index = db.Column(db.Integer)
    transaction_index = db.Column(db.Integer)
    transaction_hash = db.Column(db.String(255))
    block_hash = db.Column(db.String(255))
    block_number = db.Column(db.Integer)
    event_type = db.Column(db.String(255))


class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255))
    reserve = db.Column(db.String(255))
    timestamp = db.Column(db.Integer)
    block_number = db.Column(db.Integer)
    block_hash = db.Column(db.String(255))
    transaction_hash = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    event_type = db.Column(db.String(255))


class NewUserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255))
    transaction_hash = db.Column(db.String(255))
    address = db.Column(db.String(255))
    block_hash = db.Column(db.String(255))
    block_number = db.Column(db.Integer)
    reserve = db.Column(db.String(255))
    on_behalf_of = db.Column(db.String(255))
    user = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    borrow_rate = db.Column(db.Integer)
    repayer = db.Column(db.String(255))
    use_atokens = db.Column(db.Boolean)
    to = db.Column(db.String(255))
    target = db.Column(db.String(255))
    asset = db.Column(db.String(255))
    referral_code = db.Column(db.Integer)
    initiator = db.Column(db.String(255))
    premium = db.Column(db.Float)
