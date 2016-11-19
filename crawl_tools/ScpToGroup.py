#coding:utf-8
"""
@file:      ScpToGroup
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-10-08 9:47
@description:
        代码版本或文件推送到集群（除ip密码用户名端口外，路径不单独配置）
        需注意：使用sshpass命令前需要手动进行第一次握手ssh，信任证书
"""
from multiprocessing.dummy import Pool as ThreadPool
from crawl_tools.JsonConfig import ServerConfig
import os

class ScpToGroup:
    def __init__(self,local_path,remote_path,
                    is_folder,config_folder_path):
        self.local_path = local_path
        self.remote_path = remote_path
        self.config_folder_path = config_folder_path
        self.is_folder = is_folder

    def get_config_infos(self):
        machines_info_list = []
        for json_fp in os.listdir(self.config_folder_path):
            machines_info_list.append(
                ServerConfig(
                    json_file_path=os.path.join(
                        self.config_folder_path,json_fp)
                ).to_dict()
            )
        return machines_info_list

    def push_one(self,machine_info):
        scp_params = '-C -v -P {} '.format(machine_info['port'])
        if self.is_folder:
            scp_params += '-r '
        cmd = 'sshpass -p {} scp {} {} {}@{}:{}'.format(
            machine_info['password'],scp_params,
            self.local_path,machine_info['user'],
            machine_info['ip'],self.remote_path
        )
        print(cmd)
        os.system(cmd)

    def push(self):
       machine_infos = self.get_config_infos()
       if len(machine_infos) < 4:
           thread_count = len(machine_infos)
       else:
           thread_count = 4
       pool = ThreadPool(thread_count)
       pool.map(self.push_one,machine_infos)
       pool.close()
       pool.join()

