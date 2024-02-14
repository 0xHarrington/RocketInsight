from app import db

class HistoricalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    leverage = db.Column(db.Float, nullable=True)
    supply_amount = db.Column(db.Float, nullable=True)
    borrow_amount = db.Column(db.Float, nullable=True)
    # Add other fields as necessary
