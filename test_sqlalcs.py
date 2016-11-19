#coding:utf-8
"""
@file:      test_sqlalcs
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-11-19 19:46
@description:
            --
"""


from models import ArticleORM,CiteRelationORM,CitationLinkORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(
    bind = create_engine(
        ('postgresql://lyn:tonylu716'
         '@45.76.197.241:5432'
         '/sf_development'),
        echo = True
    )
)


session = Session()
'''
res = session.query(ArticleORM).filter_by(id=17475957).first()
print(res)
'''
'''
session.add(CitationLinkORM(
    link = '12dasdas.com',
    article_google_id = 'fdsfsdf',
    is_crawled = False
))
'''

from sqlalchemy import text
res = session.query(ArticleORM).filter(
     text("google_id is NULL limit :x")).\
     params(x=100).all()

for x in res:
    print(x)