import pandas as pd
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
# Computes the start time
start_time = time.time() 
from app.api import api

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# db = SQLAlchemy(app)
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    db.init_app(app)
    app.register_blueprint(api, url_prefix="/api")
    return app


class AllMarkets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "market": self.market,
        }


class HistoricalData(db.Model):
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
    referral_code = db.Column(db.Integer, nullable=True)
    initiator = db.Column(db.String(255), nullable=True)
    premium = db.Column(db.Float, nullable=True)

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
def create_tables():
    """
    Create database tables based on SQLAlchemy models.
    """
    with app.app_context():
        db.create_all()

def add_dataframe_to_db(df, model, table_name):
    """
    Add a pandas DataFrame to the corresponding SQLAlchemy model table in the database.

    Args:
        df (pandas.DataFrame): The DataFrame to be added to the database.
        model (SQLAlchemy model): The SQLAlchemy model representing the database table.
        table_name (str): The name of the table to which the DataFrame will be added.

    Returns:
        bool: True if the DataFrame was successfully added to the database, False otherwise.
    """
    with app.app_context():
        try:
            create_tables()
            # Replace NaN values with None
            df = df.where(pd.notnull(df), None)
            # Write DataFrame to SQL table
            df.to_sql(table_name, con=db.engine, if_exists='replace', index=False)
            return True
        except Exception as e:
            print(f"Error adding DataFrame to database: {e}")
            return False

# Add the DataFrame to the HistoricalData table in the database
historic_data_df = pd.read_csv('historic_data.csv')
if add_dataframe_to_db(historic_data_df, HistoricalData, 'HistoricalData'):
    print("DataFrame added to database successfully.")
else:
    print("Failed to add DataFrame to database.")
    
# Add the DataFrame to the UserHistory table in the database
user_history_df = pd.read_csv('user_history.csv')
if add_dataframe_to_db(user_history_df, UserHistory, 'UserHistory'):
    print("DataFrame added to database successfully.")
else:
    print("Failed to add DataFrame to database.")

# Computes the end time and runtime   
end_time = time.time()
print('Runtime:', str(end_time - start_time) + ' seconds')
