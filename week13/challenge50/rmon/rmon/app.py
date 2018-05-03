import os
from flask import Flask
import re
import json


def create_app():
    """ 创建并初始化 Flask app

    Returns:
        app (object): Flask App 实例
    """

    app = Flask('rmon')

    # 获取 json 配置文件名称
    file = os.environ.get('RMON_CONFIG','config.json')

    # TODO 从 json_file 中读取配置项并将每一项配置写入 app.config 中
    result = ''
    pattern = re.compile('([^#]*)')
    with open(file,'r') as f:
        for line in f:
            result += pattern.search(line).group()
    config = json.loads(result)
    uconfig = {}
    for k,v in config.items():
        uconfig[k.upper()] = v
    app.config.update(uconfig)

    return app
