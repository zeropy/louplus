
from flask import Blueprint
from flask import render_template, url_for, redirect, request, flash
from simpledu.decorators import admin_required
from simpledu.models import db, Course, User
from flask import current_app
from simpledu.forms import CourseForm, UserForm

admin = Blueprint('admin',__name__,url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page',default=1,type=int)
    pagination = Course.query.paginate(
      page=page,
      per_page=current_app.config['ADMIN_PER_PAGE'],
      error_out=False
    )
    return render_template('admin/courses.html',pagination=pagination)

@admin.route('/courses/create',methods=['GET','POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功','success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_course.html',form=form)

@admin.route('/courses/<int:course_id>/edit',methods=['GET','POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程修改成功','success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_course.html',form=form, course=course)

@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('删除课程成功','success')
    return redirect(url_for('admin.courses'))

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page',default=1, type=1)
    pagination = User.query.paginate(
         page=page,
         per_page=current_app.config['ADMIN_PER_PAGE'],
         error_out=False
    )
    return render_template('admin/users.html',pagination=pagination)

@admin.route('/users/add', methods=['GET','POST'])
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('添加用户成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/add_user.html',form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET','POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('更新用户成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html',form=form, user=user)

@admin.route('/user/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('删除用户成功','success')
    return redirect(url_for('admin.users'))
