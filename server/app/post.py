from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash
)
from werkzeug.utils import secure_filename
from .models import Post, User
from app import db
from datetime import datetime
from .util import get_session_user

import os

# define blueprint
bp = Blueprint("post", __name__, url_prefix="/post")

IMAGE_UPLOAD_REL_DIRECTORY = "static\\upload\\images"
REAL_PATH = os.path.dirname(os.path.realpath(__file__))
IMAGE_UPLOAD_DIRECTORY = os.path.join(REAL_PATH, IMAGE_UPLOAD_REL_DIRECTORY)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


def is_file_allowed(filename: str) -> bool:
    """Returns whether or not a filename is valid (if it has an allowed extension).

    :param filename: the filename to check
    :return: whether the file is valid or not
    """
    print(f"ext: {filename.rsplit('.', 1)[1].lower()}")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/create", methods=["POST", "GET"])
def create():
    """Creates a post as the signed in user.

    A post is successfully made if it has text. An image are optional.

    :return: the create post page or a redirect to the feed if the post is 
    successfully made
    """
    if request.method == "POST":
        post_text = request.form["posttext"]
        post_has_image = "image" in request.files and request.files["image"].filename != ""

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
            if not is_file_allowed(file.filename):
                flash("That file is not valid")
                return redirect(request.url)
            filename = secure_filename(file.filename)

            # when saving, we need absolute path
            img_abs_path = os.path.join(IMAGE_UPLOAD_DIRECTORY, filename)

            # when displaying in html, we need relative path
            img_rel_path = os.path.join(IMAGE_UPLOAD_REL_DIRECTORY, filename)

            file.save(img_abs_path)
            db.session.add(Post(user_id=user.id, username=user.username,
                                content=post_text, date_time=datetime.now(), 
                                image=img_rel_path, likes=[], like_count=0))
        else:
            db.session.add(Post(user_id=user.id, username=user.username,
                                content=post_text, date_time=datetime.now(), 
                                likes=[], like_count=0))
        db.session.commit()
        return redirect(url_for("feed.feed"))
    return render_template("createpost.html", text="")


@bp.route("/edit/<int:post_id>", methods=["POST", "GET"])
def edit(post_id):
    """Edits a post as the signed in user.

    :return: the edit post page or a redirect to the feed if the post is 
    successfully edited
    """
    # get the post
    post: Post = Post.query.get(post_id)

    if not post:
        flash("That post does not exist!")
        return redirect(url_for("feed.feed"))

    if request.method == "POST":
        post_text = request.form["posttext"]
        post_has_image = "image" in request.files

        if post_text == "":
            error = "You cannot post nothing!"

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

        # check that the person trying to edit the post is the author
        if user.id != post.user_id:
            error = "You are not the author of this post!"

        # upload the new image and delete the old one
        if post_has_image:
            os.remove(os.path.join(REAL_PATH, post.image))
            file = request.files["image"]
            if file.filename == "" or not is_file_allowed(file.filename):
                flash("That file is not valid")
                return redirect(request.url)
            filename = secure_filename(file.filename)

            # when saving, we need absolute path
            img_abs_path = os.path.join(IMAGE_UPLOAD_DIRECTORY, filename)

            # when displaying in html, we need relative path
            img_rel_path = os.path.join(IMAGE_UPLOAD_REL_DIRECTORY, filename)

            file.save(img_abs_path)
            db.session.add(Post(user_id=user.id, username=user.username,
                                content=post_text, date_time=datetime.now(), 
                                image=img_rel_path))
        else:
            db.session.add(Post(user_id=user.id, username=user.username,
                                content=post_text, date_time=datetime.now()))
        db.session.commit()
        return redirect(url_for("feed.feed"))
    return render_template("createpost.html", text=post.content)


@bp.route("/like/<int:post_id>", methods=["GET"])
def like(post_id):
    post: Post = Post.query.get(post_id)

    if not post:
        flash("That post does not exist!")
        return redirect(url_for("feed.feed"))
    
    user = get_session_user(session)

    if not user:
        flash("You are not signed in")
        return redirect(url_for("feed.feed"))
    
    if user in post.likes:
        post.like_count -= 1
        post.likes.remove(user)
    else:
        post.like_count += 1
        post.likes.append(user)

    db.session.commit()

    return redirect(url_for("feed.feed"))
    