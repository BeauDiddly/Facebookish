from app import db
from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash
)

from .models import User, Post

# define blueprint
bp = Blueprint("feed", __name__)


@bp.route("/feed", methods=["GET"])
def feed():
    session_username = session.get("username")

    if not session_username:
        return redirect(url_for("home"))

    current_user: User = User.query.filter_by(
        username=session_username).first()

    if not current_user:
        error = "Something has gone awfully awry."
        flash(error)
        return redirect(url_for("logout"))

    friend_id_list: list[int] = [
        friend.id for friend in current_user.friends.all()]
    friend_id_list.append(current_user.id)

    feed: list[Post] = []

    for id in friend_id_list:
        posts = Post.query.filter_by(user_id=id)
        feed.extend(posts)

    feed.sort(key=lambda post: post.date_time)
    feed.reverse()

    return render_template("feed.html", feed=feed)
