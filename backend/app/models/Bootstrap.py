import random
import string
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
    market_name = db.Column(db.String(255))

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

# Create tables
with app.app_context():
    db.create_all()

    # Populate tables with dummy data
    # For example:
    def generate_random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    def generate_random_data():
        # Generate random data for AllMarkets table
        random_market_name = generate_random_string(10)
        random_url = "http://" + generate_random_string(10) + ".com"
        random_total_supply = random.randint(1000, 100000)
        random_total_borrow = random.randint(500, 50000)
        random_supply_apy = random.uniform(0.01, 0.2)
        random_borrow_apy = random.uniform(0.01, 0.2)
        dummy_market = AllMarkets(market_name=random_market_name, url=random_url, total_supply=random_total_supply, total_borrow=random_total_borrow, supply_apy=random_supply_apy, borrow_apy=random_borrow_apy)
        db.session.add(dummy_market)

        # Generate random data for HistoricalData table
        random_timestamp = random.randint(1234567890, 1634567890)
        random_total_supplied = random.randint(1000, 9000)
        random_total_borrowed = random.randint(500, 4000)
        dummy_historical_data = HistoricalData(timestamp=random_timestamp, total_supplied=random_total_supplied, total_borrowed=random_total_borrowed)
        db.session.add(dummy_historical_data)

        # Generate random data for Transaction table
        random_reserve = generate_random_string(10)
        random_user = generate_random_string(10)
        random_amount = random.randint(100, 1000)
        random_log_index = random.randint(1, 100)
        random_transaction_index = random.randint(1, 100)
        random_transaction_hash = generate_random_string(32)
        random_block_hash = generate_random_string(32)
        random_block_number = random.randint(10000, 50000)
        random_event_type = random.choice(['Supply', 'Borrow'])
        dummy_transaction = Transaction(reserve=random_reserve, user=random_user, amount=random_amount, timestamp=random_timestamp, log_index=random_log_index, transaction_index=random_transaction_index, transaction_hash=random_transaction_hash, block_hash=random_block_hash, block_number=random_block_number, event_type=random_event_type)
        db.session.add(dummy_transaction)

        # Generate random data for UserHistory table
        random_user = generate_random_string(10)
        random_reserve = generate_random_string(10)
        random_block_number = random.randint(10000, 50000)
        random_block_hash = generate_random_string(32)
        random_transaction_hash = generate_random_string(32)
        random_amount = random.randint(100, 1000)
        random_event_type = random.choice(['Supply', 'Borrow'])
        dummy_user_history = UserHistory(user=random_user, reserve=random_reserve, timestamp=random_timestamp, block_number=random_block_number, block_hash=random_block_hash, transaction_hash=random_transaction_hash, amount=random_amount, event_type=random_event_type)
        db.session.add(dummy_user_history)

        # Generate random data for NewUserHistory table
        random_event_type = random.choice(['Supply', 'Borrow'])
        random_transaction_hash = generate_random_string(32)
        random_address = generate_random_string(42)
        random_block_hash = generate_random_string(32)
        random_block_number = random.randint(10000, 50000)
        random_reserve = generate_random_string(10)
        random_on_behalf_of = generate_random_string(10)
        random_user = generate_random_string(10)
        random_amount = random.randint(100, 1000)
        random_borrow_rate = random.randint(1, 10)
        random_repayer = generate_random_string(10)
        random_use_atokens = random.choice([True, False])
        random_to = generate_random_string(10)
        random_target = generate_random_string(10)
        random_asset = generate_random_string(10)
        random_referral_code = random.randint(1000, 9999)
        random_initiator = generate_random_string(10)
        random_premium = random.uniform(0.01, 0.5)

        dummy_new_user_history = NewUserHistory
        dummy_new_user_history = NewUserHistory(
            event_type=random_event_type,
            transaction_hash=random_transaction_hash,
            address=random_address,
            block_hash=random_block_hash,
            block_number=random_block_number,
            reserve=random_reserve,
            on_behalf_of=random_on_behalf_of,
            user=random_user,
            amount=random_amount,
            borrow_rate=random_borrow_rate,
            repayer=random_repayer,
            use_atokens=random_use_atokens,
            to=random_to,
            target=random_target,
            asset=random_asset,
            referral_code=random_referral_code,
            initiator=random_initiator,
            premium=random_premium
        )
        db.session.add(dummy_new_user_history)

        # Commit the changes to the database
        db.session.commit()

    # Call the function to generate and add random data to the tables
    generate_random_data()

    # Check if tables are created
    print("AllMarkets Table: ", db.session.query(AllMarkets).all())
    print("HistoricalData Table: ", db.session.query(HistoricalData).all())
    print("Transaction Table: ", db.session.query(Transaction).all())
    print("UserHistory Table: ", db.session.query(UserHistory).all())
    print("NewUserHistory Table: ", db.session.query(NewUserHistory).all())