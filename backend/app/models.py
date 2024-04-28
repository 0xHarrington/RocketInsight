# Imports and Helpers
from flask_sqlalchemy import SQLAlchemy

# DATABASE STUFF
db = SQLAlchemy()


class HistoricalData(db.Model):
    # set table name to CamelCase version of class name
    __tablename__ = "HistoricalData"

    id = db.Column(db.Integer, primary_key=True)
    Timestamp = db.Column(db.Integer, nullable=True)
    Market = db.Column(db.String(255), nullable=True)
    Data_Type = db.Column(db.String(255), nullable=True)
    Value = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "Timestamp": self.Timestamp,
            "Market": self.Market,
            "Data_Type": self.Data_Type,
            "Value": self.Value,
        }


class UserHistory(db.Model):
    # set table name to CamelCase version of class name
    __tablename__ = "UserHistory"

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255), nullable=True)
    transaction_hash = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    block_hash = db.Column(db.String(255), nullable=True)
    block_number = db.Column(db.Integer, nullable=True)
    reserve = db.Column(db.String(255), nullable=True)
    on_behalf_of = db.Column(db.String(255), nullable=True)
    user = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    borrow_rate = db.Column(db.Float, nullable=True)
    repayer = db.Column(db.String(255), nullable=True)
    use_atokens = db.Column(db.Boolean, nullable=True)
    to = db.Column(db.String(255), nullable=True)
    target = db.Column(db.String(255), nullable=True)
    asset = db.Column(db.String(255), nullable=True)
    initiator = db.Column(db.String(255), nullable=True)
    premium = db.Column(db.Float, nullable=True)

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
            "initiator": self.initiator,
            "premium": self.premium,
        }


class AllMarkets(db.Model):
    # set table name to CamelCase version of class name
    __tablename__ = "AllMarkets"

    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "market": self.market,
        }
