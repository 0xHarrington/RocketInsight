from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/data.db'
    db.init_app(app)
    return app

def create_tables(app):
    with app.app_context():
        db.create_all()
