#!/usr/bin/env python3
from flask import request, Blueprint

from meme_api import db
from meme_api.models import MemeTemplate
from meme_api.utils import token_required

meme_template = Blueprint("meme_template", __name__)


@meme_template.route('/', methods=['GET'])
@meme_template.route('/template', methods=['GET'])
@token_required
def get_all_templates(current_user):
    meme_templates = MemeTemplate.query.all()
    output = [template.to_dict() for template in meme_templates]
    return {'templates' : output}


@meme_template.route('/template/<template_id>', methods=['GET'])
@token_required
def get_one_template(current_user, template_id):
    template = MemeTemplate.query.filter_by(id=template_id).first()
    if not template:
        return {'message' : 'No template found!'}, 404
    return {'template':template.to_dict()}


@meme_template.route('/template', methods=['POST'])
@token_required
def create_template(current_user):
    data = request.form
    title, description, url = data.get('title'), data.get('description'), data.get('url')
    if not title or not url:
        return {'message':"Non nullable items are empty"}, 400

    template = MemeTemplate(title=title, description=description, url=url, user_id=current_user.public_id)
    db.session.add(template)
    db.session.commit()
    return {'message' : "MemeTemplate created!"}


@meme_template.route('/template/<template_id>', methods=['PUT'])
@token_required
def complete_template(current_user, template_id):
    data = request.form
    title, description, url = data.get('title'), data.get('description'), data.get('url')
    if None in (title, url):
        return {'message':"Not nullable item is empty"}, 400

    template = MemeTemplate.query.get(template_id)
    if not template:
        return {'message' : 'No template found!'}, 404

    template.title = title
    template.description = description
    template.url = url
    db.session.commit()
    return {'message' : 'MemeTemplate item has been updated!'}


@meme_template.route('/template/<template_id>', methods=['DELETE'])
@token_required
def delete_template(current_user, template_id):
    template = MemeTemplate.query.get(template_id)
    if not template:
        return {'message' : 'No template found!'}, 404

    db.session.delete(template)
    db.session.commit()
    return {'message' : 'MemeTemplate item deleted!'}
