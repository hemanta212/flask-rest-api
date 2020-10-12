#!/usr/bin/env python3
from functools import wraps
from meme_api.apps import registered

import jwt
from flask import request, current_app

from meme_api.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'message' : 'User Token is missing!'}, 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return {'message' : 'User Token is invalid!'}, 401

        return f(current_user, *args, **kwargs)

    return decorated


def registration_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-application-token' in request.headers:
            token = request.headers['x-application-token']

        if not token:
            return {'message' : 'App Token is missing!'}, 401

        if token in registered.values():
            registered  = True
        else:
            return {'message' : 'App Token is invalid!'}, 401

        return f(*args, **kwargs)

    return decorated
