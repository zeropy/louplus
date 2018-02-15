#!/usr/bin/env python3

from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
import os
import json
from datetime import datetime
from pymongo import  MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou?charset=utf8'

db = SQLAlchemy(app)

mclient = MongoClient('127.0.0.1',27017)
mdb = mclient.shiyanlou

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    content = db.Column(db.Text)

    def __init__(self,title,created_time,category_id,content):
        self.title = title
        self.created_time = created_time
        self.category_id = category_id
        self.content = content
        #mdb.tag.insert({'title':self.title})

    def __repr__(self):
        return "<File(title={:s})>".format(self.title)

    def add_tag(self,tag_name):
        # 为当前文章添加标签
        mdb.tag.update(
            {'_id':self.id},
            {'$addToSet':{'tags':tag_name}},
            **{'upsert':True}
        )

    def remove_tag(self,tag_name):
        # 从mongo 中删除当前文章的tag_name 标签
        mdb.tag.update(
            {'_id':self.id},
            {'$pull':{'tags':tag_name}}
        )


    #标签了列表
    @property
    def tags(self):
        # 读取mongodb,返回当前文章的标签列表
        result = mdb.tag.find_one({'_id':self.id})['tags']
        return result



class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return "<Category(name={:s})>".format(self.name)



@app.route('/')
def index():
    ''' 显示文章名称的列表
    页面需要显示'/home/shiyanlou/files'
    目录下所有josn文件中的tilte信息列表
    '''
    files = File.query.all()
    return render_template('index.html',files=files)


@app.route('/files/<int:file_id>')
def file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if not file:
        abort(404)
    category  = Category.query.filter_by(id=file.category_id).first()
    #tags = mdb.tag.find({'_id':file.id})['tags']

    return render_template('file.html',file=file,category=category)

@app.errorhandler(404)
def not_found(error):
    error_message = 'shiyanlou 404'
    return render_template('404.html',error_message=error_message),404
