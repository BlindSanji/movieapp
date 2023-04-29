from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin
from sqlalchemy.types import PickleType
from sqlalchemy.ext.mutable import MutableDict

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    likes = db.relationship('Like', backref='user', lazy=True)
    # watch_later = db.relationship('WatchLater', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def add_like(self, movie_id, title, image):
        like = Like(user_id=self.id, movie_id=movie_id, title=title, image=image)
        self.likes.append(like)
        db.session.commit()

    def get_likes(self):
        return [like.movie_id for like in self.likes]

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.title}')"

# class WatchLater(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     movie_id = db.Column(db.String, nullable=False)
#     title = db.Column(db.String, nullable=False)
#     image = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     def __repr__(self):
#         return f"WatchLater('{self.title}')"