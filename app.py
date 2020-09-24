import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


SQLALCHEMY_DATABASE_URI = (
    "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASS"),
        hostname=os.getenv("DB_HOST"),
        databasename=os.getenv("DB_NAME"),
    )
)

print("@@@GOT DBURL DLKDSJFLDFJ", SQLALCHEMY_DATABASE_URI)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from models import MemeTemplate


@app.route("/")
def home():
    # get data as dict from the database
    data = [meme_template.to_dict() for meme_template in MemeTemplate.query.all()]
    return jsonify(data)


@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        title = request.args.get("title")
        url = request.args.get("url")
        description = request.args.get("description")
        if None in (title, url):
            return "Non nullable items are empty", 400

        dup_title = MemeTemplate.query.filter_by(title=title).first()
        if dup_title:
            return f"duplicate title {title}", 409

        meme_template = MemeTemplate(title=title, description=description, url=url)
        db.session.add(meme_template)
        db.session.commit()
        return f"Posted {title} {url} {description if description else ''}"
    return "this is post endpoint"

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        title = request.args.get("title")
        url = request.args.get("url")
        description = request.args.get("description")
        item_id = request.args.get("id")
        if None in (item_id, title, url):
            return "Not nullable item is empty", 400

        dup_title = MemeTemplate.query.filter_by(title=title).first()
        if dup_title and dup_title.id != item_id:
            return f"duplicate title {title}", 409

        meme_template = MemeTemplate.query.get(item_id)
        meme_template.title = title
        meme_template.description = description
        meme_template.url = url
        db.session.commit()
        return f"Updated {item_id} {title} {url} {description if description else ''}"
    return "This is update endpoint"

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        item_id = request.args.get("id")
        if not item_id:
            return "No item id provided", 400

        meme_template = MemeTemplate.query.get(item_id)
        if meme_template:
            db.session.delete(meme_template)
            db.session.commit()
            return f"deleted item {item_id}"
        else:
            return f"No obj with that id: {item_id}", 404

        return f"unknown error cant delete item_id:{item_id}", 500

    return "this is delete endpoint"
