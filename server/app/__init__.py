import os

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.secret_key = 'f87d243efeeedc392349ec7b8e35f80bde77bdeac7043a04390884759490c3ad'

    db.init_app(app)

    from . import auth, index, friends, post, feed, my_page

    with app.app_context():
        db.create_all()

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # register blueprints
    app.register_blueprint(index.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(friends.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(feed.bp)
    app.register_blueprint(my_page.bp)
    
    # Home page
    @app.route('/home')
    def home():
        return render_template('home.html')
    
    return app
