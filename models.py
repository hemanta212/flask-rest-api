from app import db

class MemeTemplate(db.Model):

    __tablename__ = "meme_template"


    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(4096))
    title = db.Column(db.String(4096), nullable=False)
    url = db.Column(db.String(4096), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'description': self.description
        }
