from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Required
from simpledu.models import db, User
from wtforms import ValidationError

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[Required(),Length(6,24)])
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validator_email(self,field):
        user = User.query.filter_by(email=field.email.data).first()
        if user is None:
            raise ValidationError('邮箱不存在')

    def validator_password(self,field):
        user = User.query.filter_by(email=field.email.data).first()
        if user and not user.check_password(field.password.data):
            raise ValidationError('密码错误')
