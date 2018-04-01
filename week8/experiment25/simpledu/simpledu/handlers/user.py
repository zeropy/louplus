#!/usr/bin/env python

from flask import Blueprint
from flask import render_template
from simpledu.models import User, Course

user = Blueprint('user',__name__,
                 url_prefix='/user')


@user.route('/<string:username>')
def index(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return render_template('user.html',user=user)

