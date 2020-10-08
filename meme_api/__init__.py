#!/usr/bin/env python3
import os
from flask import  Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
            username=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASS"),
            hostname=os.getenv("DB_HOST"),
            databasename=os.getenv("DB_NAME"),
        )
    )
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    CUSTOM_DB = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["SQLALCHEMY_DATABASE_URI"] = CUSTOM_DB if CUSTOM_DB else SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from meme_api.user_routes import users
    from meme_api.meme_template_routes import meme_template

    app.register_blueprint(users)
    app.register_blueprint(meme_template)

    return app
