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

        if not username or not password:
            error = "Username and password are required"

        if not error and password == "password":
            session["username"] = username
            return redirect(url_for("index.index"))
        
        if error:
            flash(error)

    return render_template("login.html", name="test")

@bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index.index"))