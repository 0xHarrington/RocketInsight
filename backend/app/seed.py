from app.models import db, HistoricalData
import pandas as pd


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
                record = model(
                    **row.to_dict()
                )  # Create a new record from DataFrame row
                db.session.add(record)  # Add the record to the session

            db.session.commit()  # Commit the session to persist changes
            return True
        except Exception as e:
            print(f"Error adding DataFrame to database: {e}")
            db.session.rollback()  # Rollback the session in case of error
            return False


if __name__ == "__main__":
    # Add the DataFrame to the HistoricalData table in the database
    success = add_dataframe_to_db(scrape_historic_all(timeframe=1), HistoricalData)
    if success:
        print("DataFrame added to database successfully.")
    else:
        print("Error adding DataFrame to database.")
