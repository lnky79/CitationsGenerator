#coding:utf-8
"""
@file:      sql_generator.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-09-09 16:57
@description:
            SQL generator with paras_dict initialized.

	* 通用模块，包括sql解析至dict以及dict解析至sql，两个大方法
	* 作为sql转储为python数据结构的一种方式
	* 在抽象基类方法中将大幅使用
	* 比如增加sql中where语句的条件，不转储只做字符串的处理难于实现，且代码较乱

"""

class SQL_Generator:
    def __init__(self,paras_dict):
        self.paras_dict = paras_dict

    @property
    def keys(self):
        return self.paras_dict.keys()

    def to_sql(self):
        self.sql = ''
        self._select()
        self._from()
        self._where()
        self._orderby()
        self._desc()
        self._limit()
        return self.sql

    def _select(self):
        if 'SELECT' in self.keys:
            self.sql += 'SELECT '
            for select_row_name in self.paras_dict['SELECT']:
                self.sql += select_row_name+','
            self.sql = self.sql[:-1]

    def _from(self):
        if 'FROM' in self.keys:
            self.sql += ' FROM ' + self.paras_dict['FROM']

    def _where(self):
        if 'WHERE' in self.keys:
            self.sql += ' WHERE '
            for term_set in self.paras_dict['WHERE']:
                for sign in term_set:
                    if isinstance(sign,str):
                        if sign==term_set[-1] and sign is not 'null' and sign[0] != "'":
                            #字符串值时：需加引号
                            sign = "'" + sign + "'"
                        self.sql += sign + ' '
                    elif isinstance(sign,int):
                        self.sql += str(sign) + ' '
                    else:
                        raise TypeError('[ERROR] in SQL_Generator:\n\tThe value sign in "WHERE" could be int or str,\
                                not {}'.format(type(sign)))
                self.sql = self.sql[:-1]
                self.sql += ' AND '
            self.sql = self.sql[:-5]

    def _orderby(self):
        if 'ORDER BY' in self.keys:
            self.sql += ' ORDER BY ' + self.paras_dict['ORDER BY'] + ' '

    def _desc(self):
        if 'DESC' in self.keys:
            if self.paras_dict['DESC']:
                self.sql += 'DESC '

    def _limit(self):
        if 'LIMIT' in self.keys:
            limit = self.paras_dict['LIMIT']
            if isinstance(limit,int):
                limit = str(limit)
            elif isinstance(limit,str):
                pass
            else:
                raise TypeError('[ERROR] in SQL_Generator:\n\tLimit value could be int or str,not {}'.format(type(self.paras_dict['LIMIT'])))
            self.sql += 'LIMIT ' + limit


class SQL_Parser:
    def __init__(self,sql):
        self.sql = sql

    def to_dict(self):
        keys = ['SELECT','FROM','WHERE','ORDER','DESC','LIMIT']
        keywords = self.sql.split(' ')
        self.paras_dict = {}
        for keyword in keywords:
            if not keyword:
                continue
            if keyword.upper() in keys:
                self.paras_dict[keyword] = []
                key = keyword.upper()
            if key not in self.paras_dict.keys():
                self.paras_dict[key] = []
            self.paras_dict[key].append(keyword)
        self.keys = self.paras_dict.keys()
        self._select()
        self._from()
        self._where()
        self._orderby()
        self._desc()
        self._limit()
        return self.paras_dict

    def _select(self):
        if 'SELECT' in self.keys:
            self.paras_dict['SELECT'] = self.paras_dict['SELECT'][-1].split(',')
            #print(self.paras_dict['SELECT'])

    def _from(self):
        if 'FROM' in self.keys:
            self.paras_dict['FROM'] = self.paras_dict['FROM'][-1]
            #print(self.paras_dict['FROM'])

    def _where(self):
        if 'WHERE' in self.keys:
            where_list = []
            keyword_list = []
            for keyword in self.paras_dict['WHERE'][1:]:
                if keyword=='AND':
                    where_list.append(keyword_list)
                    keyword_list = []
                else:
                    keyword_list.append(keyword)
                if keyword == self.paras_dict['WHERE'][-1]:
                    where_list.append(keyword_list)
            self.paras_dict['WHERE'] = where_list
            #print(self.paras_dict['WHERE'])

    def _orderby(self):
        if 'ORDER' in self.keys:
            self.paras_dict['ORDER BY'] = self.paras_dict['ORDER'][-1]
            self.paras_dict.pop('ORDER')

    def _desc(self):
        if 'DESC' in self.keys:
            self.paras_dict['DESC'] = True
        else:
            self.paras_dict['DESC'] = False

    def _limit(self):
        if 'LIMIT' in self.keys:
            self.paras_dict['LIMIT'] = int(self.paras_dict['LIMIT'][-1])


if __name__=="__main__":
    paras_dict = {
        'SELECT':   ['title','google_id','pdf_temp_url'],
        'FROM':     'articles',
        'WHERE':[
            ['resource_link','is','null'],
            ['journal_temp_info','like','%ieee%'],
        ],
        'ORDER BY': 'id',
        'DESC':     True,
        'LIMIT':    100
    }
    sg = SQL_Generator(paras_dict)
    print(sg.to_sql())
    sg.paras_dict['WHERE'].append(['id','>',200])
    print(sg.to_sql())
    print(sg.paras_dict['WHERE'])
    #sql = 'SELECT  title,google_id,pdf_temp_url  FROM articles WHERE resource_link is null AND journal_temp_info like %ieee% AND id > 200 ORDER BY id DESC LIMIT 100'
    sql = 'SELECT title,google_id,pdf_temp_url FROM articles WHERE resource_link is null AND journal_temp_info like %ieee% AND id > 200 ORDER BY id DESC LIMIT 100'
    print(SQL_Parser(sql=sg.to_sql()).to_dict())