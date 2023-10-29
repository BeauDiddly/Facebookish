from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash
)

# define blueprint
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print(f"{request.form['username']}, {request.form['password']}")

        username = request.form["username"]
        password = request.form["password"]

        # track error
        error = None

        # if they didn't input a username or password
        if not username or not password:
            error = "Username and password are required"

        # if the username exists and the password is right
        if not error and password == "password":
            session["username"] = username
            return redirect(url_for("index.index"))
        
        if error:
            flash(error)

    return render_template("login.html", name="test")

@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        error = None

        if not username or not password or not confirm_password:
            error = "All fields are required"

        if password != confirm_password:
            error = "Password confirmation does not match password"

        # check if username exists

        # if not, create the user

        if error:
            flash(error)
        
    return render_template("register.html")

@bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index.index"))