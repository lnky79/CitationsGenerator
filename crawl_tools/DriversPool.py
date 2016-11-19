#coding:utf-8
"""
@file:      DriversPool.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-09-04 0:32
@description:
            selenium webdriver的pool类

	* 通用模块
	* 适用于大量需要selenium webdriver工作的环境
	* webdriver启动关闭耗时耗配置，影响了爬虫的工作进度
	* pool开启后：
	*
		* driver无任务时status为‘free’，等待调用
		* 有任务status为‘busy’，会被检测器忽略

	* 封装了函数：get_one_free_driver（wait=True）
	*
		* 返回一个闲置的driver对象
		* wait模式开启，会等待闲置driver出现再返回
		* wait模式未开启，仅检查当前，无则返回空列表

	* 某项任务需要，调用get_one_free即可

"""
import time
from selenium import webdriver
from multiprocessing.dummy import Pool as ThreadPool

class Driver:
    '''
        driver类，封装了webdriver和其编号，状态
    '''
    def __init__(self,visual,index=None):
        self.index = index
        self.status = 'free'
        if visual:
            self.engine = webdriver.Chrome()
        else:
            self.engine = webdriver.PhantomJS()


class DriversPool:
    def __init__(self,size=4,visual=True,launch_with_thread_pool=None):
        self.size = size
        self.visual = visual
        self.pool = []
        self.create(launch_with_thread_pool)

    def add_to_pool(self,index):
        print("DriversPool:\n\tLaunching Engine-{}...".format(index))
        self.pool.append(
            Driver(visual=self.visual,index=index)
        )

    def create(self,launch_with_thread_pool=None):
        if launch_with_thread_pool:
            #启动大幅加速
            launch_with_thread_pool.map(self.add_to_pool,range(self.size))
        else:
            launch_with_thread_pool = ThreadPool(8)
            launch_with_thread_pool.map(self.add_to_pool,range(self.size))
            launch_with_thread_pool.close()
            launch_with_thread_pool.join()


    def alter_driver_status(self,index,status):
        self.pool[index].status = status

    def get_one_free_driver(self,wait=True):
        while(1):
            self.show_pool_info()
            for driverObj in self.pool:
                if driverObj.status == 'free':
                    driverObj.status = 'busy'
                    return driverObj
            if wait:
                print('DriversPool:\n\tSorry, no FREE driver now.\n\tSearch again in ten seconds...')
                time.sleep(10)
            else:
                break
        return None

    def close(self):
        for driverObj in self.pool:
            driverObj.engine.close()

    def show_pool_info(self):
        status_str = 'Driver_pool:\n\t'
        for driverObj in self.pool:
            status_str += (driverObj.status+',')
        print(status_str[:-1])