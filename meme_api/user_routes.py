#!/usr/bin/env python3

import datetime
import uuid

from functools import wraps

import jwt

from flask import request, make_response, Blueprint, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from meme_api import db
from meme_api.models import User
from meme_api.utils import token_required, registration_required

users = Blueprint("users", __name__)


@users.route("/user", methods=["GET"])
@token_required
@registration_required
def get_all_users(current_user):
    if not current_user.admin:
        return {"message": "Cannot perform that function!"}, 403
    all_users = User.query.all()
    output = [user.to_dict() for user in all_users]
    return {"users": output}


@users.route("/user/<public_id>", methods=["GET"])
@token_required
@registration_required
def get_one_user(current_user, public_id):
    if not current_user.admin:
        return {"message": "Cannot perform that function!"}, 403
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return {"message": "No user found!"}, 404
    user_data = user.to_dict()
    return {"user": user_data}


@users.route("/user", methods=["POST"])
@token_required
@registration_required
def create_user(current_user):
    if not current_user.admin:
        return {"message": "Cannot perform that function!"}, 403
    data = request.form

    username, password = data.get("username"), data.get("password")
    if not username or not password:
        return "Non nullable items are empty", 400

    hashed_password = generate_password_hash(password, method="sha256")
    new_user = User(
        public_id=str(uuid.uuid4()),
        username=username,
        password=hashed_password,
        admin=False,
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "New user created!"}


@users.route("/user/<public_id>", methods=["PUT"])
@token_required
@registration_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return {"message": "Cannot perform that function!"}, 403

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return {"message": "No user found!"}, 404

    user.admin = True
    db.session.commit()
    return {"message": "The user has been promoted!"}


@users.route("/user/<public_id>", methods=["DELETE"])
@token_required
@registration_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return {"message": "Cannot perform that function!"}, 403

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return {"message": "No user found!"}, 404

    db.session.delete(user)
    db.session.commit()
    return {"message": "The user has been deleted!"}


@users.route("/login")
@registration_required
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )

    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {"public_id": user.public_id}, current_app.config["SECRET_KEY"]
        )
        return {"token": token.decode("UTF-8")}

    return make_response(
        "Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'}
    )
