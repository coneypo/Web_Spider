# Author:   coneypo
# Created:  08.31
# Updated:  09.01
# web spider for xxx.com

from bs4 import BeautifulSoup
import requests
import random
import datetime
import csv
import pandas as pd


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}


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
        print("可能被代理网站屏蔽了", '\n')
    else:
        print("拿到的代理个数:", len(proxy_list), '\n')
        with open("proxies.csv", 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            for i in range(len(proxy_list)):
                # print(proxy_list[i])
                writer.writerow([proxy_list[i]])


# 执行一次就可以了；
# 执行一次可以更新本地代理地址；
get_proxy()


# 从存放代理的 csv 中随机获取一个代理
def get_random_proxy():
    column_names = ["proxy"]
    proxy_csv = pd.read_csv("proxies.csv", names=column_names)

    # 新建一个列表用来存储代理地址
    proxy_arr = []

    for i in range(len(proxy_csv["proxy"])):
        proxy_arr.append(proxy_csv["proxy"][i])

    # 随机选择一个代理
    random_proxy = proxy_arr[random.randint(0, len(proxy_arr)-1)]

    print("当前代理:", random_proxy)
    return random_proxy


# 爬取网站
def get_news():
    html = "https://www.ithome.com/blog/"
    resp = requests.get(html, headers=headers, proxies=get_random_proxy())
    resp.encoding = 'utf-8'

    # 网页内容
    bsObj = BeautifulSoup(resp.content, "lxml")
    # print(bsObj)

    # 分析
    block = bsObj.find_all("div", {"class": "block"})
    # print(block)

    current_titles = []
    current_times = []

    # analysis every block
    for i in range(len(block)):
        # get Time
        time_classes = ["state tody", "state other"]
        for time_class in time_classes:
            tmp = block[i].find_all('span', {'class': time_class})
            if tmp:
                current_time = (block[i].find('span', {'class': time_class})).get_text()
                current_times.append(current_time)

        # get Title
        if block[i].find_all('a', {'target': "_blank"}):
            current_title = (block[i].find('a', {'target': "_blank"})).get_text()
            current_titles.append(current_title)

    for i in range(len(current_times)):
        print(current_times[i], current_titles[i])
    return current_times, current_titles


get_news()

# 计时
start_time = datetime.datetime.now()
tmp = 0
sec_cnt = 0

while 1:
    current_time = datetime.datetime.now()

    # second 是以60为周期
    # 将开始时间的秒second / 当前时间的秒second 进行对比
    if current_time.second >= start_time.second:
        if tmp != current_time.second - start_time.second:
            # print("<no 60>+  ", tmp)
            sec_cnt += 1
            print("Time_cnt:", sec_cnt)
            if sec_cnt % 10 == 0:
                get_news()
                print('\n')
        tmp = current_time.second - start_time.second

    # when get 60
    else:
        if tmp != current_time.second + 60 - start_time.second:
            sec_cnt += 1
            print("Time_cnt:", sec_cnt)

            if sec_cnt % 10 == 0:
                get_news()
                print('\n')
        tmp = current_time.second + 60 - start_time.second
