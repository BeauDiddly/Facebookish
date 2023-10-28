from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250))
    password = db.Column(db.String(250))
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    #posts = db.relationship("Post", backref="author")
    #friends = db.relationship("User")

    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friends = db.relationship('User', backref=db.backref('added_by', remote_side=[id]), lazy='dynamic')
