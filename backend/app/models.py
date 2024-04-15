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

    def to_dict(self):
        return {
            "id": self.id,
            "market": self.market,
        }


class HistoricalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Timestamp = db.Column(db.Integer)
    Market = db.Column(db.String(255))
    Data_Type = db.Column(db.String(255))
    Value = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "Timestamp": self.Timestamp,
            "Market": self.Market,
            "Data_Type": self.Data_Type,
            "Value": self.Value,
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "reserve": self.reserve,
            "user": self.user,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "log_index": self.log_index,
            "transaction_index": self.transaction_index,
            "transaction_hash": self.transaction_hash,
            "block_hash": self.block_hash,
            "block_number": self.block_number,
            "event_type": self.event_type,
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "reserve": self.reserve,
            "timestamp": self.timestamp,
            "block_number": self.block_number,
            "block_hash": self.block_hash,
            "transaction_hash": self.transaction_hash,
            "amount": self.amount,
            "event_type": self.event_type,
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "transaction_hash": self.transaction_hash,
            "address": self.address,
            "block_hash": self.block_hash,
            "block_number": self.block_number,
            "reserve": self.reserve,
            "on_behalf_of": self.on_behalf_of,
            "user": self.user,
            "amount": self.amount,
            "borrow_rate": self.borrow_rate,
            "repayer": self.repayer,
            "use_atokens": self.use_atokens,
            "to": self.to,
            "target": self.target,
            "asset": self.asset,
            "referral_code": self.referral_code,
            "initiator": self.initiator,
            "premium": self.premium,
        }
