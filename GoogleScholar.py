#coding:utf-8
"""
@file:      GoogleScholarParser
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-11-17 18:59
@description:
            谷歌scholar的搜索结果页面解析器
"""
import re
from bs4 import BeautifulSoup
from .models import ArticleORM
from crawl_tools.Timer import get_beijing_time
from crawl_tools.decorators import except_return_none
ERN_METHOD = lambda func:except_return_none(func,ModelName='Google Scholar PageParser')


class PageParser:
    def __init__(self,html_source=None,from_web=True):
        if not from_web:
            with open('./sample_google.html','rb') as f:
                html_source = f.read()
        self.soup = BeautifulSoup(html_source,'lxml')

    @property
    def sections(self):
        '''得到文章列表'''
        try:
            return self.soup.select('.gs_r')
        except:
            return []


class GoogleArticle:
    def __init__(self,sec):
        self.sec = sec
        self.domain = 'https://scholar.google.com'

    @property
    @ERN_METHOD
    def title(self):
        try:
            return self.sec.select('.gs_rt > a')[0].text
        except:
            return self.sec.select('.gs_rt')[0].text

    @property
    @ERN_METHOD
    def year(self):
        try:
            return int(self.sec.select('.gs_a')[0].text.split('-')[-2].split(',')[-1][1:-1])
        except:
            try:
                return int(self.sec.select('.gs_a')[0].text.split(',')[-1].split('-')[0].strip(' '))
            except:
                return -1

    @property
    @ERN_METHOD
    def citations_count(self):
        return int(re.split('：| ',self.sec.select('.gs_fl > a')[0].text)[-1])

    @property
    @ERN_METHOD
    def citations_link(self):
        res = self.sec.select('.gs_fl > a')[0]['href']
        if res == '#':
            return None
        else:
            return self.domain + res

    @property
    @ERN_METHOD
    def link(self):
        return self.sec.select('.gs_rt > a')[0]['href']

    @property
    @ERN_METHOD
    def resource_type(self):
        return self.sec.select('.gs_ctg2')[0].text.strip()[1:-1]

    @property
    @ERN_METHOD
    def resource_link(self):
        if self.resource_type:
            return self.sec.select('.gs_ggsd > a')[0]['href']
        else:
            return None

    @property
    @ERN_METHOD
    def summary(self):
        return self.sec.select('.gs_rs')[0].text.strip()

    @property
    @ERN_METHOD
    def google_id(self):
        return self.sec.select('.gs_nph > a')[0]['onclick'].split('(')[-1].split(',')[0][1:-1]

    @property
    @ERN_METHOD
    def index(self):
        return self.sec.select('.gs_nph > a')[0]['onclick'].split('(')[-1].split(',')[1][1:-2]

    @property
    @ERN_METHOD
    def journal_site(self):
        return self.sec.select_one('.gs_a').text.split('-')[-1].strip()

    def show_in_cmd(self):
        print('\n******** New Article of <Google Scholar> *********')
        print('title:\t\t{}'.format(self.title))
        print('journal_site:\t\t{}'.format(self.journal_site))
        print('google_id:\t{}'.format(self.google_id))
        print('year:\t\t{}'.format(self.year))
        print('citations_count:\t{}'.format(self.citations_count))
        print('citations_link:\t{}'.format(self.citations_link))
        print('link:\t\t\t{}'.format(self.link))
        print('summary:\t\t{}'.format(self.summary))
        print('resource_type:\t{}'.format(self.resource_type))
        print('resource_link:\t{}'.format(self.resource_link))

    def save_to_db(self):
        ArticleORM(
            title=self.title,
            link=self.link,
            year=self.year,
            resource_type=self.resource_type,
            resource_link=self.resource_link,
            google_id=self.google_id,
            citations_link=self.citations_link,
            citations_count=self.citations_count,
            create_time=get_beijing_time(need_transfer_string=False)
        ).save()

if __name__=='__main__':
    for sec in PageParser(from_web=False).sections:
        Article(sec).show_in_cmd()
