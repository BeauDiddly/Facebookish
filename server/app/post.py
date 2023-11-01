from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash
)
from werkzeug.utils import secure_filename
from .models import Post, User
from app import db
from datetime import datetime

# define blueprint
bp = Blueprint("post", __name__, url_prefix="/post")

IMAGE_UPLOAD_DIRECTORY = "/upload/images"
ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif"]


def is_file_allowed(filename: str) -> bool:
    """Returns whether or not a filename is valid (if it has an allowed extension).

    :param filename: the filename to check
    :return: whether the file is valid or not
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/create", methods=["POST", "GET"])
def create():
    """Creates a post as the signed in user.

    A post is successfully made if it has any content, i.e. text or an image.

    :return: the create post page or a redirect to the feed if the post is successfully made
    """
    if request.method == "POST":
        post_text = request.form["posttext"]
        post_has_image = "image" in request.files

        # check if there's no content
        if post_text == "":
            flash("You cannot post nothing!")
            return redirect(request.url)

        session_username = session.get("username")

        # check that the user is signed in
        if not session_username:
            flash("You are not signed in!")
            return redirect(request.url)

        user: User = User.query.filter_by(username=session_username).first()

        # the user does not exist... can happen
        if not user:
            flash("Something has gone wrong.")
            return redirect(request.url)

        # create post
        if post_has_image:
            file = request.files["image"]
            if file == "" or not is_file_allowed(file):
                flash("That file is not valid")
                return redirect(request.url)
        db.session.add(Post(user_id=user.id, username=user.username,
                            content=post_text, date_time=datetime.now()))
        db.session.commit()

        return redirect(url_for("feed.feed"))
    return render_template("createpost.html", text="")


@bp.route("/edit/<int:post_id>", methods=["POST", "GET"])
def edit(post_id):
    # get the post
    post: Post = Post.query.get(post_id)

    if not post:
        flash("That post does not exist!")
        return redirect(url_for("feed.feed"))

    if request.method == "POST":
        error = None

        post_text = request.form["posttext"]

        if post_text == "" and "image" not in request.files:
            error = "You cannot post nothing!"

        session_username = session.get("username")

        if not session_username:
            error = "You are not signed in!"

        user: User = User.query.filter_by(username=session_username).first()

        # the user does not exist... can happen
        if not user:
            error = "Something has gone wrong."

        if user.id != post.user_id:
            error = "You are not the author of this post!"

        if error:
            flash(error)
            return render_template("createpost.html", text=post.content)

        post.content = post_text
        db.session.commit()
        return redirect(url_for("feed.feed"))

    return render_template("createpost.html", text=post.content)
