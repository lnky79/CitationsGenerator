#coding:utf-8
"""
@file:      complete_journal_items
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-11-19 14:15
@description:
            --
"""
import os,sys
sys.path.append(
    os.path.dirname(
        sys.path[0]
    )
)

from CitationInitializor import CitationInitializor

ini =  CitationInitializor()

items = ini.get_filter_items(
    query_args={
        'google_id': None,
    },
    limit=100
)

for item in items:
    print(item)