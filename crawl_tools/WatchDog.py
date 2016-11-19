#coding:utf-8
"""
@file:      WatchDog.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    2.7
@editor:    PyCharm
@create:    2016-08-19 14:33
@description:
            The basic class of process monitor of one specific task.

	* 是对于今后所有任务的通用模块
	* 父进程是watchdog，子进程为特定的task
	* 主类包含进程级别的task异常的处理方法，杀进程，重启进程，管理员邮件提示等
	* 子类具体写task逻辑异常的识别，如数据量异常等
	* 子类再写一些关键数据的打印，交互性的东西，以及数据的监控统计之类

"""

import sys,os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from crawl_tools.Email import Email
import psutil,os,subprocess


class WatchDog:
    '''
        对于每个process(对应于每个任务)的监视管理器
        如果需要定制，可做父类继承
    '''
    def __init__(self,cmd_line,task_proc_cmd_line,pid=None,kill_prev=True):
        self.cmd_line = cmd_line
        self.task_proc_cmd_line = task_proc_cmd_line
        self.kill_prev = kill_prev
        self.kill_prev_watchdog_procs()#清理之前的类似看门狗进程
        if pid:
            #直接以pid初始化task_proc
            self.task_proc = psutil.Process(pid)
        else:
            #未指定已存在的子进程id，看门狗自动为其创建
            self.kill_prev_task_procs()
            self.create_new_task_proc()
            print('WatchDog:\n\tThe new pid is : {}'.format(self.task_proc.pid))

    def kill_prev_watchdog_procs(self):
        if not self.kill_prev:
            return
        print(self.cmd_line)
        prev_pids = get_prev_pids(self.cmd_line)[:-1]
        print('WatchDog:\n\tPrevious watchdog pids: {}'.format(prev_pids))
        #清理之前的看门狗进程,注意最后一项是当前watchdog自身，不要kill
        close_procs(prev_pids)

    def kill_prev_task_procs(self):
        if not self.kill_prev:
            return
        prev_pids = get_prev_pids(self.task_proc_cmd_line)
        print('WatchDog:\n\tPrevious task pids: {}'.format(prev_pids))
        #清理之前的相同task进程
        close_procs(prev_pids)

    def send_mail(self,admin_address,subject):
        emailAI = Email(
            receiver = admin_address,
            sender   = 'luyangaini@vip.qq.com',
            subject  = subject,
            content  = 'rt',
        )
        emailAI.conn_server(
            host='smtp.qq.com',
            port = 587
        )
        emailAI.login(
            username='luyangaini@vip.qq.com',
            password='ptuevbbulatcbcfh'
        )
        emailAI.send()
        emailAI.close()

    def restart_network(self,sudo_key):
        if os.name!='nt':
            cmd = 'sudo service network-manager restart'
            os.system('echo %s|sudo -S %s' % (sudo_key, cmd))
            print("network restarting...")
        else:
            pass

    def close_task_proc(self):
        print('WatchDog:\n\tKilling process:  {}  ...'.format(self.task_proc.pid))
        if os.name is "nt" :
            subprocess.Popen("taskkill /F /T /PID %i" % self.task_proc.pid , shell=True)
        else :
            os.kill(self.task_proc.pid, 9)

    def create_new_task_proc(self):
        print('WatchDog:\n\tCreating new task_process...')
        self.task_proc = psutil.Process(
            pid = subprocess.Popen(
                args = self.task_proc_cmd_line,
                bufsize = 0
            ).pid
        )

    def restart_task_proc(self):
        self.close_task_proc()
        self.create_new_task_proc()
        print('WatchDog:\n\tRestart ok! The new pid is: ' + str(self.task_proc.pid))

    @property
    def task_proc_status(self):
        try:
            return self.task_proc.status()
        except:
            return 'dead'
    '''
    def run(self):
        pass

        maybe like that:
            while(1):
                if self.proc_status() is 'sleeping':
                    self.send_mail('fuck')
                time.sleep(timeout)
    '''


'''
    funcs of process tools...
'''

def get_existed_proc(cmd_line=None,pname=None):
    #cmd_line is like:  ['python','amount_status.py']
    for proc in psutil.process_iter():
        try:
            if proc.cmdline() == cmd_line:
                return proc  # return if found one
            if pname is not None and proc.name().lower() == pname.lower():
                return proc
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
    return None

def get_prev_procs(cmd_line=None,pname=None,grep=None,sort_by_time=True):
    #cmd_line is like:  ['python','amount_status.py']
    #print('cmd_line',cmd_line)
    #前面三个筛选参数有且仅有一个
    procs = []
    for proc in psutil.process_iter():
        try:
            #print(proc.create_time(),proc.cmdline())
            if proc.cmdline() == cmd_line \
                or ( pname is not None and proc.name().lower() == pname.lower() )\
                    or ( grep is not None and grep in proc.name() ):
                print('proc info search:',proc)
                procs.append({'proc':proc,'create_time':proc.create_time()})
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
    if sort_by_time:
        procs = sorted(procs,
                key = lambda x:x['create_time']
            )#否则默认按id大小排
    '''
    if not procs:
        print('Process manager: No procs searched...')
    '''
    try:
        return list(map(lambda x:x['proc'],procs))
    except Exception as e:
        print(' [Error] in get_prev_procs():{}'.format(str(e)))
        return None


def get_prev_pids(cmd_line=None,pname=None,grep=None,sort_by_time=True):
    procs = get_prev_procs(cmd_line,pname,grep,sort_by_time)
    #print(procs)
    try:
        return list(map(lambda x:x.pid,procs))
    except Exception as e:
        print(' [Error] in get_prev_pids():{}'.format(str(e)))
        return None


def close_procs(pids):
    for pid in pids:
        try:
            if os.name is "nt" :
                subprocess.Popen("taskkill /F /T /PID %i" % pid , shell=True)
            else :
                os.kill(pid, 9)
            print (
                '\tKill pid:{} ok!'.format(pid)
            )
        except:
            pass


def close_procs_by_keyword(keyword):
    close_procs(get_prev_pids(grep=keyword))


if __name__=="__main__":
    #测试代码
    '''
    import time
    pids = get_prev_pids(grep='python')
    for pid in pids:
        time_str = time.localtime(psutil.Process(pid).create_time())#localtime参数为float类型，这里1317091800.0为float类型
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time_str)
        print create_time
    '''
    close_procs_by_keyword('Major')

