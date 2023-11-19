from app import db
from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash, jsonify
)

from .models import User

# define blueprint
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        input_username = request.form["username"]
        input_password = request.form["password"]

        # track error
        error = None

        user: User = User.query.filter_by(username=input_username).first()
        # if they didn't input a username or password
        if not input_username or not input_password or not user or user.password != input_password:
            error = "Invalid Username or Password"
        else:
            session["username"] = input_username

        if error:
            flash(error)
            return render_template("login.html")

        return redirect(url_for("my_page.user_page"))

    return render_template("login.html")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        input_username = request.form["username"]
        input_password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        error = None

        if not input_username or not input_password or not confirm_password:
            error = "All fields are required"

        if input_password != confirm_password:
            error = "Password confirmation does not match password"

        # check if username exists
        users = User.query.filter_by(username=input_username).all()

        if len(users) != 0:
            error = "That username is taken!"

        if error:
            flash(error)
            return render_template("register.html")
        
        db.session.add(User(username=input_username, password=confirm_password, bio='User of Facebook-ish.'))
        db.session.commit()
        return redirect(url_for("feed.feed"))

    return render_template("register.html")


@bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@bp.route("/get_user_id", methods=['GET'])
def get_user_id():
    session_username = session.get("username")

    if not session_username:
        return jsonify({
            'status': 'error',
            'msg': 'not signed in'
        }), 404
    
    sender: User = User.query.filter_by(username=session_username).first()
    
    return jsonify({
        'status': 'success',
        'id': str(sender.id)
    }), 200