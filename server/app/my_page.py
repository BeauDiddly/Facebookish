from app import db
from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash, jsonify
)

from .models import User, Post

# define blueprint
bp = Blueprint("my_page", __name__, url_prefix="/my_page")

@bp.route("/", methods=["GET"])
def user_page():
    session_username = session.get("username")

    if not session_username:
        return redirect(url_for("home"))
    
    current_user: User = User.query.filter_by(username=session_username).first()

    if not current_user:
        error = "Something has gone awfully awry."
        flash(error)
        return redirect(url_for("auth.logout"))
    
    feed: list[Post] = []
    posts = Post.query.filter_by(user_id=current_user.id)
    feed.extend(posts)

    feed.sort(key=lambda post: post.date_time)
    feed.reverse()
    db.session.commit()

    return render_template("home.html", feed=feed, bio=current_user.bio)

@bp.route('/<string:username>/update_bio', methods=['POST'])
def update_bio(username):
    user = User.query.filter_by(username=username).first()

    if user:
        bio = request.form["bio"]
        user.bio = bio
        db.session.commit()
        return redirect(url_for('my_page.user_page'))
