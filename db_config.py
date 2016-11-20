#coding:utf-8
"""
@file:      db_config
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-11-20 12:18
@description:
            sqlalchemy 配置数据库
"""
from crawl_tools.JsonConfig import DB_Config

for path in ['.','..']:
    try:
        db = DB_Config(
            json_file_path=
                '{}/pgdb_config.json'.format(path)
        ).to_dict()
    except:
        continue

pg_url = (
    'postgresql://{}:{}@{}:{}/{}'
).format(
    db['user'],db['password'],
    db['host'],db['port'],db['db_name'],
)

print(pg_url)

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(
    bind = create_engine(
        name_or_url=pg_url,echo=True
    )
)

db_session = Session()