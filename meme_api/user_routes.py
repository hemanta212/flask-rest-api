#!/usr/bin/env python3

import datetime
import uuid

from functools import wraps

import jwt

from flask import request, jsonify, make_response, Blueprint, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from meme_api import db
from meme_api.models import User
from meme_api.utils import token_required

users = Blueprint("users", __name__)


@users.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
#    if not current_user.admin:
#        return jsonify({'message' : 'Cannot perform that function!'})
    all_users = User.query.all()
    output = [user.to_dict() for user in all_users]
    return jsonify({'users' : output})


@users.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    user_data = user.to_dict()
    return jsonify({'user' : user_data})


@users.route('/user', methods=['POST'])
def create_user():
    #if not current_user.admin:
    #    return jsonify({'message' : 'Cannot perform that function!'})
    data = request.form
    print("REQUEST>GET_DATA", data)

    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return "Non nullable items are empty", 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), username=username, password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'New user created!'})


@users.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()
    return jsonify({'message' : 'The user has been promoted!'})


@users.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message' : 'The user has been deleted!'})


@users.route('/login')
def login():
    auth = request.authorization
    print('OBA  AUTH YO HO', auth)
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id}, current_app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

