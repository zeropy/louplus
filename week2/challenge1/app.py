#!/usr/bin/env python3

from flask import Flask,render_template,abort
import os
import json

app = Flask(__name__)
@app.route('/')
def index():
    ''' 显示文章名称的列表
    页面需要显示'/home/shiyanlou/files'
    目录下所有josn文件中的tilte信息列表
    '''
    curdir = os.path.abspath('.')
    filedir = os.path.join(curdir,'files')
    file_list = [ os.path.join(filedir,x) for x in os.listdir(filedir) if x.endswith('.json') ]
    titles = []
    for file in file_list:
        with open(file,'r') as f:
            spamjson = json.load(f)
            title = spamjson['title']
            titles.append(title)
    return render_template('index.html',titles=titles)


@app.route('/files/<filename>')
def file(filename):
    #读取并显示filename.json中的文章内容
    # 如果文章不存在,则显示包含字符串shiyanlou 404的404错误页面
    if not os.path.isfile('./files/%s.json' % filename):
        abort(404)
    with open('./files/%s.json' % filename,'r') as f:
        spamjson = json.load(f)
        content = spamjson['content']
    return render_template('file.html',content=content)

@app.errorhandler(404)
def not_found(error):
    error_message = 'shiyanlou 404'
    return render_template('404.html',error_message=error_message),404
