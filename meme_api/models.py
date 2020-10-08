from meme_api import db

class MemeTemplate(db.Model):
    __tablename__ = "meme_template"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(4096), nullable=False)
    description = db.Column(db.String(4096))
    url = db.Column(db.String(4096), nullable=False)
    user_id = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "user_id": self.user_id,
        }

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "public_id": self.public_id,
            "username": self.username,
            "password": self.password,
            "admin": self.admin,
        }
