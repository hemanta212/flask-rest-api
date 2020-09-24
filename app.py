from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="memekokhani",
    password="memerforlife",
    hostname="memekokhani.mysql.pythonanywhere-services.com",
    databasename="meme_template",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from models import MemeTemplate

@app.route('/')
def home():
    # get data as dict from the database
    data =[
            {
            'url' : 'https://github.com/hemanta212.png',
            'title' : 'title 3',
            'description' : '',
            },
            {
            'url' : 'https://github.com/hemanta212.png',
            'title' : 'title2',
            'description' : 'abc',
            },
            {
            'url' : 'https://github.com/hemanta212.png',
            'title' : 'Yestai t honi boro',
            'description' : None,
            },
            {
            'url' : 'https://github.com/hemanta212.png',
            'title' : 'Yestai t honi boro',
            'description' : """            'url' : 'https://github.com/hemanta212.png',
            'title' : 'Yestai t honi boro',
            'description' : """,
            },
    ]
    return jsonify(data)

@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        title = request.args.get('title')
        url = request.args.get('url')
        description = request.args.get('description')
        if None in (title, url):
            return '303'
        return f"Posted {title} {url} {description if description else ''}"
    return "Hello"

