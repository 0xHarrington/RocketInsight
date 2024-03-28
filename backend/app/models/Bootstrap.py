import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class AllMarkets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    market = db.Column(db.String(255))
    data_type = db.Column(db.String(255))
    value = db.Column(db.Float)

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
    
def create_tables():
    """
    Create database tables based on SQLAlchemy models.
    """
    with app.app_context():
        db.create_all()

def add_dataframe_to_db(df, model):
    """
    Add a pandas DataFrame to the corresponding SQLAlchemy model table in the database.

    Args:
        df (pandas.DataFrame): The DataFrame to be added to the database.
        model (SQLAlchemy model): The SQLAlchemy model representing the database table.

    Returns:
        bool: True if the DataFrame was successfully added to the database, False otherwise.
    """
    with app.app_context():
        try:
            create_tables()
            # Iterate over DataFrame rows and add them to the database session
            for _, row in df.iterrows():
                record = model(**row.to_dict())  # Create a new record from DataFrame row
                db.session.add(record)  # Add the record to the session

            db.session.commit()  # Commit the session to persist changes
            return True
        except Exception as e:
            print(f"Error adding DataFrame to database: {e}")
            db.session.rollback()  # Rollback the session in case of error
            return False

# Example usage:
# Assuming df is your pandas DataFrame
df = pd.DataFrame({
    'timestamp': [12345, 23456, 34567],
    'total_supplied': [1000, 2000, 3000],
    'total_borrowed': [500, 1000, 1500],
    'market_name': ['Market1', 'Market2', 'Market3']
})

# Add the DataFrame to the HistoricalData table in the database
success = add_dataframe_to_db(df, HistoricalData)
if success:
    print("DataFrame added to database successfully.")
else:
    print("Error adding DataFrame to database.")
