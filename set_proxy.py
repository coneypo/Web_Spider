# Author:   coneypo
# Created:  08.31
# Updated:  09.01
# set proxy
# save to csv

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import random

path_proxy_csv = "proxies.csv"


# 从 xicidaili.com 爬取代理地址，存入本地csv中
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

    if len(proxy_list) == 0:
        print("可能被屏蔽了")
    else:
        print("拿到的代理个数:", len(proxy_list))
        with open(path_proxy_csv, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            for i in range(len(proxy_list)):
                print(proxy_list[i])
                writer.writerow([proxy_list[i]])


# get_proxy()


# 从代理的 csv 中随机获取一个代理
def get_random_proxy():
    column_names = ["proxy"]
    proxy_csv = pd.read_csv("proxies.csv", names=column_names)

    # 新建一个列表用来存储代理地址
    proxy_arr = []

    for i in range(len(proxy_csv["proxy"])):
        proxy_arr.append(proxy_csv["proxy"][i])

    # 随机选择一个代理
    random_proxy = proxy_arr[random.randint(0, len(proxy_arr) - 1)]

    print(random_proxy)
    return random_proxy

# get_random_proxy()
