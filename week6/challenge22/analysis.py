#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import json


def analysis(file, user_id):
    times = 0
    minutes = 0
    df = pd.read_json(file)
    user_data = df[df.user_id == user_id]
    if user_data.empty:
        times = 0
        minutes = 0
    else:
        times = user_data.user_id.count()
        minutes = user_data.minutes.sum()
    return times, minutes


if __name__ == '__main__':
    times, minutes = analysis('user_study.json', 5348)
    print(times, minutes)
