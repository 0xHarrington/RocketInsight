from app.database import create_app, create_tables
from app.seed import (
    add_dataframe_to_db,
    pd,
)  # Assuming add_dataframe_to_db is correctly adjusted for this context
from app.data_utils import scrape_historic_all  # Import the function that fetches data

app = create_app()


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


if __name__ == "__main__":
    # initialize_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
