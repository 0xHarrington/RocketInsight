from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
    
    db.init_app(app)

    from app.routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/')

    return app
