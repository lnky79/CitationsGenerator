#coding:utf-8
"""
@file:      InitCitation
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-11-17 13:51
@description:
            本模块为生成初始化文章的引用关系，以及与年份的关系
"""
import os,sys
sys.path.append(os.path.dirname(sys.path[0]))
import requests,random
from GoogleScholar import PageParser,GoogleArticle
from models import CiteRelationORM,ArticleORM
from google_info_complete_api import GoogleInfoGenerator

from sqlalchemy import text,func,select


class CitationInitializor:
    def __init__(self,db_session):
        self.db_session = db_session
        self.max_id = 0
        self.generate_max_id()

    def update_google_info(self,Article):
        GoogleInfoGenerator(ArticleORM=Article).update()

    def generate_max_id(self):
        self.max_id = self.db_session.query(
            func.max(ArticleORM.id)
        ).first()[0]

    def get_uninitialized_items(self,limit):
        gap = random.choice(range(self.max_id))
        print(('Reeceice db request: '
               'max_id: {} , gap: {} , range_length: {}')\
                .format(self.max_id,gap,limit))
        #print(gap)
        return self.db_session.query(ArticleORM).filter(
            text("google_id is NULL and id>:left and id<:right")
        ).params(left=gap,right=gap+limit).all()

    def generate_citation_page_urls(self,
            cite_google_id,results_num):
        page_num = int( results_num / 10 )
        page_urls = []
        for page_index in range(1,page_num+1):
            page_url = (
                'https://scholar.google.com/scholar'
                '?start={}&hl=en&sciodt=0,5'
                '&cites={}&lr=lang_en&scipsc='
            ).format(page_index*10-10,cite_google_id)
            page_urls.append(page_url)
        return page_urls

    def generate_per_page_articles(self,page_url):
        html = requests.get(page_url).text
        sections = PageParser(html_source=html).sections
        if sections==[]:
            print('[ERROR] Page Url: {} '.format(page_url))
            return False
        for sec in sections:
            GoogleArticle(sec).show_in_cmd()
        return True

    def save_relation(self,cite_google_id,cited_google_id):
        db_session.add(
            CiteRelationORM(
                cite_google_id=cite_google_id,
                cited_google_id=cited_google_id
            )
        )
        db_session.commit()

    def add_article_citations(self,article_item):
        pass

