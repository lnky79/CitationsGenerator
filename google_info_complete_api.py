#coding:utf-8
"""
@file:      google_info_complete_api.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-11-18 20:42
@description:
        为journal方向采集到的article赋予缺失的
            google_id,cite_link(首页)，citations_count信息
"""
from GoogleScholar import PageParser,GoogleArticle
from crawl_tools.request_with_proxy import request_with_proxy
from models import ArticleORM

class GoogleInfoGenerator:
    '''
        搜索特定的条目title，补全数据库条目信息
    '''
    def __init__(self,ArticleObj,db_session):
        self.ArticleObj = ArticleObj
        self.db_session = db_session

    def get_google_item_by_search(self):
        search_url = (
                'https://scholar.google.com'
                '/scholar?q={}&btnG=&hl=en&lr=lang_en&as_sdt=0%2C5'
            ).format(self.ArticleObj.title.strip().replace(' ','+'))
        req = request_with_proxy(
                timeout = 20,
                url = search_url,
                #no_proxy_test=True     
             )
        parser = PageParser(
            html_source=req.text
        )
        sections = parser.sections
        if len(sections)!=1:
            if parser.robot_error:
                #print(parser.robot_error)
                raise ConnectionError(
                    'Robot Error:{}'.\
                        format(parser.robot_error))
            else:
                print('No Robot limit')
            raise LookupError(
                'Locate Article Error: '
                ' Multi or No Results:  len: {}'
                '\n{}\n'.format(len(sections),search_url)
            )
        return GoogleArticle(sec=sections[0])

    def update(self):
        google_item = self.get_google_item_by_search()
        google_id = google_item.google_id
        citations_link = google_item.citations_link
        citations_count = google_item.citations_count
        info = (
            'Serach: {}\nGet: {}\n'
            'google_id:  {}\n'
            'citations_link:  {}\n'
            'citations_count:  {}\n'
        ).format(self.ArticleObj.title,google_item.title,
                 google_id,citations_link,citations_count)
        print(info)
        self.db_session.query(ArticleORM).filter_by(
            id = self.ArticleObj.id
        ).update(
            values={
                'google_id': google_id,
                'citations_link': citations_link,
                'citations_count': citations_count,
            }
        )
        self.db_session.commit()
        print('Update google_id OK!')
