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

from GoogleInfoGenerator import GoogleInfoGenerator

from db_config import Session


ex_db_session = Session()
ini = CitationInitializor(ex_db_session)


def update_per_item(item):
    #print(item.id)
    db_session = Session()
    status = '{}: '.format(item.id)
    err = ''
    try:
        GoogleInfoGenerator(
            ArticleObj=item,
            db_session=db_session
        ).update()
    except LookupError as e:
        err += str(e)
    except ConnectionError as e:
        err += str(e)
    except Exception as e:
        err += str(e)
    db_session.close()
    if err=='':
        status += 'Success'
        print(status)
        return True
    else:
        return False


if __name__=="__main__":
    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(256)
    while True:
        range_length = 10000
        items = ini.get_uninitialized_items(limit=range_length)
        print('Got {} items between range {}...'\
              .format(len(items),range_length))
        crawl_res = pool.map(update_per_item,items)
        success = crawl_res.count(True)
        err = crawl_res.count(False)
        print(('********* Unit Result **************\n'
               'Error: {}      Success: {} \n'
               '************************************\n')\
              .format(err,success))
    ex_db_session.close()
