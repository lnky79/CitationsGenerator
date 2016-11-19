#coding:utf-8
"""
@file:      Timer.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-09-08 15:22
@description:
            用于对任务某区间计时
"""
import time
from datetime import datetime, timedelta, timezone

class Timer:
    def __init__(self):
        self.start_ok = False

    def start(self):
        self.st = time.time()
        self.start_ok = True

    def end(self):
        if not self.start_ok:
            raise Exception('[Error] in Timer: Please run start() first.')
        self.gap = round(time.time()-self.st,2)


def get_beijing_time(need_transfer_string=True,format="%Y-%m-%d %H:%M:%S"):
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    if need_transfer_string:
        return utc_dt.astimezone(timezone(
            timedelta(hours=8))).strftime(format)
    else:
        return utc_dt.astimezone(
            timezone(timedelta(hours=8)))