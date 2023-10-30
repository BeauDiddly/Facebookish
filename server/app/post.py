from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash
)
from .models import Post, User
from app import db
from datetime import datetime

# define blueprint
bp = Blueprint("post", __name__, url_prefix="/post")


@bp.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        post = request.form["posttext"]
        error = None

        if post == "":
            error = "You cannot post nothing!"

        session_username = session.get("username")

        if not session_username:
            error = "You are not signed in!"

        user: User = User.query.filter_by(username=session_username).first()

        if error:
            flash(error)
            return render_template("createpost.html", text="")

        db.session.add(Post(user_id=user.id, username=user.username,
                            content=post, date_time=datetime.now()))
        db.session.commit()
        return redirect(url_for("feed.feed"))

    return render_template("createpost.html", text="")


@bp.route("/edit/<int:post_id>", methods=["POST", "GET"])
def edit(post_id):
    post: Post = Post.query.get(post_id)

    if request.method == "POST":
        post_text = request.form["posttext"]
        error = None

        if post_text == "":
            error = "You cannot post nothing!"

        session_username = session.get("username")

        if not session_username:
            error = "You are not signed in!"

        user: User = User.query.filter_by(username=session_username).first()

        if user.id != post.user_id:
            error = "You are not the author of this post!"

        if error:
            flash(error)
            return render_template("createpost.html", text=post.content)

        post.content = post_text
        db.session.commit()
        return redirect(url_for("feed.feed"))

    return render_template("createpost.html", text=post.content)
