from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class AllMarkets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    market_name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    total_supply = db.Column(db.Integer)
    total_borrow = db.Column(db.Integer)
    supply_apy = db.Column(db.Float)
    borrow_apy = db.Column(db.Float)

class HistoricalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    total_supplied = db.Column(db.Integer)
    total_borrowed = db.Column(db.Integer)

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

# Create tables
with app.app_context():
    db.create_all()

    # Populate tables with dummy data
    # For example:
    dummy_market = AllMarkets(market_name='Dummy Market', url='http://dummy.com', total_supply=10000, total_borrow=5000, supply_apy=0.05, borrow_apy=0.08)
    db.session.add(dummy_market)

    dummy_historical_data = HistoricalData(timestamp=1234567890, total_supplied=8000, total_borrowed=4000)
    db.session.add(dummy_historical_data)

    dummy_transaction = Transaction(reserve='Dummy Reserve', user='dummy_user_address', amount=1000, timestamp=1234567890, log_index=1, transaction_index=1, transaction_hash='dummy_tx_hash', block_hash='dummy_block_hash', block_number=12345, event_type='Supply')
    db.session.add(dummy_transaction)

    dummy_user_history = UserHistory(user='dummy_user', reserve='Dummy Reserve', timestamp=1234567890, block_number=12345, block_hash='dummy_block_hash', transaction_hash='dummy_tx_hash', amount=1000, event_type='Borrow')
    db.session.add(dummy_user_history)

    # Commit the changes to the database
    db.session.commit()
    
    # Check if tables are created
    print("AllMarkets Table: ", db.session.query(AllMarkets).all())
    print("HistoricalData Table: ", db.session.query(HistoricalData).all())
    print("Transaction Table: ", db.session.query(Transaction).all())
    print("UserHistory Table: ", db.session.query(UserHistory).all())
