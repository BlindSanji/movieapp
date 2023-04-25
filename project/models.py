from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin
# import pickle

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # likes = db.Column(db.PickleType, nullable=False, default=[])

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    # def add_likes(self, value):
    #     likes = self.likes
    #     likes.append(value)
    #     self.likes = pickle.dumps(likes)

    # def remove_likes(self, value):
    #     likes = self.likes
    #     likes.remove(value)
    #     self.likes = pickle.dumps(likes)

    # def get_likes_list(self):
    #     return pickle.loads(self.likes)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"