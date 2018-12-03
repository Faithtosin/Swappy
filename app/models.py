from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    books = db.relationship('Books', backref='sender', lazy='dynamic')
    history = db.relationship('History', backref='exchanger', lazy='dynamic')
    about_me = db.Column(db.String(140))
    points = db.Column(db.String(140), index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True)
    author = db.Column(db.String(140), index=True)
    pages = db.Column(db.String(40), index=True)
    cost = db.Column(db.String(60), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    description = db.Column(db.String(140))
    status = db.Column(db.BOOLEAN, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Books {}>'.format(self.title)




class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True)
    author = db.Column(db.String(140), index=True)
    pages = db.Column(db.String(40), index=True)
    cost = db.Column(db.String(60), index=True)
    type = db.Column(db.BOOLEAN, index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<History {}>'.format(self.title)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)