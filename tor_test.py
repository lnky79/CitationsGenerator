import requests
from bs4 import BeautifulSoup
import time

def test_port(port_num):
    proxies = {
        "http": "socks5://127.0.0.1:{}".format(port_num),
        "https": "socks5://127.0.0.1:{}".format(port_num)
    }
    r = requests.get("https://api.ipify.org/", proxies=proxies, timeout=20)
    return r.text

duplicate = 0
error = 0
error_ports = []
ip_list = []
for i in range(9054, 9154):
    try:
        ip = test_port(i)
        print(ip)
        if ip not in ip_list:
            ip_list.append(ip)
        else:
            duplicate += 1
    except Exception as e:
        error += 1
        error_ports.append(i)
        print(i)
        print(e)

    time.sleep(30)

print("duplicate " + str(duplicate))
print("how many ips can be used " + str(len(ip_list)))
print("how many ips can not be used " + str(error))
print(error_ports)
