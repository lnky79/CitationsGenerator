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
from .GoogleScholar import PageParser,GoogleArticle
from crawl_tools.request_with_proxy import request_with_proxy

class GoogleInfoGenerator:
    '''
        搜索特定的条目title，补全数据库条目信息
    '''
    def __init__(self,ArticleObj):
        self.ArticleObj = ArticleObj

    def get_google_item_by_search(self):
        sections = PageParser(
            html_source=request_with_proxy(
                timeout = 10,
                url = (
                    'https://scholar.google.com'
                    '/scholar?hl=en&lr=lang_en&q={}'
                ).format(self.ArticleObj.title)
             ).text
        ).sections
        if len(sections) > 1:
            raise LookupError(
                'Locate Article Error: '
                ' Multi Results'
            )
        return GoogleArticle(sec=sections[0])

    def update(self):
        google_item = self.get_google_item_by_search()
        google_id = google_item.google_id
        citations_link = google_item.citations_link
        citations_count = google_item.citations_count
        (
            'Serach: {}\nGet: {}\n'
            'google_id:  {}\n'
            'citations_link:  {}\n'
            'citations_count:  {}\n'
        ).format(self.ArticleObj.title,google_item.title,
                 google_id,citations_link,citations_count)
        self.ArticleObj.google_id = google_id
        self.ArticleObj.citations_link = citations_link
        self.ArticleObj.citations_count = citations_count
        self.ArticleObj.save()
        print('Update google_id OK!')