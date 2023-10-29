from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash
)

# define blueprint
bp = Blueprint("post", __name__, url_prefix="/post")

@bp.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        post = request.form["createpost"]
    return render_template("createpost.html", name="test")

@bp.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        post = request.form["createpost"]
    return render_template("createpost.html", name="test")
