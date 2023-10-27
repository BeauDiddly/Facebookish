import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .login import setup_login

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .models import User

    with app.app_context():
        db.create_all()

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    setup_login(app)

    return app