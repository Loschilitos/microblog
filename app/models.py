from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from datetime import datetime
from flask_login import UserMixin
from app import db
from app import login
from hashlib import md5
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    about_me = db.Column(db.String(140))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    profile_photo = db.Column(db.String(256))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def avatar(self, size):
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.body)




class Church(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    church_name = db.Column(db.String(100), unique=True, nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    num_participants = db.Column(db.Integer, nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Church {self.church_name}, Contact: {self.contact_person}>'
