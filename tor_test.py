import requests,time
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool


def get_tor_ip(port_num):
    proxies = {
        "http": "socks5://127.0.0.1:{}".format(port_num),
        "https": "socks5://127.0.0.1:{}".format(port_num)
    }
    r = requests.get("https://api.ipify.org/", proxies=proxies, timeout=20)
    return r.text

def work_per_proc(port_num):
    try:
        ip = get_tor_ip(port_num)
        print('%s: %s'%(port_num,ip))
        return ip
    except Exception as e:
        print('%s: %s'%(port_num,'error'))
        return 'error port'

pool = ThreadPool(64)
res = pool.map(work_per_proc,range(9054,9154))

error_cot = res.count('error port')

print(type(res))

res = res.remove('error port')

print(res)

ip_count = len(res)

ip_real_count = len(set(res))

print(error_cot,ip_count,ip_real_count)