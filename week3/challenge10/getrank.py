#!/usr/bin/env python
# coding=utf-8

import sys
from pymongo import MongoClient
from bson.son import SON
import pprint

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    # 计算用户 user_id 的排名,分数及花费总时间
    pipeline = [
        {'$group':{
            '_id':'$user_id',
            'score':{'$sum':'$score'},
            'submit_time':{'$sum':'$submit_time'}
        }},
        {
            '$sort':SON([('score',-1),('submit_time',1)])
        }
    ]
    all_data = [x for x in contests.aggregate(pipeline)]

    rank = 0
    for udata in all_data:
        rank += 1
        if user_id == udata['_id']:
            score = udata['score']
            submit_time = udata['submit_time']
            break

    # 依次返回排名,分数和时间,不能修改排序
    return rank, score, submit_time

if __name__ == '__main__':
    '''
    1. 判断参数是否符合要求
    2. 获取 user_id 参数
    '''
    try:
        user_id = sys.argv[1]
        user_id = int(user_id)
    except (IndexError,ValueError) as e:
        print('Parameter Error')
        sys.exit(1)

    # 根据用户 ID 获取用户排名,分数和时间
    userdata = get_rank(user_id)
    print(userdata)
