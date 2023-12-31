from flask import (
    render_template, request, session, redirect, Blueprint, url_for, flash
)
from werkzeug.utils import secure_filename
from .models import Post, User, Comment
from app import db
from datetime import datetime
from .util import get_session_user

import os

# define blueprint
bp = Blueprint("post", __name__, url_prefix="/post")

IMAGE_UPLOAD_REL_DIRECTORY = os.path.join("static", "upload", "images")
REAL_PATH = os.path.dirname(os.path.realpath(__file__))
IMAGE_UPLOAD_DIRECTORY = os.path.join(REAL_PATH, IMAGE_UPLOAD_REL_DIRECTORY)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


def is_file_allowed(filename: str) -> bool:
    """Returns whether or not a filename is valid (if it has an allowed extension).

    :param filename: the filename to check
    :return: whether the file is valid or not
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension(filename: str) -> str:
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

@bp.route("/<int:post_id>")
def view_post(post_id):
    post: Post = Post.query.get(post_id)

    if not post:
        flash("That post does not exist!")
        return redirect(url_for("feed.feed"))

    return render_template("post.html", post=post)

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
        
        post = Post(user_id=user.id, username=user.username,
                    content=post_text, date_time=datetime.now(), 
                    likes=[], like_count=0, comment_count=0, share_count=0)
        
        db.session.add(post)
        db.session.commit()

        if post_has_image:
            # Check if the directory already exists
            if not os.path.exists(IMAGE_UPLOAD_DIRECTORY):
                # Create the directory, also create intermediate directories if necessary
                os.makedirs(IMAGE_UPLOAD_DIRECTORY)

            file = request.files["image"]
            if not is_file_allowed(file.filename):
                flash("That file is not valid")
                return redirect(request.url)
            
            filename = f"{post.id}.{get_extension(file.filename)}"

            # when saving, we need absolute path
            img_abs_path = os.path.join(IMAGE_UPLOAD_DIRECTORY, filename)

            if not os.path.exists(IMAGE_UPLOAD_DIRECTORY):
                os.mkdir(IMAGE_UPLOAD_DIRECTORY)

            # when displaying in html, we need relative path
            img_rel_path = os.path.join(IMAGE_UPLOAD_REL_DIRECTORY, filename)

            file.save(img_abs_path)
            print(img_rel_path)
            img_rel_path = "\\" + img_rel_path
            post.image = img_rel_path

        db.session.commit()
        return redirect(url_for("feed.feed"))
    return render_template("create_post.html", text="")


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
        post_has_image = "image" in request.files and request.files["image"].filename != ""

        if post_text == "":
            error = "You cannot post nothing!"

        session_username = session.get("username")

        # check that the user is signed in
        if not session_username:
            flash("You are not signed in!")
            return redirect(request.url)

        user: User = User.query.filter_by(username=session_username).first()

        error = None

        # check that the person trying to edit the post is the author
        if user.id != post.user_id:
            error = "You are not the author of this post!"
        # the user does not exist... can happen
        if not user:
            error = "Something has gone wrong."
            
        if error:
            flash(error)
            return redirect(request.url)


        # upload the new image and delete the old one
        if post_has_image:
            # Check if the directory already exists
            if not os.path.exists(IMAGE_UPLOAD_DIRECTORY):
                # Create the directory, also create intermediate directories if necessary
                os.makedirs(IMAGE_UPLOAD_DIRECTORY)

            if post.image:
                os.remove(os.path.join(
                    IMAGE_UPLOAD_DIRECTORY, 
                    f"{post.id}.{get_extension(post.image)}"
                    ))

            file = request.files["image"]
            if file.filename == "" or not is_file_allowed(file.filename):
                flash("That file is not valid")
                return redirect(request.url)
            
            filename = f"{post.id}.{get_extension(file.filename)}"

            # when saving, we need absolute path
            img_abs_path = os.path.join(IMAGE_UPLOAD_DIRECTORY, filename)

            # when displaying in html, we need relative path
            img_rel_path = os.path.join(IMAGE_UPLOAD_REL_DIRECTORY, filename)

            file.save(img_abs_path)
            post.image = img_rel_path
        post.content = post_text
        db.session.commit()
        return redirect(url_for("feed.feed"))
    return render_template("create_post.html", text=post.content)


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

    return redirect(f"../{post.id}")
    
@bp.route("/comment/<int:post_id>", methods=["GET", "POST"])
def comment(post_id):
    post: Post = Post.query.get(post_id)

    if not post:
        flash("That post does not exist!")
        return redirect(url_for("feed.feed"))
    
    if request.method == "POST":
        comment_text = request.form["comtext"]

        if comment_text == "":
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
        
        comment = Comment(post_id=post.id, content=comment_text, date_time=datetime.now(),
                          user_id=user.id, username=user.username)
        db.session.add(comment)
        post.comments.append(comment)
        post.comment_count += 1
        db.session.commit()

        return redirect(f"/post/{post.id}")
    
    return render_template("create_comment.html", content="")

@bp.route("/comment/edit/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    comment: Comment = Comment.query.get(comment_id)

    if not comment:
        flash("That comment does not exist!")
        return redirect(url_for("feed.feed"))
    
    if request.method == "POST":
        comment_text = request.form["comtext"]

        if comment_text == "":
            flash("You cannot post nothing!")
            return redirect(request.url)
        
        user = get_session_user(session)

        if not user:
            flash("Who are you?")
            # to go against the word of my father?
            return redirect(request.url)
        
        comment.content = comment_text
        db.session.commit()
        return redirect(f"/post/{comment.post_id}")
    
    return render_template("create_comment.html", content=comment.content)

@bp.route("/share/<int:post_id>", methods=["GET", "POST"])
def share(post_id):
    post: Post = Post.query.get(post_id)

    if not post:
        flash("That post does not exist!")
        return redirect(url_for("feed.feed"))
    
    if post.original_poster_id != None:
        flash("That post cannot be shared again!")
        return redirect(f"/post/{post.id}")
    
    user = get_session_user(session)

    if not user:
        flash("You are not signed in")
        return redirect(url_for("feed.feed"))
    
    if request.method == "POST":
        post = Post(user_id=user.id, username=user.username, 
                    original_poster_id=post.user_id, 
                    original_poster_username=post.username,
                    content=post.content, image=post.image,
                    comment_count=0, like_count=0, date_time=datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(f"/post/{post.id}")

    return render_template("share.html")