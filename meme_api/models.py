from datetime import datetime
from meme_api import db


class MemeTemplate(db.Model):
    __tablename__ = "meme_template"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(4096), nullable=False)
    description = db.Column(db.String(4096))
    url = db.Column(db.String(4096), nullable=False)
    username = db.Column(db.String(4096), nullable=True)
    posted = db.Column(db.DateTime, default=datetime.now)
    approved = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "user_id": self.username,
            "posted": self.posted,
            "approved": self.approved,
        }


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "public_id": self.public_id,
            "username": self.username,
            "password": self.password,
            "admin": self.admin,
        }
