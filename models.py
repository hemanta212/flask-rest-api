from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class MemeTemplate(db.Model):

    __tablename__ = "meme_template"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(4096))
    title = db.Column(db.String(4096), nullable=False)
    url = db.Column(db.String(4096), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "description": self.description,
        }


class User(UserMixin):
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username
