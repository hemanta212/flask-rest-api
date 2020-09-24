import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASS"),
    hostname=os.getenv("DB_HOST"),
    databasename=os.getenv("DB_NAME"),
)

print("@@@GOT DBURL DLKDSJFLDFJ", SQLALCHEMY_DATABASE_URI)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from models import MemeTemplate

@app.route('/')
def home():
    # get data as dict from the database
    data = [meme_template.to_dict() for meme_template in MemeTemplate.query.all()]
    return jsonify(data)

@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        title = request.args.get('title')
        url = request.args.get('url')
        description = request.args.get('description')
        if None in (title, url):
            return '303'

        titles = [row.title for row in MemeTemplate.query.all()]
        if title in titles:
            return "334"

        meme_template = MemeTemplate(title=title, description=description, url=url)
        db.session.add(meme_template);
        db.session.commit();
        return f"Posted {title} {url} {description if description else ''}"
    return "Hello"
