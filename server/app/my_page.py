from app import db
from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash
)

from .models import User, Post

# define blueprint
bp = Blueprint("my_page", __name__)

@bp.route("/my_page", methods=["GET"])
def user_page():
    session_username = session.get("username")

    if not session_username:
        return redirect(url_for("home"))
    
    current_user: User = User.query.filter_by(username=session_username).first()

    if not current_user:
        error = "Something has gone awfully awry."
        flash(error)
        return redirect(url_for("logout"))
    
    feed: list[Post] = []
    posts = Post.query.filter_by(user_id=current_user.id)
    feed.extend(posts)

    feed.sort(key=lambda post: post.date_time)
    feed.reverse()

    bio = "User of Facebook-ish"
    if current_user.bio:
        bio = current_user.bio
    db.session.commit()

    return render_template("home.html", feed=feed, bio=bio)
