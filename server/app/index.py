from flask import Blueprint, session, redirect, url_for

# define blueprint
bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/")
def index():
    return redirect(url_for("home"))
        