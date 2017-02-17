#coding:utf-8
'''
    request_with_proxy.py 用于设置爬虫代理
'''
import sys,os
up_level_N = 1
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
root_dir = SCRIPT_DIR
for i in range(up_level_N):
    root_dir = os.path.normpath(os.path.join(root_dir, '..'))
sys.path.append(root_dir)

import time
from crawl_tools.ua_pool import get_one_random_ua
import requests
requests.packages.urllib3.disable_warnings()
from random import randint

'''
功能：随机分配端口
传入参数：
    x,y：    随机域的两个边界，
    exclude：以及一个包含所有不可能值的集合对象
返回随机端口
'''
def rand_port(x, y, exclude):
    r = None
    while r in exclude or not r:
        r = randint(x, y)
    return r

def test_port(port_num):
    proxies = {
        "http": "socks5://127.0.0.1:{}".format(port_num),
        "https": "socks5://127.0.0.1:{}".format(port_num)
    }
    try:
        r = requests.get(
            url="https://api.ipify.org/",
            proxies=proxies,
            timeout=10,
            headers={'User-Agent': get_one_random_ua()}
        )
        return r.text
    except:
        return None

'''
功能：发送代理请求
传入参数：
    url：    请求地址url，
    timeout：爬取时间间隔，
    use_ss： 是否使用shadowsocks代理
    sleep:   运行前等待时间
返回请求结果
'''
def request_with_proxy(url,
        gap_time=15,
        timeout=14,
        use_ss=False,
        no_proxy_test=False,
        use_self_pool=False
    ):
    headers = {'User-Agent': get_one_random_ua()}
    if use_self_pool:
        return req_with_proxy_pool(url,headers)
    if no_proxy_test:
        return requests.get(url, headers=headers, timeout=timeout)
    time.sleep(gap_time)
    if not use_ss:
        proxy_port = rand_port(9054, 9155, [])
        #print('use port {}...'.format(proxy_port))
        proxies = {
                "http": "socks5://127.0.0.1:{}".format(proxy_port),
                "https": "socks5://127.0.0.1:{}".format(proxy_port)
        }
        return requests.get(url, proxies=proxies, headers=headers, timeout=timeout,verify=False)
    else:
        #port_range = (1080, 1108)
        error_ports = [1094, 1098]
        port = rand_port(1080, 1108, error_ports)
        proxies = {
            "http": "socks5://127.0.0.1:{}".format(port),
            "https": "socks5://127.0.0.1:{}".format(port)
        }
        return requests.get(url, proxies=proxies, timeout=timeout, headers=headers,verify=False)

def request_with_random_ua(url,timeout=3):
    for i in range(6):
        try:
            return requests.get(
                url = url,
                timeout = timeout,
                headers = {'User-Agent': get_one_random_ua()}
            )
        except Exception as e:
            print('[Error]request_with_random_ua :%s'%str(e))
    return None

global proxy_servers_cache
proxy_servers_cache = []

import json,random
def load_proxy_cache(is_ano=0,counts=10,get_all_valid=True):
    if get_all_valid:
        url = 'http://127.0.0.1:8000/tool/get_proxy_configs?get_all_valid=1'
    else:
        url = 'http://127.0.0.1:8000/tool/get_proxy_configs?quantity={}'.format(counts)
    if is_ano:
        url += '&is_anonymous=1'
    resp = requests.get(url).text
    with open('/home/lyn/test.html','w') as f:
        f.write(resp)
    proxy_confs = json.loads(resp)['data']
    global proxy_servers_cache
    proxy_servers_cache = proxy_confs 
    print(proxy_servers_cache)

print('loading proxy cache...')
load_proxy_cache(get_all_valid=True,is_ano=0)

def req_with_proxy_pool(url,headers=None,need_print_res=False):
    proxy_conf = random.choice(proxy_servers_cache)
    #print('conf',proxy_conf)
    proxy_url = '{}://{}:{}'.format(
        proxy_conf['type'].lower(),
        proxy_conf['ip'],
        proxy_conf['port']
    )
    if need_print_res:
        print(proxy_url,proxy_conf)
    return requests.get(
        url = url,
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        },
        headers = headers
    )


