#!/usr/bin/env python3


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(128),unique=True,index=True)
    publish_courses = db.relationship('Course')
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    job = db.Column(db.String(64))

    def __str__(self):
        return '<User(username={:s})>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == ROLE_STAFF

class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),unique=True,index=True,nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    author = db.relationship('User',uselist=False)

    def __str__(self):
        return '<Course(name={:s})>'.format(self.name)
