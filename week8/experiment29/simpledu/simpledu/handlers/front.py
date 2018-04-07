#!/usr/bin/env python
# coding=utf-8

from flask import Flask, Blueprint, render_template, flash,redirect, url_for, request, current_app
from simpledu.models import Course, User
from simpledu.forms import LoginForm, RegisterForm
from flask_login import login_user,login_required,logout_user

front = Blueprint('front',__name__)

@front.route('/')
def index():
    # courses = Course.query.all()
    page = request.args.get('page',default=1,type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    # return  render_template('index.html',courses=courses)
    return render_template('index.html',pagination=pagination)

@front.route('/login',methods=['get','post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(url_for('.index'))
    return render_template('login.html',form=form)

@front.route('/register',methods=['get','post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功,请登录','success')
        return redirect(url_for('.login'))
    # if request.method == 'POST':
    #     flash('注册失败','success')
    return render_template('register.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出的登录','success')
    return redirect(url_for('.index'))
