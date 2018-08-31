# Author:   coneypo
# Created:  08.31
# set proxy

from bs4 import BeautifulSoup
import requests
import random


def get_proxy():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    proxy_url = 'http://www.xicidaili.com/nn/'
    resp = requests.get(proxy_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    ips = soup.find_all('tr')
    proxy_list = []

    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        proxy_list.append(tds[1].text + ':' + tds[2].text)

    proxy = proxy_list[random.randint(0, len(proxy_list))]

    print(proxy)
    return proxy
get_proxy()


