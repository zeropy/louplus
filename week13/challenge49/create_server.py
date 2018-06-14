#!/usr/bin/env python
# coding=utf-8


import requests
import json

def create_server(name, host):
    url = 'http://127.0.0.1:5000/servers/'
    headers = {'Content-Type': 'application/json'}
    data = {'name':name, 'host':host}
    r = requests.post(url,data=json.dumps(data), headers=headers)
    # print(r.content)
    return r.json()

if __name__ == '__main__':
    create_server('test','127.0.0.1')
