from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(500))
    date_time = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    shares = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='post')
