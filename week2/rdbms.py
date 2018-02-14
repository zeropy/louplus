#!/usr/bin/env python3
# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey



engine = create_engine('mysql://root@localhost/shiyanlou2?charset=utf8')

def condb():
    #连接数据库
    engine = create_engine('mysql://root@localhost/shiyanlou?charset=utf8')
    result = engine.execute('select * from user').fetchall()
    print(result)

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    email = Column(String)
    def __repr__(self):
        return "<User(name={:s})>".format(self.name)

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer,ForeignKey('user.id'))
    teacher = relationship('User')
    def __repr__(self):
        return '<Course(name={:s})>'.format(self.name)

class Lab(Base):
    __tablename__ = 'lab'
    id = Column(Integer,primary_key=True)
    name = Column(String(64))
    course_id = Column(Integer,ForeignKey('course.id'))
    course = relationship('Course',backref='labs')
    def __repr__(self):
        return '<Lab(name={:s})>'.format(self.name)

def show_table(t):
    #__table__ 属性,记录表定义信息
    print(t.__table__)


def querydb(t):
    engine = create_engine('mysql://root@localhost/shiyanlou?charset=utf8')
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User).filter(User.name=='aiden').first()
    print(result)

def curd():
    Session = sessionmaker(bind=engine)
    session = Session()

    course = session.query(Course).first()

    lab1 = Lab(name='ORM 基础',course_id=course.id)
    lab2 = Lab(name='关系数据库',course=course)
    session.add(lab1)
    session.add(lab2)
    try:
        session.commit()
    except:
        session.rollback()
        print('lab add failed!')
    session.delete(lab1)
    session.commit()


if __name__ == '__main__':
    #condb()
    #show_table(User)
    #querydb(User)
    curd()
