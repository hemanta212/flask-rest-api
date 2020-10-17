#!/usr/bin/env python3
from flask import request, Blueprint

from meme_api import db
from meme_api.models import MemeTemplate
from meme_api.utils import token_required, registration_required

meme_template = Blueprint("meme_template", __name__)


@meme_template.route("/", methods=["GET"])
@token_required
@registration_required
def get_approved_templates(current_user):
    """
    Gives all the approved templates + user's own templates regardless of approval status
    """
    moderated = []
    meme_templates = MemeTemplate.query.all()
    for template in meme_templates:
        if template.approved:
            moderated.append(template)
        elif template.username == current_user.username:
            moderated.append(template)

    output = [template.to_dict() for template in moderated]
    return {"templates": output}


@meme_template.route("/template", methods=["GET"])
@token_required
@registration_required
def get_all_templates(current_user):
    meme_templates = MemeTemplate.query.all()
    output = [template.to_dict() for template in meme_templates]
    return {"templates": output}


@meme_template.route("/template/<template_id>", methods=["GET"])
@token_required
@registration_required
def get_one_template(current_user, template_id):
    template = MemeTemplate.query.filter_by(id=template_id).first()
    if not template:
        return {"message": "No template found!"}, 404
    return {"template": template.to_dict()}


@meme_template.route("/template", methods=["POST"])
@token_required
@registration_required
def create_template(current_user):
    data = request.form
    title, description, url = (
        data.get("title"),
        data.get("description"),
        data.get("url"),
    )
    if not title or not url:
        return {"message": "Non nullable items are empty"}, 400

    approved = True if current_user.admin else False
    template = MemeTemplate(
        title=title,
        description=description,
        url=url,
        username=current_user.username,
        approved=approved,
    )
    db.session.add(template)
    db.session.commit()
    return {"message": "MemeTemplate created!"}


@meme_template.route("/template/<template_id>", methods=["PUT"])
@token_required
@registration_required
def complete_template(current_user, template_id):
    data = request.form
    title, description, url = (
        data.get("title"),
        data.get("description"),
        data.get("url"),
    )
    if None in (title, url):
        return {"message": "Not nullable item is empty"}, 400

    template = MemeTemplate.query.get(template_id)
    if not template:
        return {"message": "No template found!"}, 404

    if (template.username != current_user.username) and (not current_user.admin):
        return {"message": "Unauthorized edit attempt"}, 403

    if template.approved and not current_user.admin:
        return {"message": "Unauthorized edit to approved post"}, 403

    template.title = title
    template.description = description
    template.url = url
    if current_user.admin:
        template.approved = True

    db.session.commit()
    return {"message": "MemeTemplate item has been updated!"}


@meme_template.route("/template/<template_id>", methods=["DELETE"])
@token_required
def delete_template(current_user, template_id):
    template = MemeTemplate.query.get(template_id)
    if not template:
        return {"message": "No template found!"}, 404

    if (template.username != current_user.username) and (not current_user.admin):
        return {"message": "Unauthorized edit attempt"}, 403

    if template.approved and not current_user.admin:
        return {"message": "Unauthorized edit to approved post"}, 403


    db.session.delete(template)
    db.session.commit()
    return {"message": "MemeTemplate item deleted!"}
