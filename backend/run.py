from flask import Flask
from flask_cors import CORS
from app.models import db
from app.api import api
from app.seed import (
    add_dataframe_to_db,
    pd,
)  # Assuming add_dataframe_to_db is correctly adjusted for this context
from app.data_utils import scrape_historic_all  # Import the function that fetches data


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    db.init_app(app)
    app.register_blueprint(api, url_prefix="/api")
    return app


def create_tables(app):
    with app.app_context():
        db.create_all()


def initialize_app():
    """
    Initialize the application, create tables, and seed the database.
    """
    # Create database tables
    with app.app_context():
        create_tables(app)
        print("Database tables created.")

        # Optionally, seed the database with initial data
        # Note: Ensure that the scrape_historic_all function returns a DataFrame
        # and add_dataframe_to_db is adapted to work with the app context correctly.
        historical_data = scrape_historic_all(timeframe=365)
        if add_dataframe_to_db(historical_data, HistoricalData):
            print("Database seeded with historical data.")
        else:
            print("Error seeding database.")


app = create_app()
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})


if __name__ == "__main__":
    # initialize_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
