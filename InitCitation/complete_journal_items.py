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

from google_info_complete_api import GoogleInfoGenerator

from db_config import Session


ex_db_session = Session()
ini = CitationInitializor(ex_db_session)


def update_per_item(item):
    print(item)
    db_session = Session()
    try:
        GoogleInfoGenerator(
            ArticleObj=item,
            db_session=db_session
        ).update()
    except LookupError as e:
        print(str(e))
    except ConnectionError as e:
        print(str(e))
    except Exception as e:
        print(str(e))
    db_session.close()


if __name__=="__main__":
    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(16)
    while True:
        res = ini.get_uninitialized_items(limit=16)
        #update_per_item(res[0])
        pool.map(update_per_item,res)
    ex_db_session.close()

