#coding:utf-8
"""
@file:      decorators.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-10-02 2:45
@description:
            放常用的装饰器
"""

def except_return_none(func,ModelName):
    def wrapper(*args, **kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            print('{}:\n\tError in {}(): {}'\
                  .format(ModelName,func.__name__,str(e)))
            return None
    return wrapper

#尽量用有返回值的
def except_pass(func,ModelName):
    def wrapper(*args, **kwargs):
        try:
            func(*args,**kwargs)
        except Exception as e:
            print('{}:\n\tError in {}(): {}'\
                  .format(ModelName,func.__name__,str(e)))
    return wrapper
