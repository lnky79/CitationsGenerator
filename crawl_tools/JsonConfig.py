#coding:utf-8
"""
@file:      JsonConfig
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-10-08 11:42
@description:
        使用json来配置私有数据的动作集合模块
"""
import json

class JsonConfig:
    def __init__(self,json_file_path,default_info_dict):
        self.json_file_path = json_file_path
        self.info_dict = default_info_dict

    def generate(self):
        with open(self.json_file_path, 'r') as fp:
            input_infos = json.load(fp)
            for input_key in input_infos.keys():
                if input_key in self.info_dict.keys():
                    self.info_dict[input_key] = input_infos[input_key]
                else:
                    raise Exception(
                        '{}: <{}> is invalid key'\
                            .format(self.__class__.__name__,input_key)
                    )

    def to_dict(self):
        self.generate()
        return self.info_dict


class ServerConfig(JsonConfig):
    def __init__(self,json_file_path):
        default_info_dict = {
            'ip':   None,
            'port': 22,
            'user': None,
            'password': None,
            'nickname': None
        }
        JsonConfig.__init__(
            self,json_file_path,default_info_dict)


class DB_Config(JsonConfig):
    def __init__(self,json_file_path):
        default_info_dict = {
            'db_name':      None,
            'user' :        None,
            'password' :    None,
            'host' :        None,
            'port' :        None,
            "local_pool_size":   20,
            "remote_pool_size":  5,
            "master_db_in":      False
        }
        JsonConfig.__init__(
            self,json_file_path,default_info_dict)
