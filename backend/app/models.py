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
    __tablename__ = "UserHistory"

    id = db.Column(db.Integer, primary_key=True, name="ID")
    event_type = db.Column(db.String(255), name="Event Type")
    transaction_hash = db.Column(db.String(255), name="Transaction Hash")
    address = db.Column(db.String(255), name="Address")
    block_hash = db.Column(db.String(255), name="Block Hash")
    block_number = db.Column(db.Integer, name="Block Number")
    reserve = db.Column(db.String(255), name="Reserve")
    on_behalf_of = db.Column(db.String(255), name="On Behalf Of")
    user = db.Column(db.String(255), name="User")
    amount = db.Column(db.Integer, name="Amount")
    borrow_rate = db.Column(db.Float, name="Borrow Rate")
    repayer = db.Column(db.String(255), name="Repayer")
    use_atokens = db.Column(db.Boolean, name="useATokens")
    to = db.Column(db.String(255), name="To")
    target = db.Column(db.String(255), name="Target")
    asset = db.Column(db.String(255), name="Asset")
    initiator = db.Column(db.String(255), name="Initiator")
    premium = db.Column(db.Float, name="Premium")

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
