from flask import Blueprint, session

# define blueprint
bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/")
def index():
    if "username" in session:
        return f"Logged in as {session['username']}"
    else:
        return "Not logged in"
        