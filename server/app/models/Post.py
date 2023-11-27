from app import db

likes = db.Table("likes",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
)

# shares = db.Table("shares",
#     db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
#     db.Column("shared_id", db.Integer, db.ForeignKey("post.id"), primary_key=True)
# )

comments = db.Table("comments",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
    db.Column("comment_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(500))
    content = db.Column(db.String(500))
    date_time = db.Column(db.DateTime)
    image = db.Column(db.String(500))
    likes = db.relationship('User', secondary=likes,
                            primaryjoin=(likes.c.post_id == id),
                            backref=db.backref("liked_by", lazy="dynamic"),
                            lazy="dynamic")
    like_count = db.Column(db.Integer)
    # shares = db.Column(db.Integer)
    comments = db.relationship('Comment', secondary=comments,
                               primaryjoin=(comments.c.post_id == id),
                               secondaryjoin=(comments.c.comment_id == id),
                               backref=db.backref("comment_on", lazy="dynamic"),
                               lazy="dynamic")

    def username_likes_post(self, username: str):
        return username in [user.username for user in self.likes]
