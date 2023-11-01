from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(500))
    content = db.Column(db.String(500))
    date_time = db.Column(db.DateTime)
    image = db.Column(db.String(500))
    # likes = db.Column(db.Integer)
    # shares = db.Column(db.Integer)
    # comments = db.relationship('Comment', backref='post')
